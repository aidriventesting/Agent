from typing import Any, Dict
from Agent.tools.base import BaseTool, ExecutorProtocol, ToolCategory
from robot.api import logger


class VerifyVisualMatchTool(BaseTool):
    """Visual verification tool - analyzes screenshots to verify conditions.
    
    This tool is used by Agent.VisualCheck to verify UI states, presence of elements,
    visual appearance, etc. by analyzing screenshots with AI vision models.
    """
    
    @property
    def name(self) -> str:
        return "verify_visual_match"
    
    @property
    def description(self) -> str:
        return "Report the results of visual verification against the given instruction"
    
    @property
    def category(self) -> ToolCategory:
        return ToolCategory.VISUAL
    
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
        
        Note: Visual tools don't use the executor for actions, they analyze results.
        """
        verification_result = arguments.get("verification_result")
        confidence_score = arguments.get("confidence_score")
        analysis = arguments.get("analysis")
        found_elements = arguments.get("found_elements", [])
        issues = arguments.get("issues", [])

        logger.info(f"👁️ Visual verification results: {arguments}")
        
        # Log detailed AI response
        logger.debug("=" * 80)
        logger.debug("AI VISUAL VERIFICATION RESPONSE")
        logger.debug("=" * 80)
        logger.debug(f"Verification Result: {'PASS' if verification_result else 'FAIL'}")
        logger.debug(f"Confidence Score: {confidence_score:.2f}")
        logger.debug(f"Analysis: {analysis}")
        
        if found_elements:
            logger.debug(f"Found Elements ({len(found_elements)} total):")
            for i, element in enumerate(found_elements[:10], 1):
                element_type = element.get("element_type", "unknown")
                description = element.get("description", "no description")
                location = element.get("location", "unknown location")
                confidence = element.get("confidence", 0.0)
                logger.debug(f"  {i}. {element_type}: {description}")
                logger.debug(f"     Location: {location}")
                logger.debug(f"     Confidence: {confidence:.2f}")
        
        if issues:
            logger.debug(f"Issues Found ({len(issues)} total):")
            for i, issue in enumerate(issues, 1):
                logger.debug(f"  {i}. {issue}")
        
        logger.debug("=" * 80)

        # Compact log for custom logger
        logger.debug(f"🔍 Verification result: {verification_result}")
        logger.debug(f"📊 Confidence score: {confidence_score}")
        logger.debug(f"📝 Analysis: {analysis}")
        
        if found_elements:
            logger.debug(f"🎯 Found elements: {len(found_elements)} elements detected")
            for i, element in enumerate(found_elements[:5], 1):
                element_type = element.get("element_type", "unknown")
                description = element.get("description", "no description")
                confidence = element.get("confidence", 0.0)
                logger.debug(f"  {i}. {element_type}: {description} (confidence: {confidence:.2f})")
        
        if issues:
            logger.debug(f"⚠️ Issues found: {len(issues)} issues detected")
            for i, issue in enumerate(issues[:3], 1):
                logger.debug(f"  {i}. {issue}")

        # Assert based on verification result
        if verification_result:
            logger.info("✅ Visual verification passed")
        else:
            error_msg = f"Visual verification failed. Analysis: {analysis}"
            if issues:
                error_msg += f" Issues: {', '.join(issues[:3])}"
            raise AssertionError(error_msg)

