import json
import pathlib
import matplotlib.pyplot as plt
import numpy as np

def main():
    base_dir = pathlib.Path(__file__).parent
    results_file = base_dir / "results.json"
    output_dir = base_dir / "output"
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if not results_file.exists():
        print(f"Error: {results_file} not found. Run runner.py first.")
        return
        
    with open(results_file, "r", encoding="utf-8") as f:
        results = json.load(f)
        
    # Consistent colors
    colors = {
        "brute_force": "#e74c3c",      # Red
        "recursive": "#e67e22",        # Orange
        "backtracking": "#9b59b6",     # Purple
        "greedy": "#2ecc71",           # Green
        "divide_conquer": "#3498db"    # Blue
    }
    
    # Extract data structures
    cases = ["small", "medium", "large"]
    algorithms = ["brute_force", "recursive", "backtracking", "greedy", "divide_conquer"]
    
    # Map data for easy access
    data_map = {algo: {case: None for case in cases} for algo in algorithms}
    expected_makespans = {}
    task_counts = {}
    
    # Fill data_map
    for record in results:
        algo = record["algorithm"]
        case = record["case"]
        data_map[algo][case] = record

    # Re-read expected makespans from test data
    data_dir = base_dir.parent / "test" / "data"
    for case in cases:
        case_file = data_dir / f"{case}.json"
        if case_file.exists():
            with open(case_file, "r", encoding="utf-8") as cf:
                cdata = json.load(cf)
                expected_makespans[case] = cdata.get("expected_optimal_makespan", 0)
                task_counts[case] = len(cdata.get("tasks", []))

    x_tasks = [task_counts.get(c, 0) for c in cases]
    
    # ---------------------------------------------------------
    # Chart 1: Execution Time vs Problem Size
    # ---------------------------------------------------------
    plt.figure(figsize=(10, 6), dpi=150)
    for algo in algorithms:
        y_times = []
        for case in cases:
            rec = data_map[algo][case]
            time_val = rec.get("avg_execution_time") if rec else None
            y_times.append(time_val)
            
        # Plot only valid points to avoid breaking the line if some are None
        valid_x = [x_tasks[i] for i, t in enumerate(y_times) if t is not None]
        valid_y = [t for t in y_times if t is not None]
        
        if valid_x and valid_y:
            plt.plot(valid_x, valid_y, marker='o', linewidth=2, label=algo, color=colors[algo])
            
    plt.yscale('log')
    plt.xticks(x_tasks, [str(t) for t in x_tasks])
    plt.xlabel("Number of Tasks")
    plt.ylabel("Average Execution Time (s) [Log Scale]")
    plt.title("Execution Time vs Problem Size")
    plt.legend()
    plt.grid(True, which="both", ls="--", alpha=0.5)
    
    plt.savefig(output_dir / "execution_time_vs_tasks.png", bbox_inches='tight')
    plt.close()
    
    # ---------------------------------------------------------
    # Chart 2: Makespan Comparison
    # ---------------------------------------------------------
    plt.figure(figsize=(10, 6), dpi=150)
    
    x = np.arange(len(cases))
    width = 0.15
    multiplier = 0
    
    for algo in algorithms:
        y_makespans = []
        for case in cases:
            rec = data_map[algo][case]
            mk = rec.get("makespan") if rec else None
            y_makespans.append(mk if mk is not None else 0)
            
        offset = width * multiplier
        bars = plt.bar(x + offset, y_makespans, width, label=algo, color=colors[algo])
        
        # Add labels to the bars
        for bar in bars:
            yval = bar.get_height()
            if yval > 0:
                plt.text(bar.get_x() + bar.get_width()/2, yval, f'{int(yval)}', ha='center', va='bottom', fontsize=8, rotation=90)
                
        multiplier += 1
        
    # Add horizontal dashed lines for expected optimal makespan
    for i, case in enumerate(cases):
        expected = expected_makespans.get(case, 0)
        group_center = x[i] + (width * len(algorithms) / 2) - (width/2)
        # Draw a short line over the group
        plt.hlines(y=expected, xmin=x[i]-width/2, xmax=x[i]+width*len(algorithms), color='black', linestyle='--', linewidth=1.5, alpha=0.7)
        if i == 0:
             plt.plot([], [], color='black', linestyle='--', label='Expected Optimal') # for legend

    plt.xlabel("Test Case")
    plt.ylabel("Makespan")
    plt.title("Makespan by Algorithm and Case")
    plt.xticks(x + width * 2, cases)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    
    plt.savefig(output_dir / "makespan_comparison.png", bbox_inches='tight')
    plt.close()

    # ---------------------------------------------------------
    # Chart 3: Execution Time by Algorithm (Large Case)
    # ---------------------------------------------------------
    plt.figure(figsize=(10, 6), dpi=150)
    
    case = "large"
    algos_large = []
    times_large = []
    colors_large = []
    
    for algo in algorithms:
        rec = data_map[algo][case]
        time_val = rec.get("avg_execution_time") if rec else None
        if time_val is not None:
            algos_large.append(algo)
            times_large.append(time_val)
            colors_large.append(colors[algo])
            
    bars = plt.bar(algos_large, times_large, color=colors_large)
    
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, f'{yval:.6f}s', ha='center', va='bottom')
        
    plt.xlabel("Algorithm")
    plt.ylabel("Average Execution Time (s)")
    plt.title(f"Execution Time on Large Case ({task_counts.get('large', 100)} tasks)")
    
    plt.savefig(output_dir / "execution_time_by_algorithm.png", bbox_inches='tight')
    plt.close()
    
    print(f"Charts successfully generated in {output_dir}")

if __name__ == "__main__":
    main()
