# importing necessary modules
import base64
import requests, zipfile
from io import BytesIO
import jwt

#url = 'https://api.chm.pl/v1/marking/programs/sl08_xyz.zip'
# previous context
#https_handler = urllib.request.HTTPSHandler(context=ssl.SSLContext)
#opener = urllib.request.build_opener(https_handler)
#ret = opener.open(url, timeout=2)



print('Downloading started')
#HMACSHA256(base64UrlEncode(header) + ’.’ + base64UrlEncode(payload), secret) // token autoryrazji https://blog.i-systems.pl/json-web-tokens-jwt/

#key = "secret"
#encoded = jwt.encode({"some": "payload"}, key, algorithm="HS256")
#print(encoded)

authorization = str(base64.b64encode(bytes(':'+ ' ', 'ascii')), 'ascii')
print(authorization)


#headers = {
# 'Accept': 'application/json',
# 'Authorization': 'Basic '+authorization
#}

#Defining the zip file URL
#url = 'https://zipextractor.app/'
#url = 'https://api.chm.pl/v1/marking/programs/sl08_xyz.zip'
url = 'https://www.learningcontainer.com/wp-content/uploads/2020/05/sample-zip-file.zip'

# Split URL to get the file name
filename = url.split('/')[-1]
print(filename)

# Downloading the file by sending the request to the URL
response = requests.get(url)
print(response)
print('Downloading Completed')

# extracting the zip file contents
zipfile= zipfile.ZipFile(BytesIO(response.content))
zipfile.extractall(r'C:\Users\piotrp\Desktop\sutaj')


