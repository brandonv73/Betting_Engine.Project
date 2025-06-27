# Betting Engine ⚙️

[![Build Status](https://img.shields.io/github/actions/workflow/status/your-username/betting-engine/ci.yml?branch=main)](https://github.com/brandonv73/Betting_Engine.Project/actions)  
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A Python engine for the full betting lifecycle: real-time odds ingestion and normalization, risk-based stake calculation (Kelly), high-concurrency matching, Flask REST API for user and bet management, and a scalable relational database with backtesting and dashboard hooks.

---

## Table of Contents

- [Features](#features)  
- [Getting Started](#getting-started)  
  - [Prerequisites](#prerequisites)  
  - [Installation](#installation)  
- [Configuration](#configuration)  
- [Usage](#usage)  
- [Architecture](#architecture)  
- [Contributing](#contributing)  
- [License](#license)

---

## Features

- **Real-time Odds Ingestion**  
  Pull odds from multiple providers, normalize payloads, handle missing data.  
- **Risk-Managed Stakes**  
  Apply Kelly criterion or custom limits to size bets responsibly.  
- **High-Throughput Matching Engine**  
  Match orders concurrently against live odds with minimal latency.  
- **RESTful API (Flask)**  
  Endpoints for user auth, placing bets, checking balances, and settling results.  
- **Scalable Storage**  
  Relational schema for events, markets, users, bets, plus hooks for backtesting & dashboards.

---

## Getting Started

### Prerequisites

- Python 3.9+  
- PostgreSQL or MySQL  
- Node.js (optional, for dashboard frontend)  

### Installation

1. **Clone the repo**  
   ```bash
   git clone https://github.com/your-username/betting-engine.git
   cd betting-engine
2. **Create a virtual environment**
   ```bash
   	 python -m venv .venv
   	 source .venv/bin/activate   # Linux/macOS
   	 .venv\Scripts\activate      # Windows
3. **Install Python dependencies**
   
 		 pip install -r requirements.txt

4. **Set up the database**
   - Create a database and update connection strings in config.yaml.

### Configuration
   - Copy config.sample.yaml to config.yaml and adjust:
     ```bash
     # Odds providers
		 providers:
 	  		name: ProviderA
    		api_key: "YOUR_API_KEY"
    		endpoint: "https://api.providerA.com/odds"

		 # Risk management
		 	stake_strategy: "kelly"
 			max_drawdown: 0.2

 		 # Database
				db:
  				uri: "postgresql://user:pass@localhost:5432/bettingdb"

		 # Backtesting & Dashboards
		 enable_backtest: true
		 dashboard_host: "localhost"
		 dashboard_port: 3000

### Usage
1. **Launch the engine**
      ```bash
			
	 			python run_engine.py --config config.yaml;
2. **Interact via API**
   	- Place a bet:
   	  ```bash

   	  	curl -X POST http://localhost:5000/api/bets \
  				-H "Content-Type: application/json" \
 					-d '{"user_id": 1, "event": "Match1", "market": "1X2", "selection": "Home", "stake": 100}'

    - Check balance:
      ```bash

      	curl http://localhost:5000/api/users/1/balance

3. **Run Backtests**
   		```bash

	 			python backtest.py --history data/historical_odds.csv

### Contributing
     
- Fork this repository
- Create a branch: feature/your-feature or fix/your-bug
- Commit your changes and push to your fork
- Open a Pull Request and respond to code review
- Please run flake8 and pytest before submitting.

### License
 - This project is licensed under the MIT License – see the LICENSE file for details.



