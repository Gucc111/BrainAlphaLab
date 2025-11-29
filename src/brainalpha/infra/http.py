"""HTTP client abstraction for WorldQuant Brain API access."""
from __future__ import annotations

import logging
import time
from typing import Any, Dict, Optional

import httpx

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = 15.0
DEFAULT_RETRIES = 3
RETRY_BACKOFF = 2.0


class BrainHttpClient:
    """Simple HTTP client with retry and base URL handling."""

    def __init__(
        self,
        base_url: str,
        api_key: str = "",
        timeout: float = DEFAULT_TIMEOUT,
        retries: int = DEFAULT_RETRIES,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
        self.retries = retries
        self._client = httpx.Client(timeout=timeout)

    def _headers(self) -> Dict[str, str]:
        headers: Dict[str, str] = {
            "User-Agent": "brainalpha-cli/0.1",
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def _request(self, method: str, path: str, **kwargs: Any) -> httpx.Response:
        url = f"{self.base_url}/{path.lstrip('/')}"
        kwargs.setdefault("headers", {}).update(self._headers())

        attempt = 0
        while True:
            attempt += 1
            try:
                response = self._client.request(method, url, **kwargs)
                if response.status_code in (429, 500, 502, 503, 504) and attempt <= self.retries:
                    delay = RETRY_BACKOFF ** (attempt - 1)
                    logger.warning(
                        "Received %s for %s %s, retrying in %.1fs (attempt %s/%s)",
                        response.status_code,
                        method,
                        url,
                        delay,
                        attempt,
                        self.retries,
                    )
                    time.sleep(delay)
                    continue
                response.raise_for_status()
                return response
            except httpx.HTTPStatusError:
                raise
            except httpx.HTTPError as exc:  # network level
                if attempt > self.retries:
                    raise
                delay = RETRY_BACKOFF ** (attempt - 1)
                logger.warning(
                    "HTTP error for %s %s: %s. Retrying in %.1fs (attempt %s/%s)",
                    method,
                    url,
                    exc,
                    delay,
                    attempt,
                    self.retries,
                )
                time.sleep(delay)

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> httpx.Response:
        return self._request("GET", path, params=params)

    def post(self, path: str, json: Optional[Dict[str, Any]] = None) -> httpx.Response:
        return self._request("POST", path, json=json)

    def patch(self, path: str, json: Optional[Dict[str, Any]] = None) -> httpx.Response:
        return self._request("PATCH", path, json=json)

    def delete(self, path: str) -> httpx.Response:
        return self._request("DELETE", path)

    def close(self) -> None:
        self._client.close()
