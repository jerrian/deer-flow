#!/usr/bin/env python3
"""Test script for API request logging.

This script tests the request logging functionality by creating a simple
agent interaction and verifying that tools are logged correctly.
"""

import os
import sys
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

# Enable request logging
os.environ["DEER_FLOW_LOG_API_REQUESTS"] = "true"
os.environ["LOG_LEVEL"] = "INFO"


def test_callback_logging():
    """Test the callback-based request logging."""
    print("=" * 80)
    print("Testing Callback-based Request Logging")
    print("=" * 80)

    from src.models.factory import create_chat_model
    from src.tools import get_available_tools
    from langchain_core.messages import HumanMessage, SystemMessage

    # Create model with logging enabled
    model = create_chat_model()
    print(f"\nModel created: {model.__class__.__name__}")

    # Get available tools
    tools = get_available_tools(subagent_enabled=True)
    print(f"Available tools: {len(tools)}")
    print(f"Tool names: {', '.join(t.name for t in tools)}")

    # Bind tools to model (this is what LangChain does internally)
    model_with_tools = model.bind_tools(tools)

    # Create a simple message
    messages = [
        SystemMessage(content="You are a helpful assistant."),
        HumanMessage(content="What tools do you have access to?"),
    ]

    print("\n" + "=" * 80)
    print("Invoking model with tools...")
    print("=" * 80)
    print("\nExpected output:")
    print("- LLM API REQUEST log with tools count")
    print("- Tool names list")
    print("- Complete tools parameter in JSON")
    print("\n" + "=" * 80)

    # Invoke the model (this will trigger the callback)
    try:
        response = model_with_tools.invoke(messages)
        print("\n✅ Request completed successfully")
        print(f"\nResponse preview: {response.content[:100]}...")
    except Exception as e:
        print(f"\n❌ Request failed: {e}")
        print("\nNote: This is expected if you don't have a valid API key configured.")
        print("The important part is that the REQUEST was logged above.")


def test_http_interception():
    """Test the HTTP-level request interception."""
    print("\n" + "=" * 80)
    print("Testing HTTP Interception")
    print("=" * 80)

    from src.utils.http_interceptor import enable_http_interception
    from src.models.factory import create_chat_model
    from src.tools import get_available_tools
    from langchain_core.messages import HumanMessage

    # Enable HTTP interception
    enable_http_interception()
    print("\n✅ HTTP interception enabled")

    # Create model and invoke
    model = create_chat_model()
    tools = get_available_tools(subagent_enabled=True)
    model_with_tools = model.bind_tools(tools)

    print("\nInvoking model with HTTP interception...")
    print("Expected: HTTP REQUEST TO LLM API log with complete request body")
    print("\n" + "=" * 80)

    try:
        response = model_with_tools.invoke([HumanMessage(content="Hello")])
        print("\n✅ Request completed successfully")
    except Exception as e:
        print(f"\n❌ Request failed: {e}")
        print("\nNote: The HTTP request should still have been logged above.")


def main():
    """Run all tests."""
    print("\n" + "=" * 80)
    print("DeerFlow API Request Logging Test")
    print("=" * 80)
    print("\nThis script will test different methods of logging API requests.")
    print("You should see detailed logs showing the tools parameter.\n")

    # Test 1: Callback logging
    try:
        test_callback_logging()
    except Exception as e:
        print(f"\n❌ Callback logging test failed: {e}")
        import traceback
        traceback.print_exc()

    # Test 2: HTTP interception
    try:
        test_http_interception()
    except Exception as e:
        print(f"\n❌ HTTP interception test failed: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 80)
    print("Test Complete")
    print("=" * 80)
    print("\nReview the logs above to verify that:")
    print("1. Tools count is displayed")
    print("2. Tool names are listed")
    print("3. Complete tool definitions are shown in JSON format")
    print("\nIf you see 'LLM API REQUEST' sections with tools data, logging is working!")


if __name__ == "__main__":
    main()
