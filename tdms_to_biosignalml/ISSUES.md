# Issues with the biosignalml Library

This document summarizes the issues encountered while using the `biosignalml` library to convert TDMS files to BioSignalML HDF5.

## 1. Installation

The version of `biosignalml` available on PyPI (0.5.0) is outdated and has a dependency issue with the `pint` library. To use the library, it was necessary to install it directly from the git repository:

```
pip install git+https://github.com/BioSignalML/biosignalml-python.git
```

## 2. Lack of Documentation

The `biosignalml` library lacks clear documentation and examples. This made it difficult to understand the library's API and how to perform basic tasks such as reading and writing BioSignalML HDF5 files.

## 3. Confusing API

The API of the `biosignalml` library is not always intuitive. The following issues were encountered:

*   **HDF5 file creation:** The `H5Recording.create` method requires a URI as the first argument, which is not clearly documented.
*   **Error handling:** The `biosignalml` library has a bug in the `create_from_graph` method of the `Recording` class that causes a `TypeError` when trying to read a BioSignalML HDF5 file. This was worked around by querying the graph directly for the signals.
