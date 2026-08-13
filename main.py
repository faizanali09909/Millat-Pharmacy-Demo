from crewai import Agent, Task, Crew, LLM
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm = LLM(model="groq/llama-3.1-8b-instant", api_key=GROQ_API_KEY)

st.set_page_config(page_title="Iqra Book Store — Owner Panel")

st.title("Iqra Book Store — Owner Panel")

if not GROQ_API_KEY:
    st.error("GROQ_API_KEY is missing. Add it in Streamlit Cloud → Manage app → Settings → Secrets.")

if "owner_account" not in st.session_state:
    st.session_state.owner_account = None  # {"username":..., "password":...}

if "Logged_In" not in st.session_state:
    st.session_state.Logged_In = False
    st.session_state.username = None

if "stock" not in st.session_state:
    st.session_state.stock = []

if not st.session_state.Logged_In:
    st.subheader("Owner Login/Sign Up")

    if st.session_state.owner_account is None:
        st.write("No owner account exists yet. Create one below.")
        username = st.text_input("Choose a username")
        Password = st.text_input("Choose a password", type="password")

        if st.button("Create Owner Account"):
            if username == "" or Password == "":
                st.error("Please fill both fields")
            else:
                st.session_state.owner_account = {"username": username, "password": Password}
                st.success("Owner account created! Please log in.")
                st.rerun()

    else:
        username = st.text_input("Username")
        Password = st.text_input("Password", type="password")

        if st.button("Login"):
            if (username == st.session_state.owner_account["username"]
                    and Password == st.session_state.owner_account["password"]):
                st.session_state.Logged_In = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Invalid username or password")

else:
    st.success(f"Welcome {st.session_state.username}")
    if st.button("Logout"):
        st.session_state.Logged_In = False
        st.session_state.username = None
        st.rerun()

    st.divider()
    st.subheader("Manage your items here")

    item_name = st.text_input("Item Name")
    item_rate = st.number_input("Item Rate", min_value=0.0, step=0.1)
    item_description = st.text_area("Item Description")

    if st.button("Add Item"):
        if item_name == "" or item_rate == 0.0:
            st.error("Item name and rate are required")
        else:
            st.session_state.stock.append({
                "Name": item_name,
                "Rate": item_rate,
                "Description": item_description
            })
            st.success("Item added successfully")

    st.divider()
    st.subheader("Current Items")
    if len(st.session_state.stock) == 0:
        st.info("No items are available right now.")
    else:
        for i in range(len(st.session_state.stock)):
            item = st.session_state.stock[i]
            st.write(f"**{item['Name']}** — PKR {item['Rate']}")
            st.write(item['Description'])
            if st.button(f"Remove '{item['Name']}'", key=f"remove_{i}"):
                st.session_state.stock.pop(i)
                st.rerun()
            st.write("---")

    st.divider()
    st.info("Customer chatbot link: add `/chatbot` to your app's URL — e.g. `https://your-app.streamlit.app/chatbot`")