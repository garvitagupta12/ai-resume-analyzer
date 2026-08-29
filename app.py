"""
ResumeIQ — AI Resume Analyzer & Job Match Scorer
--------------------------------------------------
A portfolio project by Garvita Gupta.

Wires together parser.py, analyzer.py, and matcher.py (Mistral + LangChain +
Pydantic structured outputs) into a polished, recruiter-friendly web app.
"""

import os
import json
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# ----------------------------------------------------------------------
# Page config
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="ResumeIQ | AI Resume Analyzer",
    page_icon="🧠",
    layout="wide",
)

# ----------------------------------------------------------------------
# Brand palette + global styling
# ----------------------------------------------------------------------
NAVY = "#21295C"
DEEPBLUE = "#065A82"
TEAL = "#1C7293"
ICE = "#CFE8F0"
OFFWHITE = "#F6FAFB"
MUTED = "#5B6B77"

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
    }}

    .stApp {{ background: {OFFWHITE}; }}
    .block-container {{ padding-top: 1.5rem; padding-bottom: 2rem; max-width: 1180px; }}

    /* Hero */
    .hero {{
        background: linear-gradient(135deg, {NAVY} 0%, {DEEPBLUE} 100%);
        border-radius: 18px;
        padding: 2.6rem 2.8rem;
        color: white;
        margin-bottom: 1.6rem;
        box-shadow: 0 10px 30px -12px rgba(33, 41, 92, 0.45);
        position: relative;
        overflow: hidden;
    }}
    .hero::after {{
        content: "";
        position: absolute; top: -60px; right: -60px;
        width: 220px; height: 220px; border-radius: 50%;
        background: rgba(255,255,255,0.06);
    }}
    .hero h1 {{ font-size: 2.1rem; font-weight: 800; margin: 0 0 0.4rem 0; position: relative; }}
    .hero p {{ font-size: 1.02rem; color: {ICE}; margin: 0; max-width: 640px; line-height: 1.5; position: relative; }}
    .hero-badge {{
        display:inline-block; background: rgba(255,255,255,0.14); color: {ICE};
        padding: 4px 14px; border-radius: 999px; font-size: 0.75rem; font-weight: 700;
        letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: 0.9rem; position: relative;
    }}

    /* Feature cards */
    .feat-card {{
        background: white; border: 1px solid #E3ECEF; border-radius: 14px;
        padding: 1.3rem 1.4rem; height: 100%;
        box-shadow: 0 2px 10px -4px rgba(20, 40, 70, 0.08);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }}
    .feat-card:hover {{
        transform: translateY(-3px);
        box-shadow: 0 10px 24px -8px rgba(20, 40, 70, 0.18);
    }}
    .feat-icon {{ font-size: 1.6rem; margin-bottom: 0.55rem; }}
    .feat-title {{ font-weight: 700; color: {NAVY}; font-size: 1.02rem; margin-bottom: 0.35rem; }}
    .feat-desc {{ color: {MUTED}; font-size: 0.87rem; line-height: 1.45; }}

    /* Section labels */
    .section-label {{
        font-size: 0.76rem; font-weight: 700; letter-spacing: 0.07em;
        color: {TEAL}; text-transform: uppercase; margin: 0.2rem 0 0.6rem 0;
    }}

    /* Pills */
    .pill {{
        display: inline-block; padding: 5px 14px; margin: 4px 6px 4px 0;
        border-radius: 999px; font-size: 0.83rem; font-weight: 600;
    }}
    .pill-neutral {{ background: {ICE}; color: {NAVY}; }}
    .pill-good    {{ background: #DFF5E3; color: #1B6B3A; }}
    .pill-bad     {{ background: #FBE3E3; color: #A32020; }}

    /* Fit badge under score gauge */
    .fit-badge {{
        display:block; text-align:center; margin: 0.7rem auto 0 auto; width: fit-content;
        padding: 5px 16px; border-radius: 999px; font-size: 0.8rem; font-weight: 700;
    }}

    /* Streamlit containers used as result cards */
    div[data-testid="stVerticalBlockBorderWrapper"] {{
        background: white; border-radius: 14px !important;
        box-shadow: 0 2px 10px -4px rgba(20, 40, 70, 0.07);
    }}

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{ gap: 6px; border-bottom: 1px solid #E3ECEF; }}
    .stTabs [data-baseweb="tab"] {{
        height: 46px; padding: 0 20px; background-color: transparent;
        border-radius: 10px 10px 0 0; font-weight: 600; color: {MUTED};
    }}
    .stTabs [aria-selected="true"] {{
        background-color: white; color: {NAVY} !important;
        box-shadow: 0 -2px 0 0 {DEEPBLUE} inset;
    }}
    .stTabs [data-baseweb="tab-highlight"] {{ background-color: {DEEPBLUE} !important; }}

    /* File uploader */
    div[data-testid="stFileUploaderDropzone"] {{
        background: white; border: 1.5px dashed #B9CFD9; border-radius: 12px;
    }}

    /* Divider */
    hr {{ border: none; border-top: 1px solid #E3ECEF; margin: 1.4rem 0; }}

    /* Footer */
    .app-footer {{
        text-align: center; color: {MUTED}; font-size: 0.82rem;
        padding: 1.4rem 0 0.6rem 0; border-top: 1px solid #E3ECEF; margin-top: 2rem;
    }}
    .app-footer a {{ color: {TEAL}; text-decoration: none; font-weight: 600; }}

    div.stButton > button {{
        background: {DEEPBLUE}; color: white; border: none; border-radius: 8px;
        font-weight: 600; padding: 0.55rem 1.4rem; transition: background 0.15s ease;
    }}
    div.stButton > button:hover {{ background: {NAVY}; color: white; }}
    div.stButton > button:disabled {{ background: #C7D3D8; color: white; }}

    div[data-testid="stDownloadButton"] > button {{
        background: white; color: {DEEPBLUE}; border: 1.5px solid {DEEPBLUE};
        border-radius: 8px; font-weight: 600;
    }}
    div[data-testid="stDownloadButton"] > button:hover {{
        background: {DEEPBLUE}; color: white;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


def render_pills(items, style="neutral"):
    if not items:
        st.caption("None found.")
        return
    html = "".join(f'<span class="pill pill-{style}">{i}</span>' for i in items)
    st.markdown(html, unsafe_allow_html=True)


def render_bullets(items):
    if not items:
        st.caption("None found.")
        return
    for item in items:
        st.markdown(f"- {item}")


def score_palette(score):
    if score >= 75:
        return "#1B6B3A", "#22A559"   # text, gauge fill (green)
    if score >= 50:
        return "#8A5A00", "#E9A227"   # amber
    return "#A32020", "#E5484D"       # red


def fit_label(score):
    if score >= 75:
        return "Strong Fit", "#1B6B3A", "#DFF5E3"
    if score >= 50:
        return "Moderate Fit", "#8A5A00", "#FCEFD6"
    return "Needs Improvement", "#A32020", "#FBE3E3"


def score_gauge(score):
    text_color, fill = score_palette(score)
    pct = max(0, min(100, score))
    label, label_color, label_bg = fit_label(score)
    st.markdown(
        f"""
        <div style="display:flex; justify-content:center; margin: 0.4rem 0 0.2rem 0;">
          <div style="width:160px;height:160px;border-radius:50%;
                      background: conic-gradient({fill} {pct}%, #EAF2F5 0);
                      display:flex;align-items:center;justify-content:center;">
            <div style="width:122px;height:122px;border-radius:50%;background:white;
                        display:flex;flex-direction:column;align-items:center;justify-content:center;">
              <span style="font-size:2.1rem;font-weight:800;color:{text_color};line-height:1;">{score}</span>
              <span style="font-size:0.72rem;color:{MUTED};margin-top:2px;">/ 100 match</span>
            </div>
          </div>
        </div>
        <div class="fit-badge" style="color:{label_color};background:{label_bg};">{label}</div>
        """,
        unsafe_allow_html=True,
    )


key_present = bool(os.environ.get("MISTRAL_API_KEY"))
if not key_present:
    st.error("MISTRAL_API_KEY is not set. Add it to your .env file to run this app.")
    st.stop()

# Imports deferred until the API key is set, since ChatMistralAI is
# instantiated at module import time in analyzer.py / matcher.py.
from parser import extract_text
from analyzer import analyze_resume
from matcher import match_resume_to_jd

# ----------------------------------------------------------------------
# Hero
# ----------------------------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <div class="hero-badge">AI-Powered · Structured Output</div>
        <h1>ResumeIQ — Resume Analyzer & Job Match Scorer</h1>
        <p>Extract structured insights from any resume, or score it against a job
        description to see exactly where a candidate fits — and where they don't —
        in seconds, not minutes.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

tab_overview, tab_analyze, tab_match = st.tabs(
    ["🏠 Overview", "🔍 Analyze Resume", "🎯 Match to Job Description"]
)

# ----------------------------------------------------------------------
# TAB — Overview
# ----------------------------------------------------------------------
with tab_overview:
    c1, c2, c3 = st.columns(3)
    features = [
        ("📄", "Structured Extraction", "Pulls candidate name, skills, education, experience, projects, and certifications into clean, structured fields — not a wall of text."),
        ("🎯", "Job Match Scoring", "Compares a resume against any job description and returns a 0–100 match score with matched and missing skills."),
        ("💡", "Actionable Feedback", "Surfaces candidate strengths and concrete areas for improvement, with a plain-English explanation behind every score."),
    ]
    for col, (icon, title, desc) in zip([c1, c2, c3], features):
        with col:
            st.markdown(
                f"""
                <div class="feat-card">
                    <div class="feat-icon">{icon}</div>
                    <div class="feat-title">{title}</div>
                    <div class="feat-desc">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

# ----------------------------------------------------------------------
# TAB — Analyze Resume
# ----------------------------------------------------------------------
with tab_analyze:
    resume_file = st.file_uploader(
        "Upload resume (PDF or DOCX)", type=["pdf", "docx"], key="analyze_upload"
    )

    if st.button("Analyze Resume", type="primary", disabled=resume_file is None):
        try:
            with st.spinner("Reading resume..."):
                resume_text = extract_text(resume_file)
            if not resume_text.strip():
                st.error("Couldn't extract any text from this file. Try a different file.")
            else:
                with st.spinner("Analyzing with AI..."):
                    result = analyze_resume(resume_text)
                st.session_state["analysis_result"] = result
        except Exception as e:
            st.error("Something went wrong while analyzing this resume.")
            with st.expander("Show technical details"):
                st.code(str(e))

    result = st.session_state.get("analysis_result")
    if result:
        st.markdown("<br>", unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown(f"## {result.candidate_name}")

            st.markdown('<div class="section-label">🛠️ Skills</div>', unsafe_allow_html=True)
            render_pills(result.skills, "neutral")

            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('<div class="section-label">🎓 Education</div>', unsafe_allow_html=True)
                render_bullets(result.education)
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown('<div class="section-label">📜 Certifications</div>', unsafe_allow_html=True)
                render_bullets(result.certifications)
            with col2:
                st.markdown('<div class="section-label">💼 Experience</div>', unsafe_allow_html=True)
                render_bullets(result.experience)
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown('<div class="section-label">🚀 Projects</div>', unsafe_allow_html=True)
                render_bullets(result.projects)

            st.markdown("<br>", unsafe_allow_html=True)
            st.download_button(
                "⬇️ Download as JSON",
                data=json.dumps(result.model_dump(), indent=2),
                file_name=f"{result.candidate_name.replace(' ', '_')}_analysis.json",
                mime="application/json",
            )

# ----------------------------------------------------------------------
# TAB — Match to Job Description
# ----------------------------------------------------------------------
with tab_match:
    col_left, col_right = st.columns(2)
    with col_left:
        match_resume_file = st.file_uploader(
            "Upload resume (PDF or DOCX)", type=["pdf", "docx"], key="match_upload"
        )
    with col_right:
        jd_text = st.text_area(
            "Paste the job description",
            height=200,
            placeholder="Paste the full job description here...",
        )

    match_ready = match_resume_file is not None and bool(jd_text.strip())
    if st.button("Match Resume to Job", type="primary", disabled=not match_ready):
        try:
            with st.spinner("Reading resume..."):
                resume_text = extract_text(match_resume_file)
            if not resume_text.strip():
                st.error("Couldn't extract any text from this file. Try a different file.")
            else:
                with st.spinner("Comparing resume to job description..."):
                    match_result = match_resume_to_jd(resume_text, jd_text)
                st.session_state["match_result"] = match_result
        except Exception as e:
            st.error("Something went wrong while matching this resume.")
            with st.expander("Show technical details"):
                st.code(str(e))

    match_result = st.session_state.get("match_result")
    if match_result:
        st.markdown("<br>", unsafe_allow_html=True)
        score = max(0, min(100, match_result.match_score))

        with st.container(border=True):
            score_col, exp_col = st.columns([1, 2])
            with score_col:
                score_gauge(score)
            with exp_col:
                st.markdown('<div class="section-label">Explanation</div>', unsafe_allow_html=True)
                st.write(match_result.explanation)

            st.markdown("---")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('<div class="section-label">✅ Matching Skills</div>', unsafe_allow_html=True)
                render_pills(match_result.matching_skills, "good")
            with col2:
                st.markdown('<div class="section-label">❌ Missing Skills</div>', unsafe_allow_html=True)
                render_pills(match_result.missing_skills, "bad")

            st.markdown("---")
            col3, col4 = st.columns(2)
            with col3:
                st.markdown('<div class="section-label">Relevant Experience</div>', unsafe_allow_html=True)
                render_bullets(match_result.relevant_experience)
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown('<div class="section-label">Relevant Projects</div>', unsafe_allow_html=True)
                render_bullets(match_result.relevant_projects)
            with col4:
                st.markdown('<div class="section-label">💪 Strengths</div>', unsafe_allow_html=True)
                render_bullets(match_result.strengths)
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown('<div class="section-label">📈 Areas for Improvement</div>', unsafe_allow_html=True)
                render_bullets(match_result.areas_for_improvement)

            st.markdown("<br>", unsafe_allow_html=True)
            st.download_button(
                "⬇️ Download as JSON",
                data=json.dumps(match_result.model_dump(), indent=2),
                file_name="job_match_result.json",
                mime="application/json",
            )

# ----------------------------------------------------------------------
# Footer
# ----------------------------------------------------------------------
st.markdown(
    """
    <div class="app-footer">
        Built by <b>Garvita Gupta</b> ·
        <a href="https://github.com/garvitagupta12" target="_blank">GitHub</a> ·
        <a href="https://www.linkedin.com/in/garvita-gupta-0b635529a/" target="_blank">LinkedIn</a>
    </div>
    """,
    unsafe_allow_html=True,
)
