# 🪙 Crypto Analytics Dashboard

An interactive web app built with **Streamlit** that allows users to explore real-time cryptocurrency data, historical price charts, and forecast future price trends using Facebook's **Prophet** library.

## 🚀 Features

- 🔍 **Search** cryptocurrencies by name or ticker (e.g., BTC, Ethereum)
- 📈 View **top gainers** and **top losers** from the market
- 🪙 Detailed **coin information** including:
  - Price stats
  - Market cap
  - Website and GitHub links
  - Project description
- 📊 **Historical price charts** for the last 90 days
- 🔮 **Price forecasting** using Prophet
- 📉 Visual forecast chart with trends and confidence intervals

## 🧰 Tech Stack

- Python
- [Streamlit](https://streamlit.io/)
- [Prophet](https://facebook.github.io/prophet/)
- [Plotly](https://plotly.com/python/)
- CoinGecko API (via `crypto_api.py`)

## 📦 Installation

1. **Clone the repository**

```bash
git clone https://github.com/Farisi001/Crypto_Trend_Analysis
cd Crypto_Trend_Analysis

2. Create and activate a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

4. Run app
streamlit run app.py

