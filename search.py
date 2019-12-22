from bs4 import BeautifulSoup
import requests
import sys
from prettytable import PrettyTable
import platform

mirror = 'https://manganelo.com/search/'

title = ''

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

if len(sys.argv) < 2:
    print('Format: python search.py MANGA_NAME')
    exit(0)
else:
    title = '_'.join(sys.argv[1:]).lower()


def match_class(target):
    def do_match(tag):
        classes = tag.get('class', [])
        return all(c in classes for c in target)
    return do_match


def display_search(manga_name):
    html = requests.get(mirror + title).content
    soup = BeautifulSoup(html, 'html.parser')
    count = 0
    table = PrettyTable([CRED + 'S.No' + CEND,
                         CYELLOW + 'Manga Name' + CEND,
                         CBLUE + 'Latest Chapter' + CEND,
                         CGREEN + 'Update Time' + CEND])
    for post, recent_chap, update_time in zip(
            # soup.find_all(match_class(["search-story-item"])),
            soup.find_all(match_class(["item-right"])),
            soup.find_all(match_class(["item-chapter"])),
            # soup.find_all('span')[4::3]
            soup.find_all(match_class(["item-time"]))[::2]
    ):
        table.add_row([CGREEN + str(count+1) + CEND,
                       CBLUE + post.h3.text.strip() + CEND,
                       CGREEN + recent_chap.text.strip() + CEND,
                       CYELLOW + update_time.text.strip() + CEND])
        name_list.append(post.h3.text.strip())
        count += 1
        for npost in post.h3.find_all('a'):
            post_list.append(npost['href'].split('/')[-1])
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
