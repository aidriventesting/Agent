from typing import Any, Dict


class MobileLocatorBuilder:
    """Builds Appium locators for Android and iOS."""
    
    def __init__(self, platform: str = "android"):
        self._platform = platform
    
    def set_platform(self, platform: str) -> None:
        self._platform = platform
    
    def build(self, element: Dict[str, Any]) -> str:
        """Dispatch to platform-specific method."""
        if self._platform == "ios":
            return self.build_ios(element)
        return self.build_android(element)
    
    def build_android(self, element: Dict[str, Any]) -> str:
        """
        Build Appium locator for Android.
        
        Priority: id > accessibility_id > xpath[@text] > class
        """
        resource_id = element.get('resource_id', '').strip()
        acc_label = element.get('accessibility_label', '') or element.get('content_desc', '')
        acc_label = acc_label.strip() if acc_label else ''
        text = element.get('text', '').strip()
        class_name = element.get('class_name', '').strip()
        
        if resource_id:
            return f"id={resource_id}"
        
        if acc_label:
            return f"accessibility_id={acc_label}"
        
        if text:
            return f"//*[@text='{text}']"
        
        if class_name:
            return f"class={class_name}"
        
        raise AssertionError("Cannot build locator: element has no usable attributes")
    
    def build_ios(self, element: Dict[str, Any]) -> str:
        """
        Build Appium locator for iOS.
        
        Priority: id > accessibility_id > predicate string > class
        """
        resource_id = element.get('resource_id', '').strip()
        acc_label = element.get('accessibility_label', '') or element.get('label', '')
        acc_label = acc_label.strip() if acc_label else ''
        text = element.get('text', '').strip()
        class_name = element.get('class_name', '').strip()
        
        if resource_id:
            return f"id={resource_id}"
        
        if acc_label:
            return f"accessibility_id={acc_label}"
        
        if text:
            escaped_text = text.replace("'", "\\'")
            return f"-ios predicate string:label == '{escaped_text}' OR value == '{escaped_text}'"
        
        if class_name:
            return f"class={class_name}"
        
        raise AssertionError("Cannot build locator: element has no usable attributes")
