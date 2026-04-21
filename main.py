import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import cache_algorithms as cache
import disk_algorithms as disk
import io

# Page Config
st.set_page_config(page_title="OS Simulator", layout="wide", page_icon="💻")

st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background-color: #ffffff;
        color: #1f2937;
    }
    
    /* Header Container */
    .stHeader {
        background: #f8fafc;
        border-bottom: 2px solid #e2e8f0;
        padding: 2rem;
        margin-bottom: 2rem;
    }

    /* Modern Title */
    h1 {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #1e3a8a;
        font-weight: 700;
        text-align: center;
        letter-spacing: -0.025em;
    }
    
    h2, h3 {
        color: #1e40af;
    }

    /* Attractive Buttons (Standard and Download) */
    .stButton>button, .stDownloadButton>button {
        width: 100%;
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white !important;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 0.5rem;
        font-weight: 600;
        transition: all 0.2s ease;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        text-align: center;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    .stButton>button:hover, .stDownloadButton>button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        transform: translateY(-1px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        color: white !important;
    }

    /* Card-like containers for inputs */
    [data-testid="stVerticalBlock"] > div:has(div.stNumberInput) {
        background: #f1f5f9;
        padding: 1.5rem;
        border-radius: 0.75rem;
        border: 1px solid #e2e8f0;
    }

    /* Metric Styling */
    [data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    [data-testid="stMetricValue"] {
        color: #2563eb !important;
        font-weight: 800;
    }

    /* Ensure all text/markdown is dark for readability */
    div[data-testid="stMarkdownContainer"] p, 
    div[data-testid="stWidgetLabel"] p, 
    label, 
    .stSelectbox label, 
    .stRadio label {
        color: #111827 !important;
        font-weight: 500;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #f8fafc;
        border-radius: 0.5rem;
        padding: 0.5rem;
    }

    .stTabs [data-baseweb="tab"] {
        color: #64748b;
    }

    .stTabs [aria-selected="true"] {
        color: #2563eb !important;
        background-color: white !important;
        border-radius: 0.25rem;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }

    /* Table Customization */
    .stTable {
        border-radius: 0.5rem;
        border: 1px solid #e2e8f0;
    }
    
    /* Force table text to be dark */
    .stTable td, .stTable th {
        color: #1f2937 !important;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

st.title(" OS Simulator")
st.markdown("<p style='text-align: center; color: #64748b; font-size: 1.1rem; margin-bottom: 2rem;'>Visualize Memory and Disk Algorithms in a clean, professional environment.</p>", unsafe_allow_html=True)


tab1, tab2, tab3 = st.tabs(["🧠 Cache Replacement", "💿 Disk Scheduling", "📊 Comparison"])

# --- CACHE REPLACEMENT TAB ---
with tab1:
    st.header("Cache Memory Simulation")
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader("Configuration")
        page_input = st.text_input("Page Reference String (comma separated)", "7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2")
        frame_size = st.number_input("Number of Frames", min_value=1, max_value=10, value=3)
        cache_algo = st.selectbox("Select Algorithm", ["FIFO", "LRU", "Optimal"])
        
        run_cache = st.button("Run Cache Simulation", key="run_cache")
        reset_cache = st.button("Reset", key="reset_cache")

    if run_cache:
        try:
            pages = [int(p.strip()) for p in page_input.split(",")]
            
            if cache_algo == "FIFO":
                history, hits, faults = cache.fifo(pages, frame_size)
            elif cache_algo == "LRU":
                history, hits, faults = cache.lru(pages, frame_size)
            else:
                history, hits, faults = cache.optimal(pages, frame_size)
            
            with col2:
                st.subheader(f"Results: {cache_algo}")
                
                # Metrics
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Hits", hits)
                m2.metric("Faults", faults)
                m3.metric("Hit Ratio", f"{(hits/len(pages)):.2f}")
                m4.metric("Miss Ratio", f"{(faults/len(pages)):.2f}")
                
                # Visualization Table
                st.write("### Step-by-Step Execution")
                df_data = []
                for step in history:
                    row = {"Page": step["Page"]}
                    for i in range(frame_size):
                        row[f"Frame {i+1}"] = step["Frames"][i] if i < len(step["Frames"]) else "-"
                    
                    # Add Emoji for status visibility
                    if step["Status"] == "Hit":
                        row["Status"] = "✅ Hit"
                    else:
                        row["Status"] = "❌ Miss"
                        
                    df_data.append(row)
                
                df = pd.DataFrame(df_data)
                st.table(df)
                
                # Download
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button("Export Results to CSV", csv, "cache_results.csv", "text/csv")
                
        except ValueError:
            st.error("Invalid Input! Please enter numbers separated by commas.")

# --- DISK SCHEDULING TAB ---
with tab2:
    st.header("Disk Scheduling Simulation")
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader("Configuration")
        disk_input = st.text_input("Request Queue (comma separated)", "98, 183, 37, 122, 14, 124, 65, 67")
        initial_head = st.number_input("Initial Head Position", value=53)
        disk_algo = st.selectbox("Select Algorithm", ["FCFS", "SSTF", "SCAN", "C-SCAN"])
        
        max_track = 199
        if disk_algo in ["SCAN", "C-SCAN"]:
            direction = st.radio("Direction", ["right", "left"])
            max_track = st.number_input("Max Track Size", value=199)
        
        run_disk = st.button("Run Disk Simulation", key="run_disk")
        reset_disk = st.button("Reset", key="reset_disk")

    if run_disk:
        try:
            requests = [int(r.strip()) for r in disk_input.split(",")]
            
            if disk_algo == "FCFS":
                sequence, distance = disk.fcfs(requests, initial_head)
            elif disk_algo == "SSTF":
                sequence, distance = disk.sstf(requests, initial_head)
            elif disk_algo == "SCAN":
                sequence, distance = disk.scan(requests, initial_head, direction, max_track)
            else:
                sequence, distance = disk.cscan(requests, initial_head, direction, max_track)
            
            with col2:
                st.subheader(f"Results: {disk_algo}")
                st.success(f"Total Head Movement: {distance}")
                st.write(f"**Sequence of Head Movements:** {' -> '.join(map(str, sequence))}")
                
                # Plot
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=sequence, 
                    y=list(range(len(sequence))),
                    mode='lines+markers+text',
                    text=sequence,
                    textposition="top center",
                    textfont=dict(color='#111827', size=12, family="Segoe UI Semibold"),
                    line=dict(color='#2563eb', width=3, shape='spline'),
                    marker=dict(size=12, color='#1d4ed8', symbol='circle', line=dict(width=1, color='#ffffff'))
                ))
                
                fig.update_layout(
                    title=dict(text="Disk Head Movement Path", font=dict(color='#111827', size=18)),
                    xaxis_title=dict(text="Track Number", font=dict(color='#111827')),
                    yaxis_title=dict(text="Movement Step", font=dict(color='#111827')),
                    template="plotly_white",
                    paper_bgcolor='#ffffff',
                    plot_bgcolor='#f8fafc',
                    yaxis=dict(autorange="reversed", showgrid=True, gridcolor='#e2e8f0', tickfont=dict(color='#111827')),
                    xaxis=dict(showgrid=True, gridcolor='#e2e8f0', tickfont=dict(color='#111827')),
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Export
                df_disk = pd.DataFrame({"Step": range(len(sequence)), "Track": sequence})
                csv_disk = df_disk.to_csv(index=False).encode('utf-8')
                st.download_button("Export Path to CSV", csv_disk, "disk_results.csv", "text/csv")
                
        except ValueError:
            st.error("Invalid Input! Please enter numbers separated by commas.")

# --- COMPARISON TAB ---
with tab3:
    st.header("Algorithm Comparison")
    
    comp_type = st.radio("Compare:", ["Cache Algorithms", "Disk Scheduling Algorithms"])
    
    if comp_type == "Cache Algorithms":
        c_input = st.text_input("Page String", "7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2", key="c_comp")
        c_frames = st.number_input("Frames", value=3, key="f_comp")
        
        if st.button("Compare Cache"):
            pages = [int(p.strip()) for p in c_input.split(",")]
            results = {
                "FIFO": cache.fifo(pages, c_frames)[2],
                "LRU": cache.lru(pages, c_frames)[2],
                "Optimal": cache.optimal(pages, c_frames)[2]
            }
            
            # Even more vibrant colors for each algorithm
            colors = ['#10b981', '#f59e0b', '#dc2626'] # Emerald, Amber, Red
            fig = go.Figure([go.Bar(
                x=list(results.keys()), 
                y=list(results.values()), 
                marker_color=colors,
                text=list(results.values()),
                textposition='auto',
                textfont=dict(color='white', size=14, family="Segoe UI Bold"),
            )])
            fig.update_layout(
                title=dict(text="Page Faults: Lower is Better", font=dict(color='#111827', size=18)),
                yaxis_title=dict(text="Number of Faults", font=dict(color='#111827')),
                template="plotly_white",
                paper_bgcolor='#ffffff',
                plot_bgcolor='#ffffff',
                xaxis=dict(tickfont=dict(color='#111827', size=14)),
                yaxis=dict(tickfont=dict(color='#111827')),
            )
            st.plotly_chart(fig)

    else:
        d_input = st.text_input("Request Queue", "98, 183, 37, 122, 14, 124, 65, 67", key="d_comp")
        d_head = st.number_input("Initial Head", value=53, key="h_comp")
        
        if st.button("Compare Disk"):
            reqs = [int(r.strip()) for r in d_input.split(",")]
            results = {
                "FCFS": disk.fcfs(reqs, d_head)[1],
                "SSTF": disk.sstf(reqs, d_head)[1],
                "SCAN": disk.scan(reqs, d_head, "right")[1],
                "C-SCAN": disk.cscan(reqs, d_head, "right")[1]
            }
            
            # Distinct vibrant colors for each algorithm
            colors = ['#4f46e5', '#db2777', '#7c3aed', '#0891b2'] # Indigo, Pink, Violet, Cyan
            fig = go.Figure([go.Bar(
                x=list(results.keys()), 
                y=list(results.values()), 
                marker_color=colors,
                text=list(results.values()),
                textposition='auto',
                textfont=dict(color='white', size=14, family="Segoe UI Bold"),
            )])
            fig.update_layout(
                title=dict(text="Total Head Movement: Lower is Better", font=dict(color='#111827', size=18)),
                yaxis_title=dict(text="Distance (Tracks)", font=dict(color='#111827')),
                template="plotly_white",
                paper_bgcolor='#ffffff',
                plot_bgcolor='#ffffff',
                xaxis=dict(tickfont=dict(color='#111827', size=14)),
                yaxis=dict(tickfont=dict(color='#111827')),
            )
            st.plotly_chart(fig)
