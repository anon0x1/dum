import requests

def fetch_cve_data():
    url = "https://services.nvd.nist.gov/rest/json/cves/1.0?resultsPerPage=10"  # Adjust as needed
    response = requests.get(url)
    
    # Print status code and response content for debugging
    print(f"Status Code: {response.status_code}")
    print(f"Response Content: {response.text[:500]}")  # Print only the first 500 characters for readability
    
    response.raise_for_status()  # Ensure we handle HTTP errors
    return response.json()

def generate_markdown(cve_data):
    cve_list = []
    for item in cve_data['result']['CVE_Items']:
        cve_id = item['cve']['CVE_data_meta']['ID']
        description = item['cve']['description']['description_data'][0]['value']
        link = f"https://cve.mitre.org/cgi-bin/cvename.cgi?name={cve_id}"
        cve_list.append(f"- [{cve_id}]({link}): {description}")

    with open("LATEST_CVES.md", "w") as file:
        file.write("# Latest Top 10 CVEs\n\n")  # Adjust title as needed
        file.write("\n".join(cve_list))

if __name__ == "__main__":
    data = fetch_cve_data()
    generate_markdown(data)
