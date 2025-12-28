import requests
from typing import Optional
from Agent.config.config import Config
from Agent.utilities.imguploader._imgbase import BaseImageUploader


class ImgBBUploader(BaseImageUploader):
    def __init__(self):
        self.config = Config()
        self.base_url = "https://api.imgbb.com/1/upload"
        self.headers = {"Accept": "application/json"}

    @property
    def api_key(self):
        return self.config.IMGBB_API_KEY

    def _make_request(self, payload: dict, files: bool = False) -> Optional[str]:
        try:
            if files:
                response = requests.post(self.base_url, files=payload, timeout=10)
            else:
                response = requests.post(self.base_url, data=payload, headers=self.headers, timeout=10)
            response.raise_for_status()
            json_data = response.json()
            return self._extract_url(json_data)
        except Exception:
            return None

    def _extract_url(self, json_data: dict) -> Optional[str]:
        data = json_data.get("data", {})
        return data.get("display_url")

    def upload_from_base64(self, base64_data: str, filename: str = "screenshot.png", expiration: Optional[int] = None) -> Optional[str]:
        # , was causing error
        if "," in base64_data:
            base64_data = base64_data.split(",", 1)[1]
            
        payload = {"key": self.api_key, "image": base64_data, "name": filename}
        if expiration is not None:
            payload["expiration"] = str(expiration)
        return self._make_request(payload)

    # def upload_from_file(self, file_path: str, expiration: Optional[int] = None) -> Optional[str]:
    #     try:
    #         with open(file_path, "rb") as file:
    #             payload = {"key": (None, self.api_key), "image": (os.path.basename(file_path), file)}
    #             if expiration is not None:
    #                 payload["expiration"] = (None, str(expiration))
    #             return self._make_request(payload, files=True)
    #     except FileNotFoundError:
    #         full_path = os.path.abspath(file_path)
    #         self.logger.error(f"File not found: {full_path}")
    #         raise FileNotFoundError(f"File not found: {full_path}")



