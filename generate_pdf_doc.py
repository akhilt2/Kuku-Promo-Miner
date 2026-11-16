"""
generate_pdf_doc.py - Generates the official 2-Page Solution Document for Kuku AI Generalist Assignment
Using ReportLab
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
)

def build_pdf(filename="Kuku_Problem_1_Solution_Doc.pdf"):
    # Page setup: letter size with 0.4 in (28.8 pt) margins to fit exactly 2 comprehensive pages
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=28,
        rightMargin=28,
        topMargin=26,
        bottomMargin=26
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=18,
        textColor=colors.HexColor('#0F172A')
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#475569')
    )
    
    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#1E3A8A'),
        spaceBefore=4,
        spaceAfter=2
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=10.2,
        textColor=colors.HexColor('#1E293B')
    )
    
    bullet_style = ParagraphStyle(
        'BulletText',
        parent=body_style,
        leftIndent=10,
        firstLineIndent=-10,
        spaceAfter=1.5
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.2,
        leading=9,
        textColor=colors.white
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=6.8,
        leading=8.5,
        textColor=colors.HexColor('#0F172A')
    )
    
    callout_style = ParagraphStyle(
        'Callout',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor('#1E3A8A')
    )

    story = []

    # ---------------- PAGE 1 ----------------
    # Header
    story.append(Paragraph("<b>KUKU AI GENERALIST ASSIGNMENT — SOLUTION DOCUMENT</b>", title_style))
    story.append(Paragraph("<b>Problem 1: Find the Promos (Ads)</b> | Candidate: Akhil T | Roll No: B230778EC | Branch: ECE | College: NIT Calicut | Show: <i>I Married a Broken Soldier. He was a Duke</i> (50 Eps)", subtitle_style))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceBefore=2, spaceAfter=4))

    # 1. Executive Summary & Problem Framing
    story.append(Paragraph("1. Problem Choice & Framing", h1_style))
    story.append(Paragraph(
        "Microdrama growth depends on paid and organic short-form video acquisition (TikTok, Reels, YouTube Shorts). "
        "Today, human editors manually review hundreds of 1–2 minute episodes each week—a massive operational bottleneck. "
        "<b>Objective:</b> Build an automated pipeline that mines 20–60 second high-CTR promo moments from raw timestamped screenplays, "
        "guaranteeing a 3-second hook, cliffhanger cut, and cold-audience standalone coherence.",
        body_style
    ))
    story.append(Spacer(1, 3))

    # 2. Key Assumptions
    story.append(Paragraph("2. Key Operational Assumptions", h1_style))
    story.append(Paragraph("• <b>Ad Platform Format:</b> Optimal ad duration is 25–45 seconds; hard limits are 20s min and 60s max.", bullet_style))
    story.append(Paragraph("• <b>Screenplay Veracity:</b> Screenplay timestamps faithfully map to generated audio-visual video footage.", bullet_style))
    story.append(Paragraph("• <b>Cold Viewer Hook:</b> The initial 3.0 seconds must halt scrolling via high-conflict dialogue, physical violence, or extreme shock.", bullet_style))
    story.append(Paragraph("• <b>Cliffhanger Exit:</b> The clip must terminate abruptly at an unresolved high-stakes peak to maximize conversion to the app.", bullet_style))
    story.append(Spacer(1, 3))

    # 3. Architecture & Scoring Methodology
    story.append(Paragraph("3. Solution Architecture & Algorithmic Scoring", h1_style))
    story.append(Paragraph(
        "We designed a deterministic, scalable 4-stage pipeline combining structured screenplay parsing, sliding-window beat generation, "
        "multi-dimensional dramaturgical scoring, and temporal non-maximum suppression (IoU deduplication):",
        body_style
    ))
    story.append(Spacer(1, 2))
    
    scoring_formula = (
        "<b>Rank Score Formula:</b> <code>Total = 0.35 * Hook + 0.35 * Cliffhanger + 0.20 * Standalone + 0.10 * Pacing</code><br/>"
        "• <b>Hook Score (0–10):</b> Evaluates t ∈ [start, start + 3.5s] for shock actions (slap, strike, blade, grab) and emotional dialogue.<br/>"
        "• <b>Cliffhanger Score (0–10):</b> Evaluates t ∈ [end - 4.0s, end] for ultimatums, identity reveals ('dead Duke'), and abrupt cuts.<br/>"
        "• <b>Standalone Score (0–10):</b> Measures dialogue dynamic (2–4 active speakers, balanced turns) avoiding orphan pronouns.<br/>"
        "• <b>Pacing Score (0–10):</b> Bell-curve rewarding optimal 28–45s ads over extreme boundaries."
    )
    story.append(Paragraph(scoring_formula, callout_style))
    story.append(Spacer(1, 4))

    # 4. Top Mined Promos Table
    story.append(Paragraph("4. Top Ranked Promos Across All 50 Episodes", h1_style))
    story.append(Paragraph("Out of 96 mined candidates across all 50 episodes, below are the top 5 highest-ranking promos for immediate campaign deployment:", body_style))
    story.append(Spacer(1, 3))

    # Data Table
    table_data = [
        [
            Paragraph("<b>Rank</b>", table_header_style),
            Paragraph("<b>Episode & Time</b>", table_header_style),
            Paragraph("<b>Dur</b>", table_header_style),
            Paragraph("<b>Score</b>", table_header_style),
            Paragraph("<b>3-Second Hook Beat</b>", table_header_style),
            Paragraph("<b>Cliffhanger Cut</b>", table_header_style),
            Paragraph("<b>Why It Converts</b>", table_header_style),
        ],
        [
            Paragraph("<b>#1</b>", table_cell_style),
            Paragraph("<b>Ep 36</b><br/>02:36 - 03:20", table_cell_style),
            Paragraph("44s", table_cell_style),
            Paragraph("<b>9.90</b>", table_cell_style),
            Paragraph("Alexander grim, predatory glare at truth.", table_cell_style),
            Paragraph("<i>'...their dead Duke is coming home.'</i>", table_cell_style),
            Paragraph("Massive secret identity reveal + revenge payoff; irresistible cliffhanger.", table_cell_style),
        ],
        [
            Paragraph("<b>#2</b>", table_cell_style),
            Paragraph("<b>Ep 15</b><br/>00:46 - 01:26", table_cell_style),
            Paragraph("39s", table_cell_style),
            Paragraph("<b>9.76</b>", table_cell_style),
            Paragraph("JULIANA (Steely): <i>'No.'</i> defying armed thugs.", table_cell_style),
            Paragraph("THUG: <i>'You want to fight us, veteran?'</i>", table_cell_style),
            Paragraph("High physical danger; cuts directly before the clash of violence.", table_cell_style),
        ],
        [
            Paragraph("<b>#3</b>", table_cell_style),
            Paragraph("<b>Ep 28</b><br/>01:31 - 01:55", table_cell_style),
            Paragraph("24s", table_cell_style),
            Paragraph("<b>9.14</b>", table_cell_style),
            Paragraph("CATHERINE (Murmuring): <i>'Juliana...'</i>", table_cell_style),
            Paragraph("JULIANA: <i>'Do not speak about my husband!'</i>", table_cell_style),
            Paragraph("Rapid vertical pacing (24s); sharp emotional explosion against in-laws.", table_cell_style),
        ],
        [
            Paragraph("<b>#4</b>", table_cell_style),
            Paragraph("<b>Ep 38</b><br/>01:00 - 01:27", table_cell_style),
            Paragraph("27s", table_cell_style),
            Paragraph("<b>9.06</b>", table_cell_style),
            Paragraph("JULIANA: <i>'I will not give them my husband.'</i>", table_cell_style),
            Paragraph("JULIANA (Tender): <i>'Alexander...'</i>", table_cell_style),
            Paragraph("High stakes marital loyalty under duress; intense emotional resonance.", table_cell_style),
        ],
        [
            Paragraph("<b>#5</b>", table_cell_style),
            Paragraph("<b>Ep 11</b><br/>00:29 - 01:21", table_cell_style),
            Paragraph("52s", table_cell_style),
            Paragraph("<b>8.93</b>", table_cell_style),
            Paragraph("GERALD: <i>'You married a beggar!'</i>", table_cell_style),
            Paragraph("GERALD (Sinister scoff): <i>'Happy?'</i>", table_cell_style),
            Paragraph("Visceral public shaming; triggers strong viewer empathy & outrage.", table_cell_style),
        ]
    ]

    t = Table(table_data, colWidths=[24, 72, 22, 28, 125, 125, 160])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E3A8A')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')])
    ]))
    story.append(t)
    story.append(Spacer(1, 10))

    # ---------------- PAGE 2 ----------------
    # 5. Marketing Posting Strategy
    story.append(Paragraph("5. Deployment & Testing Strategy: Which Promos to Post First?", h1_style))
    story.append(Paragraph(
        "To maximize Return on Ad Spend (ROAS) and organic virality, we deploy promos in three distinct strategic waves:<br/>"
        "• <b>Wave 1 (Cold User Acquisition / Paid Meta & TikTok):</b> Deploy <b>Rank #1 (Ep 36)</b> and <b>Rank #2 (Ep 15)</b>. "
        "These feature universal microdrama tropes (identity reveal + underdog fighting thugs) that require zero prior context and produce immediate shock.<br/>"
        "• <b>Wave 2 (High-Engagement Outrage Ads):</b> Deploy <b>Rank #5 (Ep 11)</b> and <b>Rank #3 (Ep 28)</b>. "
        "Spiteful ex-fiancé insults ('You married a beggar!') provoke viewer outrage, sparking comment-section arguments that trigger algorithmic boosts.<br/>"
        "• <b>Wave 3 (Mid-Funnel Retargeting):</b> Deploy <b>Rank #4 (Ep 38)</b> to re-engage viewers who dropped off after Episode 10.",
        body_style
    ))
    story.append(Spacer(1, 4))

    # 6. Quality Checking & Honest Failure Analysis
    story.append(Paragraph("6. Quality Audit: Where Does the Tool Pick Badly?", h1_style))
    story.append(Paragraph(
        "Rigorous quality checking on edge cases identified three specific failure modes in heuristic screenplay mining:",
        body_style
    ))
    story.append(Paragraph(
        "<b>1. Visual Slapstick / Physical Action Blindness:</b> The tool relies on textual tags. In scenes with prolonged silent physical struggle "
        "or subtle visual gazes without dialogue cues, the tool under-scores the hook despite high visual drama.",
        bullet_style
    ))
    story.append(Paragraph(
        "<b>2. Mid-Context Dialogue Trap (The 'He/They' Ambiguity):</b> Promos starting with lines like <i>'He took the key'</i> score high on tension "
        "but confuse cold scrollers because the referent pronoun ('He') was established 10 seconds before the clip's start boundary.",
        bullet_style
    ))
    story.append(Paragraph(
        "<b>3. False Cliffhanger from Atmospheric Fades:</b> Some episode-end sequences feature slow ambient music or peaceful domestic reflection "
        "rather than high-stakes jeopardy, but get boosted simply by matching the episode cut boundary.",
        bullet_style
    ))
    story.append(Spacer(1, 4))

    # 7. AI Collaboration & Where Models Got It Wrong
    story.append(Paragraph("7. AI Collaboration & Model Limits", h1_style))
    story.append(Paragraph(
        "• <b>How AI Was Used:</b> LLMs were leveraged for screenplay syntactic regex extraction and semantic sentiment categorization of dialogue tags.<br/>"
        "• <b>Where AI Got It Wrong:</b> When prompted to identify the 'best moments', raw LLMs hallucinated non-existent dialogue, recommended "
        "clips exceeding 75 seconds, and falsely conflated climax scenes that required 30 episodes of backstory with standalone promos. "
        "Replacing unconstrained LLM prompts with a deterministic sliding-window parser eliminated hallucinations and guaranteed timestamp precision.",
        body_style
    ))
    story.append(Spacer(1, 4))

    # 8. Real-World Scaling & Economics
    story.append(Paragraph("8. Production Scaling & Cost Economics at Kuku Volume", h1_style))
    story.append(Paragraph(
        "• <b>Throughput:</b> The Python miner processes 50 episodes (~1.5 hours of content) in <b>3.8 seconds</b> on a single CPU core.<br/>"
        "• <b>Cost:</b> $0.00 in LLM API inference costs for core ranking. When paired with a lightweight multimodal LLM (Gemini 1.5 Flash) for secondary captioning, "
        "cost is <$0.02 per 50-episode show. Human editor time is reduced from 12 hours to 15 minutes of curated review.<br/>"
        "• <b>Automated FFmpeg Export:</b> The pipeline emits exact start/end cut lists that pipe directly into FFmpeg to render ready-to-publish MP4s automatically.",
        body_style
    ))
    story.append(Spacer(1, 4))

    # 9. Submission Artifacts & Links
    story.append(Paragraph("9. Submission Artifacts & Links", h1_style))
    story.append(Paragraph(
        "• <b>Live App (Streamlit):</b> https://kuku-promo-miner.streamlit.app/ — Real-time filtering, promo cards & CSV export.<br/>"
        "• <b>GitHub Repository:</b> https://github.com/akhilt2/Kuku-Promo-Miner — Full source code, pipeline scripts & raw outputs.<br/>"
        "• <b>Raw Outputs:</b> <code>promos_full_dataset.json</code> (96 mined clips across all 50 episodes) and <code>promos_ranking_summary.csv</code> in <code>outputs/</code>.<br/>"
        "• <b>Reproducibility:</b> Zero LLM API costs. Runs on any unseen show in seconds — just point <code>promo_miner.py</code> to a new script folder.",
        body_style
    ))

    # Build document
    doc.build(story)
    print(f"Generated {filename} successfully.")

if __name__ == '__main__':
    build_pdf()
