import psutil
from datetime import datetime

THRESHOLD_MB = 500          # alert limit
LOG_FILE = "memory_alert.log"

def log_message(message):
    with open(LOG_FILE, "a") as f:
        f.write(message + "\n")

print("🔍 Checking memory usage...\n")

process_list = []

for process in psutil.process_iter(['pid', 'name', 'memory_info']):
    try:
        mem_mb = process.info['memory_info'].rss / (1024 * 1024)
        process_list.append((process.info['name'], mem_mb))
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass

# sort by memory usage
process_list.sort(key=lambda x: x[1], reverse=True)

print("Top 5 Memory Consuming Applications:\n")

for name, mem in process_list[:5]:
    print(f"{name:<30} {mem:.2f} MB")

print("\n⚠️ Checking threshold alerts...\n")

for name, mem in process_list:
    if mem > THRESHOLD_MB:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        alert = f"[{timestamp}] ALERT: {name} using {mem:.2f} MB RAM"
        print(alert)
        log_message(alert)
