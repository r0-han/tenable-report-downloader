from tenable.io import TenableIO
from colors import prError
from dotenv import load_dotenv
import os, sys, requests

def ret_tenableio_obj():
        load_dotenv()     
        TIO_ACCESS_KEY = os.getenv('TIO_ACCESS_KEY') 
        TIO_SECRET_KEY = os.getenv('TIO_SECRET_KEY') 
        if not TIO_ACCESS_KEY.isalnum() or len(TIO_ACCESS_KEY) != 64:
            print("TIO_ACCESS_KEY environment variable incorrect")
            sys.exit(1)

        if not TIO_SECRET_KEY.isalnum() or len(TIO_SECRET_KEY) != 64:
            print("TIO_SECRET_KEY environment variable not incorrect")
            sys.exit(1)
            
        api_check_req = requests.get('https://cloud.tenable.com/scans', headers={"X-ApiKeys": f"accessKey={TIO_ACCESS_KEY};secretKey={TIO_SECRET_KEY}"})
        if api_check_req.status_code == 401:
            prError("Wrong API key provided")
            sys.exit(1)
        else:
            tio = TenableIO(TIO_ACCESS_KEY, TIO_SECRET_KEY)

        return tio

if __name__ == "__main__":
    ret_tenableio_obj()
