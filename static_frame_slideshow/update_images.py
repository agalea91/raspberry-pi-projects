import os
import datetime
import requests
from bs4 import BeautifulSoup
from PIL import Image

path = os.path.join('static', 'live-slideshow')
date = datetime.datetime.now().strftime('%d_%m_%Y')

url = 'https://www.reddit.com/r/pics/top/?sort=top&t=day'
N_pictures = 10

page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

elements = soup.findAll('p', {'class': 'title'})
urls = [e.findAll('a')[0]['href']
        for e in elements[:N_pictures]]

i = 0
for url in urls:
    f_path = os.path.join(path, '%d_%s.jpg' % (i+1, date))
    f = open(f_path, 'wb')
    try:
        img = requests.get(url)
        f.write(img.content)
        f.close()
        print('Saved image from %s' % url)
        try:
            with Image.open(f_path) as test:
                i += 1 # Only increase the counter if the image is valid
        except OSError as e:
            print('Cannot open image %s' % f_path.split('/')[-1])
            os.remove(f_path)
    except:
        print('Cannot open URL: %s' % url)
        # Clean up if needed
        if os.path.exists(f_path):
            try:
                f.close()
                os.remove(f_path)
            except:
                pass
            #os.remove(f_path)
