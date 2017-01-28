'''
Usage: python update_images.py [how] [url] [N_pictures]
e.g.
>>> python update_images.py
>>> python update_images.py add https://www.reddit.com/r/Animewallpaper/ 5

how : str
    What to do with newly discovered images.
        add - save to live-slideshow with other images
        replace - save to live-slideshow in place of other images

    Note: all images will be archived upon saving in the archive_path.
'''

import re
import os
import sys
import glob
import time
import shutil
import datetime
import requests
from PIL import Image
from bs4 import BeautifulSoup

date = datetime.datetime.now().strftime('%d_%m_%Y')

def main():

    # Define parameters / arguments
    try:
        how = sys.argv[1]
    except:
        how = 'add'
    try:
        url = sys.argv[2]
    except:
        url = 'https://www.reddit.com/r/pics/top/?sort=top&t=day'
    try:
        N_pictures = int(sys.argv[3])
    except:
        N_pictures = 10
    temp_path = os.path.join('static', '.temp')
    archive_path = os.path.join('static', 'archive')
    live_path = os.path.join('static', 'live-slideshow')

    # Run main scripts
    save_top_images(url, N_pictures, temp_path)
    files = glob.glob(os.path.join(temp_path, '*'))
    copy(files, archive_path)
    organize_images(how, files, live_path)


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
    for u in urls:
        f_type = u.split('.')[-1]
        if f_type not in ('jpg', 'jpeg', 'png', 'gif'):
            f_type = 'jpg'
        f_category = re.findall('^.*/r/([^/]*)', url)[0]
        f_name = '%s_%d_%s.%s' % (f_category, i+1, date, f_type)
        f_path = os.path.join(save_path, f_name)
        f = open(f_path, 'wb')
        try:
            img = requests.get(u)
            f.write(img.content)
            f.close()
            print('Saved image from %s' % u)
            try:
                with Image.open(f_path) as test:
                    i += 1 # Only increase the counter if the image is valid
            except OSError as e:
                print('Cannot open image %s' % f_path.split('/')[-1])
                os.remove(f_path)
        except:
            print('Cannot open URL: %s' % u)
            # Clean up if needed
            if os.path.exists(f_path):
                try:
                    f.close()
                    #os.remove(f_path)
                except:
                    pass
                os.remove(f_path)

def copy(files, save_path_final, clean=False):

    for f in files:
        f_ = f.split('/')[-1]
        f_ = os.path.join(save_path_final, f_)
        if clean:
            os.rename(f, f_)
        else:
            shutil.copyfile(f, f_)


def organize_images(how, files, save_path_final):

    if how == 'add':
        copy(files, save_path_final)

    elif how == 'replace':
        # Remove old files
        live_files = glob.glob(os.path.join(save_path_final, '*'))
        for f in live_files:
            os.remove(f)
        # Copy from temp
        copy(files, save_path_final, clean=True)



if __name__ == '__main__':
    main()
