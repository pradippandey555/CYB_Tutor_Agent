# apis/cve_api.py
import requests

# Look up CVEs using NIST NVD API
def search_cve(keyword, max_results=5):
    url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    params = {"keywordSearch": keyword, "resultsPerPage": max_results}
    
    try:
        resp = requests.get(url, params=params, timeout=15)
        if resp.status_code != 200:
            return []
            
        data = resp.json()
        results = []
        
        for item in data.get("vulnerabilities", []):
            cve = item["cve"]
            cve_id = cve["id"]
            desc = cve["descriptions"][0]["value"][:200]
            metrics = cve.get("metrics", {})
            cvss_list = metrics.get("cvssMetricV31", metrics.get("cvssMetricV2", []))
            
            score = "N/A"
            if cvss_list:
                score = cvss_list[0]["cvssData"].get("baseScore", "N/A")
                
            results.append({"id": cve_id, "score": score, "description": desc})
            
        return results
    except Exception as e:
        print(f"Error fetching CVEs: {e}")
        return []

if __name__ == "__main__":
    keyword = input("Search CVEs for: ")
    cves = search_cve(keyword)
    for c in cves:
        print(f"[{c['id']}] CVSS Score: {c['score']}")
        print(f" {c['description']}...\n")