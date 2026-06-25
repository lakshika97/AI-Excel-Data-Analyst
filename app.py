import streamlit as st
import pandas as pd
import sqlite3
from sqlalchemy import create_engine
from langchain_groq import ChatGroq
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent

# 1. Page Configuration & Setup
st.set_page_config(page_title="AI Data Analyst", layout="wide")
st.title("🤖 Autonomous Local Data Analyst")
st.markdown("Upload any Excel sheet and use AI to immediately query its data.")

# 2. Excel File Upload Interface Step
uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx", "xls"])

if uploaded_file is not None:
    try:
        # Load the uploaded file directly into a Pandas DataFrame
        df = pd.read_excel(uploaded_file)
        
        st.success("File uploaded successfully!")
        
        # Display an expandable data preview window
        with st.expander("🔍 Preview Raw Data Columns"):
            st.dataframe(df.head(5))

        # 3. Create a clean, transient In-Memory SQLite database 
        # This acts as the bridge so LangChain can interface with the Excel rows
        conn = sqlite3.connect(":memory:", check_same_thread=False)
        
        # Sanitize column spaces so SQL queries don't break on execution
        df.columns = [c.replace(' ', '_').replace('.', '') for c in df.columns]
        
        # Write dataframe into the local dynamic table named "uploaded_data"
        #df.to_sql("uploaded_data", conn, index=False, if_exists="replace")

        # Point LangChain's SQL abstraction engine to our virtual storage connection
        #db = SQLDatabase.from_uri("sqlite://", creator=lambda: conn)

        # Build an independent virtual connection instance
        engine = create_engine("sqlite:///:memory:")

        # Write dataframe directly into our virtual storage engine table
        df.to_sql("uploaded_data", engine, index=False, if_exists="replace")
        
        # Wrap the engine cleanly into LangChain's SQL abstraction engine
        db = SQLDatabase(engine)
        
        # 4. Initialize Groq LLM
        # IMPORTANT: Remember to replace this with your *new* revoked key!
        GROQ_API_KEY = "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" 

        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0,
            groq_api_key=GROQ_API_KEY
        )

        # 5. Build LangChain SQL Agent Executor
        agent_executor = create_sql_agent(
            llm=llm,
            db=db,
            agent_type="zero-shot-react-description",
            verbose=True,
            handle_parsing_errors=True
        )

        # 6. Maintain Chat Session State
        if "messages" not in st.session_state:
            st.session_state.messages = [{"role": "assistant", "content": "Hello! I can query your uploaded Excel data. What would you like to know?"}]

        # Render Historical Chat Thread
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # 7. Main Interaction Execution Loop
        if user_prompt := st.chat_input("e.g., Which product category generated the most revenue?"):
            
            # Display user's question
            st.session_state.messages.append({"role": "user", "content": user_prompt})
            with st.chat_message("user"):
                st.markdown(user_prompt)

            # Generate Response via LLM Agent
            with st.chat_message("assistant"):
                response_placeholder = st.empty()
                with st.spinner("Analyzing database schemas and executing queries..."):
                    try:
                        # Append context tip explicitly telling the agent where the excel data lives
                        context_prompt = f"{user_prompt} (Note: The dataset is inside the table called 'uploaded_data')"
                        
                        # Run the text prompt through LangChain's agent
                        result = agent_executor.invoke({"input": context_prompt})
                        output_text = result["output"]
                        
                        response_placeholder.markdown(output_text)
                        st.session_state.messages.append({"role": "assistant", "content": output_text})
                            
                    except Exception as e:
                        error_msg = f"An execution error occurred: {str(e)}"
                        response_placeholder.error(error_msg)
                        
    except Exception as upload_err:
        st.error(f"Could not read Excel file formatting structure: {str(upload_err)}")
else:
    st.info("💡 Please upload an Excel document above to initialize the data analysis environment.")