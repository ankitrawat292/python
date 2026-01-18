import os 
import shutil
import psutil

#========================================
# 1. Counts Files and Folders
#========================================
downloads_path = os.path.join(os.environ["USERPROFILE"], "Downloads")

file_count = 0
dir_count = 0

for item in os.listdir(downloads_path):
  full_path = os.path.join(downloads_path, item)
  if os.path.isfile(full_path):
    file_count += 1
  elif os.path.isdir(full_path):
    dir_count +=1
print("Downalod Folder info")
print("File Count   :", file_count)
print("Folder Count :", dir_count)

#-------------------------------------------
#2. Disk Usage Details
#-------------------------------------------
disk = shutil.disk_usage("C:\\")

print("\n Disk Usage (C Drive)")
print("Total:", round(disk.total / (1024**3), 2), "GB")
print("Used :", round(disk.used / (1024**3),2), "GB")
print("Free :", round(disk.free / (1024**3), 2), "GB")

#------------------------------------------------
# 3. Memory usage
#------------------------------------------------

memory = psutil.virtual_memory()

print("\n Memory Usage (RAM)")
print("Total :", round(memory.total / (1024**3), 2), "GB")
print("Used :", round(memory.used / (1024**3), 2), "GB")
print("Free :", round(memory.free / (1024**3), 2), "GB")

#---------------------------------------------------------
# 4. Which application is using high memory
#---------------------------------------------------------

process_list = []

for process in psutil.process_iter(['pid', 'name', 'memory_info']):
  try:
    mem_mb = process.info['memory_info'].rss / (1024 * 1024)
    process_list.append((process.info['name'], mem_mb))
  except (psutil.NoSuchProcess, psutil.AccessDenied):
    pass

# Memory usage sorting (higest first)

process_list.sort(key=lambda x: x[1], reverse=True)

print("Top 5 Memory consuming Applications:\n")

for name, mem in process_list[:5]:
  print(f"{name:<30} {mem:.2f} MB")
