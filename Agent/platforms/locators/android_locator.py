from typing import Any, Dict


class AndroidLocatorBuilder:
    """Builds Appium locators for Android elements."""
    
    def build(self, element: Dict[str, Any], robust: bool = False) -> str:
        if robust:
            return self.build_robust(element)
        return self.build_priority(element)
    
    def build_priority(self, element: Dict[str, Any]) -> str:
        """
        Args:
            element: Dict with raw XML attributes
        Returns:
            First available locator: id > accessibility_id > text > class
        """
        resource_id = self._get_str(element, 'resource-id')
        if resource_id:
            return f"id={resource_id}"
        
        content_desc = self._get_str(element, 'content-desc')
        if content_desc:
            return f"accessibility_id={content_desc}"
        
        text = self._get_str(element, 'text')
        if text:
            return f"//*[@text={self._escape_xpath(text)}]"
        
        class_name = self._get_str(element, 'class')
        if class_name:
            return f"class={class_name}"
        
        raise AssertionError("Cannot build locator: no usable attributes")
    
    def build_robust(self, element: Dict[str, Any]) -> str:
        """
        Args:
            element: Dict with raw XML attributes
        Returns:
            XPath combining all available attributes for uniqueness
        """
        conditions = []
        
        resource_id = self._get_str(element, 'resource-id')
        if resource_id:
            conditions.append(f"@resource-id={self._escape_xpath(resource_id)}")
        
        content_desc = self._get_str(element, 'content-desc')
        if content_desc:
            conditions.append(f"@content-desc={self._escape_xpath(content_desc)}")
        
        text = self._get_str(element, 'text')
        if text:
            conditions.append(f"@text={self._escape_xpath(text)}")
        
        bounds = self._get_str(element, 'bounds')
        if bounds:
            conditions.append(f"@bounds='{bounds}'")
        
        class_name = self._get_str(element, 'class')
        base = f"//{class_name}" if class_name else "//*"
        
        if not conditions:
            if class_name:
                return base
            raise AssertionError("Cannot build locator: no usable attributes")
        
        return f"{base}[{' and '.join(conditions)}]"
    
    def _get_str(self, element: Dict[str, Any], key: str) -> str:
        val = element.get(key, '')
        return str(val).strip() if val else ''
    
    def _escape_xpath(self, value: str) -> str:
        """
        Args:
            value: "It's a test"
        Returns:
            concat('It', \"'\", 's a test') or 'simple'
        """
        if "'" not in value:
            return f"'{value}'"
        if '"' not in value:
            return f'"{value}"'
        
        parts = []
        current = ""
        for char in value:
            if char == "'":
                if current:
                    parts.append(f"'{current}'")
                    current = ""
                parts.append("\"'\"")
            else:
                current += char
        if current:
            parts.append(f"'{current}'")
        
        return f"concat({', '.join(parts)})"

