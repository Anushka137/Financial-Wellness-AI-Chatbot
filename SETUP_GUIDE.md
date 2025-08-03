# Financial Wellness AI Chatbot - Setup Guide

This guide will help you set up and run the Financial Wellness AI Chatbot with MCP integration.

## Prerequisites

- Python 3.8 or higher
- Google Gemini API key (free tier available)
- Internet connection

## Step 1: Install Dependencies

1. **Install server dependencies:**
```bash
pip install -r requirements.txt
```

2. **Install client dependencies:**
```bash
cd client
pip install -r requirements.txt
cd ..
```

## Step 2: Get API Keys

### Google Gemini API Key
1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Click "Get API key" or go to [API Keys page](https://makersuite.google.com/app/apikey)
4. Create a new API key
5. Copy the key (it starts with "AIza...")

### API Key (Optional)
For production use, you can set a custom API key. For local development, the default key works fine.

## Step 3: Configure the Application

1. **Edit the configuration file:**
```bash
# Open config.json and update with your keys
{
  "GOOGLE_API_KEY": "AIza...your-actual-gemini-key...",
  "API_KEY": "your-api-key-here",
  "API_URL": "http://localhost:8000"
}
```

2. **Or use the interactive setup:**
```bash
cd client
python config_manager.py
```

## Step 4: Start the Server

1. **Start the FastAPI server:**
```bash
python api_server.py
```

The server will start on `http://localhost:8000`

2. **Verify the server is running:**
```bash
curl http://localhost:8000/
```

You should see a JSON response with API information.

## Step 5: Test the Chatbot

### Option 1: Interactive Mode
```bash
cd client
python universal_client.py
```

This starts an interactive conversation where you can ask questions like:
- "How much did I spend on food this month?"
- "Show me my budget status"
- "What are my savings goals?"

### Option 2: Single Query Mode
```bash
cd client
python universal_client.py "How much did I spend on food this month?"
```

### Option 3: MCP Server Mode
```bash
cd client
python mcp_client.py
```

This starts the MCP server that can be integrated with other AI agents.

## Step 6: Example Queries

Try these example queries to test the system:

### Basic Queries
```bash
# Check spending
python universal_client.py "How much did I spend on food this month?"

# View budget
python universal_client.py "Show me my budget status"

# Check savings
python universal_client.py "What are my savings goals?"

# Get analytics
python universal_client.py "Show me my financial summary"
```

### Advanced Queries
```bash
# Add a transaction
python universal_client.py "Add an expense of $50 for groceries today"

# Get recommendations
python universal_client.py "Give me financial advice"

# Generate charts
python universal_client.py "Show me a spending breakdown chart"
```

## Step 7: API Testing

You can also test the API directly:

```bash
# Get all transactions
curl http://localhost:8000/transactions

# Get budget status
curl http://localhost:8000/budget

# Get analytics
curl http://localhost:8000/analytics

# Get recommendations
curl http://localhost:8000/recommendations
```

## Step 8: MCP Integration

The MCP server exposes these tools for AI agents:

- `get_transactions` - Fetch transaction history
- `add_transaction` - Add new expense/income
- `get_budget_status` - Check budget vs actual spending
- `get_savings_goals` - Retrieve savings goals
- `create_savings_goal` - Set new savings target
- `get_analytics` - Get financial insights
- `get_spending_analysis` - Detailed spending analysis
- `get_recommendations` - Personalized recommendations
- `generate_chart` - Create visualizations

## Troubleshooting

### Common Issues

1. **"No Google API key provided"**
   - Make sure you've added your Gemini API key to `config.json`
   - Verify the key is correct and active

2. **"API request failed"**
   - Ensure the server is running on `http://localhost:8000`
   - Check that all dependencies are installed

3. **"Module not found"**
   - Install missing dependencies: `pip install -r requirements.txt`
   - Make sure you're in the correct directory

4. **Chart generation fails**
   - Install system dependencies for matplotlib: `brew install pkg-config` (macOS)
   - For Linux: `sudo apt-get install libfreetype6-dev`

### Debug Mode

To see detailed error messages, you can modify the client to show more verbose output:

```python
# In universal_client.py, add:
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Data Management

### Sample Data
The system comes with sample financial data in `financial_data.json`. You can:
- Modify this file to add your own transactions
- Use the API to add transactions programmatically
- Start with empty data and build up your financial history

### Data Backup
Your financial data is stored in `financial_data.json`. Make sure to:
- Back up this file regularly
- Keep it secure (it contains sensitive financial information)
- Consider encrypting it for production use

## Next Steps

Once you have the basic system running, you can:

1. **Customize the categories** - Modify the budget categories in the API
2. **Add more features** - Extend the API with new endpoints
3. **Integrate with other systems** - Use the MCP server with other AI agents
4. **Deploy to production** - Set up proper authentication and hosting
5. **Add real bank integration** - Replace mock data with real financial APIs

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify all dependencies are installed correctly
3. Ensure your API keys are valid and active
4. Check the server logs for detailed error messages

For more information, see the main README.md file. 