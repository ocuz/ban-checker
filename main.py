import requests,time,os

def scrape_users():
    file_path = input("Enter path to ids file: ").strip()
    
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    
    with open(file_path, 'r') as f:
        ids = [line.strip() for line in f if line.strip()]
    
    print(f"Loaded {len(ids)} user IDs")
    
    start_idx = 0
    
    for i in range(start_idx, len(ids)):
        user_id = ids[i]
        url = f"https://users.roblox.com/v1/users/{user_id}"
        
        while True:
            try:
                response = requests.get(url, timeout=10)
                
                if response.status_code == 429:
                    print(f"Rate limited at id {user_id}, waiting 3 seconds...")
                    time.sleep(3)
                    continue
                
                if response.status_code == 200:
                    data = response.json()
                    name = data.get('name', 'Unknown')
                    is_banned = data.get('isBanned', False)
                    
                    filename = "true.txt" if is_banned else "false.txt"
                    with open(filename, 'a') as f:
                        f.write(f"{user_id}-{name}\n")
                    
                    status = "BANNED" if is_banned else "NOT BANNED"
                    print(f"[{i+1}/{len(ids)}] {user_id}-{name}: {status}")
                    break
                
                else:
                    print(f"Error {response.status_code} for ID {user_id}")
                    break
                    
            except Exception as e:
                print(f"Error processing ID {user_id}: {e}")
                break
    
    print("Scraping completed")

if __name__ == "__main__":
    scrape_users()
