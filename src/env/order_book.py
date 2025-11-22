import heapq

class OrderBook:
    def __init__(self):
        # Bids: Max-Heap (using negative price for min-heap impl), Asks: Min-Heap
        self.bids = [] 
        self.asks = []
        self.trades = [] # History of executions

    def submit_limit(self, agent_id, side, price, qty):
        """
        Submit a Limit Order.
        Side: 'buy' or 'sell'
        """
        if side == 'buy':
            # Python's heapq is a min-heap. To get max-heap behavior for bids,
            # we store negative prices.
            heapq.heappush(self.bids, (-price, qty, agent_id))
        elif side == 'sell':
            heapq.heappush(self.asks, (price, qty, agent_id))

    def submit_market(self, agent_id, side, qty):
        """
        Submit a Market Order (Instant Execution).
        Returns quantity filled.
        """
        filled_qty = 0
        avg_price = 0.0
        total_cost = 0.0
        
        if side == 'buy':
            while qty > 0 and self.asks:
                best_ask_price, best_ask_qty, best_ask_id = heapq.heappop(self.asks)
                
                fill = min(qty, best_ask_qty)
                qty -= fill
                filled_qty += fill
                total_cost += (fill * best_ask_price)
                
                # Record trade
                self.trades.append({
                    "buyer": agent_id, "seller": best_ask_id, 
                    "price": best_ask_price, "qty": fill
                })
                
                # If ask not fully consumed, push back residual
                if best_ask_qty > fill:
                    heapq.heappush(self.asks, (best_ask_price, best_ask_qty - fill, best_ask_id))
            
        elif side == 'sell':
            while qty > 0 and self.bids:
                # Decode negative price
                neg_best_bid_price, best_bid_qty, best_bid_id = heapq.heappop(self.bids)
                best_bid_price = -neg_best_bid_price
                
                fill = min(qty, best_bid_qty)
                qty -= fill
                filled_qty += fill
                total_cost += (fill * best_bid_price)
                
                self.trades.append({
                    "buyer": best_bid_id, "seller": agent_id, 
                    "price": best_bid_price, "qty": fill
                })
                
                if best_bid_qty > fill:
                    heapq.heappush(self.bids, (-best_bid_price, best_bid_qty - fill, best_bid_id))

        # Return matched info to be processed by environment/agents
        if filled_qty > 0:
            return filled_qty, total_cost / filled_qty
        return 0, 0.0

    def match_orders(self):
        """
        Internal matching for crossing limit orders.
        """
        while self.bids and self.asks:
            best_bid = -self.bids[0][0]
            best_ask = self.asks[0][0]
            
            if best_bid >= best_ask:
                # Match exists
                neg_bid_price, bid_qty, bid_id = heapq.heappop(self.bids)
                ask_price, ask_qty, ask_id = heapq.heappop(self.asks)
                
                trade_price = best_ask # Price priority typically goes to maker (earlier order)
                # For MVP, simplified: take mid of cross or just ask price
                
                fill = min(bid_qty, ask_qty)
                
                self.trades.append({
                    "buyer": bid_id, "seller": ask_id,
                    "price": trade_price, "qty": fill
                })
                
                # Push residuals back
                if bid_qty > fill:
                    heapq.heappush(self.bids, (neg_bid_price, bid_qty - fill, bid_id))
                if ask_qty > fill:
                    heapq.heappush(self.asks, (ask_price, ask_qty - fill, ask_id))
            else:
                break

    def get_l1_snapshot(self):
        best_bid = -self.bids[0][0] if self.bids else None
        best_ask = self.asks[0][0] if self.asks else None
        return best_bid, best_ask

    def clear_book(self):
        # Helper to clear book if we want agents to refresh quotes every step
        self.bids = []
        self.asks = []