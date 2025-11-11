# Issues with the biosignalml Library

This document summarizes the issues encountered while using the `biosignalml` library to convert TDMS files to BioSignalML.

## 1. Installation

The version of `biosignalml` available on PyPI (0.5.0) is outdated and has a dependency issue with the `pint` library. To use the library, it was necessary to install it directly from the git repository:

```
pip install git+https://github.com/BioSignalML/biosignalml-python.git
```

## 2. Lack of Documentation

The `biosignalml` library lacks clear documentation and examples. This made it difficult to understand the library's API and how to perform basic tasks such as reading and writing BioSignalML files.

## 3. Confusing API

The API of the `biosignalml` library is not always intuitive. The following issues were encountered:

*   **No dedicated reader/writer classes:** There are no `BioSignalMLReader` or `BioSignalMLWriter` classes. Instead, it is necessary to work with `biosignalml.rdf.Graph` objects directly.
*   **Adding data to signals and recordings:** To add data to a `Signal` object, you must set the `data` attribute directly. Similarly, to add signals to a `Recording` object, you must set the `signals` attribute. There are no `append` methods.
*   **RDF handling:** To create a BioSignalML file, you must create an `rdf.Graph` object and then add the recording and signals to it. This is not clearly documented.
*   **`recording.signals` is a method:** The `signals` attribute of a `Recording` object is a method, not a property. This is not immediately obvious.
*   **Loading signals from a graph:** When creating a `Recording` object from a graph, you must explicitly pass `signals=True` to the `create_from_graph` method to load the signals.
