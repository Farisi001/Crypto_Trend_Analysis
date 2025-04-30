import streamlit as st
from prophet import Prophet
import pandas as pd
import plotly.express as px
from crypto_api import get_top_cryptos, get_coin_details, get_historical_prices
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="Crypto Analytics Dashboard", layout="wide")
st.title("Crypto Analytics Dashboard")

# --- Coin details view if coin_id in URL
# --- Coin details view if coin_id in URL
params = st.query_params
if "coin_id" in params:
    coin_id = params["coin_id"]
    coin = get_coin_details(coin_id)

    if coin:
        st.image(coin['image']['large'], width=64)
        st.header(f"{coin['name']} ({coin['symbol'].upper()})")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"🌐 [Website]({coin['links']['homepage'][0]})")
            github_link = coin['links']['repos_url']['github']
            if github_link:
                st.markdown(f"💻 [GitHub]({github_link[0]})")
        with col2:
            st.markdown(f"📈 Market Cap: ${coin['market_data']['market_cap']['usd']:,.0f}")
            st.markdown(f"💰 24h Volume: ${coin['market_data']['total_volume']['usd']:,.0f}")

        st.subheader("About")
        st.markdown(coin['description']['en'][:2000] + "...", unsafe_allow_html=True)

        st.subheader("Price Statistics")
        market = coin['market_data']
        st.write({
            "Current Price (USD)": market['current_price']['usd'],
            "24h Change (%)": market['price_change_percentage_24h'],
            "7d Change (%)": market['price_change_percentage_7d'],
            "30d Change (%)": market['price_change_percentage_30d'],
            "60d Change (%)": market['price_change_percentage_60d'],
            "1y Change (%)": market['price_change_percentage_1y'],
            "Circulating Supply": market['circulating_supply'],
            "Max Supply": market.get('max_supply', 'N/A')
        })

        # ✅ Add historical price chart
        st.subheader("📊 Historical Price Chart (Last 90 Days)")
        prices = get_historical_prices(coin_id, days=90)
        if not prices.empty:
            fig = px.line(prices, x="ds", y="y", title=f"{coin['name']} Price (USD)")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("Unable to load historical price data.")

        from prophet.plot import plot_plotly
        st.subheader("🔮 Forecasted Price (Next 90 Days)")
        if not prices.empty:
            #step 1: initialize and fit model
            model = Prophet()
            model.fit(prices)
            #step 2: create dataframe
            future = model.make_future_dataframe(periods=90) #30days into the future
            #step 3: Forecast
            forecast = model.predict(future)
            #step 4: plot forecast
            fig = plot_plotly(model, forecast)
            fig.update_layout(title="90-Day Price Forecast", xaxis_title="Date", yaxis_title="Price (USD)")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Not enough data to forecast")

        st.markdown("---")
        st.markdown("[🔙 Back to Dashboard](./)")
    else:
        st.error("Coin not found.")
    st.stop()
        

# --- Session State Defaults
if "mode" not in st.session_state:
    st.session_state.mode = "normal"
if "clear_search_now" not in st.session_state:
    st.session_state.clear_search_now = False

# Handle clearing search safely BEFORE rendering input
if st.session_state.clear_search_now:
    st.session_state.search_query = ""
    st.session_state.clear_search_now = False

# --- Controls
st.subheader("Find Cryptocurrencies")
search_query = st.text_input("Search by name or ticker (e.g., BTC, Ethereum):", key="search_query")

colA, colB = st.columns(2)
with colA:
    if st.button("Top Gainers 🚀"):
        st.session_state.mode = "gainers"
        st.session_state.clear_search_now = True
with colB:
    if st.button("Top Losers 📉"):
        st.session_state.mode = "losers"
        st.session_state.clear_search_now = True

# --- Fetch coins
@st.cache_data
def get_cryptos(sort_type=None, limit=50):
    return get_top_cryptos(sort_by=sort_type, limit=limit)

if st.session_state.mode == "gainers":
    all_cryptos = get_cryptos(sort_type='gainers', limit=50)[:10]
    st.subheader("Top 10 Gainers")
elif st.session_state.mode == "losers":
    all_cryptos = get_cryptos(sort_type='losers', limit=50)[:10]
    st.subheader("Top 10 Losers")
else:
    all_cryptos = get_cryptos(sort_type=None, limit=50)

# --- Filter based on search
if search_query:
    search_query_lower = search_query.lower()
    filtered_cryptos = [
        crypto for crypto in all_cryptos
        if search_query_lower in crypto['name'].lower() or search_query_lower in crypto['symbol'].lower()
    ]
    st.subheader(f"Search results for '{search_query}'")
else:
    filtered_cryptos = all_cryptos

# --- Display coins
if not filtered_cryptos:
    st.warning("No cryptocurrencies found matching your search.")
else:
    col1, col2, col3 = st.columns(3)
    for i, crypto in enumerate(filtered_cryptos):
        col = [col1, col2, col3][i % 3]
        with col:
            change_24h = crypto.get('price_change_percentage_24h', 0)
            change_color = "green" if change_24h > 0 else "red"

            st.markdown(f"""
                <div class="coin-block">
                    <a href='/?coin_id={crypto["id"]}' style='text-decoration: none; color: inherit;'>
                        <img src="{crypto['image']}" width="50" alt="{crypto['name']} icon">
                        <h3>{crypto['name']} ({crypto['symbol']})</h3>
                    </a>
                    <p><strong>Price:</strong> ${crypto['current_price']}</p>
                    <p><strong>Market Cap:</strong> ${crypto['market_cap'] / 1e9:.2f}B</p>
                    <p><strong>24h Change:</strong> <span style="color:{change_color};">{change_24h:.2f}%</span></p>
                    <hr>
                </div>
            """, unsafe_allow_html=True)
