#!/usr/bin/env python3
"""
Financial Wellness MCP Client
Exposes financial operations as MCP tools for AI agents
"""

import json
import sys
import asyncio
import httpx
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from config_manager import ConfigManager

class FinancialWellnessMCPClient:
    def __init__(self):
        self.config = ConfigManager()
        self.api_url = self.config.get("API_URL", "http://localhost:8000")
        self.api_key = self.config.get("API_KEY", "your-api-key")
        
        # MCP tool definitions
        self.tools = [
            {
                "name": "get_transactions",
                "description": "Get financial transactions with optional filtering by category, type, or date range",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "category": {
                            "type": "string",
                            "description": "Filter by transaction category (e.g., 'Food & Dining', 'Transportation')"
                        },
                        "type": {
                            "type": "string",
                            "description": "Filter by transaction type ('expense' or 'income')"
                        },
                        "start_date": {
                            "type": "string",
                            "description": "Start date for filtering (YYYY-MM-DD format)"
                        },
                        "end_date": {
                            "type": "string",
                            "description": "End date for filtering (YYYY-MM-DD format)"
                        }
                    }
                }
            },
            {
                "name": "add_transaction",
                "description": "Add a new financial transaction (expense or income)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "date": {
                            "type": "string",
                            "description": "Transaction date (YYYY-MM-DD format)"
                        },
                        "amount": {
                            "type": "number",
                            "description": "Transaction amount"
                        },
                        "category": {
                            "type": "string",
                            "description": "Transaction category (e.g., 'Food & Dining', 'Transportation')"
                        },
                        "description": {
                            "type": "string",
                            "description": "Transaction description"
                        },
                        "type": {
                            "type": "string",
                            "description": "Transaction type ('expense' or 'income')"
                        },
                        "tags": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Optional tags for the transaction"
                        }
                    },
                    "required": ["date", "amount", "category", "description", "type"]
                }
            },
            {
                "name": "get_budget_status",
                "description": "Get current budget status and remaining amounts for all categories"
            },
            {
                "name": "get_savings_goals",
                "description": "Get all savings goals and their current progress"
            },
            {
                "name": "create_savings_goal",
                "description": "Create a new savings goal",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Name of the savings goal"
                        },
                        "target_amount": {
                            "type": "number",
                            "description": "Target amount to save"
                        },
                        "current_amount": {
                            "type": "number",
                            "description": "Current amount saved (default: 0)"
                        },
                        "deadline": {
                            "type": "string",
                            "description": "Target deadline (YYYY-MM-DD format)"
                        },
                        "description": {
                            "type": "string",
                            "description": "Description of the goal"
                        },
                        "priority": {
                            "type": "string",
                            "description": "Priority level ('low', 'medium', 'high')"
                        }
                    },
                    "required": ["name", "target_amount", "deadline", "description"]
                }
            },
            {
                "name": "get_analytics",
                "description": "Get comprehensive financial analytics including income, expenses, savings rate, and trends"
            },
            {
                "name": "get_spending_analysis",
                "description": "Get detailed spending analysis for a specified time period",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "days": {
                            "type": "integer",
                            "description": "Number of days to analyze (default: 30)"
                        }
                    }
                }
            },
            {
                "name": "get_recommendations",
                "description": "Get personalized financial recommendations based on spending patterns and goals"
            },
            {
                "name": "generate_chart",
                "description": "Generate financial charts and visualizations",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "chart_type": {
                            "type": "string",
                            "description": "Type of chart to generate: 'spending_by_category', 'monthly_trends', 'budget_vs_actual', 'savings_progress'"
                        }
                    },
                    "required": ["chart_type"]
                }
            }
        ]
    
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
            return {"error": f"API request failed: {e.response.status_code} - {e.response.text}"}
        except Exception as e:
            return {"error": f"Request failed: {str(e)}"}
    
    async def get_transactions(self, args: Dict) -> Dict:
        """Get transactions with optional filtering"""
        endpoint = "/transactions"
        params = []
        
        for key, value in args.items():
            if value is not None:
                params.append(f"{key}={value}")
        
        if params:
            endpoint += "?" + "&".join(params)
        
        result = await self.make_api_request(endpoint)
        return {
            "success": "error" not in result,
            "data": result,
            "message": f"Retrieved {len(result.get('transactions', []))} transactions"
        }
    
    async def add_transaction(self, args: Dict) -> Dict:
        """Add a new transaction"""
        # Set default values
        if "current_amount" not in args:
            args["current_amount"] = 0
        if "tags" not in args:
            args["tags"] = []
        
        result = await self.make_api_request("/transactions", "POST", args)
        return {
            "success": "error" not in result,
            "data": result,
            "message": "Transaction added successfully" if "error" not in result else result["error"]
        }
    
    async def get_budget_status(self, args: Dict = None) -> Dict:
        """Get current budget status"""
        result = await self.make_api_request("/budget")
        return {
            "success": "error" not in result,
            "data": result,
            "message": f"Retrieved budget status for {len(result.get('budgets', {}))} categories"
        }
    
    async def get_savings_goals(self, args: Dict = None) -> Dict:
        """Get savings goals"""
        result = await self.make_api_request("/savings-goals")
        return {
            "success": "error" not in result,
            "data": result,
            "message": f"Retrieved {len(result.get('savings_goals', []))} savings goals"
        }
    
    async def create_savings_goal(self, args: Dict) -> Dict:
        """Create a new savings goal"""
        # Set default values
        if "current_amount" not in args:
            args["current_amount"] = 0
        if "priority" not in args:
            args["priority"] = "medium"
        
        result = await self.make_api_request("/savings-goals", "POST", args)
        return {
            "success": "error" not in result,
            "data": result,
            "message": "Savings goal created successfully" if "error" not in result else result["error"]
        }
    
    async def get_analytics(self, args: Dict = None) -> Dict:
        """Get financial analytics"""
        result = await self.make_api_request("/analytics")
        return {
            "success": "error" not in result,
            "data": result,
            "message": "Retrieved financial analytics"
        }
    
    async def get_spending_analysis(self, args: Dict) -> Dict:
        """Get spending analysis"""
        days = args.get("days", 30)
        result = await self.make_api_request(f"/spending-analysis?days={days}")
        return {
            "success": "error" not in result,
            "data": result,
            "message": f"Retrieved spending analysis for {days} days"
        }
    
    async def get_recommendations(self, args: Dict = None) -> Dict:
        """Get recommendations"""
        result = await self.make_api_request("/recommendations")
        return {
            "success": "error" not in result,
            "data": result,
            "message": f"Retrieved {len(result.get('recommendations', []))} recommendations"
        }
    
    async def generate_chart(self, args: Dict) -> Dict:
        """Generate chart"""
        chart_type = args.get("chart_type")
        if not chart_type:
            return {
                "success": False,
                "error": "chart_type is required"
            }
        
        try:
            result = await self.make_api_request(f"/charts/{chart_type}")
            return {
                "success": "error" not in result,
                "data": {"chart_type": chart_type, "file_path": f"client/generated_graphs/{chart_type}.png"},
                "message": f"Chart '{chart_type}' generated successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to generate chart: {str(e)}"
            }
    
    def list_tools(self) -> List[Dict]:
        """List available MCP tools"""
        return self.tools
    
    async def call_tool(self, tool_name: str, args: Dict) -> Dict:
        """Call a specific MCP tool"""
        tool_methods = {
            "get_transactions": self.get_transactions,
            "add_transaction": self.add_transaction,
            "get_budget_status": self.get_budget_status,
            "get_savings_goals": self.get_savings_goals,
            "create_savings_goal": self.create_savings_goal,
            "get_analytics": self.get_analytics,
            "get_spending_analysis": self.get_spending_analysis,
            "get_recommendations": self.get_recommendations,
            "generate_chart": self.generate_chart
        }
        
        if tool_name not in tool_methods:
            return {
                "success": False,
                "error": f"Unknown tool: {tool_name}"
            }
        
        try:
            return await tool_methods[tool_name](args or {})
        except Exception as e:
            return {
                "success": False,
                "error": f"Tool execution failed: {str(e)}"
            }

class MCPProtocol:
    """Simple MCP protocol implementation"""
    
    def __init__(self):
        self.client = FinancialWellnessMCPClient()
    
    async def handle_request(self, request: Dict) -> Dict:
        """Handle MCP protocol requests"""
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")
        
        try:
            if method == "tools/list":
                tools = self.client.list_tools()
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {"tools": tools}
                }
            
            elif method == "tools/call":
                tool_name = params.get("name")
                tool_args = params.get("arguments", {})
                
                result = await self.client.call_tool(tool_name, tool_args)
                
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(result, indent=2)
                            }
                        ]
                    }
                }
            
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    }
                }
        
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }

async def main():
    """Main function for MCP server"""
    protocol = MCPProtocol()
    
    # Check if configuration is valid
    if not protocol.client.config.validate_config():
        print("Error: Invalid configuration. Please check your config.json file.")
        sys.exit(1)
    
    print("Financial Wellness MCP Server")
    print("=" * 40)
    print(f"API URL: {protocol.client.api_url}")
    print("Available tools:")
    for tool in protocol.client.list_tools():
        print(f"  - {tool['name']}: {tool['description']}")
    print()
    
    # Simple stdin/stdout MCP server
    while True:
        try:
            line = input()
            if not line:
                continue
            
            request = json.loads(line)
            response = await protocol.handle_request(request)
            print(json.dumps(response))
            
        except EOFError:
            break
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(json.dumps({
                "jsonrpc": "2.0",
                "error": {
                    "code": -32700,
                    "message": f"Parse error: {str(e)}"
                }
            }))

if __name__ == "__main__":
    asyncio.run(main()) 