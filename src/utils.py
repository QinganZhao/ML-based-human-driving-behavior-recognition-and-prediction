def convertData(folderName):
    
    '''
    This function convert the labeled data (.json files) in one .pcap file to a dataframe;
    argument: folderName (string), which is the name of the folder contains all the .json files (NO OTHER FILES!);
    return: a pandas dataframe with 3 columns: car ID, Feature, and Time;
    Element in the 'Feature' in order: car center x coordinate, y coordinate, width, length, and angle
    Example: convertData('pcap1out'), note that 'pcap1out' is in the working directory
    '''
    
    import numpy as np
    import pandas as pd
    import os
    
    def getid(df):
        return df['object_id']
    getid = np.vectorize(getid)
    
    def getFeature(df):
        return str((df['center']['x'], df['center']['y'], df['width'], df['length'], df['angle']))
    getFeature = np.vectorize(getFeature)
    
    dataMats = []
    fileids = np.sort([int(i.replace('.json', '')) for i in os.listdir(folderName)])
    for fileid in fileids:
        filename = str(fileid) + '.json'
        frame = pd.io.json.read_json(folderName + '/' + filename)
        carid = getid(frame)
        carFeature = getFeature(frame)
        carTime = np.repeat(fileid, len(frame)).reshape(len(frame), 1)
        datamat = np.hstack([carid, carFeature, carTime])
        dataMats += [datamat]
    df = pd.DataFrame(np.vstack(dataMats))
    df.columns = ['ID', 'Feature', 'Time']
    df = df.sort_values(['ID', 'Time']).reset_index(drop=True)
    
    return df


def csv2bin(path):
    
    '''
    This function convert the .csv data generated from .pcap to bin files so that it can be labeled
    Generate all the bin files into the path folder
    Parameter: path (str), should be the path only contains the .csv files
    '''
    
    import os
    import numpy as np
    
    files = os.listdir(path)
    os.chdir(path)
    for file in files:
        my_data = np.genfromtxt(file, delimiter=',')[1:, 0:4]
        print (np.shape(my_data))
        filename = file.replace(".csv", "")
        my_data.astype('float32').tofile(filename)