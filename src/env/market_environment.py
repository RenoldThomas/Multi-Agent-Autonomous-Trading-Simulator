import random
import numpy as np
from src.env.order_book import OrderBook

class MarketEnvironment:
    def __init__(self, initial_price=100.0):
        self.time_step = 0
        self.mid_price = initial_price
        self.order_book = OrderBook()
        self.volatility = 0.5  # Standard deviation for random walk
        self.spread = 0.1      # Fixed simulation spread parameter

    def step(self, agent_actions):
        """
        1. Process agent actions
        2. Execute orders
        3. Update Market Price (Random Walk)
        4. Return State
        """
        self.time_step += 1
        
        # 1. Submit orders to Order Book
        # To simplify: Market Maker cancels old orders every step (fresh quotes)
        self.order_book.clear_book()
        
        execution_reports = {}

        # Process LIMIT orders first (liquidity provision)
        for agent_id, action in agent_actions.items():
            if action and action['type'] == 'limit':
                self.order_book.submit_limit(
                    agent_id, action['side'], action['price'], action['quantity']
                )

        # Match Crossed Limit Orders
        self.order_book.match_orders()

        # Process MARKET orders (liquidity taking)
        for agent_id, action in agent_actions.items():
            if action and action['type'] == 'market':
                filled, avg_price = self.order_book.submit_market(
                    agent_id, action['side'], action['quantity']
                )
                if filled > 0:
                    if agent_id not in execution_reports: execution_reports[agent_id] = []
                    execution_reports[agent_id].append({
                        'side': action['side'], 'qty': filled, 'price': avg_price
                    })

        # Also capture trades from Limit order fills (from OrderBook history for this step)
        # Note: In a real engine, we'd have a robust event system. 
        # Here we parse the order book's trade log for the current step logic (simplified).
        while self.order_book.trades:
            trade = self.order_book.trades.pop(0)
            
            # Notify Buyer
            if trade['buyer'] not in execution_reports: execution_reports[trade['buyer']] = []
            execution_reports[trade['buyer']].append({'side': 'buy', 'qty': trade['qty'], 'price': trade['price']})
            
            # Notify Seller
            if trade['seller'] not in execution_reports: execution_reports[trade['seller']] = []
            execution_reports[trade['seller']].append({'side': 'sell', 'qty': trade['qty'], 'price': trade['price']})

        # 3. Update Mid Price (Random Walk)
        change = random.gauss(0, self.volatility)
        self.mid_price += change
        
        # Get Book State
        best_bid, best_ask = self.order_book.get_l1_snapshot()
        
        # Fallback if book is empty (use theoretical price)
        if best_bid is None: best_bid = self.mid_price - (self.spread/2)
        if best_ask is None: best_ask = self.mid_price + (self.spread/2)

        state = {
            "timestamp": self.time_step,
            "mid_price": self.mid_price,
            "bid": best_bid,
            "ask": best_ask
        }
        
        return state, execution_reports