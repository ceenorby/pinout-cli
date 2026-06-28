#!/usr/bin/env python3
#!/usr/bin/env python3
import sys
import os
import json


def load_database():
    """Dynamically parses all json library maps inside the database directory."""
    database = {}
    # Determine directory location relative to script execution path
    script_dir = os.path.dirname(os.path.realpath(__file__))
    database_dir = os.path.join(script_dir, "database")  # <-- Changed from "data" to "database"
    
    if not os.path.exists(database_dir):
        return database
        
    for filename in os.listdir(database_dir):
        if filename.endswith(".json"):
            file_path = os.path.join(database_dir, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    file_data = json.load(f)
                    database.update(file_data)
            except Exception:
                pass # Gracefully skip broken formatting states
                
    # Append aliases dynamically
    if "dht11" in database:
        database["dht22"] = database["dht11"]
    if "stm32" in database:
        database["bluepill"] = database["stm32"]
    if "esp8266" in database:
        database["nodemcu"] = database["esp8266"]
    if "hcsr04" in database:
        database["hc-sr04"] = database["hcsr04"]
    if "esp32s3" in database:
        database["esp32-s3"] = database["esp32s3"]
        
    return database

def print_help(db):
    """Renders a comprehensive interface index of found chips."""
    # High-contrast escape definitions
    BOLD = "\033[1m"
    GREEN = "\033[32m"
    CYAN = "\033[36m"
    RED = "\033[31m"
    RESET = "\033[0m"

    print(f"\n{GREEN}{BOLD}pinout-cli — Modular Hardware Pinout Lookup Tool{RESET}")
    print(f"{BOLD}Usage:{RESET} pinout <chip-name>")
    print(f"       pinout [options]")
    print(f"\n{BOLD}Options:{RESET}")
    print(f"  -h, --help       Show this index help sheet and exit")
    print(f"\n{BOLD}Available Components In Modular Storage:{RESET}")
    
    keys = sorted(list(db.keys()))
    # Filter aliases out of visual list array
    aliases = ["dht22", "bluepill", "nodemcu", "hc-sr04", "esp32-s3"]
    keys = [k for k in keys if k not in aliases]
    
    for i in range(0, len(keys), 4):
        chunk = keys[i:i+4]
        print("  " + "".join(f"{k:<15}" for k in chunk))
    print(f"\n{CYAN}💡 Pro-Tip:{RESET} Drop any custom `.json` file inside the `database/` ")
    print("directory to expand the utility dynamically without changing script logic!\n")


def main():
    db = load_database()
    
    # High-contrast escape definitions for main execution errors
    BOLD = "\033[1m"
    GREEN = "\033[32m"
    CYAN = "\033[36m"
    RED = "\033[31m"
    RESET = "\033[0m"

    if len(sys.argv) < 2:
        print_help(db)
        sys.exit(0)
        
    query = sys.argv[1].lower().strip().replace("-", "").replace(" ", "")
    
    if query in ["help", "h", "help"]:
        print_help(db)
        return
        
    if query in db:
        chip = db[query]
        print(f"\n{GREEN}{BOLD}=== {chip['name']} ==={RESET}")
        print(f"{CYAN}Info:{RESET} {chip['description']}")
        print(chip['ascii_art'])
    else:
        if not db:
            print(f"\n{RED}[!] Error: The component database is empty! No JSON files were found or loaded.{RESET}")
        else:
            print(f"\n{RED}[!] Error: Component variant '{sys.argv[1]}' is unrecognized.{RESET}")
        print_help(db)


if __name__ == "__main__":
    main()
