import os
from dotenv import load_dotenv
import pyupbit
import pandas as pd

def calculate_technical_indicators(df):
    # Moving Average (MA) and Relative Strength Index (RSI)
    df['MA20'] = df['close'].rolling(window=20).mean()
    df['RSI'] = 100 - (100 / (1 + (df['close'].diff().apply(lambda x: max(x, 0)).rolling(window=14).mean() / 
                                  df['close'].diff().apply(lambda x: -min(x, 0)).rolling(window=14).mean())))
    return df

def ai_trading():
    try:
        df = pyupbit.get_ohlcv("KRW-BTC", count=30, interval="day")
        df = calculate_technical_indicators(df)
        
        # AI Decision Process
        # Add more contextual data and process indicators along with OHLC data
        from openai import OpenAI
        client = OpenAI()

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert in Bitcoin investing..."},
                {"role": "user", "content": df.to_json()}
            ],
            response_format={"type": "json_object"}
        )
        result = response.choices[0].message.content
        
        # AI trading execution
        execute_trade(result)
        
    except Exception as e:
        print(f"Error during trading: {e}")

def execute_trade(result):
    try:
        result = json.loads(result)
        access = os.getenv("UPBIT_ACCESS_KEY")
        secret = os.getenv("UPBIT_SECRET_KEY")
        upbit = pyupbit.Upbit(access, secret)

        decision = result.get("decision")
        reason = result.get("reason")
        print(f"### AI Decision: {decision.upper()} ###\n### Reason: {reason} ###")

        if decision == "buy":
            # Trading logic remains the same
            pass
        elif decision == "sell":
            # Trading logic remains the same
            pass
        elif decision == "hold":
            print("### Hold Position ###")
    except Exception as e:
        print(f"Error executing trade: {e}")

while True:
    import time
    time.sleep(60)  # Check every 60 seconds instead of 10
    ai_trading()
