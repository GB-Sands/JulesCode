#!/usr/bin/env python

import argparse
from nptdms import TdmsFile
from biosignalml.formats.hdf5.h5recording import H5Recording
import numpy as np
import os

def main():
    parser = argparse.ArgumentParser(description='Convert a TDMS file to BioSignalML HDF5.')
    parser.add_argument('input_file', help='The input TDMS file.')
    parser.add_argument('output_file', help='The output BioSignalML HDF5 file.')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output.')
    parser.add_argument('--list', action='store_true', help='List all potential groups/channels in the TDMS file.')
    parser.add_argument('--dry-run', action='store_true', help='Describe what would be executed without doing it.')
    parser.add_argument('--data', nargs='+', help='Specify which data to convert in the format "group/channel".')

    args = parser.parse_args()

    if args.list:
        with TdmsFile.open(args.input_file) as tdms_file:
            for group in tdms_file.groups():
                for channel in group.channels():
                    print(f"{group.name}/{channel.name}")
        return

    if args.dry_run:
        print("Dry run enabled. The following actions would be taken:")
        print(f"1. Read the TDMS file: {args.input_file}")
        print(f"2. Create a new BioSignalML HDF5 file.")
        if args.data:
            print("3. Convert the following channels:")
            for item in args.data:
                print(f"   - {item}")
        else:
            print("3. Convert all channels in the TDMS file.")
        print(f"4. Write the BioSignalML HDF5 file to: {args.output_file}")
        return

    uri = "file://" + os.path.abspath(args.output_file)
    with TdmsFile.open(args.input_file) as tdms_file:
        if args.verbose:
            print(f"Reading TDMS file: {args.input_file}")

        h5_recording = H5Recording.create(uri, args.output_file, replace=True)

        data_to_convert = args.data
        if not data_to_convert:
            data_to_convert = [f"{group.name}/{channel.name}"
                               for group in tdms_file.groups()
                               for channel in group.channels()]

        for item in data_to_convert:
            group_name, channel_name = item.split('/')
            channel = tdms_file[group_name][channel_name]

            if args.verbose:
                print(f"Converting channel: {item}")

            signal_uri = f"{uri}/signal/{group_name}/{channel_name}"

            h5_recording.create_signal(
                signal_uri,
                units=channel.properties.get('unit_string', 'V'),
                data=channel[:],
                rate=1.0 / channel.properties.get('wf_increment')
            )

    h5_recording.close()

if __name__ == '__main__':
    main()
