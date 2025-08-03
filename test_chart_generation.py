#!/usr/bin/env python3
"""
Test script to verify chart generation functionality
"""

import asyncio
import json
from enhanced_financial_client import EnhancedFinancialClient

async def test_chart_generation():
    """Test chart generation through the chatbot"""
    
    print("🧪 Testing Chart Generation Functionality")
    print("=" * 50)
    
    # Load configuration
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        api_key = config.get('GOOGLE_API_KEY')
    except Exception as e:
        print(f"⚠️ Warning: Could not load API key: {e}")
        print("Using test mode...")
        api_key = "test"
    
    # Initialize client
    client = EnhancedFinancialClient(api_key)
    
    # Test queries for different chart types
    test_queries = [
        "Generate a spending trend chart",
        "Create a category breakdown chart",
        "Show me a budget vs actual chart",
        "Generate a merchant analysis chart",
        "Create a pie chart of my spending",
        "Show me a bar chart of my expenses"
    ]
    
    print("\n📊 Testing Chart Generation Queries:")
    print("-" * 50)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Testing: '{query}'")
        
        # Analyze the query
        analysis = client.analyze_query(query)
        print(f"   Analysis: {analysis}")
        
        # Process the query
        try:
            response = await client.process_query(query)
            print(f"   Response: {response[:200]}...")
            
            # Check if chart was mentioned in response
            if "chart" in response.lower() and "saved" in response.lower():
                print("   ✅ Chart generation successful!")
            else:
                print("   ❌ Chart generation failed or not mentioned")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Chart Generation Test Complete!")
    print("\nCheck the 'charts/' directory for generated files:")
    
    import os
    if os.path.exists('charts/'):
        files = os.listdir('charts/')
        for file in files:
            if file.endswith('.png'):
                print(f"  📊 {file}")

if __name__ == "__main__":
    asyncio.run(test_chart_generation()) 