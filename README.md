# Tenable IO report downloader

## Description
The intent behind this project is to download Tenable IO Vulnerability reports without exporting each report manually from Tenable IO findings page. 
- Currently only below headers are captured in the downloaded report:
	- `asset_header  = 'agent_uuid', 'hostname', 'ipv4', 'operating_system'`
	- `plugin_header  = 'description', 'cve', 'id', 'name', 'solution', 'synopsis', 'see_also', 'exploit_available', 'has_patch'`
	- `found_header  = 'first_found', 'last_found'`
- To add/remove any other header you can edit the `src/get_vulns.py` file accordingly. 
- Only active/open vulnerabilities are captured in the report. 
- Vulnerabilities that have recasted/accepted state are not captured in the report.

## Usage
