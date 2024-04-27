import sys, argparse, datetime, csv, os
sys.path.append(os.getcwd()+'/src/')

from api_obj import ret_tenableio_obj 
from tag_value_pairs import get_tags_and_values
from get_vulns import list_vulnerabilities
from csv_to_excel import convert_csv_to_xlsx
from colors import prWarning, prError, prMsg, prInfo

tio_obj = ret_tenableio_obj()

def check_tag(tag_name):
    temp_check_var = 0
    for tag in tio_obj.tags.list_categories():
        if tag.get('name') == tag_name:
            temp_check_var = 1
            break
    return temp_check_var

def check_tag_val(tag_name, tag_value):
    temp_check_var = 0
    for tag_val in tio_obj.tags.list(('category_name', 'eq', tag_name)): 
        if tag_val.get('value') == tag_value:
            temp_check_var = 1
            break
    return temp_check_var

def get_vulnerabilities(tag_name, tag_value, severity, user_dir_name):
    vulnerabilities = tio_obj.exports.vulns( tags=[(tag_name, tag_value)] )

    curr_date = datetime.datetime.now()
    day = str(curr_date.day)
    month = str(curr_date.strftime("%b"))	
    reports_dir = './' + user_dir_name + '/' + day + '-' + month + '-' + severity + '/'
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)

    file_name = tag_name + '_' + tag_value + '.csv'
    full_file_path = reports_dir + file_name
    file_status = list_vulnerabilities(vulnerabilities, full_file_path, severity)
    if file_status:
        if args.export == 'xlsx':
            convert_csv_to_xlsx(reports_dir)
            prMsg(f"{full_file_path} file created and converted to xlsx")
        else:
            prMsg(f"{full_file_path} file created")
    else:
        prInfo(f"No vulnerabilities found for {tag_name}:{tag_value}. CSV file is empty")

parser = argparse.ArgumentParser()
parser.add_argument("--tag", help = "Tag")
parser.add_argument("--value", help = "Corresponding Tag value")
parser.add_argument("--sev", help = "Severity",choices = ["critical", "high", "medium", "low"])
parser.add_argument("--export", help = "Export files. Default csv", choices = ["csv", "xlsx"], default='csv')
parser.add_argument("--list", action='store_true', help = "List tags and their corresponding values in TenableIO account. NOTE: Cannot be used with other flags")
parser.add_argument("--all", action='store_true', help = "Download reports for all tag value pairs. NOTE: Can be used with --sev and --exclude flags only")
parser.add_argument("--exclude", help = "Exclude any tag or tag value. NOTE: Can be used only with --all option. USAGE: 'tag=<tag_name>' or 'tag=<tag_name>,value=<tag_value>'")
parser.add_argument("--dir", help = "Directory for downloading reports. Default ./reports/")
args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

try:
    severity = args.sev
    exc_tag_val = None
    exclude_tag_val = None
    dir_name = 'reports'
    if args.dir:
        dir_name = args.dir

    if args.list:
        if len(sys.argv) > 2:
            prError("ERROR: --list option must be used alone")
            sys.exit(1)
        else:
            get_tags_and_values()
            sys.exit(1)
        
    elif args.all:
        if args.exclude:
            if ',' in args.exclude:
                exc = args.exclude.split(',')
                exclude_tag = exc[0].split('=')
                if exclude_tag[0] != 'tag':
                    prWarning("Check 'tag' spelling. USAGE: 'tag=<tag_name>' or 'tag=<tag_name>,value=<tag_value>'")
                    sys.exit(1)
                else:
                    exclude_tag_val = exclude_tag[1]
                    if check_tag(exclude_tag_val) != 1:
                        prError("ERROR: Incorrect tag provided. Use --list option to view all tag values")
                        sys.exit(1)

                exclude_tag_type = exc[1].split('=')
                if exclude_tag_type[0] != 'value':
                    prWarning("Check 'value' spelling. USAGE: 'tag=<tag_name>' or 'tag=<tag_name>,value=<tag_value>'")
                    sys.exit(1)
                else:
                    exclude_tag_type_val = exclude_tag_type[1]
                    if check_tag_val(exclude_tag_val, exclude_tag_type_val) != 1:
                        prError("ERROR: Incorrect tag value provided. Use --list option to view all tag values")
                        sys.exit(1)

            else:
                exc_tag = args.exclude.split('=')
                if exc_tag[0] != 'tag':
                    prWarning("Check 'tag' spelling. USAGE: 'tag=<tag_name>' or 'tag=<tag_name>,value=<tag_value>'")
                    sys.exit(1)
                else:
                    exc_tag_val = exc_tag[1]
                    if check_tag(exc_tag_val) != 1:
                        prError("ERROR: Tag found incorrect. Use --list option to view all tag values")
                        sys.exit(1)

        if severity == None:
            prWarning("Severity must be provided")
            sys.exit(1)
        for tag in tio_obj.tags.list_categories():
            tag_name = tag.get('name')
            if exc_tag_val == tag_name: 
                continue
            for tag_val in tio_obj.tags.list(('category_name', 'eq', tag_name)):
                tag_value = tag_val.get('value')
                if exclude_tag_val == tag_name and exclude_tag_type_val == tag_value:
                    continue
                get_vulnerabilities(tag_name, tag_value, severity, dir_name)
    else:    
        tag_name = args.tag
        if check_tag(tag_name) == 1:
            tag_value = args.value
            if tag_value != None: 
                if check_tag_val(tag_name, tag_value) != 1:
                    prError("ERROR: No value found for specified tag")
                    sys.exit(1)
            else:
                prError("ERROR: No tag value provided")
                sys.exit(1)
        else:
            prError("ERROR: No tag found")
            sys.exit(1)
        if severity == None:
            prError("ERROR: Severity must be provided")
            sys.exit(1)
        else:
            get_vulnerabilities(tag_name, tag_value, severity, dir_name)


except AttributeError as e:
    print(e)
    #prError("ERROR: No tag or corresponding tag value provided")
    sys.exit(1)
except KeyboardInterrupt:
    prError("ERROR: Program exited.")
    sys.exit(1)

