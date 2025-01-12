import streamlit as st
from langchain.chat_models import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.output_parsers import JsonOutputParser
from langchain.document_loaders import WebBaseLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
import pandas as pd
import os
import uuid
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Streamlit app title
st.title("Job Matching and Cold Email Generator")

# Sidebar inputs
st.sidebar.header("Input Section")
job_url = st.sidebar.text_input("Enter Job Description URL:")
uploaded_csv = st.sidebar.file_uploader("Upload Portfolio CSV", type=["csv"])

# Initialize components
if "vector_db" not in st.session_state:
    st.session_state["vector_db"] = None

if st.sidebar.button("Process Job Description"):
    try:
        # Step 1: Scrape job description
        st.write("### Step 1: Scraping Job Description")
        loader = WebBaseLoader(job_url)
        docs = loader.load()
        job_description = docs[0].page_content
        st.write(job_description)

        # Step 2: Extract structured data using LangChain
        st.write("### Step 2: Extracting Structured Data")
        chat = ChatGroq(model="llama-3.1-70b-versatile", temperature=0, groq_api_key=GROQ_API_KEY)
        prompt = PromptTemplate(
            input_variables=["job_description"],
            template=(
                "Extract the following fields from the job description:\n"
                "1. Role\n2. Experience\n3. Required Skills\n4. Description\n\n"
                "Job Description: {job_description}\n"
                "Provide output as a JSON object."
            ),
        )
        parser = JsonOutputParser()
        input_prompt = prompt.format(job_description=job_description)
        response = chat.predict(input_prompt)
        structured_data = parser.parse(response)
        st.json(structured_data)

        # Step 3: Load portfolio CSV and populate vector database
        if uploaded_csv:
            st.write("### Step 3: Populating Vector Database")
            portfolio_df = pd.read_csv(uploaded_csv)
            embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
            vector_db = Chroma("portfolio_db", embeddings)

            for index, row in portfolio_df.iterrows():
                metadata = {
                    "name": row["Name"],
                    "link": row["Portfolio Link"],
                    "skills": row["Tech Stack"],
                }
                vector_db.add_texts([row["Tech Stack"]], metadatas=[metadata], ids=[str(uuid.uuid4())])

            st.session_state["vector_db"] = vector_db
            st.success("Portfolio data has been added to the vector database.")

        # Step 4: Query database for matching portfolios
        st.write("### Step 4: Finding Relevant Portfolios")
        query_text = ", ".join(structured_data["Required Skills"])
        results = st.session_state["vector_db"].query(query_text, n_results=3)

        for result in results["documents"]:
            st.write(f"**Name**: {result['name']}")
            st.write(f"**Portfolio Link**: {result['link']}")
            st.write(f"**Skills**: {result['skills']}\n")

        # Step 5: Generate cold email
        st.write("### Step 5: Generating Cold Email")
        email_prompt = (
            "Write a professional cold email to the company based on the job description and the portfolio links provided.\n"
            "Job Description: {job_description}\n"
            "Portfolio Links: {portfolio_links}\n"
        )
        portfolio_links = ", ".join([doc['link'] for doc in results["documents"]])
        email_input = email_prompt.format(
            job_description=job_description, portfolio_links=portfolio_links
        )
        email_response = chat.predict(email_input)
        st.write(email_response)

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
