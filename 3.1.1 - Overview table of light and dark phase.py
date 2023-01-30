# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 09:31:52 2023

@author: dcs839
"""

### Overview table of TPM, SD, and p-value between light and dark phase ###

## Libraries ##

import os
import pandas as pd
from scipy.stats import ttest_ind

## Folders ##

Folder1 = "Data/Count Tables"
Folder2 = "Results"
os.makedirs(Folder2,exist_ok=True)
Folder3 = "Data/Metadata"

## Files ##

File1 = "Reduced - Count table - Nocturnal analysis.csv"
File2 = "Overview Table - Nocturnal analysis.xlsx"
File3 = "Transport of interest.csv"
File4 = "Transport overview Table - Nocturnal analysis.xlsx"
## Load data ##

df = pd.read_csv(os.path.join(Folder1,File1),sep=";")

## Variables ##

Lightphase_list = []
Darkphase_list = []

for i in range (1,7,1):
    Lightphase_list.append('Sample {} (TPM)'.format(i))
    Darkphase_list.append('Sample {} (TPM)'.format(i+6))


df_overview = df[['Ensembl ID']].copy()

## Add Mean and SD to overview ##
# Lightphase #
df_overview["Lightphase Mean (TPM)"] = df[Lightphase_list].mean(axis=1)
df_overview["Lightphase SD (TPM)"] = df[Lightphase_list].std(axis=1,ddof=1)
# Darkphase #
df_overview["Darkphase Mean (TPM)"] = df[Darkphase_list].mean(axis=1)
df_overview["Darkphase SD (TPM)"] = df[Darkphase_list].std(axis=1,ddof=1)
## add p-value of welch t test #
df_overview['P-value'] = ttest_ind(df[Lightphase_list], df[Darkphase_list],equal_var = False, axis=1)[1]

# Round Mean and SD to n decimales #
Decimals = 2
df_overview = df_overview.round({'Lightphase Mean (TPM)':Decimals,"Lightphase SD (TPM)":Decimals,"Darkphase Mean (TPM)":Decimals,"Darkphase SD (TPM)":Decimals})

## Save overview table to file ##
df_overview.to_excel(os.path.join(Folder2,File2),sheet_name="Overview",index=False)

### Table used for transporters of interest ###
#Ensembl ID	Gene	Synonym
#ENSRNOG00000010378	SLC4A5	NBCE2
#ENSRNOG00000030019	ATP1A1	NKA
#ENSRNOG00000015971	SLC12A2	NKCC1
#ENSRNOG00000011648	AQP1	AQP1
#ENSRNOG00000005307	SLC4A10	NCBE
#ENSRNOG00000014347	SLC4A2	AE2
#ENSRNOG00000005957	SLC4A7	NBCn1

## Load transport metadata ##
df_transport = pd.read_csv(os.path.join(Folder3,File3),sep=';')
# set index of overview table to Ensembl ID #
df_overview = df_overview.set_index('Ensembl ID')
# Add mean, sd and pvalues to transport dataframe #
df_transport_overview = pd.merge(df_transport,df_overview,on="Ensembl ID")

# Save transporter table #
df_transport_overview.to_excel(os.path.join(Folder2,File4),sheet_name='Transport',index=False)