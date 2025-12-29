from typing import Any, Dict


class AndroidLocatorBuilder:
    """Builds Appium locators for Android elements."""
    
    def build(self, element: Dict[str, Any], strategy: str = 'auto') -> str:
        """
        Args:
            element: Dict with raw XML attributes
            strategy: 'auto' | 'id_only' | 'bounds' | 'xpath_attrs' | 'xpath_all'
        Returns:
            Appium locator string
        Example: build(elem, 'id_only') -> 'id=com.android:id/button'
        """
        if strategy == 'auto':
            return self._build_locator_unique_content(element)
        elif strategy == 'id_only':
            return self.build_identifiers_only(element)
        elif strategy == 'bounds':
            return self.build_by_bounds(element)
        elif strategy == 'xpath_attrs':
            return self.build_xpath_attributes(element)
        elif strategy == 'xpath_all':
            return self.build_xpath_all(element)
        else:
            raise ValueError(f"Unknown strategy: {strategy}")
    
    def _build_locator_unique_content(self, element: Dict[str, Any]) -> str:
        resource_id = self._get_str(element, 'resource-id')
        if resource_id:
            return f"id={resource_id}"
        
        content_desc = self._get_str(element, 'content-desc')
        if content_desc:
            return f"accessibility_id={content_desc}"
        
        text = self._get_str(element, 'text')
        if text:
            return f"//*[@text={self._escape_xpath(text)}]"
        
        raise AssertionError("Cannot build locator: no usable attributes")
    
    #TODO: see if this should be private after adding locator strategies ( build )
    def build_identifiers_only(self, element: Dict[str, Any]) -> str:
        """
        Args:
            element: Dict with raw XML attributes
        Returns:
            Identifiers only: resource-id > content-desc, raise if none
        Example: 'id=com.android:id/button' or 'accessibility_id=Navigate up'
        """
        content_desc = self._get_str(element, 'content-desc')
        if content_desc:
            return f"accessibility_id={content_desc}"
        
        resource_id = self._get_str(element, 'resource-id')
        if resource_id:
            return f"id={resource_id}"
        
        raise ValueError("No ID attributes available")
    
    def build_by_bounds(self, element: Dict[str, Any]) -> str:
        """
        Args:
            element: Dict with raw XML attributes
        Returns:
            XPath with bounds attribute
        Example: '//*[@bounds="[0,72][1080,200]"]'
        """
        bounds = self._get_str(element, 'bounds')
        if not bounds:
            raise ValueError("No bounds attribute available")
        
        class_name = self._get_str(element, 'class')
        base = f"//{class_name}" if class_name else "//*"
        
        return f"{base}[@bounds='{bounds}']"

    def build_xpath_attributes(self, element: Dict[str, Any]) -> str:
        """
        Args:
            element: Dict with raw XML attributes
        Returns:
            XPath with content attributes (resource-id, content-desc, text)
        Example: '//Button[@resource-id="btn" and @text="Login"]'
        """
        return self._build_full_xpath(element, exclude_metadata=True)
    
    def build_xpath_all(self, element: Dict[str, Any]) -> str:
        """
        Args:
            element: Dict with raw XML attributes
        Returns:
            XPath with ALL attributes including metadata (clickable, enabled, etc.)
        Example: '//Button[@resource-id="btn" and @clickable="true"]'
        """
        return self._build_full_xpath(element, exclude_metadata=False)

    def _build_full_xpath(
        self, 
        element: Dict[str, Any],
        exclude_metadata: bool = True
    ) -> str:
        """
        Args:
            element: Dict with raw XML attributes
            exclude_metadata: If True, exclude only computed (bbox, elementId, package)
                             If False, also exclude bool/numeric values (except bounds)
        Returns:
            XPath combining selected attributes dynamically
        """
        excluded_base = {'bbox', 'elementId', 'package'}
        
        conditions = []
        class_name = self._get_str(element, 'class')
        
        for key, value in element.items():
            if key == 'class':
                continue
            
            if key in excluded_base:
                continue
            
            val_str = str(value).strip() if value else ''
            if not val_str:
                continue
            
            if not exclude_metadata:
                if key != 'bounds':
                    if val_str in ('true', 'false'):
                        continue
                    if val_str.isdigit():
                        continue
            
            conditions.append(f"@{key}={self._escape_xpath(val_str)}")
        
        base = f"//{class_name}" if class_name else "//*"
        
        if not conditions:
            if class_name:
                return base
            raise ValueError("No attributes available")
        
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

