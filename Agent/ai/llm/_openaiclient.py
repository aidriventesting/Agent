from openai import OpenAI
from openai.types.chat import ChatCompletion
from typing import Optional, Dict, List, Union
from robot.api import logger
from Agent.ai.llm._baseclient import BaseLLMClient
from Agent.config.model_config import ModelConfig
from Agent.utilities._costtracker import CostTracker


class OpenAIClient(BaseLLMClient):
    def __init__(
        self,
        api_key=None,
        model: str = "gpt-4o",
        max_retries: int = 3,
        base_backoff: int = 2,
    ):
        self.api_key: str = api_key
        if not self.api_key:
            from Agent.config.config import Config
            config = Config()
            self.api_key = config.OPENAI_API_KEY

        if not self.api_key:
            raise ValueError("API key must be provided either as an argument or in the environment variables.")

        self.default_model = model
        self.max_retries = max_retries
        self.base_backoff = base_backoff
        self.client = OpenAI(api_key=self.api_key)
        self.model_config = ModelConfig()
        self.cost_tracker = CostTracker()

    def create_chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 1.0,
        top_p: float = 1.0,
        tools: Optional[List[Dict]] = None,
        tool_choice: Optional[Union[str, Dict]] = None,
        **kwargs
    ) -> Optional[ChatCompletion]:
        try:
            self._validate_parameters(temperature, top_p)

            params = {
                "model": model or self.default_model,
                "messages": messages,
                "temperature": temperature,
                "top_p": top_p,
                **kwargs
            }

            if tools:
                params["tools"] = tools
                if tool_choice:
                    params["tool_choice"] = tool_choice

            response = self.client.chat.completions.create(**params)
            logger.debug(f"OpenAI API call successful. Tokens used: {response.usage.total_tokens}")
            logger.debug(f"messages: {response}")
            return response
        except Exception as e:
            logger.error(f"OpenAI API Error: {str(e)}")
            raise

    def _validate_parameters(self, temperature: float, top_p: float):
        if not (0 <= temperature <= 2):
            logger.error(f"Invalid temperature {temperature}. Must be between 0 and 2")
            raise ValueError(f"Invalid temperature {temperature}. Must be between 0 and 2")
        if not (0 <= top_p <= 1):
            logger.error(f"Invalid top_p {top_p}. Must be between 0 and 1")
            raise ValueError(f"Invalid top_p {top_p}. Must be between 0 and 1")
    
    def _calculate_cost(self, model: str, prompt_tokens: int, completion_tokens: int) -> Dict[str, float]:
        """
        Calculate the cost of API call based on token usage.
        
        Args:
            model: Model name used for the API call
            prompt_tokens: Number of input tokens
            completion_tokens: Number of output tokens
            
        Returns:
            Dictionary with input_cost, output_cost, and total_cost
        """
        pricing = self.model_config.get_model_pricing(model)
        
        if not pricing:
            logger.warn(f"No pricing information found for model: {model}. Cost will be 0.")
            return {
                'input_cost': 0.0,
                'output_cost': 0.0,
                'total_cost': 0.0
            }
        
        # Pricing is per 1M tokens according to llm_models.json metadata
        input_cost = (prompt_tokens / 1_000_000) * pricing['input']
        output_cost = (completion_tokens / 1_000_000) * pricing['output']
        total_cost = input_cost + output_cost
        
        return {
            'input_cost': input_cost,
            'output_cost': output_cost,
            'total_cost': total_cost
        }

    def format_response(
        self,
        response: ChatCompletion,
        include_tokens: bool = True,
        include_reason: bool = False,
    ) -> Dict[str, Union[str, int, float]]:
        if not response or not response.choices:
            logger.error(f"Invalid response or no choices in the response")
            return {}

        result = {
            "content": response.choices[0].message.content or "",
        }

        # Extract tool calls if present
        if response.choices[0].message.tool_calls:
            tool_calls = []
            for tc in response.choices[0].message.tool_calls:
                tool_calls.append({
                    "id": tc.id,
                    "type": tc.type,
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments
                    }
                })
            result["tool_calls"] = tool_calls

        if include_tokens:
            logger.debug(f"Tokens used: {response.usage}")
            result.update(
                {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens,
                }
            )
            
            # Calculate and track cost
            cost_data = self._calculate_cost(
                model=response.model,
                prompt_tokens=response.usage.prompt_tokens,
                completion_tokens=response.usage.completion_tokens
            )
            
            result.update({
                "input_cost": cost_data['input_cost'],
                "output_cost": cost_data['output_cost'],
                "total_cost": cost_data['total_cost']
            })
            
            # Track cost in the cost tracker
            self.cost_tracker.add_cost(
                input_cost=cost_data['input_cost'],
                output_cost=cost_data['output_cost'],
                model=response.model
            )
            
            logger.debug(
                f"API call cost: ${cost_data['total_cost']:.6f} "
                f"(input: ${cost_data['input_cost']:.6f}, output: ${cost_data['output_cost']:.6f})"
            )

        if include_reason:
            logger.debug(f"Finish reason: {response.choices[0].finish_reason}")
            result["finish_reason"] = response.choices[0].finish_reason

        return result


