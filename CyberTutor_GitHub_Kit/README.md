# CyberTutor: AI-Powered Security Agent

CyberTutor is a locally-hosted AI cybersecurity assistant running on Llama 3. It provides an interactive terminal interface to query and summarize live threat intelligence data.

## Features
* **Local LLM Processing:** Uses Ollama and Llama 3 to ensure zero data leakage.
* **Vulnerability Tracking:** Fetches real-time CVE data from the National Vulnerability Database.
* **Adversary Tactics:** Integrates with MITRE ATT&CK to explain TTPs.
* **Infrastructure Recon:** Queries Shodan to profile IP addresses and open ports.
* **Modern UI:** Styled terminal interface using the `rich` library.
* **Session Auditing:** Automatically logs all queries and AI responses.

## Setup Instructions
1. Install requirements: `pip install -r requirements.txt`
2. Install Ollama and pull the Llama 3 model: `ollama run llama3`
3. Create a `.env` file in the root directory and add your Shodan API key:
   `SHODAN_API_KEY=your_key_here`
4. Run the agent: `python3 agent.py`
