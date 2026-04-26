import os
import subprocess
import csv
import matplotlib.pyplot as plt
import concurrent.futures

os.makedirs("../results", exist_ok=True)

print("Compiling C++ code...")
compile_cmd = ["g++", "-O3", "-std=c++17", "main.cpp", "-o", "experiment"]
subprocess.run(compile_cmd, check=True)
print("Compilation successful.\n")

def run_test(algo, N, M, pivot = False):
    pivot_str = "1" if pivot else "0"
    result = subprocess.run(
        ["./experiment", algo, str(N), str(M), pivot_str],
        capture_output=True, text=True, check=True
    )
    output = result.stdout.strip().split(',')
    return {
        'algo': output[0],
        'N': int(output[1]),
        'M': int(output[2]),
        'distance': int(output[3]),
        'time_ms': float(output[4]),
        'mem_mb': float(output[5])
    }

def run_test_averaged(algo, N, M, pivot=False, iterations=100, max_workers=5):
    total_distance = 0
    total_time_ms = 0.0
    total_mem_mb = 0.0
    final_algo = algo
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(run_test, algo, N, M, pivot) for _ in range(iterations)]
        
        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            total_distance = res['distance']
            total_time_ms += res['time_ms']
            total_mem_mb += res['mem_mb']
            final_algo = res['algo']
            
    return {
        'algo': final_algo,
        'N': N,
        'M': M,
        'distance': total_distance,
        'time_ms': total_time_ms / iterations,
        'mem_mb': total_mem_mb / iterations
    }

def run_experiment_trace():
    print("Running TRACE Comparison (Standard DP vs Hirschberg)")
    sizes_scaling = [100, 500, 1000, 2000, 5000, 10000, 20000]
    # sizes_async = [1000, 5000, 10000, 20000] # Cap N at 20000 for standard DP to avoid 1GB+ memory blows on some systems, wait, 50000*1000 is 200MB, we can run 50000
    # sizes_async = [1000, 5000, 10000, 20000, 50000]
    algos = ["standard_trace", "hirschberg_trace"]
    
    results = []
    with open('../results/exp_trace.csv', 'w', newline='') as csvfile:
        fieldnames = ['algo', 'N', 'M', 'distance', 'time_ms', 'mem_mb']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        # 1. Scaling N=M
        for N in sizes_scaling:
            for algo in algos:
                if algo == "standard_trace" and N > 20000:
                    continue
                print(f"  [Trace] Scaling {algo} for N={N}...")
                data = run_test_averaged(algo, N, N)
                writer.writerow(data)
                results.append(data)
                
        # 2. Asymmetric (M=1000, scaling N)
        # for N in sizes_async:
        #     for algo in algos:
        #         print(f"  [Trace] Asymmetric {algo} for N={N}, M=1000...")
        #         data = run_test(algo, N, 1000)
        #         writer.writerow(data)
        #         results.append(data)
                
    return results

def run_experiment_distance():
    print("\nRunning DISTANCE Comparison (Optimized DP vs Hirschberg)")
    sizes_scaling = [100, 500, 1000, 2000, 5000, 10000, 20000, 40000,
                 80000, 160000]
    # sizes_async = [1000, 5000, 10000, 20000, 50000, 100000]
    algos = ["optimized_distance", "hirschberg_distance"]
    
    results = []
    with open('../results/exp_distance.csv', 'w', newline='') as csvfile:
        fieldnames = ['algo', 'N', 'M', 'distance', 'time_ms', 'mem_mb']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        # 1. Scaling N=M
        for N in sizes_scaling:
            for algo in algos:
                print(f"  [Distance] Scaling {algo} for N={N}...")
                data = run_test_averaged(algo, N, N)
                writer.writerow(data)
                results.append(data)
                
        # 2. Asymmetric (M=1000, scaling N)
        # for N in sizes_async:
        #     for algo in algos:
        #         print(f"  [Distance] Asymmetric {algo} for N={N}, M=1000...")
        #         data = run_test(algo, N, 1000)
        #         writer.writerow(data)
        #         results.append(data)
                
    return results

def run_experiment_pivot_distance():
    print("\nRunning Pivot Comparison (Hirschberg Trace vs Optimized Distance)")
    sizes_scaling = [100, 500, 1000, 2000, 5000, 10000, 20000, 40000,
                 80000, 160000]
    # sizes_async = [1000, 5000, 10000, 20000, 50000, 100000]
    algos = ["hirschberg_distance","hirschberg_distance"]
    
    results = []
    with open('../results/exp_pivot_distance.csv', 'w', newline='') as csvfile:
        fieldnames = ['algo', 'N', 'M', 'distance', 'time_ms', 'mem_mb']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        # 1. Scaling N=M
        for N in sizes_scaling:
            i=0
            for algo in algos:
                print(f"  [Pivot] Scaling {algo} for pivot {i} for N={N}...")
                if(i==0): data = run_test_averaged(algo, N, N, False)
                else: data = run_test_averaged(algo, N, N, True)
                writer.writerow(data)
                results.append(data)
                i+=1
                
        # 2. Asymmetric (M=1000, scaling N)
        # for N in sizes_async:
        #     for algo in algos:
        #         print(f"  [Pivot] Asymmetric {algo} for N={N}, M=1000...")
        #         data = run_test(algo, N, 1000)
        #         writer.writerow(data)
        #         results.append(data)

    return results

def run_experiment_pivot_trace():
    print("\nRunning Pivot Comparison (Hirschberg Trace vs Optimized Distance)")
    sizes_scaling = [100, 500, 1000, 2000, 5000, 10000, 20000, 40000,
                 80000, 160000]
    # sizes_async = [1000, 5000, 10000, 20000, 50000, 100000]
    algos = ["hirschberg_trace","hirschberg_trace"]
    
    results = []
    with open('../results/exp_pivot_trace.csv', 'w', newline='') as csvfile:
        fieldnames = ['algo', 'N', 'M', 'distance', 'time_ms', 'mem_mb']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        # 1. Scaling N=M
        for N in sizes_scaling:
            i=0
            for algo in algos:
                print(f"  [Pivot] Scaling {algo} for pivot {i} for N={N}...")
                if(i==0): data = run_test_averaged(algo, N, N, False)
                else: data = run_test_averaged(algo, N, N, True)
                writer.writerow(data)
                results.append(data)
                i+=1
                
        # 2. Asymmetric (M=1000, scaling N)
        # for N in sizes_async:
        #     for algo in algos:
        #         print(f"  [Pivot] Asymmetric {algo} for N={N}, M=1000...")
        #         data = run_test(algo, N, 1000)
        #         writer.writerow(data)
        #         results.append(data)

    return results

def plot_results(trace_data, distance_data, pivot_distance_data, pivot_trace_data):
    print("\nGenerating plots...")
    
    # --- TRACE PLOTS ---
    # Memory Scaling (N=M)
    plt.figure(figsize=(10, 6))
    for algo in ["standard_trace", "hirschberg_trace"]:
        x = [d['N'] for d in trace_data if d['algo'] == algo and d['N'] == d['M']]
        y = [d['mem_mb'] for d in trace_data if d['algo'] == algo and d['N'] == d['M']]
        if x: plt.plot(x, y, marker='o', label=algo)
    plt.title('TRACE: Memory Usage vs Sequence Length (N=M)')
    plt.xlabel('Sequence Length (N)')
    plt.ylabel('Peak Memory (MB)')
    plt.legend()
    plt.grid(True)
    plt.savefig('../results/trace_memory_scaling.png')
    plt.close()

    # Time Scaling (N=M)
    plt.figure(figsize=(10, 6))
    for algo in ["standard_trace", "hirschberg_trace"]:
        x = [d['N'] for d in trace_data if d['algo'] == algo and d['N'] == d['M']]
        y = [d['time_ms'] for d in trace_data if d['algo'] == algo and d['N'] == d['M']]
        if x: plt.plot(x, y, marker='o', label=algo)
    plt.title('TRACE: Execution Time vs Sequence Length (N=M)')
    plt.xlabel('Sequence Length (N)')
    plt.ylabel('Time (ms)')
    plt.legend()
    plt.grid(True)
    plt.savefig('../results/trace_time_scaling.png')
    plt.close()

    # Edit Distance (N=M)
    plt.figure(figsize=(10, 6))
    for algo in ["standard_trace", "hirschberg_trace"]:
        x = [d['N'] for d in trace_data if d['algo'] == algo and d['N'] == d['M']]
        y = [d['distance'] for d in trace_data if d['algo'] == algo and d['N'] == d['M']]
        if x: plt.plot(x, y, marker='o', label=algo)
    plt.title('TRACE: Edit Distance vs Sequence Length (N=M)')
    plt.xlabel('Sequence Length (N)')
    plt.ylabel('Edit Distance')
    plt.legend()
    plt.grid(True)
    plt.savefig('../results/trace_edit_distance.png')
    plt.close()
    
    # --- DISTANCE PLOTS ---
    # Memory Scaling (N=M)
    plt.figure(figsize=(10, 6))
    for algo in ["optimized_distance", "hirschberg_distance"]:
        x = [d['N'] for d in distance_data if d['algo'] == algo and d['N'] == d['M']]
        y = [d['mem_mb'] for d in distance_data if d['algo'] == algo and d['N'] == d['M']]
        if x: plt.plot(x, y, marker='o', label=algo)
    plt.title('DISTANCE ONLY: Memory Usage vs Sequence Length (N=M)')
    plt.xlabel('Sequence Length (N)')
    plt.ylabel('Peak Memory (MB)')
    plt.legend()
    plt.grid(True)
    plt.savefig('../results/distance_memory_scaling.png')
    plt.close()

    # Time Scaling (N=M)
    plt.figure(figsize=(10, 6))
    for algo in ["optimized_distance", "hirschberg_distance"]:
        x = [d['N'] for d in distance_data if d['algo'] == algo and d['N'] == d['M']]
        y = [d['time_ms'] for d in distance_data if d['algo'] == algo and d['N'] == d['M']]
        if x: plt.plot(x, y, marker='o', label=algo)
    plt.title('DISTANCE ONLY: Execution Time vs Sequence Length (N=M)')
    plt.xlabel('Sequence Length (N)')
    plt.ylabel('Time (ms)')
    plt.legend()
    plt.grid(True)
    plt.savefig('../results/distance_time_scaling.png')
    plt.close()

    # Edit Distance (N=M)
    plt.figure(figsize=(10, 6))
    for algo in ["optimized_distance", "hirschberg_distance"]:
        x = [d['N'] for d in distance_data if d['algo'] == algo and d['N'] == d['M']]
        y = [d['distance'] for d in distance_data if d['algo'] == algo and d['N'] == d['M']]
        if x: plt.plot(x, y, marker='o', label=algo)
    plt.title('DISTANCE ONLY: Edit Distance vs Sequence Length (N=M)')
    plt.xlabel('Sequence Length (N)')
    plt.ylabel('Edit Distance')
    plt.legend()
    plt.grid(True)
    plt.savefig('../results/distance_edit_distance.png')
    plt.close()

    # --- PIVOT TRACE PLOTS ---
    # Memory Scaling (N=M)
    plt.figure(figsize=(10, 6))
    for algo in ["hirschberg_trace","hirschberg_pivot"]:
        x = [d['N'] for d in pivot_trace_data if d['algo'] == algo and d['N'] == d['M']]
        y = [d['mem_mb'] for d in pivot_trace_data if d['algo'] == algo and d['N'] == d['M']]
        if x: plt.plot(x, y, marker='o', label=algo)
    plt.title('TRACE: Memory Usage vs Sequence Length (N=M)')
    plt.xlabel('Sequence Length (N)')
    plt.ylabel('Peak Memory (MB)')
    plt.legend()
    plt.grid(True)
    plt.savefig('../results/pivot_trace_memory_scaling.png')
    plt.close()

    # Time Scaling (N=M)
    plt.figure(figsize=(10, 6))
    for algo in ["hirschberg_trace","hirschberg_pivot"]:
        x = [d['N'] for d in pivot_trace_data if d['algo'] == algo and d['N'] == d['M']]
        y = [d['time_ms'] for d in pivot_trace_data if d['algo'] == algo and d['N'] == d['M']]
        if x: plt.plot(x, y, marker='o', label=algo)
    plt.title('TRACE: Execution Time vs Sequence Length (N=M)')
    plt.xlabel('Sequence Length (N)')
    plt.ylabel('Time (ms)')
    plt.legend()
    plt.grid(True)
    plt.savefig('../results/pivot_trace_time_scaling.png')
    plt.close()

    # Edit Distance (N=M)
    plt.figure(figsize=(10, 6))
    for algo in ["hirschberg_trace","hirschberg_pivot"]:
        x = [d['N'] for d in pivot_trace_data if d['algo'] == algo and d['N'] == d['M']]
        y = [d['distance'] for d in pivot_trace_data if d['algo'] == algo and d['N'] == d['M']]
        if x: plt.plot(x, y, marker='o', label=algo)
    plt.title('TRACE: Edit Distance vs Sequence Length (N=M)')
    plt.xlabel('Sequence Length (N)')
    plt.ylabel('Edit Distance')
    plt.legend()
    plt.grid(True)
    plt.savefig('../results/pivot_trace_edit_distance.png')
    plt.close()

    # --- PIVOT DISTANCE PLOTS ---
    # Memory Scaling (N=M)
    plt.figure(figsize=(10, 6))
    for algo in ["hirschberg_distance","hirschberg_pivot"]:
        x = [d['N'] for d in pivot_distance_data if d['algo'] == algo and d['N'] == d['M']]
        y = [d['mem_mb'] for d in pivot_distance_data if d['algo'] == algo and d['N'] == d['M']]
        if x: plt.plot(x, y, marker='o', label=algo)
    plt.title('DISTANCE ONLY: Memory Usage vs Sequence Length (N=M)')
    plt.xlabel('Sequence Length (N)')
    plt.ylabel('Peak Memory (MB)')
    plt.legend()
    plt.grid(True)
    plt.savefig('../results/pivot_distance_memory_scaling.png')
    plt.close()

    # Time Scaling (N=M)
    plt.figure(figsize=(10, 6))
    for algo in ["hirschberg_distance","hirschberg_pivot"]:
        x = [d['N'] for d in pivot_distance_data if d['algo'] == algo and d['N'] == d['M']]
        y = [d['time_ms'] for d in pivot_distance_data if d['algo'] == algo and d['N'] == d['M']]
        if x: plt.plot(x, y, marker='o', label=algo)
    plt.title('DISTANCE ONLY: Execution Time vs Sequence Length (N=M)')
    plt.xlabel('Sequence Length (N)')
    plt.ylabel('Time (ms)')
    plt.legend()
    plt.grid(True)
    plt.savefig('../results/pivot_distance_time_scaling.png')
    plt.close()

    # Edit Distance (N=M)
    plt.figure(figsize=(10, 6))
    for algo in ["hirschberg_distance","hirschberg_pivot"]:
        x = [d['N'] for d in pivot_distance_data if d['algo'] == algo and d['N'] == d['M']]
        y = [d['distance'] for d in pivot_distance_data if d['algo'] == algo and d['N'] == d['M']]
        if x: plt.plot(x, y, marker='o', label=algo)
    plt.title('DISTANCE ONLY: Edit Distance vs Sequence Length (N=M)')
    plt.xlabel('Sequence Length (N)')
    plt.ylabel('Edit Distance')
    plt.legend()
    plt.grid(True)
    plt.savefig('../results/pivot_distance_edit_distance.png')
    plt.close()

    print("Plots saved in results/ directory.")


if __name__ == "__main__":
    trace_data = run_experiment_trace()
    distance_data = run_experiment_distance()
    pivot_distance_data = run_experiment_pivot_distance()
    pivot_trace_data = run_experiment_pivot_trace()
    plot_results(trace_data, distance_data, pivot_distance_data, pivot_trace_data)
    print("All experiments completed successfully!")
