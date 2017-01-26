'''
Usage: python update_images.py [url] [N_pictures]
e.g.
>>> python update_images.py
>>> python update_images.py https://www.reddit.com/r/Animewallpaper/ 5
'''

import os
import sys
import time
import datetime
import requests
from PIL import Image
from bs4 import BeautifulSoup

date = datetime.datetime.now().strftime('%d_%m_%Y')

def main():

    # Define parameters / arguments
    try:
        url = sys.argv[1]
    except:
        url = 'https://www.reddit.com/r/pics/top/?sort=top&t=day'
    try:
        N_pictures = int(sys.argv[2])
    except:
        N_pictures = 10
    save_path = os.path.join('static', 'live-slideshow')

    # Run the script
    save_top_images(url, N_pictures, save_path)


def save_top_images(url, N_pictures, save_path):
    ''' Save the top images on a reddit.com page to your
    local machine.

    url : str
        Reddit URL from which to find pictures.

    N_pictures : int
        Number of pictures to (attempt to) save.

    save_path : str
        Where to save images on local machine.
    '''

    page = requests.get(url)
    # Make sure the page loded properly
    if page.status_code != 200:
        # Wait and try again
        time.sleep(3)
        save_top_images(url, N_pictures, save_path)

    soup = BeautifulSoup(page.content, 'html.parser')

    elements = soup.findAll('p', {'class': 'title'})
    urls = [e.findAll('a')[0]['href']
            for e in elements[:N_pictures]]

    i = 0
    for url in urls:
        f_type = url.split('.')[-1]
        if f_type not in ('jpg', 'jpeg', 'png', 'gif'):
            f_type = 'jpg'
        f_path = os.path.join(save_path, '%d_%s.%s' % (i+1, date, f_type))
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
                    #os.remove(f_path)
                except:
                    pass
                os.remove(f_path)

if __name__ == '__main__':
    main()
