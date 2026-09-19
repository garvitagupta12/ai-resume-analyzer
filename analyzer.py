import os

from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI

from models import ResumeAnalysis


# Load environment variables from .env locally
load_dotenv()


# Get Groq API key
api_key = os.getenv("MISTRAL_API_KEY")


# Initialize Groq LLM
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    api_key=api_key,
)


# Enable structured output using the Pydantic model
structured_llm = llm.with_structured_output(ResumeAnalysis)


def analyze_resume(resume_text):

    prompt = f"""
You are a very experienced resume analyzer.

Analyze the following resume and extract:

1. Candidate name
2. Skills
3. Education
4. Work experience
5. Projects
6. Certifications

Resume:
{resume_text}

Extract only information that is actually present in the resume.
Do not invent or assume information.
"""

    response = structured_llm.invoke(prompt)

    return response
