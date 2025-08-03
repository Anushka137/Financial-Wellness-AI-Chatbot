# Financial Wellness AI Chatbot - Usage Examples

This document provides comprehensive examples of how to use the Financial Wellness AI Chatbot for various financial management tasks.

## Getting Started

### 1. Quick Start
```bash
# Run the quick start script (recommended for first-time users)
python quick_start.py
```

### 2. Manual Setup
```bash
# Install dependencies
pip install -r requirements.txt
cd client && pip install -r requirements.txt && cd ..

# Start the server
python api_server.py

# In another terminal, run the client
cd client && python universal_client.py
```

## Example Queries and Use Cases

### 📊 Financial Analysis Queries

#### Basic Spending Questions
```bash
# Check spending by category
"How much did I spend on food this month?"
"What's my total spending on transportation?"
"Show me my entertainment expenses for the last 30 days"

# Spending summaries
"What's my total spending this month?"
"How much did I spend last week?"
"Show me my spending breakdown"
```

#### Budget Monitoring
```bash
# Budget status
"Show me my budget status"
"Am I over budget in any category?"
"What's my remaining budget for food?"
"Which categories am I close to exceeding?"

# Budget vs actual
"Compare my budget vs actual spending"
"Show me where I'm over budget"
```

#### Income Analysis
```bash
# Income tracking
"How much income did I receive this month?"
"What's my total income vs expenses?"
"Show me my income sources"
```

### 🎯 Savings Goals

#### Goal Management
```bash
# View goals
"What are my savings goals?"
"Show me my savings progress"
"How close am I to my emergency fund goal?"

# Create goals
"Create a new savings goal for a vacation"
"Set up a goal to save $5000 by December"
"Add a goal for a new laptop"
```

#### Goal Progress
```bash
# Progress tracking
"How much progress have I made on my goals?"
"Which goals am I closest to achieving?"
"Show me my savings rate"
```

### 💡 Smart Recommendations

#### Financial Advice
```bash
# Get recommendations
"Give me financial advice"
"What can I do to save more money?"
"Suggest ways to reduce my spending"
"Am I saving enough?"

# Personalized insights
"What are my spending patterns?"
"Where can I cut back on expenses?"
"How can I improve my financial health?"
```

### 📈 Analytics and Insights

#### Detailed Analysis
```bash
# Spending analysis
"Show me my spending analysis for the last 30 days"
"What are my top spending categories?"
"Show me my daily spending trends"
"Analyze my spending patterns"

# Financial health
"What's my savings rate?"
"Show me my financial summary"
"Am I on track with my financial goals?"
```

#### Trend Analysis
```bash
# Monthly trends
"Show me my spending trends over the last 3 months"
"How has my income changed?"
"Compare this month to last month"
```

### ➕ Transaction Management

#### Adding Transactions
```bash
# Add expenses
"Add an expense of $45.50 for groceries today"
"Record a $25 gas station expense"
"Log a $120 entertainment expense for movie tickets"

# Add income
"Add income of $3500 for my salary"
"Record freelance payment of $300"
```

#### Transaction Queries
```bash
# Recent transactions
"Show me my recent transactions"
"What transactions did I make today?"
"Show me transactions from last week"

# Category-specific
"Show me all my food expenses"
"List my transportation costs"
"What entertainment expenses do I have?"
```

### 📊 Chart Generation

#### Visual Analytics
```bash
# Generate charts
"Show me a spending by category chart"
"Generate a monthly trends chart"
"Create a budget vs actual chart"
"Show me my savings progress chart"
```

### 🔄 Interactive Mode Examples

When running in interactive mode (`python universal_client.py`), you can have conversations like:

```
You: How much did I spend on food this month?
Assistant: Based on your transaction data, you've spent $185.50 on food and dining this month. This includes groceries, restaurant meals, and coffee purchases. You're currently under your $400 monthly budget for this category with $214.50 remaining.

You: Am I on track with my savings goals?
Assistant: Looking at your savings goals, you have 3 active goals:
- Emergency Fund: 50% complete ($2,500 of $5,000)
- Vacation Fund: 40% complete ($800 of $2,000) 
- New Laptop: 50% complete ($600 of $1,200)

Your overall savings rate is 66.17%, which is excellent! You're well on track to meet your financial goals.

You: Give me some financial advice
Assistant: Based on your spending patterns, here are some recommendations:
1. Your entertainment budget is nearly maxed out (97.5% used). Consider reducing entertainment spending to stay within budget.
2. Your savings rate of 66.17% is excellent - keep up the good work!
3. Consider setting up automatic transfers to your savings goals to make saving even easier.
4. Your food spending is well within budget - great job managing this category!
```

## Advanced Usage

### MCP Integration

The MCP client can be used with other AI agents:

```bash
# Start MCP server
cd client && python mcp_client.py
```

Available MCP tools:
- `get_transactions` - Fetch transaction history
- `add_transaction` - Add new expense/income
- `get_budget_status` - Check budget vs actual spending
- `get_savings_goals` - Retrieve savings goals
- `create_savings_goal` - Set new savings target
- `get_analytics` - Get financial insights
- `get_spending_analysis` - Detailed spending analysis
- `get_recommendations` - Personalized recommendations
- `generate_chart` - Create visualizations

### API Direct Access

You can also interact with the API directly:

```bash
# Get all transactions
curl http://localhost:8000/transactions

# Get budget status
curl http://localhost:8000/budget

# Get analytics
curl http://localhost:8000/analytics

# Get recommendations
curl http://localhost:8000/recommendations

# Generate a chart
curl http://localhost:8000/charts/spending_by_category
```

## Sample Data

The system comes with sample financial data including:
- 15 sample transactions (expenses and income)
- 6 budget categories with limits
- 3 savings goals with progress
- User profile and analytics

You can modify `financial_data.json` to add your own data or use the API to add transactions programmatically.

## Tips for Best Results

1. **Be specific** - Instead of "show me spending", try "show me my food spending for this month"

2. **Use natural language** - The AI understands conversational queries like "How am I doing with my budget?"

3. **Ask for insights** - Use queries like "Give me financial advice" or "What are my spending patterns?"

4. **Use the interactive mode** - It maintains conversation context for better responses

5. **Generate charts** - Visual data can be more helpful than text summaries

## Troubleshooting

### Common Issues

1. **"No Google API key provided"**
   - Edit `config.json` and add your Gemini API key
   - Get a free key from https://aistudio.google.com/

2. **"API request failed"**
   - Make sure the server is running: `python api_server.py`
   - Check that the API URL in config.json is correct

3. **"No data found"**
   - The system comes with sample data in `financial_data.json`
   - Add your own transactions using the API or edit the JSON file

### Getting Help

- Run the test script: `python test_system.py`
- Check the setup guide: `SETUP_GUIDE.md`
- Use the quick start script: `python quick_start.py`

## Next Steps

Once you're comfortable with the basic usage:

1. **Customize categories** - Modify budget categories in the API
2. **Add real data** - Replace sample data with your actual financial information
3. **Integrate with other tools** - Use the MCP server with other AI agents
4. **Extend functionality** - Add new features to the API
5. **Deploy to production** - Set up proper hosting and security

The Financial Wellness AI Chatbot is designed to be extensible and can grow with your needs! 