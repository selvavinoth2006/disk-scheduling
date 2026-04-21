# Cache Replacement and Disk Scheduling Simulator

A comprehensive simulation tool for visualizing Operating System algorithms. Built with Python and Streamlit.

## 🚀 Features

### 🧠 Cache Replacement
- **Algorithms**: FIFO (First-In-First-Out), LRU (Least Recently Used), Optimal.
- **Visualization**: Step-by-step frame allocation table.
- **Metrics**: Hits, Faults, Hit Ratio, Miss Ratio.

### 💿 Disk Scheduling
- **Algorithms**: FCFS, SSTF, SCAN, C-SCAN.
- **Visualization**: Interactive disk head movement graph.
- **Metrics**: Total Seek Time / Head Movement.

### 📊 Advanced Tools
- **Algorithm Comparison**: Side-by-side performance charts.
- **Data Export**: Save simulation results directly to CSV.
- **Error Handling**: Input validation for page strings and disk queues.

---

## 🛠️ Installation & Setup

1. **Clone the project** to your local machine.
2. **Install Dependencies**:
   ```bash
   pip install streamlit pandas plotly matplotlib
   ```
3. **Run the Application**:
   ```bash
   streamlit run main.py
   ```

---

## 📂 File Structure

- `main.py`: The UI and integration logic.
- `cache_algorithms.py`: Core logic for memory management.
- `disk_algorithms.py`: Logic for disk head scheduling.
- `README.md`: Project documentation.

---

## 📝 Usage

- **Cache Tab**: Enter a page string (e.g., `1, 2, 3, 4, 1, 2, 5`) and specify frames. Click "Run" to see the frame-by-frame history.
- **Disk Tab**: Enter tracks (e.g., `98, 183, 37`) and initial head position. The graph shows the path taken.
- **Comparison Tab**: Quickly see which algorithm performs best for your specific input.

---
*Created for Academic OS Project Excellence.*
"# disk-scheduling" 
