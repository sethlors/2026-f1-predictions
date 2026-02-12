"""Shared CSS styles for the F1 Predictions app."""

# Common CSS that's used across all pages
COMMON_STYLES = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; background: #0a0a0a !important; }

.page-header {
    background: linear-gradient(135deg, #e10600 0%, #8b0000 50%, #1e1e1e 100%);
    border-radius: 18px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    color: white;
    box-shadow: 0 12px 40px rgba(225, 6, 0, 0.35), 0 0 0 1px rgba(255,255,255,0.08) inset;
    position: relative;
    overflow: hidden;
}
.page-header::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -5%;
    width: 150px;
    height: 150px;
    background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 70%);
}
.page-header h1 { 
    font-size: 2.5rem; 
    font-weight: 900; 
    margin: 0; 
    letter-spacing: -1px;
    text-shadow: 0 2px 10px rgba(0,0,0,0.3);
    position: relative;
}
.page-header p { 
    opacity: 0.85; 
    margin: 0.4rem 0 0 0;
    font-size: 1.05rem;
    font-weight: 500;
    position: relative;
}

.team-badge {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 8px;
    font-size: 0.75rem;
    font-weight: 700;
    color: white;
    margin-left: 8px;
    vertical-align: middle;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3);
}

.pos-label {
    display: inline-block;
    width: 40px;
    text-align: center;
    font-weight: 800;
    font-size: 0.8rem;
    border-radius: 8px;
    padding: 3px 0;
    margin-right: 6px;
    color: white;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3);
}
.pos-gold   { background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%); color: #1e1e1e; box-shadow: 0 2px 12px rgba(255,215,0,0.5); }
.pos-silver { background: linear-gradient(135deg, #E8E8E8 0%, #C0C0C0 100%); color: #1e1e1e; box-shadow: 0 2px 12px rgba(192,192,192,0.5); }
.pos-bronze { background: linear-gradient(135deg, #CD7F32 0%, #8B4513 100%); color: white; box-shadow: 0 2px 12px rgba(205,127,50,0.4); }
.pos-points { background: linear-gradient(135deg, #2d6a4f 0%, #1b4332 100%); box-shadow: 0 2px 10px rgba(45,106,79,0.4); }
.pos-rest   { background: linear-gradient(135deg, #444 0%, #2a2a2a 100%); }

.user-col-header {
    font-weight: 800;
    font-size: 1.1rem;
    padding: 1rem 0 0.5rem 0;
    border-bottom: 3px solid #e10600;
    margin-bottom: 0.75rem;
    letter-spacing: -0.3px;
    background: linear-gradient(90deg, rgba(225,6,0,0.1) 0%, transparent 100%);
    padding-left: 0.5rem;
    border-radius: 4px 4px 0 0;
}

.trash-btn {
    display: flex;
    justify-content: flex-end;
    margin-top: -2.8rem;
    margin-bottom: 1.2rem;
    padding-right: 0.75rem;
}
.trash-btn button {
    background: transparent !important;
    border: none !important;
    color: #e10600 !important;
    font-size: 0.95rem !important;
    padding: 0.1rem 0.4rem !important;
    min-height: 0 !important;
    line-height: 1 !important;
    opacity: 0.35;
    transition: opacity 0.15s;
    cursor: pointer;
}
.trash-btn button:hover {
    opacity: 1;
    background: transparent !important;
}
</style>
"""

# Styles specific to season predictions page
SEASON_PREDICTIONS_STYLES = """
<style>
.championship-section {
    background: linear-gradient(135deg, #e10600 0%, #8b0000 50%, #1a1a1a 100%);
    border: 1px solid rgba(225, 6, 0, 0.4);
    border-radius: 18px;
    padding: 0;
    margin-bottom: 2rem;
    box-shadow: 0 8px 32px rgba(225, 6, 0, 0.25), 0 0 0 1px rgba(255,255,255,0.08) inset;
    position: relative;
    overflow: hidden;
}
.championship-section::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: repeating-linear-gradient(
        45deg,
        transparent,
        transparent 10px,
        rgba(255,255,255,0.02) 10px,
        rgba(255,255,255,0.02) 20px
    );
    pointer-events: none;
}
.championship-section h3 {
    margin: 0;
    padding: 1.75rem 2rem;
    font-weight: 900;
    font-size: 1.5rem;
    letter-spacing: -0.5px;
    color: white;
    text-shadow: 0 2px 12px rgba(0,0,0,0.4);
    position: relative;
    background: linear-gradient(135deg, rgba(225, 6, 0, 0.95) 0%, rgba(139, 0, 0, 0.85) 100%);
    border-bottom: 2px solid rgba(255, 255, 255, 0.1);
}
.championship-body {
    padding: 1.5rem 2rem 2rem 2rem;
    background: linear-gradient(135deg, #1a1a1a 0%, #0f0f0f 100%);
    position: relative;
}

.result-row {
    display: flex;
    align-items: center;
    padding: 6px 10px;
    border-radius: 8px;
    margin-bottom: 3px;
    font-size: 0.9rem;
    transition: background 0.2s;
    border: 1px solid transparent;
}
.result-row:nth-child(odd) { background: rgba(255,255,255,0.02); }
.result-row:hover { 
    background: rgba(225,6,0,0.08); 
    border-color: rgba(225,6,0,0.2);
}
.result-pos {
    width: 40px;
    font-weight: 800;
    flex-shrink: 0;
    margin-right: 1rem;
}
.result-driver { 
    flex: 1;
    font-weight: 600;
}
.result-team {
    font-size: 0.75rem;
    opacity: 0.6;
    padding-left: 10px;
    font-weight: 600;
}
</style>
"""

# Styles for prediction cards
PREDICTION_CARD_STYLES = """
<style>
.pred-grid {
    display: flex;
    gap: 1.5rem;
    flex-wrap: wrap;
}
.pred-card {
    flex: 1;
    min-width: 280px;
    background: linear-gradient(135deg, #1a1a1a 0%, #151515 100%);
    border: 1px solid #2a2a2a;
    border-radius: 16px;
    padding: 2rem 1.75rem;
    color: white;
    text-align: center;
    position: relative;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 20px rgba(0,0,0,0.4);
}
.pred-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, #e10600, #ff6347);
    border-radius: 16px 16px 0 0;
}
.pred-card:hover {
    transform: translateY(-3px);
    border-color: rgba(225, 6, 0, 0.3);
    box-shadow: 0 8px 30px rgba(225, 6, 0, 0.2);
}
.pred-card .user-name {
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    opacity: 0.5;
    font-weight: 700;
    margin-bottom: 1rem;
}
.pred-card .pick-label {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    opacity: 0.45;
    margin-top: 1.2rem;
    font-weight: 600;
}
.pred-card .pick-value {
    font-size: 1.2rem;
    font-weight: 800;
    color: #e10600;
    margin-top: 0.3rem;
    text-shadow: 0 2px 8px rgba(225, 6, 0, 0.3);
}

.form-card {
    background: linear-gradient(135deg, #1a1a1a 0%, #151515 100%);
    border: 1px solid rgba(225, 6, 0, 0.15);
    border-radius: 16px;
    padding: 2rem;
    color: white;
    margin-bottom: 2rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    transition: border-color 0.3s;
}
.form-card:hover {
    border-color: rgba(225, 6, 0, 0.3);
}
.form-card h3 { 
    margin: 0 0 0.4rem 0; 
    font-weight: 800;
    font-size: 1.2rem;
    letter-spacing: -0.3px;
}
.form-card .form-hint { 
    opacity: 0.6; 
    font-size: 0.9rem; 
    margin-bottom: 1.2rem;
    line-height: 1.5;
}
</style>
"""
