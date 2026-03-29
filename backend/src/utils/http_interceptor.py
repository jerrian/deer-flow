"""HTTP request interceptor for debugging API calls.

This module patches httpx to log all HTTP requests and responses,
including the complete request body with tools parameter.
"""

import json
import logging
from typing import Any

import httpx

logger = logging.getLogger(__name__)

# Store original send methods
_original_sync_send = None
_original_async_send = None
_interceptor_enabled = False


def _log_request(request: httpx.Request) -> None:
    """Log HTTP request details."""
    try:
        # Parse JSON body if present
        body = None
        if request.content:
            try:
                body = json.loads(request.content.decode("utf-8"))
            except (json.JSONDecodeError, UnicodeDecodeError):
                body = request.content[:500]  # Log first 500 bytes

        log_data = {
            "method": request.method,
            "url": str(request.url),
            "headers": dict(request.headers),
            "body": body,
        }

        # If this is an LLM API request, highlight the tools parameter
        if body and isinstance(body, dict):
            if "tools" in body or "functions" in body:
                tools = body.get("tools") or body.get("functions", [])
                logger.info("=" * 80)
                logger.info("HTTP REQUEST TO LLM API")
                logger.info("=" * 80)
                logger.info(f"URL: {request.url}")
                logger.info(f"Model: {body.get('model', 'unknown')}")
                logger.info(f"Messages count: {len(body.get('messages', []))}")
                logger.info(f"Tools count: {len(tools)}")

                if tools:
                    tool_names = []
                    for tool in tools:
                        if isinstance(tool, dict):
                            if "function" in tool:
                                tool_names.append(tool["function"].get("name", "unknown"))
                            elif "name" in tool:
                                tool_names.append(tool["name"])

                    logger.info(f"Tool names: {', '.join(tool_names)}")
                    logger.info("\nFull tools parameter:")
                    logger.info(json.dumps(tools, indent=2, ensure_ascii=False))
                else:
                    logger.info("No tools in request")

                logger.info("=" * 80)
            else:
                logger.debug(f"HTTP {request.method} {request.url}")
        else:
            logger.debug(f"HTTP {request.method} {request.url}")

    except Exception as e:
        logger.error(f"Failed to log HTTP request: {e}")


def _patched_sync_send(self, request: httpx.Request, **kwargs) -> httpx.Response:
    """Patched sync send method."""
    _log_request(request)
    return _original_sync_send(self, request, **kwargs)


async def _patched_async_send(self, request: httpx.Request, **kwargs) -> httpx.Response:
    """Patched async send method."""
    _log_request(request)
    return await _original_async_send(self, request, **kwargs)


def enable_http_interception() -> None:
    """Enable HTTP request interception.

    This patches httpx.Client and httpx.AsyncClient to log all requests.
    Call this once at application startup.
    """
    global _original_sync_send, _original_async_send, _interceptor_enabled

    if _interceptor_enabled:
        logger.warning("HTTP interception already enabled")
        return

    try:
        # Patch sync client
        _original_sync_send = httpx.Client.send
        httpx.Client.send = _patched_sync_send

        # Patch async client
        _original_async_send = httpx.AsyncClient.send
        httpx.AsyncClient.send = _patched_async_send

        _interceptor_enabled = True
        logger.info("HTTP request interception enabled (httpx patched)")
    except Exception as e:
        logger.error(f"Failed to enable HTTP interception: {e}")


def disable_http_interception() -> None:
    """Disable HTTP request interception and restore original methods."""
    global _original_sync_send, _original_async_send, _interceptor_enabled

    if not _interceptor_enabled:
        logger.warning("HTTP interception not enabled")
        return

    try:
        if _original_sync_send:
            httpx.Client.send = _original_sync_send
        if _original_async_send:
            httpx.AsyncClient.send = _original_async_send

        _interceptor_enabled = False
        logger.info("HTTP request interception disabled")
    except Exception as e:
        logger.error(f"Failed to disable HTTP interception: {e}")
