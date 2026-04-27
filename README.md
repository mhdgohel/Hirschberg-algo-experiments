# Hirschberg Algorithm Performance Analysis

This project rigorously validates the performance, accuracy, and memory utilization of the **Hirschberg sequence alignment algorithm**. It benchmarks Hirschberg's linear space complexity $O(N+M)$ against standard dynamic programming baselines.

The benchmarking suite is written in C++17 for high-performance sequence alignment execution, wrapped in a Python automation script that handles compilation, multi-threaded execution, and data visualization.

---

## Experiments Coverage

The suite performs multiple automated experiments tracking **Execution Time (ms)**, **Peak Memory (MB)**, and **Edit Distance (accuracy)** over varying DNA sequences.

### 1. Trace Extraction Comparison (`Standard DP` vs `Hirschberg Trace`)
Compares the full sequence alignment trace generation.
* **Standard DP**: Requires $O(N \times M)$ memory. Fails/blows up at scale (N=20,000 takes ~1 GB of RAM).
* **Hirschberg Trace**: Divides and conquers to build the trace in $O(N+M)$ linear space. Drastically reduces memory usage for large strings.

### 2. Distance-Only Comparison (`Space-Optimized DP` vs `Hirschberg Distance`)
Compares algorithms where *only* the edit distance score is required (no alignment trace is retained).
* **Space-Optimized DP**: Only keeps two rows in memory, achieving $O(\min(N, M))$ memory naturally. 
* **Hirschberg Distance**: Verified alongside standard space-optimized DP to ensure mathematically precise memory behavior and alignment accuracy up to sequence lengths of $N = 160,000$.

### 3. Pivot Strategies (`Pivot Trace` & `Pivot Distance`)
Compares the standard Hirschberg partitioning (splitting exactly at the midpoint `N/2`) against a **randomized pivot selection** approach to evaluate performance impacts on highly asymmetric or worst-case sequence distributions.

---

## How to Run

### Prerequisites
Ensure you have the following installed on your system:
* **`g++`** compiler supporting C++17.
* **Python 3.x**
* **`matplotlib`** (for plotting the generated results).

You can install the required Python dependency using:
```bash
pip install matplotlib
```

### Execution
The entire experimental suite is fully automated. The script will automatically compile the C++ source code, execute all benchmarks across different sequence sizes, generate CSV datasets, and plot the performance graphs.

1. Navigate to the `src` directory:
   ```bash
   cd src
   ```

2. Run the experiment script:
   ```bash
   python3 run_experiments.py
   ```

### Output
Once the experiments are completed, you will find all the generated data and plots in the `results/` directory located at the root of the project:
* `*.csv`: Raw data metrics containing the algorithm, sequence dimensions, edit distance, time, and peak memory.
* `*.png`: Visual graphs demonstrating execution time, peak memory scaling, and edit distance validation.
