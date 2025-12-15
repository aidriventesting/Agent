# TODO: clean, validate, and plug

from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class BoundingBox:
    x: int = 0
    y: int = 0
    width: int = 0
    height: int = 0
    
    def is_valid(self) -> bool:
        return self.width > 0 and self.height > 0
    
    def to_dict(self) -> Dict[str, int]:
        return {"x": self.x, "y": self.y, "width": self.width, "height": self.height}
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BoundingBox":
        if not data:
            return cls()
        return cls(
            x=int(data.get("x", 0)),
            y=int(data.get("y", 0)),
            width=int(data.get("width", 0)),
            height=int(data.get("height", 0)),
        )


@dataclass
class WebElement:
    """Web element (Playwright)."""
    text: str = ""
    element_id: str = ""
    tag: str = ""
    aria_label: str = ""
    placeholder: str = ""
    css_class: str = ""
    href: str = ""
    role: str = ""
    name: str = ""
    element_type: str = ""
    clickable: bool = True
    enabled: bool = True
    bbox: BoundingBox = field(default_factory=BoundingBox)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "resource_id": self.element_id,
            "class_name": self.tag,
            "aria_label": self.aria_label,
            "placeholder": self.placeholder,
            "css_class": self.css_class,
            "href": self.href,
            "role": self.role,
            "name": self.name,
            "type": self.element_type,
            "clickable": self.clickable,
            "enabled": self.enabled,
            "bbox": self.bbox.to_dict(),
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WebElement":
        bbox = BoundingBox.from_dict(data.get("bbox", {}))
        return cls(
            text=data.get("text", ""),
            element_id=data.get("resource_id", "") or data.get("element_id", ""),
            tag=data.get("class_name", "") or data.get("tag", ""),
            aria_label=data.get("aria_label", ""),
            placeholder=data.get("placeholder", ""),
            css_class=data.get("css_class", ""),
            href=data.get("href", ""),
            role=data.get("role", ""),
            name=data.get("name", ""),
            element_type=data.get("type", "") or data.get("element_type", ""),
            clickable=data.get("clickable", True),
            enabled=data.get("enabled", True),
            bbox=bbox,
        )


@dataclass
class AndroidElement:
    """Android element (Appium)."""
    text: str = ""
    resource_id: str = ""
    class_name: str = ""
    content_desc: str = ""
    clickable: bool = True
    enabled: bool = True
    bbox: BoundingBox = field(default_factory=BoundingBox)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "resource_id": self.resource_id,
            "class_name": self.class_name,
            "content_desc": self.content_desc,
            "accessibility_label": self.content_desc,
            "clickable": self.clickable,
            "enabled": self.enabled,
            "bbox": self.bbox.to_dict(),
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AndroidElement":
        bbox = BoundingBox.from_dict(data.get("bbox", {}))
        return cls(
            text=data.get("text", ""),
            resource_id=data.get("resource_id", ""),
            class_name=data.get("class_name", ""),
            content_desc=data.get("content_desc", "") or data.get("accessibility_label", ""),
            clickable=data.get("clickable", True),
            enabled=data.get("enabled", True),
            bbox=bbox,
        )


@dataclass
class IOSElement:
    """iOS element (Appium)."""
    text: str = ""
    name: str = ""
    label: str = ""
    element_type: str = ""
    clickable: bool = True
    enabled: bool = True
    bbox: BoundingBox = field(default_factory=BoundingBox)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "resource_id": self.name,
            "name": self.name,
            "label": self.label,
            "accessibility_label": self.label,
            "class_name": self.element_type,
            "clickable": self.clickable,
            "enabled": self.enabled,
            "bbox": self.bbox.to_dict(),
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "IOSElement":
        bbox = BoundingBox.from_dict(data.get("bbox", {}))
        return cls(
            text=data.get("text", ""),
            name=data.get("name", "") or data.get("resource_id", ""),
            label=data.get("label", "") or data.get("accessibility_label", ""),
            element_type=data.get("element_type", "") or data.get("class_name", ""),
            clickable=data.get("clickable", True),
            enabled=data.get("enabled", True),
            bbox=bbox,
        )
