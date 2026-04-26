# 🎯 TalentScout AI — AI-Powered Talent Scouting & Engagement Agent

> **Deccan AI Hackathon 2025 Submission**

TalentScout AI is an end-to-end recruiting agent that takes a Job Description as input, discovers matching candidates, simulates personalised conversational outreach, and outputs a ranked shortlist scored on two dimensions: **Match Score** and **Interest Score**.

---

## 🚀 Live Demo

**Deployed URL:** `[your-app-name].streamlit.app`  
**Demo Video:** `[YouTube / Loom link]`

---

## ✨ Features

| Feature | Description |
|---|---|
| 📄 **JD Parsing** | Claude AI extracts required skills, nice-to-have skills, experience, and responsibilities |
| 🔍 **Candidate Discovery** | Searches a pool of 10 realistic candidate profiles |
| 🧠 **AI Match Scoring** | Semantic + skill overlap + experience fit, with explainability |
| 💬 **Conversational Outreach** | Claude simulates a recruiter message and realistic candidate reply |
| 🏆 **Ranked Shortlist** | Combined score (60% match + 40% interest) with full explanations |
| ⬇️ **CSV Export** | Download the shortlist for your ATS or spreadsheet |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   TALENTSCOUT AI AGENT                  │
│                                                         │
│  ┌──────────┐    ┌──────────┐    ┌──────────────────┐  │
│  │ JD Input │───▶│  Claude  │───▶│  Parsed JD JSON  │  │
│  │ (text)   │    │  Sonnet  │    │  skills/exp/role  │  │
│  └──────────┘    └──────────┘    └────────┬─────────┘  │
│                                           │             │
│                  ┌────────────────────────▼──────────┐  │
│                  │       Candidate Database (10+)     │  │
│                  │  name, skills, exp, location,      │  │
│                  │  summary                           │  │
│                  └────────────────────────┬──────────┘  │
│                                           │             │
│  ┌────────────────────────────────────────▼──────────┐  │
│  │               AI MATCH SCORING (per candidate)    │  │
│  │  • Skill overlap (required vs candidate skills)   │  │
│  │  • Experience fit (strong / partial / weak)       │  │
│  │  • Semantic similarity via Claude                 │  │
│  │  • One-line explainability reason                 │  │
│  │  ──────────────────────────────────────────────  │  │
│  │  OUTPUT: match_score (0-100) + explanation        │  │
│  └────────────────────────────────────────┬──────────┘  │
│                                           │             │
│  ┌────────────────────────────────────────▼──────────┐  │
│  │         CONVERSATIONAL OUTREACH (top 5)           │  │
│  │  • Claude generates personalised recruiter msg    │  │
│  │  • Claude simulates realistic candidate reply     │  │
│  │  • Interest scored: Hot / Warm / Neutral / Cold   │  │
│  │  ──────────────────────────────────────────────  │  │
│  │  OUTPUT: interest_score (0-100) + reply text      │  │
│  └────────────────────────────────────────┬──────────┘  │
│                                           │             │
│  ┌────────────────────────────────────────▼──────────┐  │
│  │               RANKED SHORTLIST                    │  │
│  │  final_score = 0.6 × match + 0.4 × interest       │  │
│  │  Sorted descending — ready for recruiter action   │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

---

## 📊 Scoring Logic

### Match Score (0–100)
Computed by Claude Sonnet 4 per candidate:
- **Skill overlap**: required JD skills vs candidate's skill list
- **Experience fit**: candidate years vs JD minimum
- **Semantic fit**: candidate summary vs JD role context

### Interest Score (0–100)
Computed via simulated outreach:
- Claude generates a personalised recruiter outreach message
- Claude simulates the candidate's realistic reply (based on their profile fit)
- Interest score reflects engagement level: Hot (80–100), Warm (60–79), Neutral (40–59), Cold (<40)

### Final Score
```
final_score = 0.6 × match_score + 0.4 × interest_score
```

Weighting rationale: match quality is primary; genuine interest ensures outreach ROI.

---

## 🛠️ Local Setup

### Prerequisites
- Python 3.10+
- An Anthropic API key ([get one here](https://console.anthropic.com))

### Steps

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/talentscout-ai
cd talentscout-ai

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your API key
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit secrets.toml and paste your ANTHROPIC_API_KEY

# 4. Run
streamlit run app.py
```

App will open at `http://localhost:8501`

---

## ☁️ Deploy to Streamlit Cloud (Free)

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo → select `app.py`
4. In **Secrets**, add:
   ```toml
   ANTHROPIC_API_KEY = "sk-ant-..."
   ```
5. Click **Deploy** — live in ~2 minutes ✅

---

## 📁 Project Structure

```
talentscout-ai/
├── app.py                    # Main Streamlit app (all-in-one)
├── requirements.txt          # Dependencies
├── README.md                 # This file
└── .streamlit/
    ├── config.toml           # Dark theme config
    └── secrets.toml          # API key (gitignored)
```

---

## 🎨 Sample Input / Output

**Input JD:**
```
We are looking for a Python Machine Learning Engineer with 2+ years of experience. 
You will build and deploy NLP models, create Flask APIs, and work with scikit-learn 
and TensorFlow. Strong Python fundamentals required. MLOps experience is a plus.
```

**Output (Rank #1):**
```
Name:           Rahul Sharma
Location:       Hyderabad
Experience:     3 years
Match Score:    88%
Interest Score: 90%
Final Score:    89.2%
Interest Label: Hot 🔥
Matched Skills: Python, Machine Learning, Flask, NLP
Missing Skills: TensorFlow
Reason:         Strong NLP + Flask background, experience aligns perfectly
Candidate Reply:"This role aligns really well with what I've been doing. 
                 Happy to jump on a call this week!"
```

---

## 🤖 Tech Stack

| Layer | Technology |
|---|---|
| AI Agent / LLM | Anthropic Claude Sonnet 4 |
| Frontend | Streamlit |
| Data | Pandas |
| Deployment | Streamlit Cloud |

---

## 👤 Author

Built for the **Deccan AI Hackathon 2025**

---

## 📄 License

MIT
