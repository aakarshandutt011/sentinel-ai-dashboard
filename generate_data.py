import pandas as pd
import random
from datetime import datetime, timedelta

def generate_logs():
    print("--- Generating Synthetic Web Logs ---")
    
    data = []
    endpoints = ['/home', '/login', '/dashboard', '/api/user', '/contact']
    ips = ['192.168.1.10', '192.168.1.11', '10.0.0.5', '45.33.22.11', '203.0.113.55']
    
    # Simulate a timeline starting 24 hours ago
    start_time = datetime.now() - timedelta(hours=24)
    
    for i in range(1000):
        # 1. Basic Info
        timestamp = start_time + timedelta(minutes=i)
        ip = random.choice(ips)
        endpoint = random.choice(endpoints)
        status = 200
        
        # 2. Simulate "Normal" Traffic
        if random.random() < 0.9:
            status = 200
        
        # 3. Simulate "Brute Force" Attack (High 401s from one IP)
        elif i > 800 and i < 900:
            ip = "192.168.1.666" # The Attacker
            endpoint = "/login"
            status = 401 # Unauthorized
            
        # 4. Simulate "SQL Injection" (Weird characters in URL)
        elif random.random() > 0.95:
            endpoint = "/api/user?id=1' OR '1'='1"
            status = 500 # Server Error
            
        data.append([timestamp, ip, endpoint, status])
        
    # Create DataFrame and Save
    df = pd.DataFrame(data, columns=['Timestamp', 'Source_IP', 'Endpoint', 'Status_Code'])
    df.to_csv('server_logs.csv', index=False)
    print("--- SUCCESS: 'server_logs.csv' created with 1000 entries! ---")

if __name__ == "__main__":
    generate_logs()
