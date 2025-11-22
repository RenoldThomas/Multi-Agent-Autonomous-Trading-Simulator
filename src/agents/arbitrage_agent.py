import random
from src.agents.base_agent import BaseAgent

class ArbitrageAgent(BaseAgent):
    def __init__(self, agent_id, noise_factor=0.5):
        super().__init__(agent_id)
        self.noise_factor = noise_factor

    def act(self, market_state):
        mid_price = market_state['mid_price']
        
        # Generate "Fair Price"
        fair_price = mid_price + random.gauss(0, self.noise_factor)
        
        qty = 5
        threshold = 0.2
        
        if mid_price < (fair_price - threshold):
            # Market is cheap compared to fair value -> Buy
            return {'type': 'market', 'side': 'buy', 'quantity': qty}
        
        elif mid_price > (fair_price + threshold):
            # Market is expensive -> Sell
            return {'type': 'market', 'side': 'sell', 'quantity': qty}
            
        return None