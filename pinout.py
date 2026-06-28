#!/usr/bin/env python3
import sys
import os
import json

# High-contrast escape definitions
BOLD = "\033[1m"
GREEN = "\033[32m"
CYAN = "\033[36m"
YELLOW = "\033[33m"
RED = "\033[31m"
RESET = "\033[0m"

def load_database():
    """Dynamically parses all json library maps inside the database directory."""
    database = {}
    script_dir = os.path.dirname(os.path.realpath(__file__))
    database_dir = os.path.join(script_dir, "database")
    
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
                pass
                
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

def about_tool():
    """Prints a brief metadata summary about the tool's goal."""
    print(f"\n{CYAN}{BOLD}ℹ️  About pinout-cli{RESET}")
    print(f"--------------------------------------------------")
    print(f"A blazing-fast, lightweight, offline hardware pinout dictionary.")
    print(f"Designed for engineering students and electronics makers to check")
    print(f"IC footprint configurations instantly without dragging down the workflow")
    print(f"or searching through endless manufacturer datasheets under a microscope.")
    print(f"\n{YELLOW}Version:{RESET} 1.1.0 (Modular Engine)")
    print(f"{YELLOW}License:{RESET} MIT")
    print(f"--------------------------------------------------\n")

def print_help(db):
    """Renders a comprehensive interface index of found chips."""
    print(f"\n{GREEN}{BOLD}pinout-cli — Modular Hardware Pinout Lookup Tool{RESET}")
    print(f"{BOLD}Usage:{RESET} pinout <chip-name>")
    print(f"       pinout [options]")
    print(f"\n{BOLD}Options:{RESET}")
    print(f"  -h, --help       Show this index help sheet and exit")
    print(f"  -a, --about      Show info about the tool project parameters")
    print(f"\n{BOLD}Available Components In Modular Storage:{RESET}")
    
    keys = sorted(list(db.keys()))
    aliases = ["dht22", "bluepill", "nodemcu", "hc-sr04", "esp32-s3"]
    keys = [k for k in keys if k not in aliases]
    
    for i in range(0, len(keys), 4):
        chunk = keys[i:i+4]
        print("  " + "".join(f"{k:<15}" for k in chunk))
    print(f"\n{CYAN}💡 Pro-Tip:{RESET} Drop any custom `.json` file inside the `database/` ")
    print("directory to expand the utility dynamically without changing script logic!\n")

def main():
    db = load_database()
    
    if len(sys.argv) < 2:
        print_help(db)
        sys.exit(0)
        
    # Standardize input flags by checking raw value first before stripping formatting characters
    raw_query = sys.argv[1].lower().strip()
    
    if raw_query in ["-a", "--about", "about"]:
        about_tool()
        return
        
    if raw_query in ["-h", "--help", "help"]:
        print_help(db)
        return
        
    # Process standard hardware query normalization
    query = raw_query.replace("-", "").replace(" ", "")
        
    if query in db:
        chip = db[query]
        print(f"\n{GREEN}{BOLD}=== {chip['name']} ==={RESET}")
        print(f"{CYAN}Info:{RESET} {chip['description']}")
        print(chip['ascii_art'])
    else:
        print(f"\n{RED}[!] Error: Component variant '{sys.argv[1]}' is unrecognized.{RESET}")
        print_help(db)

if __name__ == "__main__":
    main()
