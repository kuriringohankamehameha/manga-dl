# manga-dl
A command line utility to download Manga and batch convert chapters into PDF/ZIP/CBZ

## Prerequisites
Install all requirements using 

```bash
pip install -r requirements.txt

```

Before using this program, make sure that you update your `PATH` environment variable to include the directory of the cloned repository or wherever you intend to keep the source files. 

By default, this converts the chapters into PDF unless you explicitly specify the save format as a flag.

## Update
The server seems to have changed, with a modified setup now in place. Please ensure that you don't indiscriminately request the overloaded servers.

There could also be some issues when pinging from Linux machines, so you may get some handshake errors. If you encounter this problem, consider reporting an issue.

### \*NIX Users (Linux / Mac)
\*NIX users can make the the files `manga_dl.py` and `merge_manga.py` executable via :

`chmod +x manga_dl.py` and `chmod +x merge_manga.py`.

You can run the program without explicitly invoking the `python` keyword, using :

`manga_dl.py Attack on titan`.

### Windows Users
Windows users may need to update their `PYTHONPATH` environment variable. After that, you can invoke the scripts anywhere by specifying the absolute path if you want to run the script from anywhere, run it like this:

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
120 122 range merge Aot Latest
```

The above query fetches chapters 120 to 122 and puts them in a PDF file called `Aot Latest.pdf`.

* All the programs create subdirectories from the current directory in which the user invokes the program by default.

There are two types of seach queries:

1. Range Query (`FIRST_CHAPTER LAST_CHAPTER range`)
    `120 122 range`

    We input a `range` query to fetch all the chapters between 120 and chapter 122 (both inclusive), which are saved as `chapter120.pdf`, `chapter121.pdf` and `chapter122.pdf` in a new(if it doesn't exist already) subdirectory called `Attack On Titan`. Note that this corresponds to the `Manga Name` field on the Table, and not the actual query itself, so there is no need to separately rename the directory if your query was too short.

2. List Query (`CHAPTER_X CHAPTER_Y CHAPTER_Z ...`)

    Another search query can be a list of chapter/s to be fetched.

    ```
    Enter the search query:
    110 120 122
    ```

    This fetches chapters 110, 120 and 122, which are saved in appropriate PDF files.

3. Merge Query 
    
    The `merge` keyword can be appended to the Query to merge the downloaded PDFs into a single file.
    
    `FIRST_CHAPTER LAST_CHAPTER range merge OUTPUT_PDF_NAME`

    `CHAPTER_X CHAPTER_Y CHAPTER_Z ... merge OUTPUT_PDF_NAME`

### Convert to `.zip` or `.cbz` (Comic Book Zip Format)
    
An additional flag `--cbz`/ `--zip` can be appended to the end of the query string to generate a `.cbz` / `.zip` file instead of a `.pdf` file in the merge query.

The below query merges chapters 1 to 20 in a file called `Volume1.cbz`:

`1 20 range merge Volume1 --cbz`

The below query puts chapters 1, 2 and 3 into `chapter1.zip`, `chapter2.zip` and `chapter3.zip`:

`1 2 3 --zip`

Note : All `CHAPTER_X`s are Integers.

## Merging PDFs
Merging of multiple PDF files can be accomplished via `merge_manga.py`, which processes a batch sequence of PDFs or a list of PDFs in order and merges them into an output PDF file.

There are two ways of merging a batch of PDFs:

### Sequential Merging (Merges PDFs in a range in sequential order)

Invoke with : `python merge_manga.py {START_CHAPTER} {END_CHAPTER} {OUTPUT_PDF_NAME}` 

Example Output:

```bash
python merge_manga.py 120 122 Attack on Titan Latest
```
This merges the files `chapter120.pdf`, `chapter121.pdf`, `chapter122.pdf` into `'Attack on Titan Latest.pdf'`. 

### List Merging (Merges a list of PDFs in order)

Invoke with : `python merge_manga.py list {CHAPTER_X} {CHAPTER_Y} ..... {OUTPUT_PDF_NAME}`

```bash

python merge_manga.py list 122 121 Jumbled Aot
```
This way of merging takes in a list of the chapters, that is, here, `chapter122.pdf` and `chapter121.pdf` are merged into `'Jumbled Aot.pdf'`. Notice the order is subjected to how the user gives input, and is not sequential.

Note : 

* `OUTPUT_PDF_NAME` can be space separated. It just needs to come after all the Chapter Numbers.
* The Chapter numbers must be integers.

### Perform Cleanup
The original PDFs can be removed after successful merging if the `--clean` flag is appended to the Merge Query.

Example:

```bash
python merge_manga.py list 120 121 122 Aot Latest Chapters --clean
```

```bash
python merge_manga.py 120 122 Aot Latest Chapters --clean
```

This flag must come at the very end

## Miscellaneous
### Note
* For Windows users, there is a time limit of upto 5 minutes to download a chapter. Change the `timeout` argument appropriately in `manga_dl.py` in the `main` module.
