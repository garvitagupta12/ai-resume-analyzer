from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from models import ResumeAnalysis
load_dotenv()

llm = ChatMistralAI(
    model="mistral-small-2506",
    temperature=0
)

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