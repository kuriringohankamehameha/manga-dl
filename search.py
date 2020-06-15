from bs4 import BeautifulSoup
import requests
from prettytable import PrettyTable
import platform
import sys

from manga_dl import headers, session, API_URL

import json

mirror = 'https://manganelo.com/search/'

post_list = []
name_list = []

if platform.system() != 'Windows':
    # For printing ANSI Colors in *NIX
    CRED = '\033[91m'
    CEND = '\033[0m'
    CYELLOW = '\033[93m'
    CBLUE = '\033[94m'
    CGREEN = '\033[92m'
else:
    # No xterm color support for Windows cmd
    CRED = ''
    CEND = ''
    CYELLOW = ''
    CBLUE = ''
    CGREEN = ''


def match_class(target):
    def do_match(tag):
        classes = tag.get('class', [])
        return all(c in classes for c in target)
    return do_match


def display_search(manga_name):
    payload = {'searchword': manga_name}
    
    response = session.post(API_URL, headers={**headers, 'content-type': 'application/x-www-form-urlencoded'}, data=payload)
    html = response.content

    content = json.loads(html)

    count = 0
    table = PrettyTable([CRED + 'S.No' + CEND,
                         CYELLOW + 'Manga Name' + CEND,
                         CBLUE + 'Latest Chapter' + CEND
                         ])
    for manga in content:
        post_list.append(manga['id_encode'])
        name_text = manga['name']
        soup = BeautifulSoup(name_text, features="lxml")
        name = ' '.join([s.contents[0] for s in soup.findAll('span')])
        if name is None or name.strip() == '':
            name = name_text
        last_chapter = manga['lastchapter']
        name_list.append(name)
        table.add_row([CGREEN + str(count + 1) + CEND,
            CBLUE + name + CEND,
            CGREEN + last_chapter + CEND])
        count += 1
    assert len(post_list) == count
    if count == 0:
        print('No manga named {}. Please enter another keyword'
              .format(' '.join(sys.argv[1:])))
        return (None, None)
    print(table)
    manga_num = int(input('Enter the Manga number: (Press 0 to exit)\n'))
    if manga_num == 0:
        return (None, None)
    if manga_num <= count:
        return name_list[manga_num-1], post_list[manga_num-1]
    print('Error. Index out of bounds. Maximum number is {}'.format(count))
    return (None, None)


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('Format: python search.py MANGA_NAME')
        exit(0)
    else:
        title = '_'.join(sys.argv[1:]).lower()
    display_search(title)
