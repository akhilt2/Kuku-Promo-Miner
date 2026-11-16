"""
promo_miner.py - Automated Promo & Ad Clip Miner for Microdrama Screenplays
Engineered for Kuku TV Microdrama Content Pipelines
"""

import os
import glob
import re
import json
import csv
from typing import List, Dict, Any, Tuple

# Microdrama Dramaturgical Keywords
HOOK_KEYWORDS = {
    # Physical confrontation & violence
    'slap': 4.0, 'strike': 3.5, 'grab': 3.0, 'choke': 4.0, 'draws sword': 4.5, 'blade': 3.5,
    'shove': 3.0, 'kneel': 3.5, 'drops to one knee': 4.5, 'seized': 3.0, 'blood': 3.5,
    # Extreme emotional dialogue & accusations
    'liar': 3.5, 'bastard': 3.5, 'whore': 4.0, 'mistress': 3.5, 'divorce': 4.5, 'marry': 3.5,
    'betray': 3.5, 'disown': 4.0, 'kill': 4.0, 'murder': 4.0, 'unworthy': 3.0, 'shame': 3.0,
    'scandal': 3.5, 'pregnant': 4.5, 'imposter': 4.0, 'traitor': 3.5, 'beg': 3.0,
    # Shock reactions & audio cues
    'gasps': 3.0, 'gasps in horror': 3.8, 'widens': 2.5, 'murmurs': 2.0, 'stuns': 3.5,
    'screams': 3.5, 'cries out': 3.0, 'thunder': 2.5, 'swell': 2.5
}

CLIFFHANGER_KEYWORDS = {
    # High stakes unanswered questions / ultimatums
    'who are you': 4.5, 'what have you done': 4.0, 'how dare you': 3.5, 'or else': 4.0,
    'never see him again': 4.0, 'your true identity': 4.5, 'duke': 4.0, 'is dead': 4.5,
    'my husband': 4.0, 'my wife': 4.0, 'the true heir': 4.5, 'you will pay': 4.0,
    # Audio/Visual cliffhanger triggers
    'cut to black': 4.5, 'swells to an ominous': 4.0, 'freeze': 3.5, 'cliffhanger': 4.5,
    'tight close-up': 3.0, 'extreme close-up': 3.5, 'dramatic crescendo': 4.0,
    'hardening into': 3.5, 'eyes flare': 3.5, 'stops in his tracks': 3.5, 'stands frozen': 3.5
}

def parse_time(t_str: str) -> float:
    """Converts mm:ss.ss or ss.ss into seconds."""
    parts = t_str.strip().split(':')
    if len(parts) == 2:
        return float(parts[0]) * 60 + float(parts[1])
    elif len(parts) == 3:
        return float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2])
    return float(parts[0])

def format_time(seconds: float) -> str:
    """Formats seconds into mm:ss.ss."""
    m = int(seconds // 60)
    s = seconds % 60
    return f"{m:02d}:{s:05.2f}"

class ScreenplayParser:
    """Parses microdrama script text files into structured scene beats."""
    
    @staticmethod
    def parse_file(filepath: str) -> Dict[str, Any]:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
            
        ep_match = re.search(r'EPISODE NUMBER:\s*(.*)', text)
        logline_match = re.search(r'EPISODE LOGLINE:\s*(.*)', text)
        ep_name = ep_match.group(1).strip() if ep_match else os.path.basename(filepath)
        logline = logline_match.group(1).strip() if logline_match else ""
        
        # Regex to match character dialogue / camera / action blocks
        block_pattern = re.compile(
            r'\*\*([^*]+)\:\*\*\s*\n\s*Start:\s*\(([0-9:.]+)\)\s*\|\s*End:\s*\(([0-9:.]+)\)\s*\n(.*?)(?=\n\*\*[^*]+\:\*\*|\n--- SCRIPT END ---|\Z)',
            re.DOTALL
        )
        
        beats = []
        for match in block_pattern.finditer(text):
            role_raw = match.group(1).strip()
            start_str = match.group(2).strip()
            end_str = match.group(3).strip()
            content = match.group(4).strip()
            
            start_sec = parse_time(start_str)
            end_sec = parse_time(end_str)
            
            # Classify element type
            if 'CAMERA' in role_raw:
                elem_type = 'CAMERA'
            elif 'ACTION' in role_raw:
                elem_type = 'ACTION'
            elif 'SOUND' in role_raw or 'MUSIC' in role_raw:
                elem_type = 'SOUND'
            else:
                elem_type = 'DIALOGUE'
                
            beats.append({
                'role': role_raw,
                'type': elem_type,
                'start_sec': start_sec,
                'end_sec': end_sec,
                'start_str': start_str,
                'end_str': end_str,
                'content': content
            })
            
        # Sort beats by start_sec
        beats.sort(key=lambda x: (x['start_sec'], x['end_sec']))
        
        # Total episode duration
        ep_duration = max([b['end_sec'] for b in beats]) if beats else 0.0
        
        return {
            'filepath': filepath,
            'episode': ep_name,
            'logline': logline,
            'duration': ep_duration,
            'beats': beats
        }

class PromoScorer:
    """Scores candidate video windows based on Hook, Cliffhanger, Standalone, and Pacing metrics."""
    
    @staticmethod
    def score_window(window_beats: List[Dict[str, Any]], ep_duration: float, window_start: float, window_end: float) -> Dict[str, Any]:
        duration = window_end - window_start
        if duration < 20.0 or duration > 60.0:
            return {'total_score': 0.0}
            
        # 1. Evaluate Hook (First 3.5 seconds of the clip)
        hook_window_end = window_start + 4.0
        hook_beats = [b for b in window_beats if b['start_sec'] <= hook_window_end]
        
        hook_score = 0.0
        hook_text = ""
        for b in hook_beats:
            text_lower = (b['role'] + " " + b['content']).lower()
            for kw, val in HOOK_KEYWORDS.items():
                if kw in text_lower:
                    hook_score += val
            if not hook_text:
                if b['type'] == 'DIALOGUE':
                    hook_text = f"{b['role']}: {b['content']}"
                else:
                    hook_text = f"[{b['role']}] {b['content']}"
                    
        # Bonus for opening right on dialogue or abrupt visual punch
        if hook_beats and hook_beats[0]['type'] == 'DIALOGUE':
            hook_score += 2.0
        # Normalize hook score (0 to 10 scale)
        norm_hook = min(10.0, max(1.0, hook_score * 1.2))
        
        # 2. Evaluate Cliffhanger (Last 4.0 seconds of the clip)
        cliff_window_start = window_end - 4.5
        cliff_beats = [b for b in window_beats if b['end_sec'] >= cliff_window_start]
        
        cliff_score = 0.0
        cliff_text = ""
        for b in cliff_beats:
            text_lower = (b['role'] + " " + b['content']).lower()
            for kw, val in CLIFFHANGER_KEYWORDS.items():
                if kw in text_lower:
                    cliff_score += val
            if b['type'] == 'DIALOGUE':
                cliff_text = f"{b['role']}: {b['content']}"
            elif not cliff_text:
                cliff_text = f"[{b['role']}] {b['content']}"
                
        # If it aligns with episode end / cliffhanger fade
        if window_end >= ep_duration - 1.5:
            cliff_score += 3.5
            
        norm_cliff = min(10.0, max(1.0, cliff_score * 1.2))
        
        # 3. Standalone Coherence & Dialogue Dynamics
        dialogues = [b for b in window_beats if b['type'] == 'DIALOGUE']
        char_set = set(d['role'].split('(')[0].strip() for d in dialogues)
        num_turns = len(dialogues)
        
        # Ideal promo has high tension dynamic exchange between 2 or 3 central characters
        standalone_score = 5.0
        if 2 <= len(char_set) <= 4:
            standalone_score += 2.5
        if num_turns >= 4:
            standalone_score += 2.0
        elif num_turns <= 1:
            standalone_score -= 2.0
            
        # Penalize if it starts mid-sentence without clear subject
        norm_standalone = min(10.0, max(1.0, standalone_score))
        
        # 4. Pacing & Length Penalty
        # Sweet spot for ReelShort/TikTok ads is 30 to 45 seconds
        if 28.0 <= duration <= 45.0:
            pacing_score = 10.0
        elif 22.0 <= duration < 28.0 or 45.0 < duration <= 52.0:
            pacing_score = 8.0
        else:
            pacing_score = 6.0
            
        # Composite Multi-factor Rank Score:
        # 35% Hook + 35% Cliffhanger + 20% Standalone Comprehension + 10% Pacing
        composite_score = (0.35 * norm_hook) + (0.35 * norm_cliff) + (0.20 * norm_standalone) + (0.10 * pacing_score)
        
        # Formulate rationale
        reasons = []
        if norm_hook >= 7.0:
            reasons.append("explosive hook in initial seconds")
        elif norm_hook >= 5.0:
            reasons.append("engaging opening tension")
        if norm_cliff >= 7.0:
            reasons.append("high-stakes unresolved cliffhanger")
        elif norm_cliff >= 5.0:
            reasons.append("dramatic dialogue cut")
        if len(char_set) >= 2:
            reasons.append(f"sharp conflict between {', '.join(list(char_set)[:2])}")
        why_works = f"Features {', '.join(reasons)}; perfectly timed ({duration:.1f}s) for vertical ad retention."
        
        return {
            'total_score': round(composite_score, 2),
            'hook_score': round(norm_hook, 2),
            'cliffhanger_score': round(norm_cliff, 2),
            'standalone_score': round(norm_standalone, 2),
            'pacing_score': round(pacing_score, 2),
            'duration': round(duration, 2),
            'hook_description': hook_text[:140] if hook_text else "High visual drama opening beat",
            'cliffhanger_description': cliff_text[:140] if cliff_text else "Dramatic unresolved tension cut",
            'why_it_works': why_works
        }

class MicrodramaPromoMiner:
    """Scans all episodes to discover, score, rank, and export candidate promos."""
    
    def __init__(self, script_dir: str):
        self.script_dir = script_dir
        self.episodes_data = []
        
    def load_and_parse(self):
        files = sorted(glob.glob(os.path.join(self.script_dir, '*.txt')))
        for f in files:
            ep_data = ScreenplayParser.parse_file(f)
            self.episodes_data.append(ep_data)
        print(f"Successfully loaded and parsed {len(self.episodes_data)} episodes.")
        
    def mine_single_episode_promos(self, ep_data: Dict[str, Any], top_n_per_ep: int = 2) -> List[Dict[str, Any]]:
        beats = ep_data['beats']
        ep_duration = ep_data['duration']
        candidates = []
        
        # Identify viable start points (dialogue or key actions)
        for i, start_beat in enumerate(beats):
            # Optimization: don't start in the last 20 seconds
            if start_beat['start_sec'] > ep_duration - 20.0:
                break
                
            w_start = start_beat['start_sec']
            
            # Find end beats where duration is between 22 and 58 seconds
            for j in range(i + 1, len(beats)):
                end_beat = beats[j]
                w_end = end_beat['end_sec']
                dur = w_end - w_start
                if dur < 22.0:
                    continue
                if dur > 58.0:
                    break
                    
                window_beats = beats[i:j+1]
                scored = PromoScorer.score_window(window_beats, ep_duration, w_start, w_end)
                if scored['total_score'] > 5.0:
                    candidates.append({
                        'episode': ep_data['episode'],
                        'logline': ep_data['logline'],
                        'segments': [{
                            'episode': ep_data['episode'],
                            'start': format_time(w_start),
                            'end': format_time(w_end),
                            'start_sec': round(w_start, 2),
                            'end_sec': round(w_end, 2),
                            'duration': round(dur, 2)
                        }],
                        'total_duration': round(dur, 2),
                        'hook': scored['hook_description'],
                        'cliffhanger': scored['cliffhanger_description'],
                        'why_it_works': scored['why_it_works'],
                        'scores': scored
                    })
                    
        # Sort and deduplicate overlapping candidates within the episode
        candidates.sort(key=lambda x: x['scores']['total_score'], reverse=True)
        deduped = []
        for cand in candidates:
            c_start = cand['segments'][0]['start_sec']
            c_end = cand['segments'][0]['end_sec']
            overlap = False
            for existing in deduped:
                e_start = existing['segments'][0]['start_sec']
                e_end = existing['segments'][0]['end_sec']
                # Check intersection over union / temporal overlap
                overlap_len = max(0, min(c_end, e_end) - max(c_start, e_start))
                if overlap_len > 12.0:  # Overlaps significantly
                    overlap = True
                    break
            if not overlap:
                deduped.append(cand)
            if len(deduped) >= top_n_per_ep:
                break
                
        return deduped

    def run_all(self) -> List[Dict[str, Any]]:
        if not self.episodes_data:
            self.load_and_parse()
            
        all_promos = []
        for ep in self.episodes_data:
            ep_promos = self.mine_single_episode_promos(ep, top_n_per_ep=2)
            all_promos.extend(ep_promos)
            
        # Sort across all 50 episodes by total score descending
        all_promos.sort(key=lambda x: x['scores']['total_score'], reverse=True)
        
        # Add Global Rank
        for rank, promo in enumerate(all_promos, 1):
            promo['rank'] = rank
            
        return all_promos

    def export_results(self, promos: List[Dict[str, Any]], out_dir: str):
        os.makedirs(out_dir, exist_ok=True)
        
        # 1. Export Full JSON
        json_path = os.path.join(out_dir, "promos_full_dataset.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(promos, f, indent=2)
            
        # 2. Export Clean CSV for Editors/Media Buyers
        csv_path = os.path.join(out_dir, "promos_ranking_summary.csv")
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                "Rank", "Episode", "Segment_Start", "Segment_End", "Duration_Sec",
                "Total_Score", "Hook_Score", "Cliffhanger_Score", "Standalone_Score",
                "Hook_Description", "Cliffhanger_Description", "Why_It_Works"
            ])
            for p in promos:
                seg = p['segments'][0]
                s = p['scores']
                writer.writerow([
                    p['rank'], p['episode'], seg['start'], seg['end'], p['total_duration'],
                    s['total_score'], s['hook_score'], s['cliffhanger_score'], s['standalone_score'],
                    p['hook'], p['cliffhanger'], p['why_it_works']
                ])
                
        # 3. Export Top 10 Marketing Launch Package (Ready for TikTok/Reels)
        top10_path = os.path.join(out_dir, "top_10_launch_promos.json")
        with open(top10_path, 'w', encoding='utf-8') as f:
            json.dump(promos[:10], f, indent=2)
            
        print(f"Exported {len(promos)} promos to {out_dir}")
        return json_path, csv_path, top10_path

if __name__ == '__main__':
    data_dir = 'I Married a Broken Soldier. He was a Duke-scripts (2) (1)/I Married a Broken Soldier. He was a Duke'
    miner = MicrodramaPromoMiner(data_dir)
    results = miner.run_all()
    miner.export_results(results, "kuku_promo_miner/outputs")
    print(f"Top 5 Promos:")
    for p in results[:5]:
        print(f"Rank {p['rank']}: {p['episode']} [{p['segments'][0]['start']} - {p['segments'][0]['end']}] Score: {p['scores']['total_score']}")
        print(f"   Hook: {p['hook']}")
        print(f"   Cliff: {p['cliffhanger']}")
        print(f"   Why: {p['why_it_works']}")
