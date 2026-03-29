# API Request Debugging Guide

This guide explains how to capture and inspect the complete API requests sent to LLM providers, including the `tools` parameter that contains function definitions.

## Problem Statement

When debugging tool availability issues, you may notice that API request logs show only the text prompt, but not the complete API request body. The `tools` parameter (containing function definitions) is passed separately from the prompt text and may not appear in standard logs.

## Solution Overview

We provide three methods to capture complete API requests:

| Method | Complexity | Detail Level | Code Changes Required |
|--------|-----------|--------------|----------------------|
| LangChain Debug Mode | Low | Medium | None (env var only) |
| Callback Handler | Medium | High | None (env var only) |
| HTTP Interceptor | High | Complete | Minimal (startup hook) |

---

## Method 1: LangChain Debug Mode

**Best for**: Quick debugging without code changes

### Setup

```bash
# Set environment variable
export LANGCHAIN_VERBOSE=true

# Restart LangGraph server
cd backend
make dev
```

### Expected Output

```
[chain/start] [1:chain:AgentExecutor] Entering Chain run with input: {...}
[llm/start] [1:chain:AgentExecutor > 2:llm:ChatOpenAI] Entering LLM run with input:
{
  "messages": [
    SystemMessage(content="You are..."),
    HumanMessage(content="What is..."),
  ]
}
```

**Limitations**: May not show the complete `tools` parameter.

---

## Method 2: Callback Handler (Recommended)

**Best for**: Detailed tool inspection with minimal setup

### Setup

```bash
# Enable request logging
export DEER_FLOW_LOG_API_REQUESTS=true

# Optional: Set log level to INFO
export LOG_LEVEL=INFO

# Restart LangGraph server
cd backend
make dev
```

### Expected Output

```
================================================================================
LLM API REQUEST
================================================================================
{
  "event": "chat_model_start",
  "model": "gpt-4-turbo",
  "message_count": 2,
  "messages": [
    [
      {
        "type": "SystemMessage",
        "content": "You are DeerFlow 2.0, an open-source super agent..."
      },
      {
        "type": "HumanMessage",
        "content": "What is the weather today?"
      }
    ]
  ],
  "tools_count": 15,
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "bash",
        "description": "Execute a bash command...",
        "parameters": {
          "type": "object",
          "properties": {
            "command": {
              "type": "string",
              "description": "The command to execute"
            }
          },
          "required": ["command"]
        }
      }
    },
    {
      "type": "function",
      "function": {
        "name": "read_file",
        "description": "Read contents of a file...",
        "parameters": {...}
      }
    },
    // ... 13 more tools
  ],
  "other_params": {
    "temperature": 0.7,
    "max_tokens": 4096
  }
}
================================================================================
Tools in request (15): bash, read_file, write_file, str_replace, ls, web_search, web_fetch, tavily_search, present_file, ask_clarification, view_image, task, mcp_tool_1, mcp_tool_2, custom_tool
```

**Advantages**:
- Complete visibility into tools parameter
- Structured JSON output
- No code changes (environment variable only)
- Automatic tool name extraction

---

## Method 3: HTTP Interceptor

**Best for**: Network-level inspection of actual HTTP requests

### Setup

1. Enable HTTP interception in your application startup:

```python
# Add to backend/src/main.py or langgraph server startup
import os
from src.utils.http_interceptor import enable_http_interception

if os.getenv("DEER_FLOW_INTERCEPT_HTTP", "").lower() in ("true", "1", "yes"):
    enable_http_interception()
```

2. Set environment variables:

```bash
export DEER_FLOW_INTERCEPT_HTTP=true
export LOG_LEVEL=INFO

# Restart LangGraph server
cd backend
make dev
```

### Expected Output

```
================================================================================
HTTP REQUEST TO LLM API
================================================================================
URL: https://api.openai.com/v1/chat/completions
Model: gpt-4-turbo
Messages count: 2
Tools count: 15
Tool names: bash, read_file, write_file, str_replace, ls, web_search, web_fetch, tavily_search, present_file, ask_clarification, view_image, task, mcp_tool_1, mcp_tool_2, custom_tool

Full tools parameter:
[
  {
    "type": "function",
    "function": {
      "name": "bash",
      "description": "Execute a bash command in a persistent shell session...",
      "parameters": {
        "type": "object",
        "properties": {
          "command": {
            "type": "string",
            "description": "The command to execute"
          },
          "timeout": {
            "type": "number",
            "description": "Optional timeout in milliseconds"
          }
        },
        "required": ["command"]
      }
    }
  },
  // ... complete function definitions for all 15 tools
]
================================================================================
```

**Advantages**:
- Captures the **exact** HTTP request body
- Shows actual network payload
- Includes headers and authentication
- Works for all HTTP-based providers

**Disadvantages**:
- Requires minimal code change (startup hook)
- More verbose output
- May log sensitive data (API keys in headers)

---

## Comparison: What Each Method Logs

| Feature | Debug Mode | Callback | HTTP Interceptor |
|---------|-----------|----------|-----------------|
| System Prompt | ✅ | ✅ | ✅ |
| Messages | ✅ | ✅ | ✅ |
| Tools Parameter | ⚠️ Partial | ✅ Complete | ✅ Complete |
| Tool Definitions | ❌ | ✅ | ✅ |
| HTTP Headers | ❌ | ❌ | ✅ |
| Request URL | ❌ | ❌ | ✅ |
| Authentication | ❌ | ❌ | ✅ |

---

## Troubleshooting

### No logs appearing

1. Check log level:
   ```bash
   export LOG_LEVEL=INFO  # or DEBUG
   ```

2. Verify environment variable:
   ```bash
   env | grep DEER_FLOW
   ```

3. Restart the server:
   ```bash
   cd backend
   make stop
   make dev
   ```

### Tools parameter still not visible

If you're using **Method 1** (Debug Mode) and still don't see tools, upgrade to **Method 2** (Callback Handler).

### Too much output

Filter logs by logger name:
```bash
# Only show request logger output
export LOG_FILTER="src.utils.request_logger"
```

Or use grep:
```bash
make dev 2>&1 | grep -A 50 "LLM API REQUEST"
```

---

## Security Considerations

⚠️ **WARNING**: These debugging methods log complete API requests, which may include:
- API keys in headers (Method 3 only)
- User messages and conversation history
- System prompts with sensitive instructions
- Internal tool configurations

**Recommendations**:
1. **Only enable in development environments**
2. **Never commit logs to version control**
3. **Disable before deploying to production**
4. **Use log rotation to prevent disk space issues**

---

## Implementation Details

### How Tools Are Passed to LLM APIs

The `tools` parameter is passed separately from the text prompt:

```json
{
  "model": "gpt-4",
  "messages": [
    {"role": "system", "content": "You are..."},
    {"role": "user", "content": "What is..."}
  ],
  "tools": [
    {"type": "function", "function": {...}},
    {"type": "function", "function": {...}}
  ],
  "temperature": 0.7
}
```

**Why standard logs miss this**:
- Most logging captures only the `messages` array (the text prompt)
- The `tools` parameter is a separate field in the request body
- LangChain's `create_agent()` function binds tools internally
- The binding happens inside provider-specific code (OpenAI, Anthropic, etc.)

### Where Tools Come From

Tools are assembled in `src/tools/tools.py` from 4 sources:

1. **Config tools** (`config.yaml`)
2. **MCP tools** (`extensions_config.json`)
3. **Built-in tools** (hardcoded)
4. **Subagent tools** (conditional)

See `get_available_tools()` function for details.

---

## Example: Debugging Tool Availability

**Scenario**: AI mentions a tool that shouldn't be available

1. Enable callback logging:
   ```bash
   export DEER_FLOW_LOG_API_REQUESTS=true
   make dev
   ```

2. Trigger the problematic request

3. Check the logs for `Tools in request`:
   ```
   Tools in request (15): bash, read_file, ...
   ```

4. Verify against expected tools in `config.yaml` and `extensions_config.json`

5. If tool count doesn't match:
   - Check MCP server status
   - Verify `subagent_enabled` config
   - Review model's `supports_vision` setting

---

## See Also

- [Tool System Documentation](../README.md#tool-system)
- [MCP Integration Guide](./MCP.md)
- [LangChain Callbacks Documentation](https://python.langchain.com/docs/modules/callbacks/)
