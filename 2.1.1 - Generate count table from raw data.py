# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 09:21:33 2023

@author: dcs839
"""

#### Convert RNA-STAR gene count files to csv ###

## Import libraries ##

import os
import pandas as pd

## Folders #
Folder1 = "Data/RSEM"
Folder2 = "Data/Count Tables"
os.makedirs(Folder2,exist_ok=True)

## Files ##

File1 = "Count table - Nocturnal analysis.csv"
File2 = "Reduced - Count table - Nocturnal analysis.csv"

## for each sample file from RNAstar GeneCount -> Generate raw count file ## 
for i in range(1,13,1):
    # Initialize file names #
    file_name_in = "RSEM_sample_{}.txt".format(i)
    #file_name_out = "Sample_{}_rawcounts.csv".format(i)
    # Load data #
    df = pd.read_csv(os.path.join(Folder1,file_name_in),sep="\t")
    # Rename columns #
    df = df.rename(columns=({"gene_id":"Ensembl ID"}))
    ## Create count table ##
    # If first iteration -> Create Count table #
    if i == 1:
        df_count_table = df[['Ensembl ID','TPM']].rename(columns=({'TPM':'Sample 1 (TPM)'})).copy()
    # else append samples into count table #
    else:
        df_count_table = pd.merge(df_count_table, df[['Ensembl ID','TPM']].rename(columns=({'TPM':'Sample {} (TPM)'.format(i)})), on="Ensembl ID")

## reduce count table ##

# Remove rows with only zeroes #
df_count_table_reduced = df_count_table.set_index('Ensembl ID').loc[~(df_count_table.set_index('Ensembl ID')==0).all(axis=1)]

## Save count tables to file ##

# Count table #
df_count_table.to_csv(os.path.join(Folder2,File1),index=False,sep=";")

# Redued count table
df_count_table_reduced.to_csv(os.path.join(Folder2,File2),sep=";")