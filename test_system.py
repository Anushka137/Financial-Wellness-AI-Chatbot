#!/usr/bin/env python3
"""
Test script for Financial Wellness AI Chatbot
Verifies that all components are working correctly
"""

import asyncio
import json
import sys
import os
from datetime import datetime

# Add client directory to path
sys.path.append('client')

from config_manager import ConfigManager

async def test_config():
    """Test configuration loading"""
    print("Testing configuration...")
    config = ConfigManager()
    
    if config.validate_config():
        print("✓ Configuration is valid")
        return True
    else:
        print("✗ Configuration is invalid")
        print("Please run: cd client && python config_manager.py")
        return False

async def test_api_server():
    """Test API server connectivity"""
    print("Testing API server...")
    
    try:
        import httpx
        config = ConfigManager()
        api_url = config.get("API_URL", "http://localhost:8000")
        
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{api_url}/")
            if response.status_code == 200:
                print("✓ API server is running")
                return True
            else:
                print(f"✗ API server returned status {response.status_code}")
                return False
    except Exception as e:
        print(f"✗ Cannot connect to API server: {e}")
        print("Make sure to start the server with: python api_server.py")
        return False

async def test_data_file():
    """Test financial data file"""
    print("Testing data file...")
    
    if os.path.exists("financial_data.json"):
        try:
            with open("financial_data.json", 'r') as f:
                data = json.load(f)
            
            if "transactions" in data and "budgets" in data:
                print(f"✓ Data file loaded successfully ({len(data['transactions'])} transactions)")
                return True
            else:
                print("✗ Data file is missing required fields")
                return False
        except Exception as e:
            print(f"✗ Error loading data file: {e}")
            return False
    else:
        print("✗ Data file not found")
        return False

async def test_dependencies():
    """Test required dependencies"""
    print("Testing dependencies...")
    
    required_packages = [
        "fastapi",
        "uvicorn", 
        "google.generativeai",
        "httpx",
        "matplotlib",
        "pandas",
        "plotly"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace(".", "_"))
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} - missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("Install with: pip install -r requirements.txt")
        return False
    
    return True

async def test_client():
    """Test client functionality"""
    print("Testing client...")
    
    try:
        from universal_client import FinancialWellnessClient
        
        client = FinancialWellnessClient()
        
        # Test API request
        result = await client.get_analytics()
        if "analytics" in result:
            print("✓ Client can connect to API")
            return True
        else:
            print("✗ Client API request failed")
            return False
            
    except Exception as e:
        print(f"✗ Client test failed: {e}")
        return False

async def test_mcp_client():
    """Test MCP client"""
    print("Testing MCP client...")
    
    try:
        from mcp_client import FinancialWellnessMCPClient
        
        client = FinancialWellnessMCPClient()
        tools = client.list_tools()
        
        if len(tools) >= 8:  # Should have at least 8 tools
            print(f"✓ MCP client has {len(tools)} tools available")
            return True
        else:
            print(f"✗ MCP client has insufficient tools: {len(tools)}")
            return False
            
    except Exception as e:
        print(f"✗ MCP client test failed: {e}")
        return False

async def run_sample_queries():
    """Run sample queries to test the system"""
    print("Testing sample queries...")
    
    try:
        from universal_client import FinancialWellnessClient
        
        client = FinancialWellnessClient()
        
        # Test basic queries
        queries = [
            "How much did I spend on food this month?",
            "Show me my budget status",
            "What are my savings goals?"
        ]
        
        for query in queries:
            print(f"Testing: {query}")
            try:
                response = await client.process_query(query)
                if response and "error" not in response.lower():
                    print(f"✓ Query successful")
                else:
                    print(f"✗ Query failed: {response}")
            except Exception as e:
                print(f"✗ Query error: {e}")
        
        return True
        
    except Exception as e:
        print(f"✗ Sample queries test failed: {e}")
        return False

async def main():
    """Run all tests"""
    print("Financial Wellness AI Chatbot - System Test")
    print("=" * 50)
    print()
    
    tests = [
        ("Dependencies", test_dependencies),
        ("Configuration", test_config),
        ("Data File", test_data_file),
        ("API Server", test_api_server),
        ("Client", test_client),
        ("MCP Client", test_mcp_client),
        ("Sample Queries", run_sample_queries)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        try:
            result = await test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your system is ready to use.")
        print("\nNext steps:")
        print("1. Start the server: python api_server.py")
        print("2. Test the chatbot: cd client && python universal_client.py")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please fix the issues above.")
        
        if not any(name == "API Server" and result for name, result in results):
            print("\nTo start the server:")
            print("python api_server.py")
        
        if not any(name == "Configuration" and result for name, result in results):
            print("\nTo configure the system:")
            print("cd client && python config_manager.py")

if __name__ == "__main__":
    asyncio.run(main()) 