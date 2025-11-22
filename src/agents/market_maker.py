from src.agents.base_agent import BaseAgent

class MarketMaker(BaseAgent):
    def __init__(self, agent_id, spread=0.2, max_inventory=100):
        super().__init__(agent_id)
        self.spread = spread
        self.max_inventory = max_inventory

    def act(self, market_state):
        mid = market_state['mid_price']
        
        # Inventory Skewing
        # If we have too much long inventory, lower bid/ask to encourage selling
        skew = -(self.inventory / self.max_inventory) * 0.5
        
        bid_price = mid - (self.spread / 2) + skew
        ask_price = mid + (self.spread / 2) + skew
        
        # In this simplified simulation, the MM submits TWO orders (Limit Buy and Limit Sell)
        # But our interface returns ONE action per step for simplicity. 
        # We will alternate or prioritize based on inventory.
        # To make it robust for MVP, we'll just provide liquidity on both sides 
        # by hacking the simulation runner to accept a LIST of actions, 
        # OR just picking the side we need most.
        
        # Let's modify logic: If inventory is positive, we prioritize selling (Limit Sell).
        # If negative, prioritize buying (Limit Buy).
        # If neutral, random or alternate. 
        
        # Actually, a real MM places both. Since BaseAgent.act returns a dict, 
        # let's cheat slightly and assume the MarketEnvironment can handle list of actions
        # OR we force the Agent to only place one side per tick.
        # Let's place order to close position.
        
        # SIMPLIFICATION: MM places Limit orders. 
        # Since we return one dict, we decide side based on inventory balance.
        
        qty = 10
        
        if self.inventory > 20:
            return {'type': 'limit', 'side': 'sell', 'price': round(ask_price, 2), 'quantity': qty}
        elif self.inventory < -20:
            return {'type': 'limit', 'side': 'buy', 'price': round(bid_price, 2), 'quantity': qty}
        else:
            # If balanced, maybe we just place a Buy this tick, next tick Sell?
            # Let's default to Buy (Bid) for now, trusting randomness will flip inventory eventually
            return {'type': 'limit', 'side': 'buy', 'price': round(bid_price, 2), 'quantity': qty}