#!/usr/bin/env python3
"""
Löneprocess API - Run both v1 and v2 in parallel
Startar både API v1 (port 8000) och v2 (port 8001) samtidigt
"""

import subprocess
import time
import sys
import os
from pathlib import Path

# Colors for terminal output
class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'='*70}{Colors.RESET}")
    print(f"{Colors.GREEN}{text}{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}{'='*70}{Colors.RESET}\n")

def print_info(text):
    print(f"{Colors.YELLOW}ℹ️  {text}{Colors.RESET}")

def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")

def print_error(text):
    print(f"{Colors.RED}✗ {text}{Colors.RESET}")

def main():
    # Get the directory of this script
    script_dir = Path(__file__).parent.absolute()
    api_dir = script_dir / "loneprocess-api"
    
    if not api_dir.exists():
        print_error(f"API directory not found: {api_dir}")
        sys.exit(1)
    
    print_header("🚀 Löneprocess API - Running v1 and v2 in Parallel")
    
    # Change to API directory
    os.chdir(api_dir)
    
    print_info("Starting API v1 on port 8000...")
    print(f"  Command: python standalone_api.py")
    
    try:
        # Start v1
        process_v1 = subprocess.Popen(
            [sys.executable, "standalone_api.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print_success(f"API v1 started (PID: {process_v1.pid})")
        
        time.sleep(2)
        
        print_info("Starting API v2 on port 8001...")
        print(f"  Command: python standalone_api_v2.py --port 8001")
        
        # Start v2
        process_v2 = subprocess.Popen(
            [sys.executable, "standalone_api_v2.py", "--port", "8001"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print_success(f"API v2 started (PID: {process_v2.pid})")
        
        print_header("✅ Both APIs are now running!")
        
        print(f"{Colors.YELLOW}📊 API Status:{Colors.RESET}")
        print(f"   {Colors.CYAN}v1 Swagger UI:     http://localhost:8000/docs{Colors.RESET}")
        print(f"   {Colors.CYAN}v1 ReDoc:          http://localhost:8000/redoc{Colors.RESET}")
        print(f"   {Colors.CYAN}v1 Health:         http://localhost:8000/health{Colors.RESET}")
        print()
        print(f"   {Colors.CYAN}v2 Swagger UI:     http://localhost:8001/docs{Colors.RESET}")
        print(f"   {Colors.CYAN}v2 ReDoc:          http://localhost:8001/redoc{Colors.RESET}")
        print(f"   {Colors.CYAN}v2 Health:         http://localhost:8001/health{Colors.RESET}")
        
        print(f"\n{Colors.YELLOW}📝 Process IDs:{Colors.RESET}")
        print(f"   v1: {process_v1.pid}")
        print(f"   v2: {process_v2.pid}")
        
        print(f"\n{Colors.YELLOW}🛑 To stop the APIs:{Colors.RESET}")
        print(f"   - Press Ctrl+C to stop both")
        print(f"   - Or kill processes: kill {process_v1.pid} {process_v2.pid}")
        
        print(f"\n{Colors.CYAN}{Colors.BOLD}{'='*70}{Colors.RESET}\n")
        
        # Wait for processes
        while True:
            if process_v1.poll() is not None:
                print_error("API v1 has stopped!")
                break
            if process_v2.poll() is not None:
                print_error("API v2 has stopped!")
                break
            time.sleep(1)
    
    except KeyboardInterrupt:
        print_info("Stopping APIs...")
        process_v1.terminate()
        process_v2.terminate()
        time.sleep(1)
        
        if process_v1.poll() is None:
            process_v1.kill()
        if process_v2.poll() is None:
            process_v2.kill()
        
        print_success("APIs stopped")
        sys.exit(0)
    
    except Exception as e:
        print_error(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
