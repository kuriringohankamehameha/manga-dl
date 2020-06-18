#!/usr/bin/env python3

import time
from tqdm import tqdm
import os
import sys
import requests
from PIL import Image
from bs4 import BeautifulSoup
import shutil
import search
import merge_manga
import platform
from fake_useragent import UserAgent

ua = UserAgent()

headers = { 'User-Agent' : str(ua.chrome) }

machine = {'Linux': 'L', 'Windows': 'W', 'Darwin': 'M'}

session = requests.Session()

API_URL = 'https://manganelo.com/getstorysearchjson'

try:
    my_system = machine.get(platform.system(), 'E')
except KeyError:
    print('Error: System is not Linux/Windows/Mac')
    exit(0)

if my_system == 'E':
    print('Error: System is not Linux/Windows/Mac')
    exit(0)
elif my_system == 'W':
    if __name__ == '__main__':
        from multiprocessing import Pool
        pool = Pool()


def process_chapter(url_list, chapter_url, referral_url):
    """ Get the URLs of each page in the chapter """
    try:
        headers['referer'] = referral_url
        html = session.get(chapter_url, headers=headers).content
    except requests.exceptions.ConnectionError:
        print('Error while connecting. Try again')
    soup = BeautifulSoup(html, 'html.parser')
    for post in soup.find_all('div', {'class': 'container-chapter-reader'}):
        for npost in post.find_all('img'):
            url_list.append(npost['src'])
    return url_list


def remove(path):
    """ param <path> could either be relative or absolute. """
    if os.path.isfile(path):
        os.remove(path)  # remove the file
    elif os.path.isdir(path):
        shutil.rmtree(path)  # remove dir and all contains
    else:
        raise ValueError("file {} is not a file or dir.".format(path))


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


def make_zip(zipFileName, listPages, curr, parent, format='.zip'):
    """ Convert the batch of images into a zip file """
    import zipfile
    if (parent):
        parent += "/"
    if (curr):
        curr += "/"
    compression = zipfile.ZIP_DEFLATED
    zf = zipfile.ZipFile(parent + zipFileName + format, "w")
    try:
        for page in listPages:
            zf.write(curr + page + ".jpg", page + ".jpg", compress_type=compression)
    except FileNotFoundError:
        print("File Not Found")
    finally:
        zf.close()


def download_chapter(num, chapter_url, manga_dir, referral_url, format='pdf'):
    """ Download #num chapter of the manga """
    if isinstance(num, int):
        curr = manga_dir
        new_dir = os.path.join(curr, 'chapter_' + str(num))
        if os.path.isdir(new_dir) is False:
            os.mkdir(new_dir)
        os.chdir(new_dir)
        url_list = process_chapter([], chapter_url, referral_url)
        listPages = []
        i = 2
        headers['referer'] = chapter_url
        for img_url in url_list:
            r = session.get(img_url, headers=headers)
            if r.status_code != 200:
                raise ValueError('Server is not allowing requests from the client. Possible Cloudflare setup. Please file an issue here: https://github.com/kuriringohankamehameha/manga-dl')
            with open('chapter_' + str(num) + '_' +
                      str(i) + '.jpg', 'wb') as f:
                f.write(r.content)
            listPages.append('chapter_' + str(num) + '_' + str(i))
            i += 1
            # Avoid indiscriminate pinging. Be polite
            time.sleep(0.5)
        if my_system != 'W':
            pid = os.fork()
            if pid > 0:
                os.chdir(curr)
            else:
                if format == 'pdf':
                    make_pdf_simple("chapter" + str(num),
                                    listPages, os.getcwd(), curr)
                elif format in ('cbz', 'zip'):
                    make_zip("chapter" + str(num),
                             listPages, os.getcwd(), curr, '.' + format)
                else:
                    print('Format currently unsupported')
                    exit(0)
                remove(new_dir)
                print('Finished Chapter ' + str(num))
                exit(0)
        else:
            if format == 'pdf':
                make_pdf_simple("chapter" + str(num), listPages, os.getcwd(), curr)
            elif format in ('cbz', 'zip'):
                make_zip("chapter" + str(num),
                        listPages, os.getcwd(), curr, '.' + format)
            else:
                print('Format currently unsupported')
                exit(0)
            os.chdir(curr)
            remove(new_dir)
            print('Finished Chapter ' + str(num))


def exit_with_msg():
    print('Format:')
    print('========> 1. START_CHAP END_CHAP range')
    print('========> 1. START_CHAP END_CHAP range merge OUTPUT_PDF')
    print('========> 2. CHAP_1 CHAP_2 CHAP_3 ... ')
    print('========> 2. CHAP_1 CHAP_2 CHAP_3 ... merge OUTPUT_PDF')
    exit(0)


if __name__ == '__main__':
    """
    Mirror Options:
            1. https://manganelo.com
            2. https://mangakalot.com
    """

    MIRROR = 'https://manganelo.com/'

    manga_name, manga_hash = search.display_search(
        '_'.join(sys.argv[1:]).lower()
    )

    if manga_name is None:
        exit(0)

    URL_MANGA = MIRROR + 'manga/' + manga_hash
    TITLE = manga_name

    chapters = []
    chap_names = []
    chap_list = []
    doMerge = False
    fmt = 'pdf'

    inp_string = input('Enter the search query:\n')
    inp_list = inp_string.split(' ')

    if inp_list[-1] == '--cbz':
        del inp_list[-1]
        fmt = 'cbz'
    elif inp_list[-1] == '--zip':
        del inp_list[-1]
        fmt = 'zip'
    if inp_list[-1] == 'merge':
        exit_with_msg()
    try:
        idx = inp_list.index('merge')
        OUTPUT_PDF = inp_list[idx + 1:]
        doMerge = True
        inp_list = inp_list[:idx]
    except ValueError:
        pass

    if len(inp_list) == 1 and inp_list[0].isdigit():
        chap_list = [int(inp_list[0])]
    elif len(inp_list) == 3 and inp_list[2] == 'range' and inp_list[0].isdigit() and inp_list[1].isdigit():
        chap_list = [i for i in range(int(inp_list[0]), int(inp_list[1]) + 1)]
    elif all(i.isdigit() for i in inp_list):
        chap_list = [int(i) for i in inp_list]
    else:
        exit_with_msg()

    URL_CHAPTER = MIRROR + 'chapter/' + manga_hash + '/chapter_' + inp_list[0]
    count = None

    orig = os.getcwd()
    new_dir = os.path.join(orig, TITLE)
    if not os.path.isdir(new_dir):
        os.mkdir(new_dir)
    os.chdir(new_dir)
    if my_system != 'W':
        pids = []
        for i in chap_list:
            pid = os.fork()
            if pid > 0:
                pids.append(pid)
                continue
            else:
                download_chapter(i, MIRROR + 'chapter/' +
                                manga_hash + '/chapter_' + str(i),
                                new_dir, referral_url=URL_MANGA, format=fmt)
                exit(0)
    else:
        process_jobs = []
        BATCH_SIZE = 5
        size = len(chap_list)
        with tqdm(total=size) as pbar:
            for idx in range(0, size, BATCH_SIZE):
                batch_size = min(size - idx, BATCH_SIZE)
                batch = chap_list[idx: idx + batch_size]
                for i in batch:
                    process_jobs.append(pool.apply_async(download_chapter,
                        [i, MIRROR + 'chapter/' + manga_hash + '/chapter_' + str(i),
                            new_dir, URL_MANGA, fmt]))
                for job in process_jobs:
                    # A job takes a maximum time of 300 seconds
                    job.get(timeout=300)
                    pbar.update(1)

    if my_system != 'W':
        orig_len = len(pids)
        # Wait for the child processes to finish
        # while len(pids) > 0:
        for _ in tqdm(range(orig_len)):
            while True:
                # Increase progress bar only if the terminated process is one of the
                # spawned children
                pid, status = os.wait()
                if pid in pids:
                    pids.pop(pids.index(pid))
                    break
    if doMerge and fmt == 'pdf':
        time.sleep(1)
        merge_manga.perform_merge(
            ['merge_manga.py', 'list'] + [str(chap) for chap in chap_list] +
            OUTPUT_PDF + ['--clean']
            )
        print('Merged chapters into {}!'.format(' '.join(OUTPUT_PDF) + '.pdf'))
    os.chdir(orig)
