import requests
import json

# Fetch the latest CVEs from NVD
response = requests.get("https://services.nvd.nist.gov/rest/json/cves/1.0?resultsPerPage=100")
cve_data = response.json()

# Extract relevant information
cve_list = []
for cve in cve_data['result']['CVE_Items']:
    cve_id = cve['cve']['CVE_data_meta']['ID']
    description = cve['cve']['description']['description_data'][0]['value']
    link = f"https://cve.mitre.org/cgi-bin/cvename.cgi?name={cve_id}"
    cve_list.append(f"- [{cve_id}]({link}): {description}")

# Save to a Markdown file
with open("LATEST_CVES.md", "w") as file:
    file.write("# Latest Top 100 CVEs\n\n")
    file.write("\n".join(cve_list))
