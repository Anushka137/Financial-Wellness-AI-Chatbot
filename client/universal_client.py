#!/usr/bin/env python3
"""
Financial Wellness AI Chatbot - Universal Client
A natural language interface for personal finance management
"""

import sys
import os
import json
import asyncio
import httpx
import google.generativeai as genai
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import matplotlib.pyplot as plt
import pandas as pd
from config_manager import ConfigManager

class FinancialWellnessClient:
    def __init__(self):
        self.config = ConfigManager()
        self.api_url = self.config.get("API_URL", "http://localhost:8000")
        self.api_key = self.config.get("API_KEY", "your-api-key")
        self.google_api_key = self.config.get("GOOGLE_API_KEY", "")
        
        # Initialize Gemini AI
        if self.google_api_key:
            genai.configure(api_key=self.google_api_key)
            self.model = genai.GenerativeModel('gemini-1.5-pro-latest')
        else:
            self.model = None
            print("Warning: No Google API key provided. AI features will be limited.")
        
        # Query memory for context
        self.query_memory = []
        self.max_memory = 10
    
    async def make_api_request(self, endpoint: str, method: str = "GET", data: Dict = None) -> Dict:
        """Make API request to the financial wellness server"""
        url = f"{self.api_url}{endpoint}"
        headers = {"X-API-Key": self.api_key} if self.api_key != "your-api-key" else {}
        
        try:
            async with httpx.AsyncClient() as client:
                if method == "GET":
                    response = await client.get(url, headers=headers)
                elif method == "POST":
                    response = await client.post(url, json=data, headers=headers)
                elif method == "PUT":
                    response = await client.put(url, json=data, headers=headers)
                
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            print(f"API Error: {e.response.status_code} - {e.response.text}")
            return {"error": f"API request failed: {e.response.status_code}"}
        except Exception as e:
            print(f"Request Error: {e}")
            return {"error": f"Request failed: {str(e)}"}
    
    def add_to_memory(self, query: str, response: str):
        """Add query-response pair to memory for context"""
        self.query_memory.append({
            "query": query,
            "response": response,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep only recent queries
        if len(self.query_memory) > self.max_memory:
            self.query_memory.pop(0)
    
    def get_context_from_memory(self) -> str:
        """Get context from recent queries"""
        if not self.query_memory:
            return ""
        
        context = "Recent conversation context:\n"
        for item in self.query_memory[-3:]:  # Last 3 queries
            context += f"User: {item['query']}\n"
            context += f"Assistant: {item['response'][:200]}...\n\n"
        
        return context
    
    async def get_transactions(self, filters: Dict = None) -> Dict:
        """Get transactions with optional filtering"""
        endpoint = "/transactions"
        if filters:
            params = []
            for key, value in filters.items():
                if value:
                    params.append(f"{key}={value}")
            if params:
                endpoint += "?" + "&".join(params)
        
        return await self.make_api_request(endpoint)
    
    async def add_transaction(self, transaction_data: Dict) -> Dict:
        """Add a new transaction"""
        return await self.make_api_request("/transactions", "POST", transaction_data)
    
    async def get_budget_status(self) -> Dict:
        """Get current budget status"""
        return await self.make_api_request("/budget")
    
    async def get_savings_goals(self) -> Dict:
        """Get savings goals"""
        return await self.make_api_request("/savings-goals")
    
    async def create_savings_goal(self, goal_data: Dict) -> Dict:
        """Create a new savings goal"""
        return await self.make_api_request("/savings-goals", "POST", goal_data)
    
    async def get_analytics(self) -> Dict:
        """Get financial analytics"""
        return await self.make_api_request("/analytics")
    
    async def get_spending_analysis(self, days: int = 30) -> Dict:
        """Get spending analysis for specified days"""
        return await self.make_api_request(f"/spending-analysis?days={days}")
    
    async def get_recommendations(self) -> Dict:
        """Get personalized recommendations"""
        return await self.make_api_request("/recommendations")
    
    async def generate_chart(self, chart_type: str) -> str:
        """Generate and save a chart"""
        try:
            response = await self.make_api_request(f"/charts/{chart_type}")
            if "error" not in response:
                return f"Chart generated successfully: {chart_type}"
            else:
                return f"Failed to generate chart: {response['error']}"
        except Exception as e:
            return f"Chart generation failed: {str(e)}"
    
    def parse_financial_query(self, query: str) -> Dict:
        """Parse natural language query to determine intent and extract parameters"""
        query_lower = query.lower()
        
        # Define intent patterns
        intent_patterns = {
            "get_transactions": [
                "show", "get", "list", "view", "see", "what", "how much", "spent", "spending"
            ],
            "add_transaction": [
                "add", "record", "log", "enter", "new expense", "new income", "spent", "earned"
            ],
            "budget_status": [
                "budget", "budget status", "budget vs", "remaining", "limit"
            ],
            "savings_goals": [
                "savings", "goal", "target", "progress", "save"
            ],
            "analytics": [
                "analytics", "analysis", "insights", "trends", "breakdown", "summary"
            ],
            "recommendations": [
                "recommend", "advice", "suggest", "tip", "improve"
            ],
            "generate_chart": [
                "chart", "graph", "visualize", "plot", "pie chart", "bar chart"
            ]
        }
        
        # Determine intent
        intent = "general"
        for intent_name, patterns in intent_patterns.items():
            if any(pattern in query_lower for pattern in patterns):
                intent = intent_name
                break
        
        # Extract parameters
        params = {}
        
        # Date filters
        if "this month" in query_lower:
            params["period"] = "this_month"
        elif "last month" in query_lower:
            params["period"] = "last_month"
        elif "this week" in query_lower:
            params["period"] = "this_week"
        elif "last week" in query_lower:
            params["period"] = "last_week"
        elif "today" in query_lower:
            params["period"] = "today"
        
        # Category filters
        categories = ["food", "dining", "transportation", "entertainment", "shopping", 
                     "utilities", "healthcare", "income"]
        for category in categories:
            if category in query_lower:
                params["category"] = category.title()
                break
        
        # Amount extraction (simple pattern matching)
        import re
        amount_match = re.search(r'\$?(\d+(?:\.\d{2})?)', query)
        if amount_match:
            params["amount"] = float(amount_match.group(1))
        
        return {
            "intent": intent,
            "params": params,
            "original_query": query
        }
    
    async def process_query(self, query: str) -> str:
        """Process a natural language query and return response"""
        if not self.model:
            return "AI features are not available. Please configure your Google API key."
        
        # Parse the query
        parsed = self.parse_financial_query(query)
        intent = parsed["intent"]
        params = parsed["params"]
        
        # Get context from memory
        context = self.get_context_from_memory()
        
        # Build system prompt
        system_prompt = f"""
You are a helpful financial wellness assistant. You help users manage their personal finances through natural language queries.

Available financial data includes:
- Transactions (income and expenses)
- Budget categories and limits
- Savings goals and progress
- Financial analytics and insights
- Personalized recommendations

Context from recent conversation:
{context}

Current query: {query}
Detected intent: {intent}
Extracted parameters: {params}

Please provide a helpful, informative response. If the user is asking for specific data, you can reference the available endpoints but focus on being conversational and helpful.
"""
        
        try:
            # Get relevant data based on intent
            data_response = ""
            
            if intent == "get_transactions":
                filters = {}
                if "category" in params:
                    filters["category"] = params["category"]
                if "period" in params:
                    # Add date filtering logic here
                    pass
                
                result = await self.get_transactions(filters)
                if "transactions" in result:
                    transactions = result["transactions"]
                    if transactions:
                        data_response = f"Found {len(transactions)} transactions. "
                        total = sum(t["amount"] for t in transactions)
                        data_response += f"Total amount: ${total:.2f}"
                    else:
                        data_response = "No transactions found for the specified criteria."
            
            elif intent == "budget_status":
                result = await self.get_budget_status()
                if "budgets" in result:
                    budgets = result["budgets"]
                    data_response = f"Budget status: {len(budgets)} categories tracked. "
                    for category, info in budgets.items():
                        remaining = info.get("remaining", 0)
                        data_response += f"{category}: ${remaining:.2f} remaining. "
            
            elif intent == "savings_goals":
                result = await self.get_savings_goals()
                if "savings_goals" in result:
                    goals = result["savings_goals"]
                    data_response = f"You have {len(goals)} savings goals. "
                    for goal in goals:
                        progress = (goal["current_amount"] / goal["target_amount"]) * 100
                        data_response += f"{goal['name']}: {progress:.1f}% complete. "
            
            elif intent == "analytics":
                result = await self.get_analytics()
                if "analytics" in result:
                    analytics = result["analytics"]
                    data_response = f"Financial summary: Income: ${analytics.get('total_income', 0):.2f}, "
                    data_response += f"Expenses: ${analytics.get('total_expenses', 0):.2f}, "
                    data_response += f"Savings rate: {analytics.get('savings_rate', 0):.1f}%"
            
            elif intent == "recommendations":
                result = await self.get_recommendations()
                if "recommendations" in result:
                    recommendations = result["recommendations"]
                    data_response = f"Found {len(recommendations)} recommendations. "
                    for rec in recommendations[:3]:  # Show top 3
                        data_response += f"{rec['message']} "
            
            # Generate AI response
            full_prompt = f"{system_prompt}\n\nAvailable data: {data_response}\n\nPlease provide a helpful response to the user's query."
            
            response = self.model.generate_content(full_prompt)
            ai_response = response.text
            
            # Add to memory
            self.add_to_memory(query, ai_response)
            
            return ai_response
            
        except Exception as e:
            return f"I encountered an error while processing your query: {str(e)}. Please try again."
    
    async def interactive_mode(self):
        """Run interactive mode for continuous conversation"""
        print("Financial Wellness AI Chatbot")
        print("=" * 40)
        print("Type 'exit' to quit, 'help' for available commands")
        print()
        
        while True:
            try:
                query = input("You: ").strip()
                
                if query.lower() in ['exit', 'quit', 'bye']:
                    print("Goodbye! Take care of your finances!")
                    break
                
                if query.lower() == 'help':
                    print("\nAvailable commands:")
                    print("- Ask about your spending: 'How much did I spend on food this month?'")
                    print("- Check budget: 'Show me my budget status'")
                    print("- View savings: 'What are my savings goals?'")
                    print("- Get insights: 'Show me my spending analysis'")
                    print("- Add transaction: 'Add expense of $50 for groceries'")
                    print("- Get recommendations: 'Give me financial advice'")
                    print()
                    continue
                
                if not query:
                    continue
                
                print("Assistant: ", end="", flush=True)
                response = await self.process_query(query)
                print(response)
                print()
                
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")

async def main():
    """Main function"""
    if len(sys.argv) < 2:
        # Interactive mode
        client = FinancialWellnessClient()
        if not client.config.validate_config():
            print("Please configure your API keys first.")
            client.config.setup_config()
        await client.interactive_mode()
    else:
        # Single query mode
        query = " ".join(sys.argv[1:])
        client = FinancialWellnessClient()
        if not client.config.validate_config():
            print("Please configure your API keys first.")
            return
        
        response = await client.process_query(query)
        print(response)

if __name__ == "__main__":
    asyncio.run(main()) 