# iAdmix Scrape, Clean, and Merge
## Git Repository Info
This Git Repo contains the following items: 

#### clean_ancestry.py
A python script that, given an iAdmix output file, scrapes key data and outputs a .csv file containing the following: 
1. Sample ID (code that scrapes this info will not work unless your iAdmix output file names have the same structure as output files from the Dave Lab SNP_ANCESTRY pipeline) 
2. Calculated ancestry proportions for each HapMap3 population (YRI, CHD, CHB, LWK, MKK, JPT, TSI, CEU) 
3. Aggregated ancestry proportions for meta-populations (European, African, and Asian)
4. Calculated race heuristic result
5. Calculated ethnicity heuristic result
#### snp_ancestry_merger.py
A python script that, given a directory containing output files from clean_ancestry.py, outputs a .csv file containing all the data from each of the clean_ancestry.py output files. 
#### data_folder
A directory containing two sample iAdmix output files.

#### This README
Oh really? 

## Running the Program
clean_ancestry.py can be run in the command line and has the following required arguments: 
1. -f, --input_filename: the iAdmix output file.
2. -o, --output_filenam: the name you want to give to the .csv file that gets outputted. You must include .csv when defining this argument.

If you want to run the program in the command line on one of the samples in data_folder and write the output to a .csv file named single_output.csv, you would use the following command:

python3 clean_ancestry.py -f data_folder/8953_snpancestry_snp_ancestry__dna_snpancestry_snp_ancestry__dna_SNPAncestry.sd.gr.zz.10016_T_1_S32188.ancestry.out -o single_output.csv

snp_merger_ancestry.py can be run in the command line and has the following required arguments: 
1. -d, --directory: the directory containing the clean_ancestry.py output files you want to merge.
2. -o, --output_filename: the name you want to give to the .csv file that gets outputted. You must include .csv when defining this argument.

If you want to run the program in the command line on the clean_ancestry.py outputs in a directory named clean_ancestry_outputs and write the output to a .csv file named merged_output.csv you would enter the following command:

python3 snp_ancestry_merger.py -d clean_ancestry_outputs -o merged_output.csv
  
## Reference: 
Find the iAdmix GitHub repository here: https://github.com/vibansal/ancestry
 
