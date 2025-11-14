# TDMS to BioSignalML HDF5 Converter

This script converts data from a TDMS file to the BioSignalML HDF5 format.

## Installation

First, install the required Python libraries:

```
pip install nptdms lxml h5py git+https://github.com/BioSignalML/biosignalml-python.git
```

## Usage

```
python -m tdms_to_biosignalml.tdms_to_biosignalml <input_file> <output_file> [options]
```

### Arguments

*   `input_file`: The input TDMS file.
*   `output_file`: The output BioSignalML HDF5 file.

### Options

*   `--verbose`: Enable verbose output.
*   `--list`: List all potential groups/channels in the TDMS file.
*   `--dry-run`: Describe what would be executed without doing it.
*   `--data <group/channel>`: Specify which data to convert in the format "group/channel". This argument can be used multiple times.

## Example

To convert all channels in `TestData.tdms` to `TestData.h5`:

```
python -m tdms_to_biosignalml.tdms_to_biosignalml tdms_to_biosignalml/tests/TestData.tdms tdms_to_biosignalml/tests/TestData.h5
```

To list all channels in `TestData.tdms`:

```
python -m tdms_to_biosignalml.tdms_to_biosignalml tdms_to_biosignalml/tests/TestData.tdms --list
```

To convert only the `Devices/ECG` channel:

```
python -m tdms_to_biosignalml.tdms_to_biosignalml tdms_to_biosignalml/tests/TestData.tdms tdms_to_biosignalml/tests/TestData.h5 --data Devices/ECG
```
