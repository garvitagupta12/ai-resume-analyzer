import json
import streamlit as st
from analyzer import analyze_resume
from matcher import match_resume_to_jd
from parser import extract_text

# =========================================================
# Page Configuration
# =========================================================

st.set_page_config(
    page_title="Dossier — AI Resume Review",
    page_icon="🗂️",
    layout="wide",
)


# =========================================================
# Design system — fonts, tokens, component overrides
# =========================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

    :root {
        /* Soft Pastel Palette */
        --desk: #F5EFEB;         /* Soft Pastel Linen */
        --desk-2: #E8DFD8;       /* Muted Warm Sand */
        --line: rgba(74, 63, 53, 0.12);
        --paper: #FFFFFF;        /* Pure White */
        --paper-2: #FAF7F2;      /* Off-White Ivory */
        --brass: #CBA358;        /* Soft Pastel Amber */
        --brass-dim: #9E7B3B;    /* Muted Gold */
        --sage: #8BB18A;         /* Soft Pastel Mint/Sage */
        --sage-dark: #4F734E;    /* Readable Dark Mint */
        --rust: #D98880;         /* Soft Pastel Coral/Terracotta */
        --rust-dark: #A3483F;    /* Readable Dark Coral */
        --ink: #362E2B;          /* Soft Charcoal Dark Brown */
        --ink-soft: #7A6F6B;     /* Muted Charcoal Text */
    }

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    /* ---------- App shell ---------- */
    [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(1200px 500px at 15% -10%, rgba(203,163,88,0.12), transparent 60%),
            var(--desk);
    }
    [data-testid="stHeader"] { background: transparent; }
    .block-container { padding-top: 2rem; max-width: 1180px; }

    h1, h2, h3 { font-family: 'Fraunces', serif; letter-spacing: -0.01em; color: var(--ink); }

    /* ---------- Sidebar: the "folder spine" panel ---------- */
    [data-testid="stSidebar"] {
        background: var(--desk-2);
        border-right: 1px solid var(--line);
    }
    [data-testid="stSidebar"] * { color: var(--ink); }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        font-family: 'Fraunces', serif;
    }
    [data-testid="stSidebar"] hr { border-color: var(--line); }

    /* Sidebar labels -> typewritten field tags */
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] .stMarkdown p {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.72rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: var(--ink-soft) !important;
    }

    /* ---------- Buttons ---------- */
    .stButton > button {
        width: 100%;
        background: var(--paper);
        color: var(--brass-dim) !important;
        border: 1px solid var(--brass);
        border-radius: 6px;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.78rem;
        letter-spacing: 0.10em;
        text-transform: uppercase;
        padding: 0.6rem 1rem;
        transition: all 0.15s ease;
    }
    .stButton > button:hover {
        background: var(--brass-dim);
        color: var(--paper) !important;
        border-color: var(--brass-dim);
    }
    .stButton > button:disabled {
        color: #C2B8B2 !important;
        border-color: #DDD4CE;
        background: transparent;
    }

    /* ---------- File uploader ---------- */
    [data-testid="stFileUploaderDropzone"] {
        background: rgba(255, 255, 255, 0.4);
        border: 1px dashed var(--line);
        border-radius: 6px;
    }

    /* ---------- Tabs styled as folder tabs ---------- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        border-bottom: 1px solid var(--brass-dim);
        background: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        background: var(--desk-2);
        border: 1px solid var(--line);
        border-bottom: none;
        border-radius: 8px 8px 0 0;
        color: var(--ink-soft);
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.78rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        padding: 10px 22px;
    }
    .stTabs [aria-selected="true"] {
        background: var(--paper-2) !important;
        color: var(--ink) !important;
        border-color: var(--paper-2) !important;
        font-weight: 600;
    }
    .stTabs [data-baseweb="tab-panel"] {
        background: var(--paper-2);
        border-radius: 0 10px 10px 10px;
        padding: 30px 34px 24px 34px;
        border: 1px solid var(--line);
        border-top: none;
    }
    .stTabs [data-baseweb="tab-panel"] * { color: var(--ink); }
    .stTabs [data-baseweb="tab-panel"] h3, .stTabs [data-baseweb="tab-panel"] h4 {
        font-family: 'Fraunces', serif;
        color: var(--ink);
    }

    /* ---------- Paper card: a document with a folded corner ---------- */
    .paper {
        position: relative;
        background: var(--paper);
        border: 1px solid var(--line);
        border-radius: 6px;
        padding: 18px 20px 16px 20px;
        margin-bottom: 18px;
        box-shadow: 0 4px 12px rgba(54, 46, 43, 0.04);
    }
    .paper::after {
        content: "";
        position: absolute;
        top: 0; right: 0;
        width: 0; height: 0;
        border-style: solid;
        border-width: 0 16px 16px 0;
        border-color: transparent var(--paper-2) transparent transparent;
        filter: drop-shadow(-1px 1px 1px rgba(54, 46, 43, 0.08));
    }
    .paper-label {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.68rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: var(--brass-dim);
        margin-bottom: 8px;
        display: block;
    }
    .paper li, .paper p { color: var(--ink); }

    /* ---------- Tags (skills, matches, misses) ---------- */
    .tag {
        display: inline-block;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.74rem;
        letter-spacing: 0.03em;
        padding: 3px 10px;
        margin: 3px 4px 3px 0;
        border-radius: 4px;
        border: 1px solid;
    }
    .tag-brass { color: var(--brass-dim); border-color: var(--brass); background: #FAF3E6; }
    .tag-sage  { color: var(--sage-dark); border-color: var(--sage); background: #EEF5EE; }
    .tag-rust  { color: var(--rust-dark); border-color: var(--rust); background: #FDF2F0; }

    /* ---------- Hero ---------- */
    .hero-eyebrow {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.72rem;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: var(--brass-dim);
        margin-bottom: 6px;
    }
    .hero-title {
        font-family: 'Fraunces', serif;
        font-size: 2.6rem;
        font-weight: 600;
        color: var(--ink);
        line-height: 1.08;
        margin: 0 0 10px 0;
    }
    .hero-sub {
        font-family: 'Inter', sans-serif;
        color: var(--ink-soft);
        font-size: 1.02rem;
        max-width: 620px;
        margin-bottom: 6px;
    }
    .hero-rule { border: none; border-top: 1px solid var(--line); margin: 22px 0 28px 0; }

    /* ---------- Seal badge for match score ---------- */
    .seal-wrap { display: flex; align-items: center; gap: 28px; }
    .seal {
        flex-shrink: 0;
        width: 128px; height: 128px;
        border-radius: 50%;
        border: 3px double var(--seal-color, var(--brass-dim));
        display: flex; flex-direction: column;
        align-items: center; justify-content: center;
        transform: rotate(-6deg);
        background: rgba(203, 163, 88, 0.08);
    }
    .seal-score {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 2.1rem;
        font-weight: 600;
        color: var(--seal-color, var(--brass-dim));
        line-height: 1;
    }
    .seal-caption {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.62rem;
        letter-spacing: 0.14em;
        color: var(--seal-color, var(--brass-dim));
        margin-top: 4px;
    }
    .seal-verdict {
        font-family: 'Fraunces', serif;
        font-size: 1.3rem;
        color: var(--ink);
        margin-bottom: 6px;
    }

    /* ---------- Candidate name plate ---------- */
    .nameplate {
        font-family: 'Fraunces', serif;
        font-size: 1.9rem;
        color: var(--ink);
        margin: 4px 0 2px 0;
    }
    .nameplate-eyebrow {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.68rem;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        color: var(--brass-dim);
    }

    [data-testid="stExpander"] {
        background: var(--paper);
        border: 1px solid var(--line);
        border-radius: 6px;
    }
    [data-testid="stExpander"] summary { color: var(--ink); }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# Session State
# =========================================================

defaults = {
    "resume_text": None,
    "resume_name": None,
    "analysis": None,
    "match_result": None,
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def tags(items, css_class="tag-brass", empty_label="None identified"):
    if not items:
        st.caption(empty_label)
        return
    html = "".join(f'<span class="tag {css_class}">{i}</span>' for i in items)
    st.markdown(html, unsafe_allow_html=True)


def paper_list(label, items, empty_label="None identified"):
    st.markdown('<div class="paper">', unsafe_allow_html=True)
    st.markdown(f'<span class="paper-label">{label}</span>', unsafe_allow_html=True)
    if items:
        st.markdown(
            "".join(f"<li>{i}</li>" for i in items),
            unsafe_allow_html=True,
        )
    else:
        st.caption(empty_label)
    st.markdown("</div>", unsafe_allow_html=True)


def seal_color(score):
    if score >= 75:
        return "#4F734E"  # pastel mint/sage
    if score >= 50:
        return "#9E7B3B"  # pastel amber/gold
    return "#A3483F"  # pastel coral/rust


def verdict_text(score):
    if score >= 75:
        return "Strong Fit"
    if score >= 50:
        return "Worth a Conversation"
    return "Significant Gaps"


# =========================================================
# Sidebar — the control panel
# =========================================================

with st.sidebar:
    st.markdown(
        "<div class='hero-eyebrow' style='margin-top:-6px;'>DOSSIER</div>"
        "<div style='font-family:Fraunces,serif;font-size:1.3rem;color:#362E2B;margin-bottom:4px;'>Review Desk</div>",
        unsafe_allow_html=True,
    )
    st.caption("Case intake")

    st.divider()
    st.markdown("**Exhibit A — Resume**")

    uploaded_file = st.file_uploader(
        "Upload resume", type=["pdf", "docx"], label_visibility="collapsed"
    )

    if (
        uploaded_file is not None
        and uploaded_file.name != st.session_state.resume_name
    ):
        with st.spinner("Extracting text..."):
            st.session_state.resume_text = extract_text(uploaded_file)
        st.session_state.resume_name = uploaded_file.name
        st.session_state.analysis = None
        st.session_state.match_result = None

    if st.session_state.resume_text:
        st.markdown(
            f"<span style='color:#4F734E;font-family:IBM Plex Mono,monospace;font-size:0.75rem;'>"
            f"✓ ON FILE — {st.session_state.resume_name}</span>",
            unsafe_allow_html=True,
        )

    st.divider()
    st.markdown("**Exhibit B — Job Description**")

    jd_text = st.text_area(
        "Paste job description",
        height=200,
        placeholder="Paste the job description here...",
        label_visibility="collapsed",
    )

    st.divider()
    analyze_clicked = st.button(
        "Analyze Resume",
        use_container_width=True,
        disabled=st.session_state.resume_text is None,
    )
    match_clicked = st.button(
        "Check Job Match",
        use_container_width=True,
        disabled=not (st.session_state.resume_text and jd_text.strip()),
    )


# =========================================================
# Trigger Actions
# =========================================================

if analyze_clicked:
    with st.spinner("Reviewing the resume..."):
        st.session_state.analysis = analyze_resume(
            st.session_state.resume_text
        )

if match_clicked:
    with st.spinner("Weighing the resume against the job description..."):
        st.session_state.match_result = match_resume_to_jd(
            st.session_state.resume_text, jd_text
        )


# =========================================================
# Hero
# =========================================================

st.markdown(
    """
    <div class="hero-eyebrow">Candidate Review · AI-Assisted</div>
    <div class="hero-title">Every resume,<br>reviewed properly.</div>
    <div class="hero-sub">Upload a resume to open the file. Add a job description to weigh it against
    a real role. Nothing here is invented — only what's actually on the page.</div>
    <hr class="hero-rule">
    """,
    unsafe_allow_html=True,
)

if st.session_state.resume_text is None:
    st.info("No case open. Upload a resume from the panel on the left to begin.")
else:
    with st.expander("View extracted resume text"):
        st.text_area(
            "Resume Content",
            st.session_state.resume_text,
            height=250,
            label_visibility="collapsed",
        )

tab_analysis, tab_match = st.tabs(["ANALYSIS", "JOB MATCH"])


# ---------------------------------------------------------
# Tab 1 — Resume Analysis
# ---------------------------------------------------------

with tab_analysis:
    analysis = st.session_state.analysis

    if analysis is None:
        st.caption(
            "Run **Analyze Resume** from the panel on the left to open this file."
        )
    else:
        st.markdown(
            f"<div class='nameplate-eyebrow'>Candidate</div>"
            f"<div class='nameplate'>{analysis.candidate_name}</div>",
            unsafe_allow_html=True,
        )
        st.write("")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<div class="paper">', unsafe_allow_html=True)
            st.markdown(
                '<span class="paper-label">Skills</span>',
                unsafe_allow_html=True,
            )
            tags(analysis.skills, "tag-brass")
            st.markdown("</div>", unsafe_allow_html=True)

            paper_list("Education", analysis.education)
            paper_list("Certifications", analysis.certifications)

        with col2:
            paper_list("Experience", analysis.experience)
            paper_list("Projects", analysis.projects)
            st.download_button(
                "⬇️ Download Analysis",
                data=analysis.model_dump_json(indent=4),
                file_name="resume_analysis.json",
                mime="application/json",
            )


# ---------------------------------------------------------
# Tab 2 — Job Match
# ---------------------------------------------------------

with tab_match:
    match_result = st.session_state.match_result

    if match_result is None:
        st.caption(
            "Paste a job description on the left and run **Check Job Match** to open this file."
        )
    else:
        score = match_result.match_score
        color = seal_color(score)

        st.markdown('<div class="paper">', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="seal-wrap">
                <div class="seal" style="--seal-color:{color};">
                    <div class="seal-score">{score}</div>
                    <div class="seal-caption">/ 100</div>
                </div>
                <div>
                    <div class="seal-verdict">{verdict_text(score)}</div>
                    <p style="margin:0;">{match_result.explanation}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="paper">', unsafe_allow_html=True)
            st.markdown(
                '<span class="paper-label">Matching Skills</span>',
                unsafe_allow_html=True,
            )
            tags(match_result.matching_skills, "tag-sage")
            st.markdown("</div>", unsafe_allow_html=True)

            paper_list("Relevant Experience", match_result.relevant_experience)
            paper_list("Strengths", match_result.strengths)

        with col2:
            st.markdown('<div class="paper">', unsafe_allow_html=True)
            st.markdown(
                '<span class="paper-label">Missing Skills</span>',
                unsafe_allow_html=True,
            )
            tags(match_result.missing_skills, "tag-rust")
            st.markdown("</div>", unsafe_allow_html=True)

            paper_list("Relevant Projects", match_result.relevant_projects)
            paper_list(
                "Areas for Improvement", match_result.areas_for_improvement
            )
            st.download_button(
                "⬇️ Download Match Report",
                data=match_result.model_dump_json(indent=4),
                file_name="resume_match_report.json",
                mime="application/json",
            )