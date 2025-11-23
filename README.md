# Multi-Agent Autonomous Trading Simulator

## 🚀 Project Overview
This project simulates a **financial market** where multiple AI agents with distinct trading strategies (momentum, mean-reversion, statistical arbitrage) interact in real-time.  
The objective is to study **multi-agent reinforcement learning (MARL)**, market microstructure, and coordination dynamics in competitive environments.

## 🎯 Objectives
- Build a simulated trading environment with tick-level data
- Implement multiple reinforcement learning agents with unique trading strategies
- Enable **inter-agent communication** for collaborative or adversarial scenarios
- Evaluate agent performance with **PnL, Sharpe ratio, and drawdowns**

## 🛠 Tech Stack
- **Python** (3.11+)
- **RLlib** (multi-agent RL)
- **PyTorch** (deep RL models)
- **Pandas/NumPy** (data handling)
- **Gymnasium** (custom trading environment)
- **ZeroMQ / asyncio** (agent communication)

## 🧠 Key AI Concepts
- Multi-Agent Reinforcement Learning (MARL)
- Adversarial RL dynamics
- Market microstructure simulation
- Low-latency decision-making

## 🔑 Implementation Steps
1. Create trading environment with synthetic or historical data
2. Define multiple agents with unique RL strategies
3. Implement real-time agent communication
4. Run simulation and compare agent performances

## ⚡ Challenges
- Designing a realistic market environment
- Avoiding overfitting to historical data
- Balancing adversarial vs. cooperative strategies

---

## 📊 Understanding the Results

### Simulation Output Files

The simulation generates several CSV files in `/results/logs/` that capture different aspects of market dynamics:

#### **1. `prices.csv`** - Market State History
Records the evolution of market prices at each simulation step:
- **step**: Simulation time step (0-999)
- **mid_price**: The theoretical mid-market price (evolves via random walk)
- **best_bid**: Highest price a buyer is willing to pay (from order book)
- **best_ask**: Lowest price a seller is willing to accept (from order book)

**What it tells us**: How the market price evolved during simulation and the spread between bid/ask prices. A tighter spread indicates better liquidity.

#### **2. `actions.csv`** - Agent Trading Activity
Logs every action taken by each agent:
- **step**: When the action occurred
- **agent_id**: Which agent took the action (MM_01, Trend_01, Arb_01)
- **type**: Order type (`limit` or `market`)
- **side**: Direction (`buy` or `sell`)
- **price**: Limit price (or `MKT` for market orders)
- **quantity**: Number of units in the order

**What it tells us**: 
- **Market Maker (MM_01)** primarily places limit orders to provide liquidity
- **Trend Follower (Trend_01)** uses market orders to chase momentum
- **Arbitrage Agent (Arb_01)** uses market orders to exploit price discrepancies

#### **3. `pnl.csv`** - Agent Performance Metrics
Tracks the financial position of each agent over time:
- **step**: Simulation time step
- **agent_id**: Agent identifier
- **inventory**: Current position (positive = long, negative = short)
- **cash**: Available cash balance
- **total_value**: Mark-to-market portfolio value (cash + inventory × current_price)

**What it tells us**: Which strategies were profitable and how agents managed risk through inventory control.

---

### 📈 Interpreting the Graphs

#### **Price History Chart**
- Shows the random walk evolution of the mid-market price
- Starting at $100, the price fluctuates based on the configured volatility (±0.5)
- In this simulation, price drifted down to ~$87-94 range by the end
- The volatility creates opportunities for different trading strategies

**Key Insight**: The price path determines which strategy performs best. Trending markets favor momentum strategies, while mean-reverting markets favor arbitrage.

#### **Agent PnL Chart**
- Displays cumulative profit/loss for each agent (normalized to $0 at start)
- **Arbitrage Agent (Arb_01)** shows moderate gains (~$200-300)
- **Trend Follower (Trend_01)** shows slight losses (-$200 to -$700)
- **Market Maker (MM_01)** shows slight gains (~$250-370)

**Key Insights**:
- The **Arbitrage Agent** performed best by exploiting price inefficiencies
- The **Trend Follower** struggled because the market lacked strong directional trends
- The **Market Maker** earned consistent profits from the bid-ask spread, despite some volatility
- All agents stayed within reasonable PnL ranges, suggesting the simulation is working as designed

#### **Agent Inventory Chart**
- Shows position sizes over time for each agent
- **Market Maker**: Oscillates around zero, occasionally building positions (±30 units)
- **Trend Follower**: Highly volatile positions, ranging from -100 to +40 units
- **Arbitrage Agent**: Moderate positions, typically -70 to +50 units

**Key Insights**:
- The **Market Maker** maintains relatively balanced inventory, as expected for a liquidity provider
- The **Trend Follower** takes large directional bets, leading to significant inventory swings
- The **Arbitrage Agent** accumulates positions when detecting mispricings
- Large inventory swings indicate higher risk exposure

---

## 🎯 Strategy Performance Analysis

### Market Maker (MM_01)
- **Strategy**: Provides liquidity by placing limit orders on both sides of the market
- **Final PnL**: +$250-370 (Small profit)
- **Inventory Management**: Good - stays relatively neutral
- **Key Strength**: Captures bid-ask spread consistently
- **Weakness**: Inventory risk when market moves against positions

### Trend Follower (Trend_01)
- **Strategy**: Chases momentum using a 3-period moving average
- **Final PnL**: -$200 to -$700 (Loss)
- **Inventory Management**: Poor - large directional positions
- **Key Strength**: Works well in trending markets
- **Weakness**: Struggles in choppy/mean-reverting markets (like this simulation)

### Arbitrage Agent (Arb_01)
- **Strategy**: Trades based on deviation from "fair value"
- **Final PnL**: +$200-300 (Best performer)
- **Inventory Management**: Moderate - controlled position sizes
- **Key Strength**: Exploits price inefficiencies effectively
- **Weakness**: Requires accurate fair value estimation

---

## 🔬 Market Microstructure Insights

1. **Liquidity Provision**: The Market Maker's limit orders provide liquidity, allowing other agents to execute trades instantly
2. **Price Discovery**: Agent interactions drive price movements beyond the random walk component
3. **Adverse Selection**: Market Makers face adverse selection when informed traders (Arbitrage) detect mispricings
4. **Inventory Risk**: All agents must balance profit opportunities against inventory risk exposure

---

## 🚀 Future Enhancements
- Implement full RL training with PPO/DQN algorithms
- Add inter-agent communication protocols
- Introduce more sophisticated strategies (statistical arbitrage, market impact models)
- Backtest on historical market data
- Add risk metrics (Sharpe ratio, max drawdown, VaR)
- Multi-asset simulation with correlation structures