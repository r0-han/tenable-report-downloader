# Tenable IO report downloader

## Description

The aim of this project is to download vulnerability findings reports from Tenable IO without manually exporting from the findings page.
- Currently only below headers are captured in the downloaded report:
	- `asset details  = agent_uuid, hostname, ipv4, operating_system`
	- `plugin details  = description, cve, id, name, solution, synopsis, see_also, exploit_available, has_patch`
	- `detected details  = first_found, last_found`
- To add/remove any other header you can edit the `src/get_vulns.py` file accordingly. 
- Only active/open vulnerabilities are captured in the report. 
- Vulnerabilities that have recasted/accepted state are not captured in the report.
- If you're using it for organizational purposes tenable recommends to use custom *User-Agent* Header in order to identify your integrations and help in troubleshooting. More on this can be read [here](https://developer.tenable.com/docs/user-agent-header)

## Installation

- [Generate API keys](https://docs.tenable.com/vulnerability-management/Content/Settings/my-account/GenerateAPIKey.htm) from Tenable IO and add them in `src/.env` file. 
- Clone the repository: `git clone https://github.com/Mrd0zz/tenable-report-downloader.git`
- Install required python3 modules: `cd tenable-report-downloader ; pip3 install -r requirements.txt`

## Usage
![Help menu](./help.png)

- List tags and corresponding tag values
	- `python3 main.py --list`

- Simple report download for any tag:value
	- `python3 main.py --tag <TAG_NAME> --value <TAG_VALUE> --sev critical` 

- Export report in xlsx format
	- `python3 main.py --tag <TAG_NAME> --value <TAG_VALUE> --sev critical --export xlsx`

- Specify download directory for the reports
	- `python3 main.py --tag <TAG_NAME> --value <TAG_VALUE> --sev critical --dir directory_name`

- Download report for all tag:value pairs 
	- `python3 main.py --all`

- Exclude any tag:value or a single tag 
	- `python3 main.py --all --exclude 'tag=<TAG_NAME>, value=<TAG_VALUE>'`
	- `python3 main.py --all --exclude 'tag=<TAG_NAME>'` 