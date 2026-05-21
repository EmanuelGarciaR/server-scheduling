import json
import os
import pathlib
import time
from backend.core.sheduler import run_scheduler, ALGORITHMS

def main():
    # Paths
    base_dir = pathlib.Path(__file__).parent.parent
    data_dir = base_dir / "test" / "data"
    output_file = pathlib.Path(__file__).parent / "results.json"

    # Test cases to load
    cases = ["small", "medium", "large"]
    algorithms = list(ALGORITHMS.keys())
    
    results = []
    
    print(f"{'Algorithm':<15} | {'Case':<8} | {'Tasks':<5} | {'Srvs':<4} | {'Makespan':<10} | {'Expected':<10} | {'Opt?':<5} | {'Avg Time (s)':<15}")
    print("-" * 90)

    for case_name in cases:
        file_path = data_dir / f"{case_name}.json"
        if not file_path.exists():
            print(f"Warning: {file_path} not found.")
            continue
            
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        num_servers = data.get("num_servers")
        expected_makespan = data.get("expected_optimal_makespan")
        n_tasks = len(data.get("tasks", []))
        
        for algo in algorithms:
            # Skip exact algorithms for large cases to avoid hanging
            if algo in ["brute_force", "recursive"] and n_tasks > 15:
                avg_time = None
                makespan = None
                is_optimal = False
                total_time = 0.0
                runs = 0
            elif algo == "backtracking" and n_tasks >= 20:
                avg_time = None
                makespan = None
                is_optimal = False
                total_time = 0.0
                runs = 0
            else:
                total_time = 0.0
                makespan = 0
                runs = 5
                
                for _ in range(runs):
                    with open(file_path, "r", encoding="utf-8") as f:
                        run_data = json.load(f)
                    
                    result = run_scheduler(run_data, algo, num_servers)
                    total_time += result.execution_time
                    makespan = result.max_load
                    
                avg_time = total_time / runs
                is_optimal = bool(makespan == expected_makespan)
            
            # Collect results
            record = {
                "algorithm": algo,
                "case": case_name,
                "n_tasks": n_tasks,
                "num_servers": num_servers,
                "makespan": makespan,
                "avg_execution_time": avg_time,
                "is_optimal": is_optimal
            }
            results.append(record)
            
            makespan_str = str(makespan) if makespan is not None else "N/A"
            avg_time_str = f"{avg_time:.6f}" if avg_time is not None else "TIMEOUT"
            print(f"{algo:<15} | {case_name:<8} | {n_tasks:<5} | {num_servers:<4} | {makespan_str:<10} | {expected_makespan:<10} | {str(is_optimal):<5} | {avg_time_str:<15}")

    # Save results
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)
        
    print(f"\nResults saved to {output_file}")

if __name__ == "__main__":
    main()
