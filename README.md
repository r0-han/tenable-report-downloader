# Tenable IO report downloader

## Description

The intent behind this project is to download Tenable IO Vulnerability reports without exporting each report manually from Tenable IO findings page. 
- Currently only below headers are captured in the downloaded report:
	- `asset details  = agent_uuid, hostname, ipv4, operating_system`
	- `plugin details  = description, cve, id, name, solution, synopsis, see_also, exploit_available, has_patch`
	- `detected details  = first_found, last_found`
- To add/remove any other header you can edit the `src/get_vulns.py` file accordingly. 
- Only active/open vulnerabilities are captured in the report. 
- Vulnerabilities that have recasted/accepted state are not captured in the report.

## Installation

- Generate API keys from Tenable IO and add them in `src/.env` file.
- It is recommended to download this in a virtual env.
		```
		python3 -m venv tenable-report-downloader
		source tenable-report-downloader/bin/activate
		pip3 install -r requirements.txt
		```

## Usage
![Help menu](image/help.png)
