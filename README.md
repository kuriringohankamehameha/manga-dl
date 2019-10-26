# manga-dl
A command line utility to download Manga and batch convert chapters into PDF

* Before using this program, make sure that you update your `PATH` environment variable to include the directory of the cloned repository or wherever you intend to keep the source files. 

* Windows users may need to update their `PYTHONPATH` environment variable. After that, you can invoke the scripts anywhere by specifying the absolute path if you want to run the script from anywhere. 
`python D:\manga-dl\manga_dl.py One Piece`
If you want to execute the script without specifying it's absolute path, again update suitable environment variables.

## Usage

Invoke with : `python manga_dl.py {MANGA_NAME}`

```bash
python manga_dl.py Attack on Titan

```

Example output:

```bash
+------+--------------------------------------+--------------------------------------------------------------+-----------------------------+
| S.No |              Manga Name              |                      Latest Chapter                          |         Update Time         |
+------+--------------------------------------+--------------------------------------------------------------+-----------------------------+
|  1   |           Attack On Titan            |       Vol.30 Chapter 122: From You, 2000 Years Ago           | Updated : Oct-05-2019 02:14 |
|  2   | Shingeki No Kyojin - Before The Fall |               Chapter 121: Future Memories                   | Updated : Oct-09-2019 08:14 |
|  3   |     Attack On Titan: Junior High     |            Vol.17 Final Chapter: To A New Age                | Updated : Oct-20-2018 12:56 |
|  4   |   Shingeki No Kyojin - Lost Girls    |          Chapter 64: Glimmer In The Umbral Dark              | Updated : Jan-08-2019 08:34 |
|  5   |  Shingeki No Kyojin - Birth Of Levi  |      Vol.5 Final Period: Farewell, Attack Junior High!       | Updated : Sep-05-2018 16:44 |
+------+--------------------------------------+--------------------------------------------------------------+-----------------------------+
Enter the Manga number: (Press 0 to exit)
1
Enter the search query:
121 122 range
```

* All the programs create subdirectories from the current directory in which the user invokes the program by default.

* We input a `range` query to fetch both the chapters 121 and chapter 122, which are saved as `chapter121.pdf` and `chapter122.pdf` in a new(if it doesn't exist already) subdirectory called `Attack On Titan`.

* Another search query can be a list of chapter/s to be fetched.

```
Enter the search query:
110 120 122
```

This fetches chapters 110, 120 and 122, which are saved in appropriate PDF files.

## Merging PDFs
Merging of multiple PDF files can be accomplished via `merge_manga.py`, which processes a batch sequence of PDFs or a list of PDFs in order and merges them into an output PDF file.

There are two ways of merging a batch of PDFs:

* Sequential Merging (Merges PDFs in a range in sequential order)

Invoke with : `python merge_manga.py {START_CHAPTER} {END_CHAPTER} {OUTPUT_PDF_NAME}` 

* List Merging (Merges a list of PDFs in order)

Invoke with : `python merge_manga.py {CHAPTER_X} {CHAPTER_Y} ..... {OUTPUT_PDF_NAME}`

Note : 

* OUTPUT_PDF_NAME can be space separated. It just needs to come after the Chapter Numbers.
* The Chapter numbers must be integers.

Example Output:

```bash
python merge_manga.py 120 122 Attack on Titan Latest
```
* This merges the files `chapter120.pdf`, `chapter121.pdf`, `chapter122.pdf` into `'Attack on Titan Latest.pdf'`. 

```bash

python merge_manga.py list 122 121 Jumbled Aot
```
* This way of merging takes in a list of the chapters, that is, here, `chapter122.pdf` and `chapter121.pdf` are merged into `'Jumbled Aot.pdf'`. Notice the order is subjected to how the user gives input, and is not sequential.

### Note
* The original PDFs are NOT deleted, and you may need to write a separate program which cleans up the output.

### TODO
* Add cleanup programs
