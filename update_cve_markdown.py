import requests

def fetch_cve_data():
    url = "https://services.nvd.nist.gov/rest/json/cves/1.0?resultsPerPage=10"
    response = requests.get(url)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response Content: {response.text[:500]}")
    
    response.raise_for_status()  # Ensure we handle HTTP errors

    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError:
        print("Failed to decode JSON. The response may not be in JSON format.")
        return {}

    return data

def generate_markdown(cve_data):
    if not cve_data:
        print("No CVE data to write.")
        return
    
    cve_list = []
    for item in cve_data.get('result', {}).get('CVE_Items', []):
        cve_id = item['cve']['CVE_data_meta']['ID']
        description = item['cve']['description']['description_data'][0]['value']
        link = f"https://cve.mitre.org/cgi-bin/cvename.cgi?name={cve_id}"
        cve_list.append(f"- [{cve_id}]({link}): {description}")

    with open("LATEST_CVES.md", "w") as file:
        file.write("# Latest Top 10 CVEs\n\n")
        file.write("\n".join(cve_list))

if __name__ == "__main__":
    data = fetch_cve_data()
    generate_markdown(data)
