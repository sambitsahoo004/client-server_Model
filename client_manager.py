# client_manager.py

import subprocess
import sys
import time

def start_client():
    subprocess.Popen([sys.executable, 'client.py'])

if __name__ == "__main__":
    num_prisoners = int(input("Enter the number of prisoners to escape: "))
    
    for _ in range(num_prisoners):
        start_client()
        time.sleep(1)  # Adding a small delay to ensure clients start sequentially

