import pandas as pd
import argparse

#Create Parser
parser = argparse.ArgumentParser(description="Scrape iAdmix Log File")
#Add arguments
parser.add_argument("-f", "--input_filename", required=True)
parser.add_argument("-o", "--output_filename", required=True)
#Get arguments
args = parser.parse_args()
file = args.input_filename
output_filename = args.output_filename

#Open log file
f = open(file)
f_text = f.read()
f.close()

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

#remove FINAL_NZ_PROPS from string representation of last line
index = f_text.index('FINAL_NZ_PROPS')
f_text = f_text[:index]

#Search for File Opening Failure Warning
failure = 0
if 'Fail to open BAM file' in f_text:
    failure = 1

#Search for Estimation Accuracy Warning
uncertain = 0
if 'difficult to estimate admixture coefficients with high confidence' in f_text:
    uncertain = 1

#Find number of useful fragments
copy = f_text
no_useful_fragments = 0
if failure == 0:
    while 'useful fragments' in copy:
        index = copy.index('useful fragments')
        copy = copy[index + len('useful fragments '):]
        index2 = copy.index('\n')
        no_useful_fragments = int(copy[:index2])
        copy = copy[index2+1:]

#Cut down f_text more so only final non-zero proportions are left
index = f_text.index('FINAL_ALL_PROPS')
final_props = f_text[index + len('FINAL_ALL_PROPS') + 1:]

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
    index2 = prop.index(':')
    props[population] = float(prop[:index2])
    index3 = prop.index(' ')
    final_props = final_props[index3 + 1:]
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
#if sample has >= 50% African meta-population ancestry:
if af >= 0.5:
    calc_race = 'Black'
#if sample has >= 50% European meta-population ancestry:
elif eu >= 0.5:
    calc_race = 'White'
#if sample has >= 50% Asian meta-population ancestry:
elif asi >= 0.5:
    calc_race = 'Asian'
#if sample has no meta-populations that are >= 50%:
else:
    calc_race = 'Mixed'
#append calc_race for single sample to calculated_race list
calculated_race.append(calc_race)

#apply Calculated Ethnicty heuristic
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
df['CalculatedRace'] = calculated_race
df['CalculatedEthnicity'] = calculated_ethnicity

#add failure to open file warning to df DataFrame
df['BAMFileOpenFailure'] = [failure]

#add uncertainity warning to df DataFrame
df['UncertaintyWarning'] = [uncertain]

#add number of useful fragments to df DataFrame
df['No.UsefulFragments'] = [no_useful_fragments]
#reorder columns
df = df[['Sample ID','YRI','MKK','LWK','TSI','CEU','CHB','CHD','JPT','African','European','Asian','CalculatedRace','CalculatedEthnicity','BAMFileOpenFailure','UncertaintyWarning', 'No.UsefulFragments']]

#Add comments to header of .csv file
c = open(output_filename, 'w')
c.write('# Sample ID: self explanatory\n')
c.write('# YRI: Yoruba People of Ibadan in Nigeria (HapMap3 population)\n')
c.write('# MKK: Maasai in Kinyawa in Kenya (HapMap3 population)\n')
c.write('# LWK: Luhya in Webuye in Kenya (HapMap3 population)\n')
c.write('# TSI: Toscani in Italia (HapMap3 population)\n')
c.write('# CEU: Utah Residents with Northern and Western European Ancestry (HapMap3 population)\n')
c.write('# CHB: Han Chinese in Beijing in China (HapMap3 population)\n')
c.write('# CHD: Chinese in Metropolitan Denver in Colorado in USA (HapMap3 population)\n')
c.write('# JPT: Japanese in Tokyo in Japan (HapMap3 population)\n')
c.write('# African = Sum of YRI MKK and LWK ancestry proportions (Meta-Population)\n')
c.write('# European = Sum of TSI and CEU ancestry proportions (Meta-Population)\n')
c.write('# Asian = Sum of CHB CHD and JPT ancestry proportions (Meta-Population)]\n')
c.write('# CalculatedRace = Black if African meta-population proportion >=50% (Heuristic)\n')
c.write('# CalculatedRace = White if European meta-population proportion >=50% (Heuristic)\n')
c.write('# CalculatedRace = Asian if Asian meta-population proportion >=50% (Heuristic)\n')
c.write('# CalculatedRace = Mixed if no meta-population proportion >=50% (Heuristic)\n')
c.write('# CalculatedEthnicity = Hispanic if >=40% European and >=10% Asian (Heuristic)\n')
c.write('# CalculatedEthnicity = Non-Hispanic if above condition not met (Heuristic)\n')
c.write('# BAMFileOpenFailure = 1 if iAdmix fails to opens BAM file\n')
c.write('# BAMFileOpenFailure = 0 if iAdmix opens BAM file\n')
c.write('# UncertaintyWarning = 1 if iAdmix prints ancestry estimation accuracy warning\n')
c.write('# UncertaintyWarning = 0 if iAdmix does not print ancestry estimation accuracy warning\n')
c.write('# No.UsefulFragments = number of fragments iAdmix uses to perform ancestry estimation calculations\n')

#output df Dataframe as a .csv file with name specified by output_filename
df.to_csv(c, index=False)
c.close()