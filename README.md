# DFS

Hosting and storing multiple small files in a single larger file-container (reducing multiple file open actions). Prove of concept.

* first results: 111Kb files load in ~800ms (rather slow)


## Installation

**Prerequisites**

* Python 2.7
* pip
* virtualenv
* uwsgi

## Usage

**Create volumes**

Create storage volumes for dfs, this will not overwrite existing files (by default, -f flag will overwrite).

```bash
./script/dfs init <target> <size_in_mb>
```

**Upload file**

Uploading multiple files through curl (example)

```bash
curl -iX POST http://localhost:5000/file/append -F "file[]=@path_to_file.ext" -F "file[]=@path_to_file2.ext"
```

## Development

**Running Local Server**

```bash
./script/dfs serve <target>
```

## Production

**Running wsgi server**

TODO: add config <target> options

```bash
uwsgi configs/wsgi.yml
```

**Nginx config**

* stub





