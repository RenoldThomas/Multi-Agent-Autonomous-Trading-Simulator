import csv
import os
from datetime import datetime

class Logger:
    def __init__(self, log_dir="results/logs"):
        self.log_dir = log_dir
        os.makedirs(self.log_dir, exist_ok=True)
        
        self.prices_file = os.path.join(log_dir, "prices.csv")
        self.actions_file = os.path.join(log_dir, "actions.csv")
        self.pnl_file = os.path.join(log_dir, "pnl.csv")
        
        # Initialize files with headers
        self._init_csv(self.prices_file, ["step", "mid_price", "best_bid", "best_ask"])
        self._init_csv(self.actions_file, ["step", "agent_id", "type", "side", "price", "quantity"])
        self._init_csv(self.pnl_file, ["step", "agent_id", "inventory", "cash", "total_value"])

    def _init_csv(self, filepath, headers):
        with open(filepath, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)

    def log_market_state(self, step, state):
        with open(self.prices_file, mode='a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([step, state['mid_price'], state['bid'], state['ask']])

    def log_action(self, step, agent_id, action):
        if not action:
            return
        with open(self.actions_file, mode='a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                step, 
                agent_id, 
                action.get('type'), 
                action.get('side'), 
                action.get('price', 'MKT'), 
                action.get('quantity')
            ])

    def log_pnl(self, step, agent_id, inventory, cash, total_value):
        with open(self.pnl_file, mode='a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([step, agent_id, inventory, cash, total_value])