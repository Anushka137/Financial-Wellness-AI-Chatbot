# Financial Wellness AI Chatbot

A modern, AI-powered financial wellness platform featuring a conversational chatbot that helps users manage their personal finances through natural language interactions. Built with MCP (Model Context Protocol) server integration and Gemini AI.

---

## Features

* **Natural Language Financial Queries** - Ask questions about your spending, savings, and budget in plain English
* **Transaction Management** - Add, edit, and categorize expenses and income
* **Budget Tracking** - Set budgets and track spending across categories
* **Savings Goals** - Create and monitor savings goals with progress tracking
* **Smart Insights** - Get personalized financial recommendations and insights
* **MCP Integration** - Extensible architecture for AI agent interactions
* **Visual Analytics** - Auto-generated charts and graphs for financial data

---

## Quick Start

### Prerequisites
* Python 3.8+
* Gemini API key
* Internet connection

### Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd mcp_ai_chatbot
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure your credentials:**
   * Create `config.json` in the root directory:
```json
{
  "GOOGLE_API_KEY": "your-gemini-api-key",
  "API_KEY": "your-api-key",
  "API_URL": "http://localhost:8000"
}
```

4. **Run the server:**
```bash
python api_server.py
```

5. **Run the client:**
```bash
python client/universal_client.py "How much did I spend on food this month?"
```

---

## Example Queries

* "How much did I spend on food this month?"
* "Show me my spending breakdown for the last 30 days"
* "Add an expense of $50 for groceries"
* "What's my current savings goal progress?"
* "Set a new savings goal of $1000 by December"
* "Show me my budget vs actual spending"
* "What are my top spending categories?"

---

## Project Structure

```
mcp_ai_chatbot/
├── client/
│   ├── universal_client.py      # Main CLI client
│   ├── mcp_client.py           # MCP server
│   ├── config_manager.py       # Configuration management
│   ├── requirements.txt        # Client dependencies
│   └── generated_graphs/       # Auto-generated charts
├── api_server.py               # FastAPI server
├── requirements.txt            # Server dependencies
├── config.json                 # Your API keys
├── financial_data.json         # Sample financial data
└── README.md                   # This file
```

---

## MCP Integration

The chatbot uses MCP (Model Context Protocol) to expose financial operations as tools that AI agents can call:

* `get_transactions` - Fetch transaction history
* `add_transaction` - Add new expense/income
* `get_budget_status` - Check budget vs actual spending
* `get_savings_goals` - Retrieve savings goals
* `create_savings_goal` - Set new savings target
* `get_spending_analysis` - Generate spending insights
* `generate_chart` - Create visualizations

---

## API Endpoints

* `GET /transactions` - Get all transactions
* `POST /transactions` - Add new transaction
* `GET /budget` - Get budget information
* `GET /savings-goals` - Get savings goals
* `POST /savings-goals` - Create new savings goal
* `GET /analytics` - Get spending analytics
* `GET /charts/{chart_type}` - Generate charts

---

## Security

* All user data is stored locally in JSON format
* API keys are stored securely in config files
* No real financial data is transmitted to external services

---

## Future Enhancements

* Real-time bank account integration
* Advanced ML-based spending predictions
* Multi-currency support
* Export functionality
* Mobile app integration
* Advanced gamification features

---

## Support

For technical details, see the individual component documentation in each file. 