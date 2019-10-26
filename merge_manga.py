#!python

from pdfrw import PdfReader, PdfWriter
import sys
import os

list_merge = False


def mergepdfs(titles, name):
    outfn = name + '.pdf'
    writer = PdfWriter()
    for inpfn in titles:
        writer.addpages(PdfReader(inpfn).pages)
    writer.write(outfn)


def exit_with_msg():
    print('Format: ')
    print('-----> 1. python merge_manga.py START_CHAPTER END_CHAPTER PDF_NAME')
    print('-----> 2. python merge_manga.py list CHAP_1 CHAP_2 ...... PDF_NAME')
    exit(0)


if len(sys.argv) < 4:
    exit_with_msg()
if not sys.argv[1].isdigit():
    if sys.argv[1] != 'list':
        exit_with_msg()
    if (not sys.argv[2].isdigit()) or (sys.argv[-1].isdigit()):
        exit_with_msg()
    list_merge = True

if list_merge:
    for index, i in enumerate(sys.argv[2:]):
        if i.isdigit():
            try:
                assert os.path.isfile("chapter" + str(i) + ".pdf")
            except AssertionError:
                print('The file {} does not exist. Download it and try again'
                      .format('chapter' + str(i) + '.pdf'))
                exit(0)
        else:
            max_index = index + 2
            break
    mergepdfs(["chapter" + str(i) + ".pdf"
               for i in sys.argv[2:max_index]],
              ' '.join(sys.argv[max_index:]))
else:
    assert int(sys.argv[1]) <= int(sys.argv[2])
    for i in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
        try:
            assert os.path.isfile("chapter" + str(i) + ".pdf")
        except AssertionError:
            print('The file {} does not exist. Download it and try again'
                  .format('chapter' + str(i) + '.pdf'))
            exit(0)
    mergepdfs(["chapter" + str(i) + ".pdf"
               for i in range(int(sys.argv[1]), int(sys.argv[2]) + 1)],
              ' '.join(sys.argv[3:]))
