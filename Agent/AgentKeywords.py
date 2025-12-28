from typing import Any, Dict, List, Optional

from Agent.agent_engine import AgentEngine
from Agent._test_listener import CostLoggingListener
from robot.api.deco import keyword


class AgentKeywords:
    """
    Robot Framework library exposing two high-level keywords:
    - Agent.Do <instruction>
    - Agent.VisualCheck <instruction>

    Agent.Do captures current UI context, composes a strict JSON prompt,
    calls the LLM with temperature=0, and executes the mapped AppiumLibrary action.
    
    Agent.VisualCheck captures a screenshot, sends it to AI for visual analysis,
    and provides detailed verification results with confidence scores.
    """

    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    ROBOT_LIBRARY_LISTENER = CostLoggingListener()

    def __init__(
        self, 
        llm_client: str | None = None, 
        llm_model: str | None = None,
        platform_type: str = "auto",
        element_source: str = "accessibility",
        llm_input_format: str = "som",
    ):
        from Agent.config.config import Config
        
        self.engine = AgentEngine(
            llm_client=llm_client or Config.DEFAULT_LLM_CLIENT, 
            llm_model=llm_model,
            platform_type=platform_type,
            element_source=element_source,
            llm_input_format=llm_input_format,
        )

    # ----------------------- Public RF Keywords -----------------------
    def do(self, instruction: str):
        """Agent.Do <instruction>
        Example: Agent.Do    accepte les cookies
        """
        self.engine.do(instruction)

    def check(self, instruction: str):
        """Agent.VisualCheck <instruction>
        Example: Agent.VisualCheck    vérifier que l'écran affiche le logo de l'application
        """
        self.engine.visual_check(instruction)

    def ask(self, question: str, format: str = "text") -> str:
        """Agent.Ask <question>    format=text|json
        Example: Agent.Ask    What is the product price?
        Example: Agent.Ask    List all buttons    format=json
        """
        return self.engine.ask(question, response_format=format)

    def find_visual_element(self, description: str, format: str = "center"):
        """Agent.Find Visual Element <description>    format=normalized|pixels|center
        Example: Agent.Find Visual Element    Login button
        Example: Agent.Find Visual Element    Search icon    format=pixels
        """
        return self.engine.find_visual_element(description, format=format)

    def set_element_source(self, source: str):
        """Agent.Set Element Source    accessibility|vision
        Example: Agent.Set Element Source    vision
        """
        self.engine.set_element_source(source)

    # def set_llm_input_format(self, format: str):
    #     """Agent.Set LLM Input Format    text|som
    #     Example: Agent.Set LLM Input Format    som
    #     """
    #     self.engine.set_llm_input_format(format)

    # def autonumous(self, instruction: str):
    #     """Agent.Autonumous <instruction>
    #     This keyword is designed to autonomously plan and execute a test based on the 
    #     given single instruction.

    #     Example: Agent.Autonumous    Navigate to settings, change language to French, 
    #     ...    then go back to home screen and verify the interface is in French"""
    #     raise NotImplementedError("Agent.Autonumous is not implemented yet")