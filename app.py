import streamlit as st
import time
import json
import pandas as pd
import numpy as np
import random

# ==========================================
# 🧠 BACKEND LOGIC (The "Brain" from before)
# ==========================================

class AIParser:
    def parse_instruction(self, text):
        time.sleep(1) # Simulate AI thinking
        text = text.lower()
        parsed = {}
        
        # Simple Rule-Based Extraction for Demo
        if "onion" in text: parsed['ingredient'] = "onion"
        else: parsed['ingredient'] = "generic_vegetable"
        
        if "saute" in text: parsed['action'] = "saute"
        elif "boil" in text: parsed['action'] = "boil"
        else: parsed['action'] = "cook"
            
        if "high" in text: parsed['heat_level'] = "high"
        elif "low" in text: parsed['heat_level'] = "low"
        else: parsed['heat_level'] = "medium"
        
        return parsed

class QuantizationEngine:
    def normalize(self, raw_data):
        heat_map = {"low": 120, "medium": 160, "high": 210}
        
        return {
            "step_id": str(int(time.time())),
            "ingredient": raw_data.get('ingredient'),
            "action": raw_data.get('action'),
            "parameters": {
                "temperature_celsius": heat_map.get(raw_data.get('heat_level'), 160),
                "duration_seconds": 240 if raw_data.get('action') == "saute" else 600,
                "stir_rpm": 40 if raw_data.get('action') == "saute" else 0
            }
        }

class FeedbackOptimizer:
    def optimize(self, schema, score, notes):
        new_schema = schema.copy()
        new_schema['parameters'] = schema['parameters'].copy() # Deep copy
        
        # Logic: If burnt, lower heat. If raw, raise heat.
        if score < 7:
            if "burnt" in notes.lower():
                new_schema['parameters']['temperature_celsius'] -= 15
                new_schema['parameters']['duration_seconds'] -= 30
                action = "📉 Reduced Temp & Time (Burnt detected)"
            elif "raw" in notes.lower():
                new_schema['parameters']['temperature_celsius'] += 10
                new_schema['parameters']['duration_seconds'] += 45
                action = "📈 Increased Energy (Undercooked)"
            else:
                action = "⚠️ Score low, but reason unclear. Small adjustment made."
                new_schema['parameters']['duration_seconds'] += 10
        else:
            action = "✅ Recipe is stable. No major changes."
            
        return new_schema, action

# ==========================================
# 🎨 FRONTEND INTERFACE (Streamlit)
# ==========================================

st.set_page_config(page_title="Posha Robotic Chef", page_icon="🤖", layout="wide")

# --- SIDEBAR ---
st.sidebar.title("🤖 System Status")
st.sidebar.success("Core Engine: ONLINE")
st.sidebar.info("Safety Protocols: ACTIVE")
st.sidebar.markdown("---")
st.sidebar.markdown("**Hardware Simulation:**")
st.sidebar.markdown("Checking Sensors... OK ✅")
st.sidebar.markdown("Checking Motors... OK ✅")

# --- MAIN TITLE ---
st.title("🍳 AI-Powered Robotic Recipe Engine")
st.markdown("> *Transforming human cooking instructions into deterministic robotic code.*")
st.markdown("---")

# --- SESSION STATE INITIALIZATION ---
if 'sop' not in st.session_state:
    st.session_state['sop'] = None
if 'history' not in st.session_state:
    st.session_state['history'] = []

# ==========================
# SECTION 1: INGESTION
# ==========================
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1️⃣ Human Recipe Input")
    recipe_input = st.text_area(
        "Enter natural language instructions:", 
        "Heat pan on medium heat, saute onions until golden brown",
        height=150
    )
    
    if st.button("🚀 Generate Robotic SOP", type="primary"):
        with st.spinner("🧠 AI Parsing & Quantizing..."):
            # Call Backend
            parser = AIParser()
            quantizer = QuantizationEngine()
            
            raw_data = parser.parse_instruction(recipe_input)
            sop = quantizer.normalize(raw_data)
            
            st.session_state['sop'] = sop
            st.success("SOP Generated Successfully!")

# ==========================
# SECTION 2: VISUALIZATION
# ==========================
with col2:
    st.subheader("2️⃣ Robot Execution Data")
    
    if st.session_state['sop']:
        sop = st.session_state['sop']
        
        # Display Metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("Target Temp", f"{sop['parameters']['temperature_celsius']}°C")
        m2.metric("Duration", f"{sop['parameters']['duration_seconds']}s")
        m3.metric("Stir Speed", f"{sop['parameters']['stir_rpm']} RPM")
        
        # Display JSON
        st.markdown("**Structured Command Payload:**")
        st.json(sop)
        
    else:
        st.info("Awaiting Input...")

# ==========================
# SECTION 3: SIMULATION GRAPH
# ==========================
if st.session_state['sop']:
    st.markdown("---")
    st.subheader("3️⃣ Thermal Simulation (Digital Twin)")
    
    # Generate fake curve data for visualization
    duration = st.session_state['sop']['parameters']['duration_seconds']
    target_temp = st.session_state['sop']['parameters']['temperature_celsius']
    
    chart_data = pd.DataFrame(
        np.random.randn(duration) * 2 + target_temp, # Add noise to target temp
        columns=['Pan Temperature (°C)']
    )
    
    st.line_chart(chart_data)
    st.caption(f"Simulated real-time sensor feedback over {duration} seconds.")

    # ==========================
    # SECTION 4: OPTIMIZATION LOOP
    # ==========================
    st.markdown("---")
    st.subheader("4️⃣ RL Feedback Loop (Reinforcement Learning)")
    
    c1, c2 = st.columns([1, 2])
    
    with c1:
        st.markdown("**Human Sensory Feedback**")
        score = st.slider("Taste Score (1-10)", 1, 10, 6)
        notes = st.text_input("Tasting Notes", "Edges slightly burnt")
        
        if st.button("🔄 Run Optimization Cycle"):
            optimizer = FeedbackOptimizer()
            new_sop, action_log = optimizer.optimize(st.session_state['sop'], score, notes)
            
            st.session_state['optimized_sop'] = new_sop
            st.session_state['opt_action'] = action_log

    with c2:
        if 'optimized_sop' in st.session_state:
            st.markdown(f"**Optimization Action:** `{st.session_state['opt_action']}`")
            
            # Compare Old vs New
            col_old, col_new = st.columns(2)
            with col_old:
                st.markdown("🔴 **Original Params**")
                st.write(st.session_state['sop']['parameters'])
            with col_new:
                st.markdown("🟢 **Optimized Params**")
                st.write(st.session_state['optimized_sop']['parameters'])
            
            st.success("New SOP deployed to robotic memory bank.")

