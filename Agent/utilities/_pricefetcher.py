"""
Price Fetcher Utility
Fetches current LLM pricing from Helicone API with fallback to local config.

How it works:
1. Fetches pricing from Helicone API (https://www.helicone.ai/api/llm-costs)
2. Stores model names exactly as returned by the API (e.g., 'gpt-4o', 'claude-sonnet-4-5-20250929')
3. When LLM APIs return response.model, that exact name is used to lookup pricing
4. Falls back to local config file if API is unavailable
5. Caches pricing for 24 hours to minimize API calls

No manual model name mapping needed - uses actual model names from both sides.
"""
import json
import requests
from typing import Dict, Optional, Tuple
from datetime import datetime, timedelta
from threading import Lock
from robot.api import logger


class PriceFetcher:
    """
    Fetches and caches LLM pricing information from Helicone API.
    Falls back to local config file if API is unavailable.
    """
    
    _instance = None
    _lock = Lock()
    HELICONE_API_URL = "https://www.helicone.ai/api/llm-costs"
    CACHE_DURATION_HOURS = 24  # Cache prices for 24 hours
    
    # Mapping from Helicone provider names to our provider names
    PROVIDER_MAP = {
        "OPENAI": "openai",
        "ANTHROPIC": "anthropic",
        "GOOGLE": "gemini",
        "DEEPSEEK": "deepseek",
    }
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._cached_prices: Optional[Dict] = None
            self._cache_timestamp: Optional[datetime] = None
            self._initialized = True
    
    def _is_cache_valid(self) -> bool:
        """Check if cached prices are still valid."""
        if self._cached_prices is None or self._cache_timestamp is None:
            return False
        
        age = datetime.now() - self._cache_timestamp
        return age < timedelta(hours=self.CACHE_DURATION_HOURS)
    
    def _fetch_from_helicone(self) -> Optional[Dict]:
        """
        Fetch pricing data from Helicone API.
        
        Returns:
            Dictionary with pricing data or None if fetch failed
        """
        try:
            logger.info("Fetching LLM pricing from Helicone API...")
            response = requests.get(self.HELICONE_API_URL, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"Successfully fetched pricing for {len(data.get('data', []))} models from Helicone")
            return data
            
        except requests.exceptions.Timeout:
            logger.warn("Helicone API request timed out")
            return None
        except requests.exceptions.RequestException as e:
            logger.warn(f"Failed to fetch from Helicone API: {str(e)}")
            return None
        except json.JSONDecodeError as e:
            logger.warn(f"Failed to parse Helicone API response: {str(e)}")
            return None
        except Exception as e:
            logger.warn(f"Unexpected error fetching from Helicone API: {str(e)}")
            return None
    
    def _parse_helicone_data(self, helicone_data: Dict) -> Dict[str, Dict[str, float]]:
        """
        Parse Helicone API response and convert to our pricing format.
        Uses the exact model names from the API response without any mapping.
        
        Args:
            helicone_data: Raw data from Helicone API
            
        Returns:
            Dictionary mapping model_name -> {'input': float, 'output': float}
        """
        pricing_dict = {}
        
        if not helicone_data or 'data' not in helicone_data:
            return pricing_dict
        
        for item in helicone_data['data']:
            provider = item.get('provider', '').upper()
            model = item.get('model', '')
            input_cost = item.get('input_cost_per_1m', 0)
            output_cost = item.get('output_cost_per_1m', 0)
            
            # Check if this is a provider we support
            if provider not in self.PROVIDER_MAP:
                continue
            
            # Skip if no model name or costs
            if not model:
                continue
            
            # Use the model name directly from Helicone - no mapping needed
            # This will match the model name returned by the LLM API response
            pricing_dict[model] = {
                'input': float(input_cost),
                'output': float(output_cost)
            }
            logger.debug(f"Fetched pricing for {provider}/{model}: input=${input_cost}/1M, output=${output_cost}/1M")
        
        return pricing_dict
    
    def get_current_prices(self, force_refresh: bool = False) -> Tuple[Dict[str, Dict[str, float]], str]:
        """
        Get current LLM pricing, either from cache, Helicone API, or fallback config.
        
        Args:
            force_refresh: If True, bypass cache and fetch fresh data
            
        Returns:
            Tuple of (pricing_dict, source) where source is 'cache', 'api', or 'config'
        """
        with self._lock:
            # Check cache first
            if not force_refresh and self._is_cache_valid():
                logger.debug("Using cached pricing data")
                return self._cached_prices, 'cache'
            
            # Try to fetch from Helicone API
            helicone_data = self._fetch_from_helicone()
            
            if helicone_data:
                pricing_dict = self._parse_helicone_data(helicone_data)
                
                if pricing_dict:
                    # Update cache
                    self._cached_prices = pricing_dict
                    self._cache_timestamp = datetime.now()
                    logger.info(f"Updated pricing cache with {len(pricing_dict)} models from Helicone API")
                    return pricing_dict, 'api'
            
            # Fallback to config file
            logger.info("Falling back to config file for pricing")
            return self._get_config_prices(), 'config'
    
    def _get_config_prices(self) -> Dict[str, Dict[str, float]]:
        """
        Load pricing from local config file.
        
        Returns:
            Dictionary with pricing from config file
        """
        try:
            from Agent.config.model_config import ModelConfig
            config = ModelConfig()
            pricing_dict = config.get_pricing_dict()
            logger.debug(f"Loaded {len(pricing_dict)} models from config file")
            return pricing_dict
        except Exception as e:
            logger.error(f"Failed to load pricing from config file: {str(e)}")
            return {}
    
    def update_pricing_for_provider(self, provider: str) -> Tuple[Dict[str, Dict[str, float]], str]:
        """
        Fetch pricing for a specific provider.
        
        Args:
            provider: Provider name (e.g., 'openai', 'anthropic', 'gemini')
            
        Returns:
            Tuple of (pricing_dict, source)
        """
        # Map our provider name to Helicone provider name
        helicone_provider = None
        for h_provider, our_provider in self.PROVIDER_MAP.items():
            if our_provider.lower() == provider.lower():
                helicone_provider = h_provider
                break
        
        if not helicone_provider:
            logger.warn(f"Provider {provider} not supported for Helicone API fetch")
            return self._get_config_prices(), 'config'
        
        try:
            logger.info(f"Fetching pricing for {provider} from Helicone API...")
            url = f"{self.HELICONE_API_URL}?provider={helicone_provider}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            pricing_dict = self._parse_helicone_data(data)
            
            if pricing_dict:
                logger.info(f"Fetched pricing for {len(pricing_dict)} {provider} models")
                return pricing_dict, 'api'
            
        except Exception as e:
            logger.warn(f"Failed to fetch {provider} pricing from Helicone: {str(e)}")
        
        # Fallback to config
        return self._get_config_prices(), 'config'
    
    def clear_cache(self):
        """Clear the pricing cache."""
        with self._lock:
            self._cached_prices = None
            self._cache_timestamp = None
            logger.debug("Pricing cache cleared")

