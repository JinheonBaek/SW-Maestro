import time
import requests

# Variables
_url = "https://westus.api.cognitive.microsoft.com/vision/v1.0/analyze"
_key = "cdd85ae8d3a448568e51d611ef9591ec"
_maxNumRetries = 3

def processRequest( json, data, headers, params ):
    """
    Parameters:
    json: Used when processing images from its URL.
    data: Used when processing image read from disk.
    headres: Used to pass the key information and the data type request
    """

    retries = 0
    result = None

    while True:
        response = requests.request( 'POST', _url, params = params, data = data, json = json, headers = headers )

        if response.status_code == 200 or response.status_code == 201:
            result = response.json()

        else:
            print(retries, _maxNumRetries)
            print( "Error code: %d" % (response.status_code) )
            print( "Error Message: %s" % (response.json()))

            if retries < _maxNumRetries:
                time.sleep(100)
                retries += 1
                continue
        
        break

    return result

'''
# URL direction to image
urlImage = 'https://oxfordportal.blob.core.windows.net/vision/Analysis/3.jpg'

params = { 'visualFeatures' : 'Categories, Tags, Description, Faces, ImageType, Color, Adult' }

headers = dict()
headers['Content-Type'] = 'application/json'
headers['Ocp-Apim-Subscription-Key'] = _key

json = { 'url' : urlImage }
data = None
'''

# Load raw image file into memory

pathToFileInDisk = r'C:\Temp\untitled.png'
with open ( pathToFileInDisk, 'rb' ) as f:
    data = f.read()

params = { 'visualFeatures' : 'Categories, Tags, Description, Faces, ImageType, Color, Adult' }

headers = dict()
headers['Content-Type'] = 'application/octet-stream'
headers['Ocp-Apim-Subscription-Key'] = _key

json = None

result = processRequest( json, data, headers, params )



# print result
print(result)
