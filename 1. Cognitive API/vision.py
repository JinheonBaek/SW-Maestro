import time
import requests
import cv2

# Variables
_url = "https://westus.api.cognitive.microsoft.com/vision/v1.0/analyze"
_key = "194ed79e69f9455f8c105258da687286"
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
img = cv2.imread(r"C:\Temp\untitled.png")
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
r, buf = cv2.imencode(".png", img)
data = bytearray(buf)

params = { 'visualFeatures' : 'Categories, Tags, Description, Faces, ImageType, Color, Adult' }

headers = dict()
headers['Content-Type'] = 'application/octet-stream'
headers['Ocp-Apim-Subscription-Key'] = _key

json = None

result = processRequest( json, data, headers, params )

# print result
print(result)
