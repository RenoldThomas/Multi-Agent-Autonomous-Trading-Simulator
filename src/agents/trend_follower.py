import numpy as np
from src.agents.base_agent import BaseAgent

class TrendFollower(BaseAgent):
    def __init__(self, agent_id, lookback=3):
        super().__init__(agent_id)
        self.lookback = lookback
        self.price_history = []

    def act(self, market_state):
        current_price = market_state['mid_price']
        self.price_history.append(current_price)
        
        if len(self.price_history) < self.lookback + 1:
            return None

        # Calculate SMA
        recent_prices = self.price_history[-(self.lookback+1):-1] # Exclude current
        sma = np.mean(recent_prices)
        
        action = None
        qty = 5
        
        if current_price > sma:
            # Trend is Up -> Buy
            action = {'type': 'market', 'side': 'buy', 'quantity': qty}
        elif current_price < sma:
            # Trend is Down -> Sell
            action = {'type': 'market', 'side': 'sell', 'quantity': qty}
            
        return action