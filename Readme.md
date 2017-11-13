# nb_compress

## What's this ?

This is a command line tool to remove unwanted information from jupyter notebook.

This may be useful when you print an ipynb file, so that you can have less pages.

## How to use

### Example

```
$ python nb_compress.py -o compressed.ipynb --first-last-epoch --no-image --no-traceback input.ipynb
```

### filter options

--first-last-epoch: show first and last epochs only

--no-image: cut image code

--no-traceback: cut traceback code

--no-execution-count: clear execution count

#### other general options

-o, --output: output filename
-h, --help: show help

## License

MIT