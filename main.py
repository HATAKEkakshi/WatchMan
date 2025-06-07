import streamlit as st
import requests

API_BASE_URL = "http://localhost:8000/watchman" # Change if your FastAPI runs elsewhere

st.title("Watchman Log Explorer")

st.sidebar.header("Actions")
action = st.sidebar.selectbox("Choose action", ["Health Check", "Store Embeddings", "Search Logs", "Chat with Logs"])

if action == "Health Check":
    if st.button("Check API Health"):
        try:
            resp = requests.get(f"{API_BASE_URL}/healthz")
            if resp.status_code == 200:
                st.success(f"API is healthy: {resp.json()}")
            else:
                st.error(f"API returned status code {resp.status_code}")
        except Exception as e:
            st.error(f"Failed to connect to API: {e}")

elif action == "Store Embeddings":
    log_dir = st.text_input("Log Directory", "logs/")
    if st.button("Store Embeddings"):
        try:
            resp = requests.get(f"{API_BASE_URL}/store", params={"log_dir": log_dir})
            if resp.status_code == 200:
                st.success(resp.json().get("message", "Embeddings stored successfully"))
            else:
                st.error(f"Failed to store embeddings: {resp.text}")
        except Exception as e:
            st.error(f"Error calling API: {e}")

elif action == "Search Logs":
    query = st.text_input("Search Query")
    top_k = st.number_input("Number of results", min_value=1, max_value=20, value=5)
    log_dir = st.text_input("Log Directory", "logs/")
    if st.button("Search"):
        if not query:
            st.warning("Please enter a search query.")
        else:
            try:
                resp = requests.get(f"{API_BASE_URL}/search", params={"query": query, "top_k": top_k, "log_dir": log_dir})
                if resp.status_code == 200:
                    results = resp.json().get("results", [])
                    if results:
                        st.write(f"Top {len(results)} matching logs:")
                        for idx, res in enumerate(results, start=1):
                            st.markdown(f"**{idx}.** {res}")
                    else:
                        st.info("No matching logs found.")
                else:
                    st.error(f"Error: {resp.text}")
            except Exception as e:
                st.error(f"API request failed: {e}")

elif action == "Chat with Logs":
    query = st.text_input("Chat Query")
    if st.button("Ask"):
        if not query:
            st.warning("Please enter a query to chat.")
        else:
            try:
                resp = requests.get(f"{API_BASE_URL}/chat", params={"query": query})
                if resp.status_code == 200:
                    answer = resp.json().get("response")
                    if answer:
                        st.markdown("### Response:")
                        st.write(answer)
                    else:
                        st.error(resp.json().get("error", "No answer returned."))
                else:
                    st.error(f"API error: {resp.text}")
            except Exception as e:
                st.error(f"Failed to call API: {e}")
