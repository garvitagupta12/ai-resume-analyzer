# ResumeIQ — Resume Analyzer & Job Match Scorer

> An AI-powered resume analysis and job matching application built with Python, Streamlit, LangChain, Mistral AI, and Pydantic.

[![🚀 Live Demo](https://img.shields.io/badge/🚀%20Live%20Demo-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://ai-resume-analyzer-matcher.streamlit.app/)

ResumeIQ analyzes resumes and compares them against job descriptions using an LLM. It extracts structured information from resumes, identifies relevant skills and experience, and provides an AI-generated compatibility assessment.

---

## ✨ Features

### 📄 Resume Analysis

Upload a resume in:

- PDF
- DOCX

The application extracts and analyzes:

- 👤 Candidate Name
- 🛠️ Skills
- 🎓 Education
- 💼 Work Experience
- 🚀 Projects
- 📜 Certifications

### 🎯 Job Description Matching

Paste a job description and compare it with the uploaded resume.

The application provides:

- 🎯 Overall compatibility score
- ✅ Matching skills
- ❌ Missing skills
- 💼 Relevant experience
- 🚀 Relevant projects
- 💪 Candidate strengths
- ⚠️ Areas for improvement
- 📝 AI-generated explanation

### 📥 Download Reports

Analysis results can be downloaded as structured JSON files:

- `resume_analysis.json`
- `resume_match_report.json`

---

## 🧰 Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Web application and UI |
| Mistral AI | Large Language Model |
| LangChain | LLM integration |
| Pydantic | Structured AI output |
| PyMuPDF | PDF text extraction |
| python-docx | DOCX text extraction |
| python-dotenv | Environment variable management |

---

## 🏗️ Project Architecture

```text
                    ┌───────────────────┐
                    │    Streamlit UI   │
                    │      app.py       │
                    └─────────┬─────────┘
                              │
                 ┌────────────┴────────────┐
                 │                         │
                 ▼                         ▼
          ┌─────────────┐          ┌─────────────┐
          │  parser.py  │          │  matcher.py │
          │             │          │             │
          │ PDF / DOCX  │          │ Resume + JD │
          │ text        │          │ comparison  │
          └──────┬──────┘          └──────┬──────┘
                 │                         │
                 │                         ▼
                 │                  ┌─────────────┐
                 │                  │   Mistral   │
                 │                  │     LLM     │
                 │                  └──────┬──────┘
                 │                         │
                 ▼                         ▼
          ┌─────────────────────────────────────┐
          │              analyzer.py            │
          │         LLM-powered analysis        │
          └──────────────────┬──────────────────┘
                             │
                             ▼
                      ┌─────────────┐
                      │  models.py  │
                      │  Pydantic   │
                      │   Models    │
                      └─────────────┘

                      ---

## 📁 Project Structure

```text
ai_resume_analyser/
│
├── .gitignore              # Git ignored files
├── README.md               # Project documentation
├── analyzer.py             # AI-powered resume analysis
├── app.py                  # Streamlit application and UI
├── matcher.py              # Resume and job description matching
├── models.py               # Pydantic data models
├── parser.py               # PDF and DOCX text extraction
├── requirements.txt        # Project dependencies

---

## ⚙️ How It Works

### 1. 📄 Upload Resume

The user uploads a resume in PDF or DOCX format.

```text
Resume
   ↓
PDF / DOCX Parser
   ↓
Extracted Resume Text
     ↓
Prompt
     ↓
Mistral AI
     ↓
Structured Response
     ↓
Pydantic Model

The user can paste a job description into the application.

The resume and job description are then analyzed together

Resume ───────────────┐
                      │
                      ▼
                 Mistral AI
                      │
                      ▲
Job Description ──────┘
                      │
                      ▼
              Match Analysis
                      │
          ┌───────────┼───────────┐
          ↓           ↓           ↓
     Match Score   Missing     Strengths
                    Skills


---

## 🧠 What I Learned

This project was built as a hands-on Generative AI learning project.

Through this project, I explored:

### 🤖 Generative AI

- Working with Large Language Models (LLMs)
- Using Mistral AI through an API
- Designing prompts for specific tasks
- Getting structured information from unstructured text

### 🔗 LangChain

- Integrating LLMs with Python applications
- Working with `ChatMistralAI`
- Invoking LLMs programmatically

### 📦 Pydantic

- Creating structured data models
- Validating AI-generated responses
- Converting unstructured LLM output into structured information

### 📄 Document Processing

- Extracting text from PDF files using PyMuPDF
- Extracting text from DOCX files using `python-docx`
- Working with uploaded files in Streamlit

### 🎨 Streamlit

- Building an interactive web application
- Handling file uploads
- Managing session state
- Creating tabs, buttons, expanders and custom UI components

### 🛠️ Software Development

- Organizing a Python project into multiple modules
- Managing environment variables using `.env`
- Creating a virtual environment
- Managing dependencies with `requirements.txt`
- Building a complete end-to-end GenAI application

---

## 🔮 Future Improvements

The current version focuses on resume analysis and basic resume-to-job matching. Future versions could include:

- 🎯 More advanced ATS-style resume scoring
- 🧠 Semantic similarity using embeddings
- ✍️ AI-powered resume improvement suggestions
- 📄 AI-generated optimized resume sections
- 🎯 Multiple job description comparison
- 💬 AI chatbot for resume-related questions
- 🔐 User authentication and profile management
- 📈 Resume tracking across multiple applications

---

## ⚠️ Disclaimer

The match score generated by Dossier is an **AI-based compatibility assessment** and should not be considered a guarantee of interview selection or employment.

The application is intended for educational and informational purposes.

---

## 👩‍💻 Author

### Garvita Gupta

Built as a hands-on project while learning **Generative AI, LLM application development, and AI-powered applications**.

I'm continuously learning and improving my understanding of Generative AI by building practical projects.

---

## ⭐ Support

If you found this project interesting or useful, consider giving the repository a ⭐ on GitHub!

Feedback and suggestions are always welcome.
