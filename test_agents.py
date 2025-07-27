#!/usr/bin/env python3
"""
Test script for OpenAI Agents Framework
Simple test to verify agents are working correctly
"""

import os
from dotenv import load_dotenv
from agents import Agent, Runner

# Load environment variables
load_dotenv()

def test_basic_agent():
    """Test basic agent functionality"""
    print("🧪 Testing basic agent functionality...")
    
    # Verify API key is set
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not found in environment")
        return False
    
    print(f"✅ API key found: {api_key[:8]}...")
    
    # Create simple test agent
    agent = Agent(
        name="Test Agent",
        instructions="You are a helpful test assistant. Provide brief, clear responses."
    )
    
    print("✅ Agent created successfully")
    
    # Test with simple query
    test_query = "What is 2+2?"
    print(f"🔍 Testing query: {test_query}")
    
    try:
        result = Runner.run_sync(agent, test_query)
        print(f"✅ Agent response: {result.final_output}")
        return True
    except Exception as e:
        print(f"❌ Agent failed: {str(e)}")
        return False

def test_nasa_agent():
    """Test NASA-specific agent"""
    print("\n🚀 Testing NASA agent...")
    
    # Create NASA agent
    nasa_agent = Agent(
        name="NASA Test Agent",
        instructions="""You are a NASA specialist. Respond with technical accuracy about space missions.
        Keep responses concise but informative."""
    )
    
    test_query = "What is the purpose of the Artemis program?"
    print(f"🔍 Testing NASA query: {test_query}")
    
    try:
        result = Runner.run_sync(nasa_agent, test_query)
        print(f"✅ NASA agent response: {result.final_output}")
        return True
    except Exception as e:
        print(f"❌ NASA agent failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("🧪 OpenAI Agents Framework Test Suite")
    print("=" * 50)
    
    # Test basic functionality
    basic_success = test_basic_agent()
    
    # Test NASA agent if basic test passes
    nasa_success = False
    if basic_success:
        nasa_success = test_nasa_agent()
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print(f"   Basic Agent: {'✅ PASS' if basic_success else '❌ FAIL'}")
    print(f"   NASA Agent:  {'✅ PASS' if nasa_success else '❌ FAIL'}")
    
    if basic_success and nasa_success:
        print("\n🎉 All tests passed! Agents framework is working correctly.")
        print("🚀 Ready to launch NASA agents application!")
    else:
        print("\n⚠️  Some tests failed. Please check configuration.")