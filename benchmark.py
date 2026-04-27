import time
from shield import AiClassifiedShield

def run_benchmark():
    print("🚀 Starting ai-classy Velocity Benchmark...")
    shield = AiClassifiedShield()
    start = time.time()
    results, score = shield.get_operability_results()
    end = time.time()
    
    latency = (end - start) * 1000
    print(f"✅ Audit Latency: {latency:.2f}ms")
    print(f"✅ System Integrity: {score}/9")

if __name__ == "__main__":
    run_benchmark()
