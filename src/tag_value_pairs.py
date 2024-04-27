from tenable.io import TenableIO
from tabulate import tabulate
from api_obj import ret_tenableio_obj

tio_obj = ret_tenableio_obj()
table_header = ['S.No', 'Tag Name', 'Tag Value']
table = []

def get_tags_and_values():
    for tag in tio_obj.tags.list_categories():
        #pprint(type(tag)) --> dict
        tag_name = tag.get('name')
        val_list = []
        for tag_val in tio_obj.tags.list(('category_name', 'eq', tag_name)):
            val_list.append(tag_val.get('value'))
        table.append([tag_name, val_list])
    print(tabulate(table, table_header, showindex=True, numalign="center", tablefmt="outline"))

if __name__ == '__main__':
    get_tags_and_values()

