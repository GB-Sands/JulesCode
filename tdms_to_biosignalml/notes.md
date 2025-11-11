# Notes for TDMS to BioSignalML Conversion

## Initial thoughts

- Need to install `nptdms` and `biosignalml`.
- The script should have a command-line interface.
- I'll use `argparse` for the command-line options.
- The script should be able to:
    - List groups and channels in a TDMS file.
    - Convert specific groups/channels to BioSignalML.
    - Handle verbose output.
    - Have a "dry-run" option.
- I will write tests for the script using the `TestData.tdms` file.
