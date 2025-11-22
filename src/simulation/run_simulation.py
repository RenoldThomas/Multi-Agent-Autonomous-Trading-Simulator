import sys
import os
import matplotlib.pyplot as plt
import pandas as pd

# Ensure src is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.env.market_environment import MarketEnvironment
from src.agents.market_maker import MarketMaker
from src.agents.trend_follower import TrendFollower
from src.agents.arbitrage_agent import ArbitrageAgent
from src.utils.logger import Logger

def run():
    print("Initializing Simulation...")
    
    # Setup
    logger = Logger(log_dir="results/logs")
    env = MarketEnvironment(initial_price=100.0)
    
    # Initialize Agents
    agents = [
        MarketMaker(agent_id="MM_01"),
        TrendFollower(agent_id="Trend_01"),
        ArbitrageAgent(agent_id="Arb_01")
    ]
    
    agent_map = {a.agent_id: a for a in agents}
    
    steps = 1000
    print(f"Running for {steps} steps...")
    
    for t in range(steps):
        # 1. Collect Actions
        actions = {}
        # Get current snapshot for decision making (before step)
        # We construct a temporary state because env.step hasn't run yet for this tick
        # In a real sim, agents see state t-1.
        
        # For MVP, we grab current env state (t-1 effectively)
        current_state = {
            'timestamp': t,
            'mid_price': env.mid_price,
            # Peek at order book for best bid/ask or use theoretical
            'bid': env.order_book.get_l1_snapshot()[0] or env.mid_price - 0.05,
            'ask': env.order_book.get_l1_snapshot()[1] or env.mid_price + 0.05
        }
        
        for agent in agents:
            action = agent.act(current_state)
            actions[agent.agent_id] = action
            logger.log_action(t, agent.agent_id, action)

        # 2. Environment Step
        next_state, execution_reports = env.step(actions)
        logger.log_market_state(t, next_state)

        # 3. Update Agents (Fills & PnL)
        for agent_id, executions in execution_reports.items():
            if agent_id in agent_map:
                agent_map[agent_id].update_portfolio(executions)
        
        for agent in agents:
            total_val = agent.update_pnl(next_state)
            logger.log_pnl(t, agent.agent_id, agent.inventory, agent.cash, total_val)

    print("Simulation Complete. Generating Charts...")
    generate_plots()
    print("Done. Results saved in /results.")

def generate_plots():
    os.makedirs("results/charts", exist_ok=True)
    
    # Load Data
    prices_df = pd.read_csv("results/logs/prices.csv")
    pnl_df = pd.read_csv("results/logs/pnl.csv")
    
    # 1. Price History
    plt.figure(figsize=(10, 6))
    plt.plot(prices_df['step'], prices_df['mid_price'], label='Mid Price', color='blue')
    plt.title("Market Price History")
    plt.xlabel("Step")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)
    plt.savefig("results/charts/price_history.png")
    plt.close()

    # 2. Agent PnL
    plt.figure(figsize=(10, 6))
    for agent_id in pnl_df['agent_id'].unique():
        subset = pnl_df[pnl_df['agent_id'] == agent_id]
        # Normalize PnL to 0 start
        initial_val = subset.iloc[0]['total_value']
        plt.plot(subset['step'], subset['total_value'] - initial_val, label=agent_id)
    
    plt.title("Agent Cumulative PnL")
    plt.xlabel("Step")
    plt.ylabel("Profit/Loss ($)")
    plt.legend()
    plt.grid(True)
    plt.savefig("results/charts/agent_pnl.png")
    plt.close()

    # 3. Inventory
    plt.figure(figsize=(10, 6))
    for agent_id in pnl_df['agent_id'].unique():
        subset = pnl_df[pnl_df['agent_id'] == agent_id]
        plt.plot(subset['step'], subset['inventory'], label=agent_id)
        
    plt.title("Agent Inventory Position")
    plt.xlabel("Step")
    plt.ylabel("Inventory (Units)")
    plt.legend()
    plt.grid(True)
    plt.savefig("results/charts/agent_inventory.png")
    plt.close()

if __name__ == "__main__":
    run()