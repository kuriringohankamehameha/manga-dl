#!/usr/bin/env python3

from pdfrw import PdfReader, PdfWriter
import sys
import os
import shutil


def mergepdfs(titles, name):
    outfn = name + '.pdf'
    writer = PdfWriter()
    for inpfn in titles:
        writer.addpages(PdfReader(inpfn).pages)
    writer.write(outfn)


def remove(path):
    """ param <path> could either be relative or absolute. """
    if os.path.isfile(path):
        os.remove(path)  # remove the file
    elif os.path.isdir(path):
        shutil.rmtree(path)  # remove dir and all contains
    else:
        raise ValueError("file {} is not a file or dir.".format(path))


def perform_cleanup_range(start_chapter, end_chapter):
    for i in range(start_chapter, end_chapter):
        remove(os.path.join(os.getcwd(), "chapter" + str(i) + ".pdf"))


def perform_cleanup_list(argList, start_index, end_index):
    for i in argList[start_index:end_index]:
        remove(os.path.join(os.getcwd(), "chapter" + str(i) + ".pdf"))


def exit_with_msg():
    print('Format: ')
    print('----> 1a. python merge_manga.py START_CHAPTER END_CHAPTER PDF_NAME')
    print('----> 1b. python merge_manga.py START_CHAPTER END_CHAPTER PDF_NAME'
          + ' --clean')
    print('----> 2a. python merge_manga.py list CHAP_1 CHAP_2 ..... PDF_NAME')
    print('----> 2b. python merge_manga.py list CHAP_1 CHAP_2 ..... PDF_NAME' +
          ' --clean')
    exit(0)


def perform_merge(argList, list_merge=False, do_cleanup=False):
    if len(argList) < 4:
        exit_with_msg()
    if argList[-1] == '--clean':
        argList.pop()
        do_cleanup = True
    if not argList[1].isdigit():
        if argList[1] != 'list':
            exit_with_msg()
        if (not argList[2].isdigit()) or (argList[-1].isdigit()):
            exit_with_msg()
        list_merge = True

    if list_merge:
        for index, i in enumerate(argList[2:]):
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
                   for i in argList[2:max_index]],
                  ' '.join(argList[max_index:]))
        if do_cleanup:
            perform_cleanup_list(argList, 2, max_index)
    else:
        assert int(argList[1]) <= int(argList[2])
        for i in range(int(argList[1]), int(argList[2]) + 1):
            try:
                assert os.path.isfile("chapter" + str(i) + ".pdf")
            except AssertionError:
                print('The file {} does not exist. Download it and try again'
                      .format('chapter' + str(i) + '.pdf'))
                exit(0)
        start_chapter, end_chapter = int(argList[1]), int(argList[2]) + 1
        mergepdfs(["chapter" + str(i) + ".pdf"
                   for i in range(start_chapter, end_chapter)],
                  ' '.join(argList[3:]))
        if do_cleanup:
            perform_cleanup_range(start_chapter, end_chapter)


if __name__ == '__main__':
    perform_merge(sys.argv)
