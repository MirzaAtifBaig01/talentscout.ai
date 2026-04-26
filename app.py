import streamlit as st
import json
import time
import random
import re
import os
import google.generativeai as genai
from datetime import datetime

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="TalentScout AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Inject CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:ital,wght@0,400;0,500;1,400&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --bg: #0a0a0f;
    --surface: #12121a;
    --surface2: #1a1a26;
    --accent: #7c6bff;
    --accent2: #ff6b9d;
    --accent3: #6bffd8;
    --text: #e8e8f0;
    --muted: #6b6b80;
    --border: rgba(124,107,255,0.2);
    --gold: #ffd166;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stAppViewContainer"] {
    background: 
        radial-gradient(ellipse 80% 50% at 10% 0%, rgba(124,107,255,0.08) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 90% 100%, rgba(107,255,216,0.05) 0%, transparent 60%),
        var(--bg) !important;
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] { display: none !important; }

h1, h2, h3, h4 { font-family: 'Syne', sans-serif !important; }

.block-container { padding: 2rem 3rem !important; max-width: 1400px !important; }

/* Hero */
.hero {
    text-align: center;
    padding: 3rem 0 2rem;
    position: relative;
}
.hero-badge {
    display: inline-block;
    background: rgba(124,107,255,0.15);
    border: 1px solid var(--border);
    color: var(--accent);
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding: 0.35rem 1rem;
    border-radius: 100px;
    margin-bottom: 1.5rem;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.5rem, 5vw, 4rem);
    font-weight: 800;
    line-height: 1.05;
    background: linear-gradient(135deg, var(--text) 0%, var(--accent) 50%, var(--accent3) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 1rem;
}
.hero-sub {
    color: var(--muted);
    font-size: 1.1rem;
    font-weight: 300;
    max-width: 560px;
    margin: 0 auto;
    line-height: 1.7;
}

/* Cards */
.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}
.card-header {
    font-family: 'Syne', sans-serif;
    font-size: 0.75rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* Rank cards */
.rank-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 1.75rem;
    margin-bottom: 1rem;
    transition: border-color 0.2s;
    position: relative;
    overflow: hidden;
}
.rank-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent), var(--accent3));
    opacity: 0;
    transition: opacity 0.2s;
}
.rank-card:hover::before { opacity: 1; }
.rank-card:hover { border-color: rgba(124,107,255,0.4); }

.rank-card.rank-1 { border-color: rgba(255,209,102,0.4); background: linear-gradient(135deg, rgba(255,209,102,0.05), var(--surface)); }
.rank-card.rank-1::before { background: linear-gradient(90deg, var(--gold), #ffa94d); opacity: 1; }

.rank-num {
    font-family: 'DM Mono', monospace;
    font-size: 0.75rem;
    color: var(--muted);
    letter-spacing: 0.1em;
}
.rank-name {
    font-family: 'Syne', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: var(--text);
    margin: 0.25rem 0;
}
.rank-location {
    font-size: 0.85rem;
    color: var(--muted);
}

/* Score bars */
.score-row {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin: 0.5rem 0;
}
.score-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    color: var(--muted);
    width: 90px;
    flex-shrink: 0;
}
.score-bar-bg {
    flex: 1;
    height: 6px;
    background: rgba(255,255,255,0.06);
    border-radius: 3px;
    overflow: hidden;
}
.score-bar-fill {
    height: 100%;
    border-radius: 3px;
    transition: width 0.8s ease;
}
.score-val {
    font-family: 'DM Mono', monospace;
    font-size: 0.8rem;
    font-weight: 500;
    width: 42px;
    text-align: right;
}

/* Tags */
.tag {
    display: inline-block;
    background: rgba(124,107,255,0.1);
    border: 1px solid rgba(124,107,255,0.25);
    color: var(--accent);
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    padding: 0.2rem 0.55rem;
    border-radius: 6px;
    margin: 0.15rem;
}
.tag.matched {
    background: rgba(107,255,216,0.1);
    border-color: rgba(107,255,216,0.3);
    color: var(--accent3);
}
.tag.missing {
    background: rgba(255,107,157,0.08);
    border-color: rgba(255,107,157,0.2);
    color: var(--accent2);
}

/* Chat bubble */
.chat-bubble {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 0.9rem 1.1rem;
    margin-top: 0.75rem;
    font-size: 0.9rem;
    font-style: italic;
    color: #c8c8d8;
    position: relative;
}
.chat-bubble::before {
    content: '💬';
    position: absolute;
    top: -10px;
    left: 14px;
    font-style: normal;
    font-size: 0.9rem;
}

/* Final score badge */
.final-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: linear-gradient(135deg, rgba(124,107,255,0.2), rgba(107,255,216,0.1));
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 0.5rem 1rem;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1.1rem;
    color: var(--text);
}

/* Pipeline step */
.step {
    display: flex;
    align-items: flex-start;
    gap: 1rem;
    padding: 0.75rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
}
.step-icon {
    width: 32px;
    height: 32px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.9rem;
    flex-shrink: 0;
    background: rgba(124,107,255,0.1);
}
.step-icon.done { background: rgba(107,255,216,0.1); }
.step-icon.running { background: rgba(255,209,102,0.1); animation: pulse 1s infinite; }
@keyframes pulse { 0%,100% { opacity: 1; } 50% { opacity: 0.4; } }

.step-text { font-size: 0.88rem; color: var(--muted); }
.step-text strong { color: var(--text); display: block; }

/* Stagger fade-in */
.fade-in {
    animation: fadeUp 0.5s ease both;
}
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* Streamlit overrides */
.stTextArea textarea {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    color: var(--text) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.85rem !important;
}
.stTextArea textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(124,107,255,0.12) !important;
}
.stButton > button {
    background: linear-gradient(135deg, var(--accent), #9b6bff) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    padding: 0.75rem 2.5rem !important;
    width: 100% !important;
    transition: opacity 0.2s, transform 0.2s !important;
    letter-spacing: 0.02em !important;
}
.stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}
div[data-testid="stMetric"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 1rem !important;
}
div[data-testid="stMetric"] label { color: var(--muted) !important; font-family: 'DM Mono', monospace !important; font-size: 0.75rem !important; }
div[data-testid="stMetric"] [data-testid="stMetricValue"] { color: var(--text) !important; font-family: 'Syne', sans-serif !important; font-weight: 700 !important; }
.stExpander { border: 1px solid var(--border) !important; border-radius: 12px !important; background: var(--surface) !important; }
.stExpander summary { font-family: 'DM Mono', monospace !important; font-size: 0.82rem !important; color: var(--muted) !important; }
</style>
""", unsafe_allow_html=True)

# ── Candidate DB ───────────────────────────────────────────────────────────────
CANDIDATES = [
    {"name":"Rahul Sharma","skills":["Python","Machine Learning","Flask","NLP","Scikit-learn"],"experience":3,"location":"Hyderabad","summary":"ML engineer with 3 years building NLP pipelines and Flask REST APIs. Deployed models to production, familiar with MLOps basics."},
    {"name":"Ayesha Khan","skills":["React","Node.js","MongoDB","TypeScript","GraphQL"],"experience":4,"location":"Bangalore","summary":"Full-stack developer specialising in React frontends and Node microservices. Shipped 5 production SaaS products."},
    {"name":"Vikram Reddy","skills":["Python","Django","SQL","PostgreSQL","Redis"],"experience":5,"location":"Hyderabad","summary":"Senior backend developer with strong Django and database optimisation experience. Led team of 4 engineers."},
    {"name":"Sneha Iyer","skills":["Python","Machine Learning","TensorFlow","Deep Learning","Computer Vision"],"experience":2,"location":"Chennai","summary":"ML engineer passionate about deep learning and computer vision. Published 2 papers, Kaggle Expert."},
    {"name":"Arjun Mehta","skills":["Python","Machine Learning","Flask","Docker","Kubernetes"],"experience":4,"location":"Mumbai","summary":"MLOps engineer who bridges data science and infrastructure. Specialises in containerising ML workloads."},
    {"name":"Priya Nair","skills":["Python","Data Science","Pandas","Matplotlib","SQL"],"experience":2,"location":"Kochi","summary":"Data analyst transitioning to ML engineering. Strong statistics background and communication skills."},
    {"name":"Karan Gupta","skills":["Java","Spring Boot","Microservices","Kafka","AWS"],"experience":6,"location":"Pune","summary":"Senior Java architect designing event-driven microservices on AWS. Team lead with strong system design skills."},
    {"name":"Divya Sharma","skills":["Python","FastAPI","Machine Learning","MLflow","AWS"],"experience":3,"location":"Delhi","summary":"Python developer building FastAPI services and managing ML model lifecycle with MLflow on AWS."},
    {"name":"Rohit Verma","skills":["Python","NLP","BERT","Transformers","Flask"],"experience":4,"location":"Hyderabad","summary":"NLP specialist with hands-on experience fine-tuning BERT and Transformer models for production systems."},
    {"name":"Ananya Singh","skills":["React","Python","Flask","MongoDB","Machine Learning"],"experience":2,"location":"Bangalore","summary":"Full-stack developer with growing ML interest. Built 3 end-to-end AI-powered web applications."},
]

# ── Gemini client ──────────────────────────────────────────────────────────────
GEMINI_API_KEY = "AIzaSyB7_e7yD91WgKhR8qSBsf7BJ2435itRvC0"

@st.cache_resource
def get_model():
    genai.configure(api_key=GEMINI_API_KEY)
    return genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        generation_config=genai.types.GenerationConfig(
            temperature=0.7,
            response_mime_type="application/json",
        ),
    )

# ── AI functions ───────────────────────────────────────────────────────────────
def parse_jd_with_ai(jd_text: str) -> dict:
    model = get_model()
    prompt = f"""Extract structured data from this job description. Respond ONLY with valid JSON.
Schema: {{"required_skills":[],"nice_to_have_skills":[],"min_experience":0,"role_title":"","key_responsibilities":[]}}

Job Description:
{jd_text}"""
    resp = model.generate_content(prompt)
    text = resp.text.strip()
    text = re.sub(r"```json|```","",text).strip()
    return json.loads(text)

def compute_match_score_ai(jd_text: str, parsed_jd: dict, candidate: dict) -> dict:
    model = get_model()
    prompt = f"""Score this candidate against the job description.

JD Summary: {jd_text[:400]}
Required Skills: {parsed_jd.get('required_skills',[])}
Min Experience: {parsed_jd.get('min_experience',0)} years

Candidate:
Name: {candidate['name']}
Skills: {candidate['skills']}
Experience: {candidate['experience']} years
Location: {candidate['location']}
Summary: {candidate['summary']}

Respond ONLY with valid JSON:
{{"match_score":0-100,"matched_skills":[],"missing_skills":[],"experience_fit":"strong/partial/weak","one_line_reason":""}}"""
    resp = model.generate_content(prompt)
    text = re.sub(r"```json|```","",resp.text).strip()
    return json.loads(text)

def simulate_conversation_ai(jd_text: str, candidate: dict, match_score: int) -> dict:
    model = get_model()
    prompt = f"""You are simulating a job candidate receiving a recruiter outreach message.

The recruiter reached out about this role: {jd_text[:300]}

You are {candidate['name']}, a {candidate['experience']}-year experienced professional with skills in {', '.join(candidate['skills'])}.
Your match with this role is roughly {match_score}%.

Simulate a realistic 2-turn conversation:
1. Recruiter's opening message (personalised to the candidate)
2. Candidate's realistic reply (based on their profile fit)

Then give an interest score 0-100 based on the reply.

Respond ONLY with valid JSON:
{{"recruiter_message":"","candidate_reply":"","interest_score":0-100,"interest_label":"Hot/Warm/Neutral/Not interested"}}"""
    resp = model.generate_content(prompt)
    text = re.sub(r"```json|```","",resp.text).strip()
    return json.loads(text)

# ── Score bar HTML ─────────────────────────────────────────────────────────────
def score_bar(label, value, color):
    return f"""
<div class="score-row">
  <span class="score-label">{label}</span>
  <div class="score-bar-bg">
    <div class="score-bar-fill" style="width:{value}%;background:{color};"></div>
  </div>
  <span class="score-val" style="color:{color};">{value}%</span>
</div>"""

def interest_color(label):
    return {"Hot":"#6bffd8","Warm":"#ffd166","Neutral":"#a0a0b8","Not interested":"#ff6b9d"}.get(label,"#a0a0b8")

# ── Main ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-badge">⚡ AI-Powered Recruiting Agent</div>
  <h1 class="hero-title">TalentScout AI</h1>
  <p class="hero-sub">Paste a Job Description. Watch the agent discover, match, and engage candidates — then hand you a ranked shortlist in seconds.</p>
</div>
""", unsafe_allow_html=True)

# ── Metrics row ────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("Candidates in DB", len(CANDIDATES))
c2.metric("Scoring Dimensions", "2 (Match + Interest)")
c3.metric("AI Model", "Gemini 2.5 Flash Lite")
c4.metric("Explainability", "✓ Full")

st.markdown("<br>", unsafe_allow_html=True)

# ── Sample JDs ─────────────────────────────────────────────────────────────────
SAMPLE_JDS = {
    "🤖 ML Engineer": "We are looking for a Python Machine Learning Engineer with 2+ years of experience. You will build and deploy NLP models, create Flask APIs, and work with scikit-learn and TensorFlow. Strong Python fundamentals required. MLOps experience is a plus.",
    "🌐 Full Stack Dev": "Seeking a Full Stack Developer with React and Node.js expertise, 3+ years experience. You will build scalable web applications with MongoDB, implement GraphQL APIs, and collaborate with design and product teams.",
    "⚙️ Backend Engineer": "Senior Backend Engineer needed with Python or Django experience (4+ years). Must have strong SQL/PostgreSQL skills, experience with Redis caching, and ability to design scalable APIs. Team lead experience preferred.",
}

col_jd, col_pipeline = st.columns([3, 2], gap="large")

with col_jd:
    st.markdown('<div class="card-header">📋 JOB DESCRIPTION INPUT</div>', unsafe_allow_html=True)

    sample_choice = st.selectbox("Load a sample JD →", ["(paste your own)"] + list(SAMPLE_JDS.keys()), label_visibility="collapsed")
    default_jd = SAMPLE_JDS.get(sample_choice, "")

    jd_input = st.text_area(
        "Job Description",
        value=default_jd,
        height=220,
        placeholder="Paste the full job description here…",
        label_visibility="collapsed"
    )

    run = st.button("🚀  Run TalentScout Agent", use_container_width=True)

with col_pipeline:
    st.markdown('<div class="card-header">🔄 AGENT PIPELINE</div>', unsafe_allow_html=True)
    pipeline_placeholder = st.empty()
    pipeline_placeholder.markdown("""
<div class="card">
<div class="step"><div class="step-icon">📄</div><div class="step-text"><strong>JD Parser</strong>Extract skills, experience, responsibilities</div></div>
<div class="step"><div class="step-icon">🔍</div><div class="step-text"><strong>Candidate Discovery</strong>Search 10 candidate profiles</div></div>
<div class="step"><div class="step-icon">🧠</div><div class="step-text"><strong>AI Match Scoring</strong>Semantic + skill + experience fit</div></div>
<div class="step"><div class="step-icon">💬</div><div class="step-text"><strong>Conversational Outreach</strong>Simulate personalised engagement</div></div>
<div class="step"><div class="step-icon">🏆</div><div class="step-text"><strong>Ranked Shortlist</strong>Combined score + explainability</div></div>
</div>""", unsafe_allow_html=True)

# ── Run pipeline ───────────────────────────────────────────────────────────────
if run and jd_input.strip():
    st.markdown("---")
    results_area = st.container()

    def update_pipeline(step_idx):
        icons = ["📄","🔍","🧠","💬","🏆"]
        labels = ["JD Parser","Candidate Discovery","AI Match Scoring","Conversational Outreach","Ranked Shortlist"]
        descs  = [
            "Extract skills, experience, responsibilities",
            "Search 10 candidate profiles",
            "Semantic + skill + experience fit",
            "Simulate personalised engagement",
            "Combined score + explainability",
        ]
        html = '<div class="card">'
        for i,(ic,lb,dc) in enumerate(zip(icons,labels,descs)):
            state = "done" if i < step_idx else ("running" if i == step_idx else "")
            emoji = "✅" if i < step_idx else ("⏳" if i == step_idx else ic)
            html += f'<div class="step"><div class="step-icon {state}">{emoji}</div><div class="step-text"><strong>{lb}</strong>{dc}</div></div>'
        html += '</div>'
        pipeline_placeholder.markdown(html, unsafe_allow_html=True)

    with results_area:
        # Step 1 — Parse JD
        update_pipeline(0)
        with st.spinner("Parsing job description with AI…"):
            try:
                parsed_jd = parse_jd_with_ai(jd_input)
            except Exception as e:
                st.error(f"JD parse error: {e}")
                st.stop()
        update_pipeline(1)

        st.markdown(f"""
<div class="card fade-in">
  <div class="card-header">📄 PARSED JD — {parsed_jd.get('role_title','Role')}</div>
  <p style="color:var(--muted);font-size:0.85rem;margin-bottom:0.75rem;">Required skills detected by AI:</p>
  {"".join(f'<span class="tag">{s}</span>' for s in parsed_jd.get('required_skills',[]))}
  {"".join(f'<span class="tag" style="opacity:0.6">{s} ✦</span>' for s in parsed_jd.get('nice_to_have_skills',[]))}
  <p style="color:var(--muted);font-size:0.8rem;margin-top:0.75rem;">Min experience: <strong style="color:var(--text)">{parsed_jd.get('min_experience',0)} years</strong></p>
</div>""", unsafe_allow_html=True)

        # Step 2 — Discover
        update_pipeline(1)
        time.sleep(0.4)
        update_pipeline(2)

        # Step 3 — Score all candidates
        all_results = []
        progress = st.progress(0, text="Scoring candidates…")
        for idx, candidate in enumerate(CANDIDATES):
            progress.progress((idx+1)/len(CANDIDATES), text=f"Evaluating {candidate['name']}…")
            try:
                match_data = compute_match_score_ai(jd_input, parsed_jd, candidate)
            except:
                match_data = {"match_score": random.randint(20,60), "matched_skills":[], "missing_skills":[], "experience_fit":"partial","one_line_reason":"Scored by fallback."}
            all_results.append({**candidate, **match_data})

        progress.empty()
        update_pipeline(3)

        # Step 4 — Conversations for top 5
        top5 = sorted(all_results, key=lambda x: x["match_score"], reverse=True)[:5]
        progress2 = st.progress(0, text="Simulating outreach conversations…")
        for idx, r in enumerate(top5):
            progress2.progress((idx+1)/5, text=f"Engaging {r['name']}…")
            try:
                convo = simulate_conversation_ai(jd_input, r, r["match_score"])
            except:
                convo = {"recruiter_message":f"Hi {r['name']}, we have a great role that fits your profile!", "candidate_reply":"Interesting, tell me more.", "interest_score":60, "interest_label":"Warm"}
            r.update(convo)
            r["final_score"] = round(0.6 * r["match_score"] + 0.4 * r["interest_score"], 1)

        progress2.empty()
        update_pipeline(4)

        # ── Results ────────────────────────────────────────────────────────────
        st.markdown(f"""
<div class="hero" style="padding:2rem 0 0.5rem;">
  <div class="hero-badge">🏆 SHORTLIST READY — {len(top5)} CANDIDATES</div>
</div>""", unsafe_allow_html=True)

        for rank, r in enumerate(top5, 1):
            rank_cls = "rank-1" if rank == 1 else ""
            medal = "🥇" if rank==1 else ("🥈" if rank==2 else ("🥉" if rank==3 else f"#{rank}"))
            int_color = interest_color(r.get("interest_label","Neutral"))

            matched_tags = "".join(f'<span class="tag matched">{s}</span>' for s in r.get("matched_skills",[]))
            missing_tags = "".join(f'<span class="tag missing">{s}</span>' for s in r.get("missing_skills",[]))
            exp_fit = r.get("experience_fit","partial")
            exp_color = {"strong":"#6bffd8","partial":"#ffd166","weak":"#ff6b9d"}.get(exp_fit,"#a0a0b8")

            st.markdown(f"""
<div class="rank-card {rank_cls} fade-in">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:1rem;">
    <div>
      <div class="rank-num">{medal} RANK {rank}</div>
      <div class="rank-name">{r['name']}</div>
      <div class="rank-location">📍 {r['location']} &nbsp;·&nbsp; {r['experience']} yrs exp &nbsp;·&nbsp; <span style="color:{exp_color};font-size:0.8rem;">{exp_fit.upper()} FIT</span></div>
    </div>
    <div class="final-badge">⭐ {r['final_score']}%</div>
  </div>

  <div style="margin:1.25rem 0 0.5rem;">
    {score_bar("Match", r['match_score'], "var(--accent)")}
    {score_bar("Interest", r['interest_score'], int_color)}
    {score_bar("Final", int(r['final_score']), "var(--gold)")}
  </div>

  <div style="margin:0.75rem 0 0.25rem;">
    <span style="font-size:0.72rem;color:var(--muted);font-family:'DM Mono',monospace;letter-spacing:0.08em;">SKILLS</span><br>
    {matched_tags or '<span class="tag missing">No direct matches</span>'}
    {f'<span style="color:var(--muted);font-size:0.75rem;margin-left:0.5rem;">Missing: </span>{missing_tags}' if missing_tags else ''}
  </div>

  <p style="font-size:0.83rem;color:var(--muted);margin:0.75rem 0 0.5rem;font-style:italic;">"{r.get('one_line_reason','AI-assessed candidate.')}"</p>

  <div style="background:rgba(124,107,255,0.06);border:1px solid rgba(124,107,255,0.15);border-radius:10px;padding:0.85rem;margin-top:0.75rem;">
    <div style="font-family:'DM Mono',monospace;font-size:0.68rem;color:var(--accent);letter-spacing:0.1em;margin-bottom:0.5rem;">SIMULATED OUTREACH</div>
    <p style="font-size:0.82rem;color:var(--muted);margin:0;">🤖 <em>{r.get('recruiter_message','—')}</em></p>
    <div class="chat-bubble">{r.get('candidate_reply','No reply.')}</div>
    <div style="margin-top:0.5rem;font-size:0.78rem;">
      <span style="color:{int_color};font-family:'DM Mono',monospace;font-weight:500;">● {r.get('interest_label','—')}</span>
      <span style="color:var(--muted);margin-left:0.5rem;">Interest score: {r['interest_score']}%</span>
    </div>
  </div>
</div>""", unsafe_allow_html=True)

        # ── Export ─────────────────────────────────────────────────────────────
        export = [{
            "Rank": i+1, "Name": r["name"], "Location": r["location"],
            "Experience (yrs)": r["experience"],
            "Match Score (%)": r["match_score"], "Interest Score (%)": r["interest_score"],
            "Final Score (%)": r["final_score"],
            "Interest Label": r.get("interest_label",""),
            "Matched Skills": ", ".join(r.get("matched_skills",[])),
            "Missing Skills": ", ".join(r.get("missing_skills",[])),
            "Candidate Reply": r.get("candidate_reply",""),
            "AI Reason": r.get("one_line_reason",""),
        } for i, r in enumerate(top5)]

        import pandas as pd
        df_export = pd.DataFrame(export)

        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button(
            "⬇️  Download Shortlist as CSV",
            df_export.to_csv(index=False),
            file_name=f"talentscout_shortlist_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            use_container_width=True,
        )

elif run:
    st.warning("Please paste a job description first.")

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:3rem 0 1rem;color:var(--muted);font-size:0.8rem;font-family:'DM Mono',monospace;">
  TalentScout AI &nbsp;·&nbsp; Built with Gemini 2.5 Flash Lite &nbsp;·&nbsp; Deccan AI Hackathon 2025
</div>""", unsafe_allow_html=True)
