
from crewai import Agent, Task, Crew, LLM
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm = LLM(model="groq/llama-3.1-8b-instant", api_key=GROQ_API_KEY)

st.set_page_config(page_title="Millat Pharmacy — Assistant", initial_sidebar_state="collapsed")

st.title("Millat Pharmacy — Ask Our Assistant")

if not GROQ_API_KEY:
    st.error("GROQ_API_KEY is missing. Add it in Streamlit Cloud → Manage app → Settings → Secrets.")

if "stock" not in st.session_state:
    st.session_state.stock = []

if len(st.session_state.stock) == 0:
    st.warning("The owner hasn't added any item till now. Please check again later.")
else:
    item_list_text = ""
    for item in st.session_state.stock:
        item_list_text += f"Name: {item['Name']}, Rate: PKR {item['Rate']}, Description: {item['Description']}\n"

    Store_Assistant = Agent(
        role="You are a great store assistant.",
        goal="Answer the customer about the availability of items, price and description only from the store inventory.",
        backstory="You are a store assistant at Al-Hashim Book Store, answering only from the store's current inventory.",
        llm=llm
    )
    Store_Assistant_Task = Task(
        description=(
            "Here is the current store inventory:\n{inventory}\n\n"
            "A customer asks: {question}\n"
            "Answer clearly using only the inventory above."
        ),
        expected_output="A short, clear answer to the customer's question.",
        agent=Store_Assistant
    )
    assistant_crew = Crew(agents=[Store_Assistant], tasks=[Store_Assistant_Task])

    question = st.text_input("Ask about item availability, prices, etc.")

    if st.button("Ask") and question:
        with st.spinner("Checking..."):
            try:
                result = assistant_crew.kickoff(inputs={
                    "inventory": item_list_text,
                    "question": question
                })
                st.write(result.raw)
            except Exception as e:
                st.error(f"Something went wrong: {e}")
