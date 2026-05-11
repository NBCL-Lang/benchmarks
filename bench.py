import subprocess
import time
import os
import matplotlib.pyplot as plt

RUNS = 50
NBCL_BIN = "target/release/nbcl-benchmarks"
RESULTS_DIR = "results"
BENCH_TASKS = {
    "fibonacci": "bench/fib/fibonacci",
    "fizzbuzz": "bench/fizzbuzz/fizzbuzz",
    "parsing_speed": "bench/fib/fibonacci" # reuse fibonacci for parsing speed
}

os.makedirs(RESULTS_DIR, exist_ok=True)

def run_benchmark(name, cmd):
    print(f"  > {name}...", end=" ", flush=True)
    times = []
    
    for _ in range(RUNS):
        start = time.perf_counter()
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        end = time.perf_counter()
        times.append(end - start)
    
    avg = sum(times) / len(times)
    print(f"Avg: {avg:.4f}s")
    return avg

def run_suite(task_name, file_base):
    print(f"\nRunning {task_name.upper()} Suite:")

    is_parse_test = (task_name == "parsing_speed")
    extra_flags = ["--parse-only"] if is_parse_test else []
    
    commands = {
        "Node.js": ["node", "--check", f"{file_base}.js"] if is_parse_test else ["node", f"{file_base}.js"],
        "Python": ["python3", "-m", "py_compile", f"{file_base}.py"] if is_parse_test else ["python3", f"{file_base}.py"],
        "Rhai": [NBCL_BIN, "--lang", "rhai", f"{file_base}.rhai"] + extra_flags,
        "Koto": [NBCL_BIN, "--lang", "koto", f"{file_base}.koto"] + extra_flags,
        "NBCL": [NBCL_BIN, "--lang", "nbcl", f"{file_base}.nbl"] + extra_flags
    }

    results = {}
    for name, cmd in commands.items():
        try:
            results[name] = run_benchmark(name, cmd)
        except Exception as e:
            print(f"Failed to run {name}: {e}")

    names = list(results.keys())
    averages = list(results.values())

    plt.figure(figsize=(10, 6))
    colors = ['#4285F4', '#34A853', '#FBBC05', '#8E44AD', '#EA4335']
    bars = plt.bar(names, averages, color=colors[:len(names)])
    
    plt.ylabel('Time (seconds)')
    plt.title(f'{task_name.capitalize()} Benchmark (Average of {RUNS} runs)')
    
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, f'{yval:.4f}s', va='bottom', ha='center')

    plt.tight_layout()
    save_path = os.path.join(RESULTS_DIR, f'{task_name}_results.png')
    plt.savefig(save_path)
    plt.close() 
    print(f"Done. Chart saved to {save_path}")

def main():
    for task_name, file_base in BENCH_TASKS.items():
        run_suite(task_name, file_base)

if __name__ == "__main__":
    main()