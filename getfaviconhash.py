#This script can be used to fetch hash of an image. This can be used to fetch favicon hash values of components or organization logos and use in recon process using Shodan search.
#Shodan Query :  http.favicon.hash:-XXXXXXXXX (or XXXXXXXXX)

#first pip install mmh3 package

import mmh3
import requests
import codecs
 
response = requests.get('https://<domain>/favicon.ico')
favicon = codecs.encode(response.content,"base64")
hash = mmh3.hash(favicon)
print(hash)


#If this doesnt work try changing it to:
#r=requests.get('http://<domain>/favicon.ico',verify=False)
#print mmh3.hash(r.content.encode('base64'))
