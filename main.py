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
        color: #0f172a;
    }
    
    /* Ensure all text/markdown is dark for readability */
    div[data-testid="stMarkdownContainer"] p, 
    div[data-testid="stWidgetLabel"] p, 
    label, 
    .stSelectbox label, 
    .stRadio label,
    h1, h2, h3, h4 {
        color: #0f172a !important; /* Deep Slate */
        font-weight: 600 !important;
    }

    /* Metric Styling */
    [data-testid="stMetricValue"] {
        color: #2563eb !important;
        font-weight: 800 !important;
    }
    
    [data-testid="stMetricLabel"] p {
        color: #475569 !important;
        font-weight: 700 !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-highlight"] {
        background-color: #2563eb !important;
    }
    
    /* Table Rows */
    .stTable td {
        color: #1e293b !important;
    }

    /* Header Container */
    .stHeader {
        background: #f8fafc;
        border-bottom: 2px solid #e2e8f0;
        padding: 2rem;
        margin-bottom: 2rem;
    }

    /* Attractive Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%) !important;
        color: white !important;
        border-radius: 0.5rem;
        font-weight: 700;
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
                m1, m2, m3 = st.columns(3)
                m1.metric("Hits", hits)
                m2.metric("Faults", faults)
                m3.metric("Hit Ratio", f"{(hits/len(pages)):.2f}")
                
                # Visualization Table
                st.write("### Step-by-Step Execution")
                df_data = []
                for step in history:
                    row = {"Page": step["Page"]}
                    for i in range(frame_size):
                        row[f"F{i+1}"] = str(step["Frames"][i]) if i < len(step["Frames"]) else "-"
                    row["Status"] = "✅ Hit" if step["Status"] == "Hit" else "❌ Miss"
                    df_data.append(row)
                
                st.dataframe(pd.DataFrame(df_data), use_container_width=True)
                
                # Export
                df_export = pd.DataFrame(df_data)
                csv_cache = df_export.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Export Simulation Results (CSV)", csv_cache, f"cache_{cache_algo.lower()}_results.csv", "text/csv")
                
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
                st.download_button("📥 Export Simulation Results (CSV)", csv_disk, "disk_results.csv", "text/csv")
                
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

            # Export
            df_comp_cache = pd.DataFrame(list(results.items()), columns=["Algorithm", "Page Faults"])
            csv_comp_cache = df_comp_cache.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Export Comparison Data (CSV)", csv_comp_cache, "cache_comparison.csv", "text/csv")

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
            
            # Export
            df_comp_disk = pd.DataFrame(list(results.items()), columns=["Algorithm", "Total Head Movement"])
            csv_comp_disk = df_comp_disk.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Export Comparison Data (CSV)", csv_comp_disk, "disk_comparison.csv", "text/csv")
