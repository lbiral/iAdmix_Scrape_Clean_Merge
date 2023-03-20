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
big_df = pd.read_csv(file_list[0], header=21)
#If file_list contains more than 1 filename, iterate through all the filenames in file_list and concatenate them to big_df
if len(file_list) > 1:
    for file in file_list[1:]:
        df = pd.read_csv(file, header=21)
        big_df = pd.concat([big_df, df])

#Add comments to header of .csv file
description_list = ['# Sample ID: self explanatory',
                    '# YRI: Yoruba People of Ibadan in Nigeria (HapMap3 population)',
                    '# MKK: Maasai in Kinyawa in Kenya (HapMap3 population)',
                    '# LWK: Luhya in Webuye in Kenya (HapMap3 population)',
                    '# TSI: Toscani in Italia (HapMap3 population)',
                    '# CEU: Utah Residents with Northern and Western European Ancestry (HapMap3 population)',
                    '# CHB: Han Chinese in Beijing in China (HapMap3 population)',
                    '# CHD: Chinese in Metropolitan Denver in Colorado in USA (HapMap3 population)',
                    '# JPT: Japanese in Tokyo in Japan (HapMap3 population)',
                    '# African = Sum of YRI MKK and LWK ancestry proportions (Meta-Population)',
                    '# European = Sum of TSI and CEU ancestry proportions (Meta-Population)',
                    '# Asian = Sum of CHB CHD and JPT ancestry proportions (Meta-Population)',
                    '# CalculatedRace = Black if African meta-population proportion >=50% (Heuristic)',
                    '# CalculatedRace = White if European meta-population proportion >=50% (Heuristic)',
                    '# CalculatedRace = Asian if Asian meta-population proportion >=50% (Heuristic)',
                    '# CalculatedRace = Mixed if no meta-population proportion >=50% (Heuristic)',
                    '# CalculatedEthnicity = Hispanic if >=40% European and >=10% Asian (Heuristic)',
                    '# CalculatedEthnicity = Non-Hispanic if above condition not met (Heuristic)',
                    '# UncertaintyWarning = 1 if iAdmix prints ancestry estimation accuracy warning',
                    '# UncertaintyWarning = 0 if iAdmix does not print ancestry estimation accuracy warning',
                    '# No.UsefulFragments = Number of fragments iAdmix uses to perform ancestry estimation calculations\n']

c = open(output_filename, 'w')
c.write('\n'.join(description_list))
#Export big_df as a .csv file
big_df.to_csv(c, index=False)
c.close()