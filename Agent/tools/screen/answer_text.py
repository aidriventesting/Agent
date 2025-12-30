from typing import Any, Dict
from Agent.tools.base import BaseTool, ExecutorProtocol, ToolCategory
from robot.api import logger


class AnswerTextTool(BaseTool):
    """Answer question about the screen with text response."""
    
    @property
    def name(self) -> str:
        return "answer_question"
    
    @property
    def description(self) -> str:
        return "Provide a text answer to the question about the screen content"
    
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
                    "type": "string",
                    "description": "The text answer to the question based on what you see in the screenshot"
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
        answer = arguments.get("answer", "")
        logger.info(f"💬 AI Answer: {answer[:100]}..." if len(answer) > 100 else f"💬 AI Answer: {answer}")
        return answer

