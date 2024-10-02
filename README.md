# GPT Auto Trader

GPT Auto Trader is an automated cryptocurrency trading bot that leverages OpenAI's GPT models to make buy, sell, or hold decisions based on historical price data. The bot fetches market data, analyzes it using GPT, and executes trades automatically.

## Features

- **Automated Trading**: The bot automatically executes buy, sell, or hold orders based on AI-driven decisions.
- **Data Fetching**: Retrieves real-time market data (e.g., Bitcoin price) from a cryptocurrency exchange API (e.g., Upbit).
- **GPT Integration**: Uses OpenAI's GPT model to make informed trading decisions based on market data.
- **Virtual Environment**: Isolated Python environment using `venv` to manage dependencies.
- **Customizable**: Easily extendable to incorporate different models, trading strategies, and indicators.

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/toitoi11/GPT-auto-trader.git
cd GPT_auto_trader
```

### 2. Set Up Virtual Environment
Create a Python virtual environment to manage dependencies:

```bash
python3 -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate     # For Windows
```

### 3. Install Dependencies
Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a .env file in the root of the project to store your environment variables (e.g., API keys for Upbit and OpenAI). Add the following to your .env file:

```bash
UPBIT_ACCESS_KEY=<your-upbit-access-key>
UPBIT_SECRET_KEY=<your-upbit-secret-key>
OPENAI_API_KEY=<your-openai-api-key>
```

### 5. Run the Bot
To start the bot, simply run:

```bash
python mvp.py
```
The bot will begin fetching market data, analyzing it with GPT, and making trades automatically.

### Configuration
* Market Data: The bot is configured to fetch 30-day candlestick data for Bitcoin from the Upbit exchange. You can modify this to trade other cryptocurrencies or fetch data from different time intervals.
* AI Model: The bot currently uses GPT to make decisions. You can customize the decision-making process by modifying the prompt or switching to a different model.
* Risk Management: Customize the trading logic for risk management, such as implementing stop-loss or take-profit strategies.

### Dependencies
* Python 3.8+
* PyUpbit: Python wrapper for Upbit API.
* OpenAI: OpenAI GPT integration for decision-making.
* Python-dotenv: To load environment variables from a .env file.
All dependencies can be found in the requirements.txt file.

### Contributing
Contributions are welcome! Feel free to submit a pull request or open an issue if you have suggestions for improvements or encounter any bugs.

### License
This project is licensed under the MIT License - see the LICENSE file for details.

### Disclaimer
This project is for educational purposes only. Cryptocurrency trading is highly speculative, and the use of an automated trading bot carries significant risk. Always trade responsibly and do thorough research before engaging in live trading.

