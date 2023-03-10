import pandas as pd
import argparse
import glob

#Create Parser
parser = argparse.ArgumentParser(description="Merger for cleaned iAdmix outputs")
#Add arguments
parser.add_argument("-d", "--directory", required=True)
parser.add_argument("-o", "--output_filename", required=True)
#Get arguments
args = parser.parse_args()
file_directory = args.directory
file_list = glob.glob(file_directory + '/*.csv')
output_filename = args.output_filename

#Set big_df to the first element in file_list
big_df = pd.read_csv(file_list[0])
#If file_list contains more than 1 filename, iterate through all the filenames in file_list and concatenate them to big_df
if len(file_list) > 1:
    for file in file_list[1:]:
        df = pd.read_csv(file)
        big_df = pd.concat([big_df, df])

#Export big_df as a .csv file
big_df.to_csv(output_filename, index=False)