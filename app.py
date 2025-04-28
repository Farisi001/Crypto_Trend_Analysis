import streamlit as st
from crypto_api import get_top_cryptos

# Streamlit app title
st.title("Crypto Analytics Dashboard")

# --- Session State Defaults
if "mode" not in st.session_state:
    st.session_state.mode = "normal"
if "clear_search_now" not in st.session_state:
    st.session_state.clear_search_now = False

# Handle clearing search safely BEFORE rendering input
if st.session_state.clear_search_now:
    st.session_state.search_query = ""
    st.session_state.clear_search_now = False  # Reset the flag

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
    all_cryptos = get_cryptos(sort_type='gainers', limit=50)
    all_cryptos = all_cryptos[:10]
    st.subheader("Top 10 Gainers")
elif st.session_state.mode == "losers":
    all_cryptos = get_cryptos(sort_type='losers', limit=50)
    all_cryptos = all_cryptos[:10]
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

# --- Handle no results case
if not filtered_cryptos:
    st.warning("No cryptocurrencies found matching your search.")

# --- Display coins
else:
    col1, col2, col3 = st.columns(3)
    for i, crypto in enumerate(filtered_cryptos):
        col = [col1, col2, col3][i % 3]
        with col:
            change_24h = crypto.get('price_change_percentage_24h', 0)
            change_color = "green" if change_24h > 0 else "red"

            st.markdown(f"""
                <div class="coin-block">
                    <img src="{crypto['image']}" width="50" alt="{crypto['name']} icon">
                    <h3>{crypto['name']} ({crypto['symbol']})</h3>
                    <p><strong>Price:</strong> ${crypto['current_price']}</p>
                    <p><strong>Market Cap:</strong> ${crypto['market_cap'] / 1e9:.2f}B</p>
                    <p><strong>24h Change:</strong> <span style="color:{change_color};">{change_24h:.2f}%</span></p>
                    <hr>
                </div>
            """, unsafe_allow_html=True)
