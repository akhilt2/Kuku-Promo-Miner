# 🎬 Kuku TV — Problem Statement 1: Find the Promos (Ads)
**Candidate:** Akhil T | **Roll No:** B230778EC | **Branch:** ECE | **College:** NIT Calicut  
**Show:** *I Married a Broken Soldier. He was a Duke* (50 Episodes)  
## Microdrama Screenplay Promo Miner & Performance Ranking Pipeline

This repository contains the complete production solution for **Problem 1: Find the Promos (Ads)** from the Kuku AI Generalist Assignment.

It automatically ingests raw microdrama screenplays, extracts high-CTR promo moments (20–60 seconds), scores them across dramaturgical retention markers (3-second hook, cliffhanger cut, standalone clarity, and pacing), and ranks them for immediate deployment on TikTok, Instagram Reels, and YouTube Shorts.

| | |
|---|---|
| 🌐 **Live App** | [https://kuku-promo-miner.streamlit.app/](https://kuku-promo-miner.streamlit.app/) |
| 💻 **GitHub Repo** | [https://github.com/akhilt2/Kuku-Promo-Miner](https://github.com/akhilt2/Kuku-Promo-Miner) |

---

### 📂 Repository Structure

- `promo_miner.py` — Core end-to-end Python engine that parses screenplays, runs the dynamic sliding window candidate miner, computes composite scores, deduplicates via temporal IoU suppression, and exports data.
- `app.py` — Interactive Streamlit web application to review, filter, and export mined promos.
- `generate_pdf_doc.py` — Script to generate the official 2-Page Solution PDF Report.
- `outputs/`
  - `promos_full_dataset.json` — Comprehensive output of all 96 mined promos across all 50 episodes.
  - `promos_ranking_summary.csv` — Tabular export containing timestamps, ranks, scores, hooks, cliffhangers, and rationales.
  - `top_10_launch_promos.json` — Immediate launch batch for marketing campaigns.
- `Kuku_Problem_1_Solution_Doc.pdf` — The official 2-Page Solution Document for submission.

---

### 🚀 Quickstart & Running Instructions

#### 1. Run the Pipeline on all 50 Episodes
```bash
python3 promo_miner.py
```
This processes all 50 episodes and updates the `outputs/` folder in ~4 seconds.

#### 2. Launch the Interactive Dashboard
```bash
streamlit run app.py
```
Open `http://localhost:8501` to view the interactive interface with card previews and CSV download capabilities.

---

### 📊 Top 3 Mined Promos Summary

1. **Rank #1 — Episode 36 (`02:36.50` - `03:20.75`, 44.25s) — Score: 9.90/10**
   - **Hook:** Profile shot of Alexander as dark realization settles over his face, turning to a grim, predatory glare.
   - **Cliffhanger:** `ALEXANDER: "...their dead Duke is coming home."`
   - **Why It Works:** Explosive high-stakes identity reveal paired with a thunderous declaration; instant curiosity engine for cold viewers.

2. **Rank #2 — Episode 15 (`00:46.50` - `01:26.00`, 39.50s) — Score: 9.76/10**
   - **Hook:** `JULIANA: "No."` (Defiant stand against thugs)
   - **Cliffhanger:** `THUG WITH CAP: "What? You want to fight us, veteran?"`
   - **Why It Works:** Immediate physical confrontation where a fragile heroine defies armed aggressors, cutting right before the first punch.

3. **Rank #3 — Episode 28 (`01:31.20` - `01:55.80`, 24.60s) — Score: 9.14/10**
   - **Hook:** Whispered high-society confrontation.
   - **Cliffhanger:** `JULIANA: "Do not speak about my husband!"`
   - **Why It Works:** Relatable emotional defense, high-speed pacing (24s) optimized for short vertical platforms.

---

### ⚙️ Scoring Heuristics
$$\text{Rank Score} = 0.35 \times \text{Hook} + 0.35 \times \text{Cliffhanger} + 0.20 \times \text{Standalone} + 0.10 \times \text{Pacing}$$
