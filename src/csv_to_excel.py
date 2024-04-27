import pandas as pd
import os

def convert_csv_to_xlsx(csv_folder):
    csv_files = [f for f in os.listdir(csv_folder) if f.endswith('.csv')]
    for csv_file in csv_files:
        csv_path = os.path.join(csv_folder, csv_file)
        df = pd.read_csv(csv_path)
        xlsx_file = os.path.splitext(csv_file)[0] + '.xlsx'
        xlsx_path = os.path.join(csv_folder, xlsx_file)
        df.to_excel(xlsx_path, index=False)
