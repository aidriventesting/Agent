from __future__ import annotations

import ast
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, TypedDict
from robot.api import logger


_LINE_PATTERN = re.compile(r"^\s*([a-zA-Z_]+)\s+(\d+):\s*(\{.*\})\s*$")


class Icon(TypedDict):
    type: str
    bbox: List[float]
    interactivity: bool
    content: str


class OmniParserResultProcessor:
    """
    Parse the raw OmniParser text payload into structured elements.

    Only `get_parsed_ui_elements` is intended to be used by consumers. 
    All helpers stay private to keep the parsing pipeline encapsulated.
    """

    def __init__(
        self,
        *,
        response_text: str,
        image_temp_path: Optional[str] = None,
    ) -> None:
        self._image_temp_path = image_temp_path or ""
        self._elements: List[OmniParserElement] = self._parse_response(response_text)
        logger.debug(f"OmniParser detected {len(self._elements)} elements")
        if self._image_temp_path:
            logger.debug(f"Temporary image: {self._image_temp_path}")
        self._log_preview(limit=8)

    def get_parsed_ui_elements(self, *, element_type: Optional[str] = None) -> Dict[str, Icon]:
        """
        Return parsed elements keyed by their OmniParser label (whitespace removed).

        Parameters
        ----------
        element_type: Optional[str]
            - "interactive" for clickable items
            - "icon" or "text" for specific OmniParser element kinds
            - None (default) returns every element
        """
        if not element_type:
            filtered = self._elements
        else:
            element_type = element_type.strip().lower()
            if element_type == "interactive":
                filtered = [el for el in self._elements if el.interactivity]
            elif element_type == "all":
                filtered = self._elements
            else:
                filtered = [el for el in self._elements if el.element_type.lower() == element_type]

        return {self._element_key(element): element.to_icon() for element in filtered}

    @property
    def image_temp_path(self) -> str:
        """Return the temporary image path created by Gradio (optional, for debugging/display)."""
        return self._image_temp_path

    @staticmethod
    def _element_key(element: "OmniParserElement") -> str:
        """Build the dictionary key, ensuring the prefix (e.g. 'icon') stays untouched."""
        return element.label.replace(" ", "")

    def _parse_response(self, response_text: str) -> List[OmniParserElement]:
        elements: List[OmniParserElement] = []
        if not response_text:
            return elements

        for line in response_text.splitlines():
            clean_line = line.strip()
            if not clean_line:
                continue

            match = _LINE_PATTERN.match(clean_line)
            if not match:
                continue

            label_prefix, index_str, dict_payload = match.groups()
            attributes = self._safe_literal_eval(dict_payload)
            if attributes is None:
                continue

            # index_str is guaranteed by regex to be digits; direct cast keeps code simple
            index = int(index_str)
            element = self._build_element(label_prefix, index, attributes)
            if element:
                elements.append(element)

        return elements

    @staticmethod
    def _safe_literal_eval(payload: str) -> Optional[Dict[str, Any]]:
        try:
            parsed = ast.literal_eval(payload)
        except (SyntaxError, ValueError):
            return None
        if not isinstance(parsed, dict):
            return None
        return parsed

    def _build_element(
        self,
        label_prefix: str,
        index: int,
        attributes: Dict[str, Any],
    ) -> Optional[OmniParserElement]:
        element_type = str(attributes.get("type", "unknown"))
        raw_bbox = attributes.get("bbox", [])
        bbox = [float(v) for v in raw_bbox] if isinstance(raw_bbox, (list, tuple)) else []
        interactivity = bool(attributes.get("interactivity", False))
        content = str(attributes.get("content", ""))

        return OmniParserElement(
            index=index,
            label=f"{label_prefix} {index}",
            element_type=element_type,
            bbox=bbox,
            interactivity=interactivity,
            content=content,
        )

    def _log_preview(self, limit: int) -> None:
        if not self._elements:
            logger.debug("OmniParser parsed elements preview: none")
            return

        preview_lines = []
        for element in self._elements[:limit]:
            preview_lines.append(
                f"[{element.index}] {element.element_type} (interactive={element.interactivity}) "
                f"content='{element.content}' bbox={element.bbox}"
            )
        description = "\n".join(preview_lines)
        logger.debug(f"OmniParser parsed elements preview:\n{description}")



@dataclass(frozen=True)
class OmniParserElement:
    index: int
    label: str
    element_type: str
    bbox: List[float] = field(default_factory=list)
    interactivity: bool = False
    content: str = ""

    def to_icon(self) -> Icon:
        return Icon(
            type=self.element_type,
            bbox=list(self.bbox),
            interactivity=self.interactivity,
            content=self.content,
        )


if __name__ == "__main__":
    parser = OmniParserResultProcessor(
        response_text="""
        icon 1: {'type': 'icon', 'bbox': [0.419, 0.17, 0.574, 0.266], 'interactivity': True, 'content': 'YouTube'}
        icon 2: {'type': 'icon', 'bbox': [0.419, 0.17, 0.574, 0.266], 'interactivity': False, 'content': 'YouTube'}
        icon 3: {'type': 'icon', 'bbox': [0.419, 0.17, 0.574, 0.266], 'interactivity': True, 'content': 'YouTube'}
        icon 4: {'type': 'icon', 'bbox': [0.419, 0.17, 0.574, 0.266], 'interactivity': False, 'content': 'YouTube'}
        icon 5: {'type': 'icon', 'bbox': [0.419, 0.17, 0.574, 0.266], 'interactivity': False, 'content': 'YouTube'}
        icon 6: {'type': 'icon', 'bbox': [0.419, 0.17, 0.574, 0.266], 'interactivity': False, 'content': 'YouTube'}
        icon 7: {'type': 'icon', 'bbox': [0.419, 0.17, 0.574, 0.266], 'interactivity': False, 'content': 'YouTube'}
        icon 8: {'type': 'icon', 'bbox': [0.419, 0.17, 0.574, 0.266], 'interactivity': False, 'content': 'YouTube'}
        """
    )
    print(parser.get_parsed_ui_elements(element_type="interactive"))