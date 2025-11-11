#!/usr/bin/env python

import argparse
from nptdms import TdmsFile
import biosignalml.model as v1
import biosignalml.rdf as rdf
from biosignalml.model.ontology import BSML
import numpy as np
import os

def main():
    parser = argparse.ArgumentParser(description='Convert a TDMS file to BioSignalML.')
    parser.add_argument('input_file', help='The input TDMS file.')
    parser.add_argument('output_file', nargs='?', help='The output BioSignalML file.')
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

    if not args.output_file:
        parser.error("the following arguments are required: output_file")

    if args.dry_run:
        print("Dry run enabled. The following actions would be taken:")
        print(f"1. Read the TDMS file: {args.input_file}")
        print(f"2. Create a new BioSignalML recording.")
        if args.data:
            print("3. Convert the following channels:")
            for item in args.data:
                print(f"   - {item}")
        else:
            print("3. Convert all channels in the TDMS file.")
        print(f"4. Write the BioSignalML recording to: {args.output_file}")
        return

    with TdmsFile.open(args.input_file) as tdms_file:
        if args.verbose:
            print(f"Reading TDMS file: {args.input_file}")

        uri = "file://" + os.path.abspath(args.output_file)
        recording = v1.Recording(uri)
        signals = []

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

            # Create a signal
            signal_uri = f"{uri}/signal/{group_name}/{channel_name}"
            signal = recording.new_signal(signal_uri,
                                          units=channel.properties.get('unit_string', 'V'))

            # Add data to the signal
            signal.data = channel[:]

            # Add signal to the list
            signals.append(signal)

    if args.verbose:
        print(f"Writing BioSignalML file to: {args.output_file}")

    graph = rdf.Graph(uri)
    graph.add_statements(recording.metadata_as_stream())
    for signal in signals:
        graph.add_statements(signal.metadata_as_stream())

    with open(args.output_file, 'wb') as f:
        f.write(graph.serialise(format=rdf.Format.TURTLE))

if __name__ == '__main__':
    main()
