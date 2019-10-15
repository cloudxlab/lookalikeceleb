from bs4 import BeautifulSoup
import requests
import time
import urllib.request

def has_class_image(tag):
    return tag.has_attr('class') and 'lister-item-image' in tag.attrs['class']

def get_actors_from_html(html):
    soup = BeautifulSoup(html)
    divs = soup.find_all(has_class_image)
    actors = []
    for div in divs:
        uid = div.a['href'].split('/')[2]
        name = div.img['alt']
        url = div.img['src']
        actors.append((url, uid+name))
        print("Actor: ", name)
    return actors

def download_html_from_url(url):
    r = requests.get(url)
    return r.text

def download_and_save_image(url, local_filename):
    urllib.request.urlretrieve(url, local_filename)
    

def get_all_pages(start_page, file):
    for i in range(start_page, 11):
        url = "https://www.imdb.com/list/ls058011111/?sort=list_order,asc&mode=detail&page=" + str(i)
        print("Downloading Page: ", i)
        html = download_html_from_url(url)
        actors = get_actors_from_html(html)
        print("Saving....")
        for actor in actors:
            file.write("%s\t%s\n" % actor)
        print("Page Finished: ", i)
        time.sleep(1)

import os

if __name__ == '__main__':
    # with open("result.txt", "w+") as out_file:
    #     get_all_pages(11, out_file)
        
    with open("result.txt") as results:
        for result in results:
            (url, name) = result.strip().split("\t")
            filename = "images/" + name + ".jpg"
            exists = os.path.isfile(filename)
            if exists:
                print("File", filename, "already exists")
            else:
                print("Downloading: ", filename)
                download_and_save_image(url, filename)
                time.sleep(1)

