#!/usr/bin/env python3

import os
import sys
import re
import requests
from PIL import Image
from bs4 import BeautifulSoup
import shutil
import search
# from fpdf import FPDF

"""
Mirror Options:
    1. https://manganelo.com
    2. https://mangakalot.com
"""

MIRROR = 'https://manganelo.com/'

manga_name, manga_hash = search.display_search(' '.join(sys.argv[1:]))

if manga_name is None:
    exit(0)

URL_MANGA = MIRROR + 'manga/' + manga_hash
TITLE = manga_name
pattern = r'.*chapter\ [0-9]+'

chapters = []
chap_names = []
chap_list = []

inp_string = input('Enter the search query:\n')
inp_list = inp_string.split(' ')

if len(inp_list) == 1 and inp_list[0].isdigit():
    chap_list = int(inp_list[0])
elif len(inp_list) == 3 and inp_list[2] == 'range' and inp_list[0].isdigit() and inp_list[1].isdigit():
    chap_list = [i for i in range(int(inp_list[0]), int(inp_list[1]) + 1)]
elif all(i.isdigit() for i in inp_list):
    chap_list = [int(i) for i in inp_list]
else:
    print('Format:')
    print('========> 1. START_CHAP END_CHAP range')
    print('========> 2. CHAP_1 CHAP_2 CHAP_3 ... ')
    exit(0)

URL_CHAPTER = MIRROR + 'chapter/' + manga_hash + '/chapter_' + inp_list[0]
count = None


def process_chapter(url_list, chapter_url):
    """ Get the URLs of each page in the chapter """
    html = requests.get(chapter_url).content
    soup = BeautifulSoup(html, 'html.parser')
    for post in soup.find_all('div', {'class': 'vung-doc'}):
        for npost in post.find_all('img'):
            url_list.append(npost['src'])
    return url_list


def check(pattern, string):
    """ Check if string matches the regex pattern """
    if re.match(pattern, string) is not None:
        return True
    return False


def remove(path):
    """ param <path> could either be relative or absolute. """
    if os.path.isfile(path):
        os.remove(path)  # remove the file
    elif os.path.isdir(path):
        shutil.rmtree(path)  # remove dir and all contains
    else:
        raise ValueError("file {} is not a file or dir.".format(path))


# def make_pdf(pdfFileName, listPages, curr, parent):
#     """ Convert the batch of images into a PDF file """
#     if (parent):
#         parent += "/"
#     if (curr):
#         curr += "/"
#     cover = Image.open(curr + str(listPages[0]) + ".jpg")
#     width, height = cover.size
#     pdf = FPDF(unit="pt", format=[width, height])
#     for page in listPages:
#         pdf.add_page()
#         pdf.image(curr + str(page) + ".jpg", 0, 0)
#     pdf.output(parent + pdfFileName + ".pdf", "F")


def pil_open(string):
    """ Helper function for PIL Image opening """
    img = Image.open(string)
    if img.mode in ('RGBA', 'LA'):
        img = img.convert('RGB')
    img.load()
    return img


def make_pdf_simple(pdfFileName, listPages, curr, parent):
    """ Convert the batch of images into a PDF file using only PIL """
    if (parent):
        parent += "/"
    if (curr):
        curr += "/"
    cover = Image.open(curr + str(listPages[0]) + ".jpg")
    if cover.mode in ('RGBA', 'LA'):
        cover = cover.convert('RGB')
    cover.load()
    im_list = [pil_open(curr + str(page) + ".jpg") for page in listPages[1:]]
    cover.save(parent + pdfFileName + ".pdf", "PDF",
               resolution=100.0, save_all=True, append_images=im_list)


def download_chapter(num, chapter_url):
    """ Download #num chapter of the manga """
    if isinstance(num, int):
        curr = os.getcwd()
        new_dir = os.path.join(curr, 'chapter_' + str(num))
        if os.path.isdir(new_dir) is False:
            os.mkdir(new_dir)
        os.chdir(new_dir)
        url_list = process_chapter([], chapter_url)
        listPages = []
        i = 2
        for img_url in url_list:
            r = requests.get(img_url)
            with open('chapter_' + str(num) + '_' +
                      str(i) + '.jpg', 'wb') as f:
                f.write(r.content)
                listPages.append('chapter_' + str(num) + '_' + str(i))
                i += 1
        pid = os.fork()
        if pid > 0:
            os.chdir(curr)
        else:
            make_pdf_simple("chapter" + str(num), listPages, os.getcwd(), curr)
            remove(new_dir)
            exit(0)


if __name__ == '__main__':
    orig = os.getcwd()
    new_dir = os.path.join(orig, TITLE)
    if not os.path.isdir(new_dir):
        os.mkdir(new_dir)
    os.chdir(new_dir)
    for i in chap_list:
        pid = os.fork()
        if pid > 0:
            continue
        else:
            download_chapter(i, MIRROR + 'chapter/' +
                             manga_hash + '/chapter_' + str(i))
            print('Finished Chapter ' + str(i))
            exit(0)
    os.chdir(orig)
