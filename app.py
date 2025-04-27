import streamlit as st
from crypto_api import get_top_cryptos

# Streamlit app title
st.title("Crypto Analytics Dashboard")

# Add custom CSS to remove margins and control layout
st.markdown("""
    <style>
        .coin-block {
            padding: 20px;
            margin: 40px;
            border-radius: 10px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            text-align: center;
        }
        .coin-block img {
            display: block;
            margin-left: auto;
            margin-right: auto;
            border-radius: 50%;
        }
        .coin-block h3 {
            margin-top: 10px;
        }
        .coin-block p {
            margin-top: 5px;
        }
    </style>
""", unsafe_allow_html=True)

# Function to fetch top cryptocurrencies
def get_cryptos_by_type(sort_type=None, limit=10):
    return get_top_cryptos(sort_by=sort_type, limit=limit)

# Streamlit Buttons
top_gainers_button = st.button("Top Gainers")
top_losers_button = st.button("Top Losers")

# Show Top Gainers or Top Losers
if top_gainers_button:
    st.subheader("Top 10 Gainers")
    top_cryptos = get_cryptos_by_type(sort_type='gainers', limit=10)
elif top_losers_button:
    st.subheader("Top 10 Losers")
    top_cryptos = get_cryptos_by_type(sort_type='losers', limit=10)
else:
    st.subheader("Top 15 Cryptocurrencies")
    top_cryptos = get_cryptos_by_type(sort_type=None, limit=15)

# Create columns for displaying the coins
col1, col2, col3 = st.columns(3)

# Loop through top cryptocurrencies and display them in columns
for i, crypto in enumerate(top_cryptos):
    if i % 3 == 0:
        with col1:
            st.markdown(f"""
                <div class="coin-block">
                    <img src="{crypto['image']}" width="50" alt="{crypto['name']} icon">
                    <h3>{crypto['name']}</h3>
                    <p><strong>Price:</strong> ${crypto['current_price']}</p>
                    <p><strong>Market Cap:</strong> ${crypto['market_cap'] / 1e9:.2f}B</p>
                    <p><strong>24h Change:</strong> {crypto.get('price_change_percentage_24h', 'N/A')}%</p>
                    <hr>
                </div>
            """, unsafe_allow_html=True)
    elif i % 3 == 1:
        with col2:
            st.markdown(f"""
                <div class="coin-block">
                    <img src="{crypto['image']}" width="50" alt="{crypto['name']} icon">
                    <h3>{crypto['name']}</h3>
                    <p><strong>Price:</strong> ${crypto['current_price']}</p>
                    <p><strong>Market Cap:</strong> ${crypto['market_cap'] / 1e9:.2f}B</p>
                    <p><strong>24h Change:</strong> {crypto.get('price_change_percentage_24h', 'N/A')}%</p>
                    <hr>
                </div>
            """, unsafe_allow_html=True)
    else:
        with col3:
            st.markdown(f"""
                <div class="coin-block">
                    <img src="{crypto['image']}" width="50" alt="{crypto['name']} icon">
                    <h3>{crypto['name']}</h3>
                    <p><strong>Price:</strong> ${crypto['current_price']}</p>
                    <p><strong>Market Cap:</strong> ${crypto['market_cap'] / 1e9:.2f}B</p>
                    <p><strong>24h Change:</strong> {crypto.get('price_change_percentage_24h', 'N/A')}%</p>
                    <hr>
                </div>
            """, unsafe_allow_html=True)
