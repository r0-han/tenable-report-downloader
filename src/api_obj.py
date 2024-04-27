from tenable.io import TenableIO
from dotenv import load_dotenv
import os, sys

def ret_tenableio_obj():
        load_dotenv()     
        TIO_ACCESS_KEY = os.getenv('TIO_ACCESS_KEY') 
        TIO_SECRET_KEY = os.getenv('TIO_SECRET_KEY') 
        if TIO_ACCESS_KEY == None:
            print("TIO_ACCESS_KEY environment variable not set")
            sys.exit(1)

        if TIO_SECRET_KEY == None:
            print("TIO_SECRET_KEY environment variable not set")
            sys.exit(1)
            
        tio = TenableIO(TIO_ACCESS_KEY, TIO_SECRET_KEY)
        return tio

if __name__ == "__main__":
    ret_tenableio_obj()
