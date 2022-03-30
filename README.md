# covid_res

A simple tool that scans VCF files for SARS-CoV-2 Antiviral Resistance

The tool takes an iVar (https://github.com/andersen-lab/ivar) output (.tsv) or Varscan (http://varscan.sourceforge.net/) output (.vcf) and parses it for mutations curated in our database. The output will return only the mutation that matches with mutations listed in the database

There are two databases available, a Omicron/Delta only and a global antiviral database (--full). This is because the two dominant circulating strains Delta and Omicron inherently carry resistance markers against existing drugs. 
The database was generated using product information sheets for each drug. e.g. 
https://www.pfizermedicalinformation.com/en-us/nirmatrelvir-tablets-ritonavir-tablets/clinical-pharmacology


The full database contains mutations against the following drugs:
|Brand Name|Drug Name|Agency Approval|Citation|Notes|
|----------|---------|---------------|--------|-----|
|Veklury|Remdesivir|FDA and TGA approved|10.1371/journal.ppat.1009929||\-|
|Xevudy|Sotromivab|FDA and TGA approved|\-|\-|
|Evusheld|Tixagevimab and Cilgavimab|FDA and TGA approved|\-|\-|
|Paxlovid|Nirmatrelvir and Ritonavir|FDA and TGA approved|\-|\-|
|\-|Bamlanivimab and Etesevimab|FDA and TGA approved|\-|Discontinued - NO LONGER WORKS FOR OMICRON VARIANT|
|Regen-Cov|Casirivimab and Imdevimab|FDA and TGA approved|\-|Discontinued - NO LONGER WORKS FOR OMICRON VARIANT|
|\-|Bebtelovimab|FDA Only|\-|\-|

Drugs with unavailable resistance mutations:
- Lagevrio (Molnupiravir) [FDA and TGA approved]
- Regikrona (Regdanvimab) [FDA and TGA approved]

Database Date: 25th March 2022

## Usage
The tool defaults to not include drugs that no longer work.

```
python input.py [Path to folder with TSV files]
```
OR
```
python input.py --full [Path to folder with TSV files]
```

FLAGS

```
--full, -f uses the full database including drugs that no longer work for Omicron
```

OUTPUT

Displays the list SNPs associated with resistance against SARS-CoV-2 antivirals within the dataset (resistant_isolates.txt).

Counts of strains carrying the type of resistance marker (summary_counts.txt)

A SNPProfile file is also generated which displays all the SNPs of the tsv in a human-readable format with accompanying resistance markers.

The final column denotes whether the resistance marker has been confirmed in wild-type virus.
 - confirmed    observed in clinical isolates
 - theoretical  cell culture assays with the mutation demonstrate resistance

## Dependencies
Pandas https://pandas.pydata.org/


## File Preparation
iVar outputs are split into their respective folders.

So to prep your data, the easiest solution is to copy the tsv files into a new folder and run the script directly on that folder

A useful script would be
```
cp **/*.tsv >> [New Folder]
```

