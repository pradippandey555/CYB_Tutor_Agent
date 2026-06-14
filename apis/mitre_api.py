# apis/mitre_api.py
import requests, json

# Fetch MITRE ATT&CK techniques
def get_all_techniques():
    url = ("https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json")
    data = requests.get(url).json()
    techniques = []
    
    for obj in data.get("objects", []):
        if obj.get("type") == "attack-pattern":
            name = obj.get("name", "")
            ext = obj.get("external_references", [{}])[0]
            tid = ext.get("external_id", "")
            desc = obj.get("description", "")[:150]
            techniques.append({"id": tid, "name": name, "desc": desc})
            
    return techniques

def search_technique(keyword):
    techniques = get_all_techniques()
    results = [t for t in techniques 
               if keyword.lower() in t["name"].lower() 
               or keyword.lower() in t["desc"].lower()]
    return results

if __name__ == "__main__":
    results = search_technique("phishing")
    for t in results[:5]:
        print(f"[{t['id']}] {t['name']}")
        print(f" {t['desc']}\n")