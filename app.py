"""
Kuku Microdrama Promo Miner - Interactive Dashboard
Streamlit Web App to Explore, Filter, and Export Top Ads/Promos
"""

import streamlit as st
import json
import pandas as pd
import os

st.set_page_config(
    page_title="Kuku AI Promo Miner | Microdrama Ad Intelligence",
    page_icon="🎬",
    layout="wide"
)

# Load data
@st.cache_data
def load_data():
    json_path = os.path.join(os.path.dirname(__file__), "outputs", "promos_full_dataset.json")
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

promos = load_data()

# Header
st.title("🎬 Kuku AI Microdrama Promo Miner")
st.markdown("""
**Automated High-CTR Ad Discovery Pipeline** for short vertical microdramas (TikTok, Reels, Shorts).
Extracts, scores, and ranks 20–60 second clips using multi-modal screenplay dramaturgical heuristics.
""")

# Top metrics banner
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Episodes Analyzed", "50 Episodes")
with col2:
    st.metric("Total Promos Mined", f"{len(promos)} Promos")
with col3:
    st.metric("Avg Promo Duration", f"{sum(p['total_duration'] for p in promos)/len(promos):.1f} sec")
with col4:
    st.metric("Top Ranked Score", f"{promos[0]['scores']['total_score']} / 10.0")

st.markdown("---")

# Sidebar filters
st.sidebar.header("🔍 Filter & Campaign Controls")
min_score = st.sidebar.slider("Minimum Composite Score", 5.0, 10.0, 7.5, 0.1)
duration_range = st.sidebar.slider("Clip Duration Range (seconds)", 20, 60, (24, 50))
episodes_available = sorted(list(set(p['episode'] for p in promos)), key=lambda x: int(x.replace('Episode ', '')) if x.replace('Episode ', '').isdigit() else 999)
selected_ep = st.sidebar.selectbox("Filter by Specific Episode", ["All Episodes"] + episodes_available)

# Filtered list
filtered = [
    p for p in promos
    if p['scores']['total_score'] >= min_score
    and duration_range[0] <= p['total_duration'] <= duration_range[1]
    and (selected_ep == "All Episodes" or p['episode'] == selected_ep)
]

st.subheader(f"🎯 Mined Candidate Promos ({len(filtered)} matches)")

# Tabs for viewing
tab_cards, tab_table, tab_methodology = st.tabs(["🎴 Promo Cards (Production Ready)", "📊 Data Table & CSV Export", "⚙️ Scoring Methodology"])

with tab_cards:
    for p in filtered[:15]:
        seg = p['segments'][0]
        s = p['scores']
        with st.expander(f"⭐ **Rank #{p['rank']}** — {p['episode']} | Time: `{seg['start']}` to `{seg['end']}` ({p['total_duration']}s) | Overall Score: **{s['total_score']} / 10**", expanded=(p['rank'] <= 3)):
            c1, c2 = st.columns([1, 1])
            with c1:
                st.markdown("#### 🎣 3-Second Hook")
                st.info(f"**Opening:** {p['hook']}")
                st.markdown(f"**Hook Score:** `{s['hook_score']}/10`")
                
                st.markdown("#### ⏳ Cliffhanger Cut")
                st.warning(f"**Ending:** {p['cliffhanger']}")
                st.markdown(f"**Cliffhanger Score:** `{s['cliffhanger_score']}/10`")
            with c2:
                st.markdown("#### 📈 Performance Rationale")
                st.write(p['why_it_works'])
                
                st.markdown("#### 📊 Metric Breakdown")
                st.progress(s['hook_score'] / 10, text=f"Hook Strength: {s['hook_score']}/10")
                st.progress(s['cliffhanger_score'] / 10, text=f"Cliffhanger Impact: {s['cliffhanger_score']}/10")
                st.progress(s['standalone_score'] / 10, text=f"Standalone Clarity: {s['standalone_score']}/10")
                st.progress(s['pacing_score'] / 10, text=f"Pacing Fit: {s['pacing_score']}/10")

with tab_table:
    table_rows = []
    for p in filtered:
        seg = p['segments'][0]
        s = p['scores']
        table_rows.append({
            "Rank": p['rank'],
            "Episode": p['episode'],
            "Start": seg['start'],
            "End": seg['end'],
            "Duration (s)": p['total_duration'],
            "Score": s['total_score'],
            "Hook": p['hook'],
            "Cliffhanger": p['cliffhanger'],
            "Why It Works": p['why_it_works']
        })
    df = pd.DataFrame(table_rows)
    st.dataframe(df, use_container_width=True)
    
    csv_bytes = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        "📥 Download Filtered Promos (CSV)",
        data=csv_bytes,
        file_name="kuku_top_promos.csv",
        mime="text/csv"
    )

with tab_methodology:
    st.markdown("""
    ### 🔬 System Architecture & Heuristics
    1. **Screenplay Beat Tokenizer:** Ingests raw timestamped screenplay format with dialogue and action cues.
    2. **Sliding Window Generator:** Evaluates every viable 20–60 second window aligned to natural dialogue and action boundary markers.
    3. **Multi-Factor Scoring Formula:**
       $$\\text{Rank Score} = 0.35 \\times \\text{Hook} + 0.35 \\times \\text{Cliffhanger} + 0.20 \\times \\text{Standalone} + 0.10 \\times \\text{Pacing}$$
    4. **Deduplication:** Uses Temporal Intersection-over-Union (IoU) window suppression to avoid redundant clips from the same scene.
    5. **Edge Cases & Failure Modes:** Handled through semantic role tracking, monologue guards, and dialogue coherence filters.
    """)
