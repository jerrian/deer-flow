"""Request logging callback for debugging API requests."""

import json
import logging
from typing import Any

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.messages import BaseMessage

logger = logging.getLogger(__name__)


class RequestLoggerCallback(BaseCallbackHandler):
    """Callback that logs complete API requests including tools parameter.

    This callback captures and logs the full LLM API request, including:
    - Messages (system, user, assistant)
    - Tools parameter (function definitions)
    - Model configuration
    - Other parameters

    Enable by setting DEER_FLOW_LOG_API_REQUESTS=true environment variable.
    """

    def on_chat_model_start(
        self,
        serialized: dict[str, Any],
        messages: list[list[BaseMessage]],
        **kwargs: Any,
    ) -> None:
        """Log when chat model starts processing."""
        try:
            # Extract invocation params which include tools
            invocation_params = kwargs.get("invocation_params", {})

            # Format messages for logging
            formatted_messages = []
            for message_batch in messages:
                batch = []
                for msg in message_batch:
                    batch.append({
                        "type": msg.__class__.__name__,
                        "content": str(msg.content)[:200] + "..." if len(str(msg.content)) > 200 else str(msg.content),
                    })
                formatted_messages.append(batch)

            # Extract tools parameter
            tools = invocation_params.get("tools", [])

            # Log the complete request
            log_data = {
                "event": "chat_model_start",
                "model": invocation_params.get("model", "unknown"),
                "message_count": sum(len(batch) for batch in messages),
                "messages": formatted_messages,
                "tools_count": len(tools),
                "tools": tools,  # Full tools parameter
                "other_params": {
                    k: v for k, v in invocation_params.items()
                    if k not in ["tools", "model"]
                },
            }

            logger.info("=" * 80)
            logger.info("LLM API REQUEST")
            logger.info("=" * 80)
            logger.info(json.dumps(log_data, indent=2, ensure_ascii=False))
            logger.info("=" * 80)

            # Also log just the tool names for quick reference
            if tools:
                tool_names = []
                for tool in tools:
                    if isinstance(tool, dict):
                        # OpenAI format: {"type": "function", "function": {"name": "..."}}
                        if "function" in tool:
                            tool_names.append(tool["function"].get("name", "unknown"))
                        # Direct format: {"name": "..."}
                        elif "name" in tool:
                            tool_names.append(tool["name"])

                logger.info(f"Tools in request ({len(tool_names)}): {', '.join(tool_names)}")
            else:
                logger.info("No tools in request")

        except Exception as e:
            logger.error(f"Failed to log API request: {e}", exc_info=True)
