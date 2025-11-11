from nptdms import TdmsFile

with TdmsFile.open("TestData.tdms") as tdms_file:
    for group in tdms_file.groups():
        print(f"Group: {group.name}")
        for channel in group.channels():
            print(f"  Channel: {channel.name}")
