import os
import json
import time
from datetime import datetime
from dotenv import load_dotenv
import pyupbit
import pandas as pd
from openai import OpenAI

# Load environment variables
load_dotenv()
UPBIT_ACCESS_KEY = os.getenv("UPBIT_ACCESS_KEY")
UPBIT_SECRET_KEY = os.getenv("UPBIT_SECRET_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize Upbit and OpenAI clients
upbit = pyupbit.Upbit(UPBIT_ACCESS_KEY, UPBIT_SECRET_KEY)
client = OpenAI(api_key=OPENAI_API_KEY)

# Trading log file
LOG_FILE = "trading_log.json"

def calculate_technical_indicators(df):
    """Calculate technical indicators like MA20 and RSI."""
    try:
        # 20-day Moving Average
        df['MA20'] = df['close'].rolling(window=20).mean()

        # Relative Strength Index (RSI)
        gain = df['close'].diff().apply(lambda x: max(x, 0))
        loss = df['close'].diff().apply(lambda x: -min(x, 0))
        avg_gain = gain.rolling(window=14).mean()
        avg_loss = loss.rolling(window=14).mean()
        df['RSI'] = 100 - (100 / (1 + (avg_gain / avg_loss)))

        return df
    except Exception as e:
        print(f"Error calculating technical indicators: {e}")
        raise

def log_trade(decision, reason, amount, price):
    """Log trading actions to a JSON file."""
    try:
        if not os.path.exists(LOG_FILE):
            data = {"total_value": 0, "start_time": str(datetime.now()), "logs": []}
        else:
            with open(LOG_FILE, "r") as file:
                data = json.load(file)

        # Add the trade log
        data["logs"].append({
            "decision": decision,
            "reason": reason,
            "amount": amount,
            "price": price,
            "timestamp": str(datetime.now())
        })

        # Update the total value based on the decision
        if decision == "buy":
            data["total_value"] -= amount * price
        elif decision == "sell":
            data["total_value"] += amount * price

        # Save the updated log
        with open(LOG_FILE, "w") as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"Error logging trade: {e}")

def execute_trade(result):
    """Execute trading decision based on AI output."""
    try:
        # Parse the AI's result
        decision = result.get("decision")
        reason = result.get("reason")

        print(f"### AI Decision: {decision.upper()} ###\n### Reason: {reason} ###")

        # Execute based on decision
        if decision == "buy":
            krw_balance = upbit.get_balance("KRW")
            current_price = pyupbit.get_current_price("KRW-BTC")
            if krw_balance > 5000:
                amount_to_buy = krw_balance * 0.9995 / current_price
                upbit.buy_market_order("KRW-BTC", krw_balance * 0.9995)
                log_trade("buy", reason, amount_to_buy, current_price)
                print("### Buy Order Executed ###")
            else:
                print("### Insufficient KRW balance to execute buy order ###")
        
        elif decision == "sell":
            btc_balance = upbit.get_balance("BTC")
            current_price = pyupbit.get_current_price("KRW-BTC")
            if btc_balance * current_price > 5000:
                upbit.sell_market_order("KRW-BTC", btc_balance)
                log_trade("sell", reason, btc_balance, current_price)
                print("### Sell Order Executed ###")
            else:
                print("### Insufficient BTC balance to execute sell order ###")
        
        elif decision == "hold":
            log_trade("hold", reason, 0, pyupbit.get_current_price("KRW-BTC"))
            print("### Holding position ###")
        
        else:
            print(f"Unknown decision: {decision}")
    except Exception as e:
        print(f"Error executing trade: {e}")

def ai_trading():
    """Main trading logic."""
    try:
        # Fetch market data
        df = pyupbit.get_ohlcv("KRW-BTC", count=30, interval="day")
        df = calculate_technical_indicators(df)

        # Send data to AI for decision
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a cryptocurrency trading expert. Analyze the following data and provide a trading decision."},
                {"role": "user", "content": f"Market data:\n{df.to_json()}"}
            ]
        )
        result = json.loads(response.choices[0].message["content"])

        # Execute trade based on AI's decision
        execute_trade(result)
    except Exception as e:
        print(f"Error during AI trading: {e}")

if __name__ == "__main__":
    while True:
        ai_trading()
        time.sleep(60)  # Run every 60 seconds
