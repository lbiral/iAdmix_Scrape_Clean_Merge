import pandas as pd
import argparse

#Create Parser
parser = argparse.ArgumentParser(description="Merger for iAdmix outputs")
#Add arguments
parser.add_argument("-f", "--input_filename", required=True)
parser.add_argument("-o", "--output_filename", required=True)
#Get arguments
args = parser.parse_args()
file = args.input_filename
output_filename = args.output_filename

#Scrape HapMap3 populations ancestry proportion estimates

#HapMap3 populations: 
#YRI: Yoruba in Ibadan, Nigeria
#CHB: Han Chinese in Beijing, China
#CHD: Denver, CO residents of Chinese descent
#TSI: Tuscan Italians
#MKK: Maasai in Kenya
#LWK: Luhya in Kenya
#CEU: Utah residents of Central European descent
#JPT: Japanese in Tokyo, Japan

#get last line of file where the non-zero ancestry proportions are located
with open(file, 'r') as f:
    lines = f.read().splitlines()
    last_line = lines[-1]
#remove FINAL_NZ_PROPS from string representation of last line
index = last_line.index('FINAL_NZ_PROPS')
final_props = last_line[:index]
#initialize props dictionary where ancestry proportions for a single sample will be stored
props = {'YRI': 0, 'CHB': 0, 'CHD': 0, 'TSI': 0, 'MKK': 0, 'LWK': 0, 'CEU': 0, 'JPT': 0}
#get non-zero ancestry proportions for all HapMap3 populations
while len(final_props) > 0:
    if 'YRI' in final_props:
        population = 'YRI'
    elif 'CHB' in final_props:
        population = 'CHB'
    elif 'CHD' in final_props:
        population = 'CHD'
    elif 'TSI' in final_props:
        population = 'TSI'
    elif 'MKK' in final_props:
        population = 'MKK'
    elif 'LWK' in final_props:
        population = 'LWK'
    elif 'CEU' in final_props:
        population = 'CEU'
    elif 'JPT' in final_props:
        population = 'JPT'
    else:
        break
    index = final_props.index(population)
    prop = final_props[index + 4:]
    index2 = prop.index(' ')
    prop = prop[:index2]
    props[population] = float(prop)
    final_props = final_props[index2 + 1:]
#get sample_id
index = file.index('.ancestry')
index2 = file.index('.')
sample_id = file[index2 + 10:index]

#Create Pandas DataFrame, add HapMap3 population proportions, calculate meta-population proportions, and apply ancestry heuristics: Calculated Race and Calculated Ethnicity
df = pd.DataFrame()
df['Sample ID'] = [sample_id]
for i in list(props.keys()):
    df[i] = [props[i]]
#initialize lists that will store meta-population proportions and calcuated race and ethnicity data for samples
african = []
euro = []
asian = []
calculated_race = []
calculated_ethnicity = []
#initialize African, European, and Asian meta-population proportions to 0
af = 0
eu = 0
asi = 0
#get Pandas Series representation of row with the row index
row = df.iloc[0]
#iterate through each column in df DataFrame, which correspond to HapMap3 populations
for i in list(df.columns):
    #sum of YRI, MKK, and LWK population proportions equal African meta-population ancestry proportion
    if i in ['YRI', 'MKK', 'LWK']:
        af += row[i]
    #sum of TSI and CEU population proportions equal European meta-population ancestry proportion
    elif i in ['TSI', 'CEU']:
        eu +=row[i]
    #sum of CHB, CHD, and JPT population proportions equal Asian meta-population ancestry proportion
    elif i in ['CHB', 'CHD', 'JPT']:
        asi += row[i]
#append meta-population fractions for sample to corresponding list
african.append(af)
euro.append(eu)
asian.append(asi)
#apply Calculated Race heuristic
#initialize calc_race local variable
calc_race = ''
#if African is the meta-population with the largest proportion:
if af == max([af, eu, asi]):
    #assign Black to the calc_race local variable
    calc_race = 'Black'
#if European is the meta-population with the largest proportion:
elif eu == max([af, eu, asi]):
    #assign White to calc_race local variable
    if calc_race == '':
        calc_race = 'White'
    #if European and African both have the largest proportion, add White to calc_race local variable
    else:
        calc_race += '_White'
#if Asian is the meta-population with the largest proportion:
elif asi == max([af, eu, asi]):
    #assign Asian to calc_race local variable
    if calc_race == '':
        calc_race += 'Asian'
    #if Asian and another population(s) have the largest proportion, add Asian to calc_race local variable
    else:
        calc_race += '_Asian'
#append calc_race for single sample to calculated_race list
calculated_race.append(calc_race)
#apply calculated ethnicty heuristic
#if sample has at least 40% European ancestry and at least 10% Asian ancestry, classify them as Hispanic
if eu >= 0.4 and asi >= 0.1:
    calculated_ethnicity.append('Hispanic')
#otherwise, classify them as non-Hispanic
else:
    calculated_ethnicity.append('Non-Hispanic')
#add collected data to df DataFrame
df['African'] = african
df['European'] = euro
df['Asian'] = asian
df['Calculated Race'] = calculated_race
df['Calculated Ethnicity'] = calculated_ethnicity
#reorder columns
df = df[['Sample ID','YRI','CHB','CHD','TSI','MKK','CEU','LWK','JPT','African','European','Asian','Calculated Race','Calculated Ethnicity']]
#output df Dataframe as a .csv file with name specified by output_filename
df.to_csv(output_filename, index=False)