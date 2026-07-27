# 📈 Nifty Calendar Spread Trading System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red?style=for-the-badge&logo=streamlit)
![Docker](https://img.shields.io/badge/Docker-Ready-blue?style=for-the-badge&logo=docker)
![SmartAPI](https://img.shields.io/badge/Broker-Angel%20One-orange?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

### An Automated Options Calendar Spread Trading System powered by Angel One SmartAPI

*Real-time Greeks • Automated Position Management • Delta-Based Adjustments • Monthly Rollovers • Streamlit Dashboard*

</div>

---

# 📖 Overview

This project is a **fully automated algorithmic trading system** implementing a **Nifty Calendar Spread Strategy** using the **Angel One SmartAPI**.

The application continuously monitors the options market in real time, dynamically manages positions based on **Greeks** and **Profit & Loss**, performs automatic **sell adjustments**, executes **monthly rollovers**, and maintains state persistence for reliable recovery after interruptions.

The trading engine is wrapped inside a modern **Streamlit Dashboard**, making it easy to configure, launch, and monitor.

---

# ✨ Features

## 📊 Trading Strategy

- Calendar Spread Strategy
- Buy Next Month Call Option
- Sell Current Month Call Option
- Automatic Delta-Based Adjustments
- Automatic Monthly Rollover
- Automatic Expiry Handling
- Live PnL Monitoring
- Continuous Risk Monitoring

---

## ⚡ Real-Time Trading

- Live WebSocket Price Feed
- Live Option Greeks
- Dynamic Option Chain
- Automatic Position Tracking
- Automatic Broker Position Restoration
- Recovery after Unexpected Shutdown
- Sequential Order Execution
- Smart Order Monitoring

---

## 🛡 Risk Management

- Balance Verification before every trade
- Pending Order Protection
- Duplicate Order Prevention
- Automatic Recovery from API Failures
- Timeout Handling
- Order Rejection Detection
- Market Session Validation

---

## 💾 Persistence

- Strategy State Serialization
- Broker Position Synchronization
- Automatic Startup Recovery
- Repository-based State Storage

---

## 🖥 Dashboard

- Streamlit Web Interface
- Secure Credential Entry
- One-Click Start
- One-Click Stop
- Live Status Display
- Docker Ready

---
# 🏗 Project UML Diagram  
![UML_DIAGRAM](https://github.com/adisri-ai/Automated-Trading-System/blob/main/UML_Diagram.png)  

---  

# 📂 Project Structure

```
TradingSystem
│
├── broker/
│
├── core/
│
├── execution/
│   ├── order_manager.py
│   ├── holdings_manager.py
│   ├── expiry_manager.py
│   └── fund_manager.py
│
├── market/
│   ├── websocket_manager.py
│   └── greeks_engine.py
│
├── strategy/
│   ├── nifty_calendar_strategy.py
│   ├── selectors/
│   └── engines/
│
├── persistence/
│
├── utils/
│
├── streamlit_app.py
│
├── requirements.txt
│
├── Dockerfile
│
└── README.md
```

---

# 🚀 Trading Workflow

```
Start System
      │
      ▼
Login to SmartAPI
      │
      ▼
Restore Existing Positions
      │
      ▼
Create Initial Calendar Spread
      │
      ▼
Subscribe WebSocket
      │
      ▼
Monitor Live Market
      │
      ▼
Delta & PnL Evaluation
      │
      ▼
Automatic Sell Adjustment
      │
      ▼
Automatic Monthly Rollover
      │
      ▼
Graceful Shutdown
```

---

# ⚙ Installation

Clone the repository

```bash
git clone https://github.com/yourusername/nifty-calendar-spread.git
```

Move into the project

```bash
cd nifty-calendar-spread
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the Streamlit application

```bash
streamlit run streamlit_app.py
```

---

# 🐳 Docker

Build the image

```bash
docker build -t nifty-calendar .
```

Run the container

```bash
docker run -p 8501:8501 nifty-calendar
```

Open

```
http://localhost:8501
```

---

# 📈 Strategy Logic

## Initial Position

✔ Buy Next Month Call Option

✔ Sell Current Month Call Option

---

## Continuous Monitoring

Every incoming market tick updates
- Delta
- PnL

---

## Sell Adjustment

If

- Delta ≥ 0.65

OR

- PnL Threshold Hit

The strategy

- Squares off current short option
- Finds a better strike
- Places a fresh short position

---

## Monthly Rollover

Before expiry

- Close Current Positions
- Open Next Calendar Spread
- Persist Strategy State

---

# 🧠 Technologies Used

| Component | Technology |
|------------|------------|
| Language | Python |
| UI | Streamlit |
| Broker API | Angel One SmartAPI |
| Live Feed | SmartAPI WebSocket |
| Containerization | Docker |
| Data Processing | Pandas |
| Time Handling | pytz |
| Concurrency | threading |

---

# 📷 Dashboard   

![Trading Dashboard](https://github.com/adisri-ai/Automated-Trading-System/blob/main/utils/Trading_Dashboard.png)
![Configuration](https://github.com/adisri-ai/Automated-Trading-System/blob/main/utils/Configuration.png)
![Current Positions](https://github.com/adisri-ai/Automated-Trading-System/blob/main/utils/Current_Positions.png)
![Strategy Documentation](https://github.com/adisri-ai/Automated-Trading-System/blob/main/utils/Strategy_Documentation.png)

---

# ⚠ Disclaimer

This software is intended **solely for educational and research purposes**.

Algorithmic trading involves significant financial risk.

The author assumes **no responsibility** for any financial losses resulting from the use or misuse of this project.

Always test thoroughly in a paper trading or controlled environment before deploying with real capital.

---

# 👨‍💻 Author

**Aditya Shrivastava**

GitHub: https://github.com/a_code_sri

---
