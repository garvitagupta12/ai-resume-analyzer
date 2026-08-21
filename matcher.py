from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from models import ResumeMatch
load_dotenv()

llm = ChatMistralAI(
    model="mistral-small-2506",
    temperature=0
)

structured_llm = llm.with_structured_output(ResumeMatch)

def match_resume_to_jd(resume_text, jd_text):

    prompt = f"""
You are an expert technical recruiter.

Compare the following resume with the job description.

RESUME:
{resume_text}

JOB DESCRIPTION:
{jd_text}

Analyze the match.

Return:

1. Overall match score from 0 to 100
2. Skills from the job description that are present in the resume
3. Skills required by the job description that are missing from the resume
4. Relevant experience
5. Relevant projects
6. Candidate strengths
7. Areas for improvement
8. Explanation of the score

Important rules:

- Do not invent information.
- Only use information actually present in the resume.
- The match score must be an integer between 0 and 100.
"""

    response = structured_llm.invoke(prompt)
    return response