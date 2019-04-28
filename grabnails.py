import requests
from PIL import Image
from urllib.request import urlopen
import io
import sys
import google_images_download   #importing the library
def go(s):
    orig_stdout = sys.stdout
    f = open('out.txt', 'w')
    sys.stdout = f

    response = google_images_download.googleimagesdownload()   #class instantiation

    arguments = {"keywords":s,"limit":5,"print_urls":True, 'no_download':True}

    paths = response.download(arguments)

    sys.stdout = orig_stdout
    f.close()

    data = open('out.txt', 'r')
    url = data.readlines()[2::2]
    del url[-1]
    del url[-1]
    urls = [i.split()[-1] for i in url[1:]]
    return urls
def im_id(i, s):
    url = go(s)
    img = Image.open(urlopen(url[i]))
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    url = "https://dialogs.yandex.net/api/v1/skills/fabc925e-2ada-4ea0-9143-c75947618944/images"
    headers = {
        'Authorization': "OAuth AQAAAAAc4bhNAAT7o9I-T9hCMkPXoL0nwVPPuDc",
        'cache-control': "no-cache"}

    response = requests.request("POST", url, files={'file': ('image.png', buf, 'jpg/png')}, headers=headers)
    return(response.json()['image']['id'])
