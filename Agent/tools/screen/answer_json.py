from typing import Any, Dict
import json
from Agent.tools.base import BaseTool, ExecutorProtocol, ToolCategory
from robot.api import logger


class AnswerJsonTool(BaseTool):
    """Answer question about the screen with JSON response."""
    
    @property
    def name(self) -> str:
        return "answer_question_json"
    
    @property
    def description(self) -> str:
        return "Provide a JSON object answer to the question about the screen content"
    
    @property
    def category(self) -> ToolCategory:
        return ToolCategory.SCREEN
    
    @property
    def works_on_locator(self) -> bool:
        return False
    
    @property
    def works_on_coordinates(self) -> bool:
        return False
    
    def get_parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "answer": {
                    "type": "object",
                    "description": "The JSON object answer to the question based on what you see in the screenshot"
                }
            },
            "required": ["answer"]
        }
    
    def execute(
        self, 
        executor: ExecutorProtocol, 
        arguments: Dict[str, Any], 
        context: Dict[str, Any]
    ) -> str:
        answer = arguments.get("answer", {})
        answer_str = json.dumps(answer, ensure_ascii=False)
        logger.info(f"💬 AI Answer (JSON): {answer_str[:100]}..." if len(answer_str) > 100 else f"💬 AI Answer (JSON): {answer_str}")
        return answer_str

