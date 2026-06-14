#!/usr/bin/env python3
# Cybersecurity AI Tutor Agent
# Run: python3 agent.py

import json
import os
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from apis.cve_api import search_cve
from apis.mitre_api import search_technique
from apis.shodan_api import host_lookup

# Load API keys from .env file
load_dotenv()

# Try to import rich for pretty output - fallback to plain print
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from rich import print

    console = Console()
    banner = Panel.fit(
        "[bold cyan] CYBERTUTOR: AI SECURITY AGENT [/bold cyan]\n[italic white]Live Threat Intelligence & Local Llama 3[/italic white]",
        border_style="bright_blue",
        padding=(1, 2)
    )
    console.print(banner)
    USE_RICH = True
except ImportError:
    USE_RICH = False

# Try Ollama first, then OpenAI as fallback
try:
    import ollama
    USE_OLLAMA = True
except ImportError:
    USE_OLLAMA = False

OLLAMA_MODEL = "llama3" # Change to "mistral" or "phi3" if you prefer
LOG_FILE = Path("logs/session_log.json")
LOG_FILE.parent.mkdir(exist_ok=True)

SYSTEM_PROMPT = """You are CyberTutor, an expert cybersecurity professor
and ethical hacking instructor. You teach:
- Linux, Bash scripting, and command-line tools
- Networking (TCP/IP, DNS, subnets, firewalls, VPNs)
- Cloud security (AWS, GCP, Azure IAM, VPCs, S3)
- Ethical hacking and penetration testing (Kali, Metasploit, Nmap)
- MITRE ATT&CK framework (tactics, techniques, procedures)
- NIST Cybersecurity Framework (Identify, Protect, Detect, Respond, Recover)
- OSINT, reconnaissance, and information gathering
- SIEM, SOC operations, log analysis, threat detection
- Python and Bash scripting for security automation
- Encryption, cryptography, TLS/SSL, hashing
- Vulnerability assessment and CVE analysis
- Documentation and incident response reporting

Always explain with real commands, examples, and practical context.
When teaching commands, always show the syntax AND explain what each flag does.
Format responses clearly with sections and examples."""

def log_session(user_msg, agent_response):
    # Save each Q&A pair to the session log
    entry = {
        "timestamp": datetime.now().isoformat(),
        "user": user_msg,
        "agent": agent_response
    }
    logs = []
    if LOG_FILE.exists():
        try:
            with open(LOG_FILE) as f:
                logs = json.load(f)
        except Exception:
            logs = []
    logs.append(entry)
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)

def ask_ollama(messages):
    # Send messages to local Ollama LLM
    response = ollama.chat(
        model=OLLAMA_MODEL,
        messages=messages
    )
    return response["message"]["content"]

def ask_openai(messages):
    # Send messages to OpenAI API (fallback)
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    return resp.choices[0].message.content

def display(text):
    # Display the agent's response
    if USE_RICH:
        console.print(Panel(Markdown(text), title="[bold cyan]CyberTutor[/bold cyan]", border_style="cyan"))
    else:
        print("\n" + "="*60)
        print("CyberTutor:")
        print(text)
        print("="*60)

def main():
    
    conversation = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    while True:
        try:
            user_input = input("You: ").strip()
             # Add this inside your main loop to trigger the APIs
            if user_input.lower().startswith("cve "):
                keyword = user_input[4:].strip()
                print(f"Searching NVD for: {keyword}...")
                results = search_cve(keyword)

                conversation = conversation[:1]
        
                # New code: Feed results to the AI instead of printing them
                agent_context = f"Here is the live CVE data for {keyword}: {results}. Please summarize these vulnerabilities clearly for the user."
                conversation.append({"role": "system", "content": agent_context})
        
                          
                
            elif user_input.lower().startswith("mitre "):
                 keyword = user_input[6:].strip()
                 print(f"Searching MITRE ATT&CK for: {keyword}...")
                 results = search_technique(keyword)

                 conversation = conversation[:1]

                 agent_context = f"Here is the MITRE ATT&CK data for {keyword}: {results}. Please explain these techniques clearly."
                 conversation.append({"role": "system", "content": agent_context})
                
            elif user_input.lower().startswith("shodan "):
                 ip = user_input[7:].strip()
                 print(f"Querying Shodan for IP: {ip}...")
                 results = host_lookup(ip)

                 conversation = conversation[:1]
        
                 agent_context = f"Here is the Shodan data for IP {ip}: {results}. Please summarize this host information clearly."
                 conversation.append({"role": "system", "content": agent_context})

        except (EOFError, KeyboardInterrupt):
            print("\nSession ended.")
            break
            
        if not user_input:
            continue
            
        if user_input.lower() == "quit":
            print("Goodbye! Keep learning.")
            break
            
        if user_input.lower() == "history":
            if LOG_FILE.exists():
                with open(LOG_FILE) as f:
                    logs = json.load(f)
                print(f"\nYou have asked {len(logs)} questions total.")
                for i, entry in enumerate(logs[-5:], 1):
                    print(f" [{i}] {entry['user'][:80]}...")
            else:
                print("No history yet.")
            continue
            
        conversation.append({"role": "user", "content": user_input})
        print("\nThinking...\n")
        
        try:
            if USE_OLLAMA:
                response = ask_ollama(conversation)
            else:
                response = ask_openai(conversation)
        except Exception as e:
            print(f"Error: {e}")
            print("Is Ollama running? Start it with: ollama serve")
            continue
            
        conversation.append({"role": "assistant", "content": response})
        display(response)
        log_session(user_input, response)
        print()

if __name__ == "__main__":
    main()