from typing import Any, Dict
from Agent.tools.base import BaseTool, ExecutorProtocol, ToolCategory
from robot.api import logger


class AssertScreenTool(BaseTool):
    """Screen assertion tool - analyzes screenshots to verify conditions.
    
    This tool is used by Agent.VisualCheck to verify UI states, presence of elements,
    visual appearance, etc. by analyzing screenshots with AI vision models.
    """
    
    @property
    def name(self) -> str:
        return "assert_screen"
    
    @property
    def description(self) -> str:
        return "Report the results of visual verification against the given instruction"
    
    @property
    def category(self) -> ToolCategory:
        return ToolCategory.SCREEN
    
    def get_parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "verification_result": {
                    "type": "boolean",
                    "description": "Whether the screenshot matches the instruction (true) or not (false)"
                },
                "confidence_score": {
                    "type": "number",
                    "description": "Confidence level of the verification from 0.0 (no confidence) to 1.0 (completely confident)",
                    "minimum": 0.0,
                    "maximum": 1.0
                },
                "analysis": {
                    "type": "string",
                    "description": "Detailed analysis explaining why the verification passed or failed"
                },
                "found_elements": {
                    "type": "array",
                    "description": "Optional list of UI elements found in the screenshot",
                    "items": {
                        "type": "object",
                        "properties": {
                            "element_type": {"type": "string"},
                            "description": {"type": "string"},
                            "location": {"type": "string"},
                            "confidence": {"type": "number"}
                        }
                    }
                },
                "issues": {
                    "type": "array",
                    "description": "Optional list of issues or problems found",
                    "items": {"type": "string"}
                }
            },
            "required": ["verification_result", "confidence_score", "analysis"]
        }
    
    def execute(
        self,
        executor: ExecutorProtocol,
        arguments: Dict[str, Any],
        context: Dict[str, Any]
    ) -> None:
        """Execute visual verification - log results and assert if failed.
        
        Note: Screen tools don't use the executor for actions, they analyze results.
        """
        verification_result = arguments.get("verification_result")
        confidence_score = arguments.get("confidence_score")
        analysis = arguments.get("analysis")
        found_elements = arguments.get("found_elements", [])
        issues = arguments.get("issues", [])
        
        min_confidence = context.get("min_confidence", 0.7)

        result_status = "PASS" if verification_result else "FAIL"
        logger.info(f"Visual check: {result_status} (confidence: {confidence_score:.2f})")
        logger.debug(f"Analysis: {analysis}")
        
        if found_elements:
            logger.debug(f"Found elements: {found_elements}")
        
        if issues:
            logger.debug(f"Issues: {', '.join(issues[:3])}")

        if not verification_result:
            error_msg = f"Visual verification failed: {analysis}"
            if issues:
                error_msg += f" | Issues: {', '.join(issues[:3])}"
            raise AssertionError(error_msg)
        elif confidence_score < min_confidence:
            raise AssertionError(
                f"Confidence too low: {confidence_score:.2f} < {min_confidence}. {analysis}"
            )

