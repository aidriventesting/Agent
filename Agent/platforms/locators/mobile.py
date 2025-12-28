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
        Build XPath locator combining all available attributes.
        
        Returns: "//*[@resource-id='x' and @content-desc='y' and @text='z']"
        """
        resource_id = element.get('resource_id', '').strip()
        acc_label = element.get('accessibility_label', '') or element.get('content_desc', '')
        acc_label = acc_label.strip() if acc_label else ''
        text = element.get('text', '').strip()
        class_name = element.get('class_name', '').strip()
        
        conditions = []
        
        if resource_id:
            conditions.append(f"@resource-id='{resource_id}'")
        
        if acc_label:
            conditions.append(f"@content-desc='{acc_label}'")
        
        if text:
            conditions.append(f"@text='{text}'")
        
        if not conditions:
            if class_name:
                return f"//{class_name}"
            raise AssertionError("Cannot build locator: element has no usable attributes")
        
        base = f"//{class_name}" if class_name else "//*"
        return f"{base}[{' and '.join(conditions)}]"
    
    def build_ios(self, element: Dict[str, Any]) -> str:
        """
        Build iOS predicate string combining all available attributes.
        
        Returns: "-ios predicate string:name == 'x' AND label == 'y'"
        """
        resource_id = element.get('resource_id', '').strip()
        acc_label = element.get('accessibility_label', '') or element.get('label', '')
        acc_label = acc_label.strip() if acc_label else ''
        text = element.get('text', '').strip()
        class_name = element.get('class_name', '').strip()
        
        conditions = []
        
        if resource_id:
            conditions.append(f"name == '{resource_id}'")
        
        if acc_label:
            escaped = acc_label.replace("'", "\\'")
            conditions.append(f"label == '{escaped}'")
        
        if text:
            escaped = text.replace("'", "\\'")
            conditions.append(f"value == '{escaped}'")
        
        if class_name:
            conditions.append(f"type == '{class_name}'")
        
        if not conditions:
            raise AssertionError("Cannot build locator: element has no usable attributes")
        
        return f"-ios predicate string:{' AND '.join(conditions)}"
