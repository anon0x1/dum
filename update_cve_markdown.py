import requests

def fetch_cve_data():
    url = "https://services.nvd.nist.gov/rest/json/cves/1.0?resultsPerPage=100"
    response = requests.get(url)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response Content: {response.text[:500]}")  # Print the first 500 characters

    response.raise_for_status()  # Raise an error for HTTP issues

    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError:
        print("Failed to decode JSON.")
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

    if not cve_list:
        print("CVE list is empty.")
    else:
        print(f"Writing {len(cve_list)} CVEs to LATEST_CVES.md")

    with open("LATEST_CVES.md", "w") as file:
        file.write("# Latest Top 100 CVEs\n\n")
        file.write("\n".join(cve_list))

if __name__ == "__main__":
    data = fetch_cve_data()
    generate_markdown(data)
