# TDMS to BioSignalML Converter

This script converts data from a TDMS file to the BioSignalML format.

## Installation

First, install the required Python libraries:

```
pip install nptdms lxml git+https://github.com/BioSignalML/biosignalml-python.git
```

## Usage

```
python tdms_to_biosignalml.py <input_file> <output_file> [options]
```

### Arguments

*   `input_file`: The input TDMS file.
*   `output_file`: The output BioSignalML file.

### Options

*   `--verbose`: Enable verbose output.
*   `--list`: List all potential groups/channels in the TDMS file.
*   `--dry-run`: Describe what would be executed without doing it.
*   `--data <group/channel>`: Specify which data to convert in the format "group/channel". This argument can be used multiple times.

## Example

To convert all channels in `TestData.tdms` to `output.bsml`:

```
python tdms_to_biosignalml.py TestData.tdms output.bsml
```

To list all channels in `TestData.tdms`:

```
python tdms_to_biosignalml.py TestData.tdms --list
```

To convert only the `Devices/ECG` channel:

```
python tdms_to_biosignalml.py TestData.tdms output.bsml --data Devices/ECG
```
