import requests
import base64
from io import BytesIO
import pyads
import os 
import glob
import urllib3
import shutil

urllib3.disable_warnings()

AMSNETID = "192.168.1.15.1.1" #definition ads net id PLC 
plc = pyads.Connection(AMSNETID, pyads.PORT_TC3PLC1) #open connection in 192.168.31.224.1.1 and port TwinCat 851
plc.open()
print(f"Connected?: {plc.is_open}") #debugging statement, optional
print(f"Local Address? : {plc.get_local_address()}") #debugging statement, optional

path_plc = r'C:\Users\piotrp\Desktop\sutaj' 
path_plc_glob = r'C:\Users\piotrp\Desktop\sutaj/*'
path_lua = r'C:\Users\piotrp\Desktop\apka\new' 

def replace_lua():
    path = path_plc 
    path = glob.glob(f'{path}\*.lua')
    dst = path_lua
    
    if path:
        for src in path:
            if src:
                shutil.copy2(src, dst)
            else:
                print('Error transferring file')
                plc.write_by_name("MAIN.bErrTransferringFile", 1)
                break

def download(url): 
    status = 0
    import zipfile #url this is variable who receive value from plc
    filename = url.split('/')[-1]

    response = requests.get(url, verify=False) #off certificate because we had problems with authorization
    status = response.status_code
    print(status)
 
    plc.write_by_name("MAIN.nResPyCode", status)
    print('Downloading Completed')

    if status == 200: 
        zipfile= zipfile.ZipFile(BytesIO(response.content))
        zipfile.extractall(path_plc) #unzip 
    else: 
        print("The file was not downloaded correctly")

    if os.listdir(path_plc):
        replace_lua()
    else:

        print('Folder after unpacking is empty')



def clearDir(url):
    path = glob.glob(path_plc_glob)
    for file in path:
        os.remove(file) #search all directory and delete everything is this catalogue
 
    if not os.listdir(path_plc):
        print('Empty directory')
        download(url) #start download file from URL with token authorization JWT
    else: 
        print('There is something in the directory')
        plc.write_by_name("MAIN.bErrClearDir", 1)
        #Send error to PLC about something is wrong with clearing directory

def replace_lua():
    path = path_plc
    path = glob.glob(f'{path}\*.lua')

    if path:
        for src in path:
            if src:
                shutil.copy2(src, path_lua)
            else:
                print('Error with transferring lua file')

def main():
    while True:
        if plc.is_open: #realize all proces
            plc.write_by_name("MAIN.bPythonIsOn", 0) #information python in on 
            if plc.read_by_name("MAIN.bDownloadZip"):
                plc.write_by_name("MAIN.bDownloadZip", 0)
                nameUrl = plc.read_by_name("MAIN.sActualURL")
                print(nameUrl)
                clearDir(nameUrl)
                print("File is downloading")
        else: 
            print("ADS is disconnected") #close connection
            plc.close()
            plc.open()
        
main()