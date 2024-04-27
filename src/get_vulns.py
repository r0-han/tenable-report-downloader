import os, csv, pandas as pd

def list_vulnerabilities(vulns, file_path, severity):
    asset_header = ['agent_uuid', 'hostname', 'ipv4', 'operating_system']
    plugin_header = ['description', 'cve', 'id', 'name', 'solution', 'synopsis', 'see_also', 'exploit_available', 'has_patch']
    found_header = ['first_found', 'last_found']
    csv_header = asset_header + plugin_header + found_header

    with open(f'{file_path}', "w") as f:
        write = csv.writer(f)
        write.writerow(csv_header)

    vuln_entry_in_csv = {}
    to_check_key = 'recast_rule_uuid'
    for vuln in vulns:
        if vuln['severity'] == severity and to_check_key not in vuln:
            for asset_head in asset_header:
                vuln_entry_in_csv[asset_head] = vuln['asset'].get(asset_head)
            for plugin_head in plugin_header:
                vuln_entry_in_csv[plugin_head] = vuln['plugin'].get(plugin_head)
            for found_head in found_header:
                vuln_entry_in_csv[found_head] = vuln.get(found_head)[:10]

            with open(f'{file_path}', "a") as fi:
                write = csv.writer(fi)
                write.writerow(vuln_entry_in_csv.values())

    df = pd.read_csv(f'{file_path}')
    if df.empty:
        os.remove(file_path)
        return 0
    else:
        return 1
