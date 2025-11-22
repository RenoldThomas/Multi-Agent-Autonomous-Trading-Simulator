from abc import ABC, abstractmethod
from src.utils.metrics import calculate_total_value

class BaseAgent(ABC):
    def __init__(self, agent_id, initial_cash=100000.0):
        self.agent_id = agent_id
        self.cash = initial_cash
        self.inventory = 0
        self.history_pnl = []

    @abstractmethod
    def act(self, market_state):
        """
        Returns a dict: 
        {'type': 'limit'/'market', 'side': 'buy'/'sell', 'price': float, 'quantity': int}
        or None
        """
        pass

    def update_portfolio(self, executions):
        """
        Update cash and inventory based on trade executions.
        executions: list of dicts {'side', 'qty', 'price'}
        """
        if not executions:
            return

        for trade in executions:
            if trade['side'] == 'buy':
                self.inventory += trade['qty']
                self.cash -= (trade['qty'] * trade['price'])
            elif trade['side'] == 'sell':
                self.inventory -= trade['qty']
                self.cash += (trade['qty'] * trade['price'])

    def update_pnl(self, market_state):
        """
        Calculate Mark-to-Market PnL
        """
        # Valuate inventory at mid_price
        current_price = market_state['mid_price']
        total_val = calculate_total_value(self.cash, self.inventory, current_price)
        
        self.history_pnl.append({
            'step': market_state['timestamp'],
            'inventory': self.inventory,
            'cash': self.cash,
            'total_value': total_val
        })
        
        return total_val