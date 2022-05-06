# Sabres

A simple tool that scans VCF files for SARS-CoV-2 Antiviral Resistance

The tool takes an iVar (https://github.com/andersen-lab/ivar) output (.tsv) or Varscan (http://varscan.sourceforge.net/) output (.vcf) and parses it for mutations curated in our database. The output will return only the mutation that matches with mutations listed in the database

There are two databases available, a filtered and a global antiviral database (--full). This is because the two dominant circulating strains Delta and Omicron inherently carry resistance markers against existing drugs. 
The database was generated using product information sheets for each drug. e.g. 
https://www.pfizermedicalinformation.com/en-us/nirmatrelvir-tablets-ritonavir-tablets/clinical-pharmacology

and the curated database collated by Stanford https://covdb.stanford.edu/page/susceptibility-data/


The full database contains mutations against the following drugs:
|Brand Name|Drug Name|Agency Approval|Citation|Notes|
|----------|---------|---------------|--------|-----|
|Veklury|Remdesivir|FDA and TGA approved|10.1371/journal.ppat.1009929, 10.1038/s41467-022-29104-y||\-|
|Xevudy|Sotromivab|FDA and TGA approved|10.1056/NEJMc2120219|\-|
|\-|Bebtelovimab|FDA Only|\-|\-|
|Paxlovid|Nirmatrelvir and Ritonavir|FDA and TGA approved|\-|\-|
|Lagevrio|Molnupiravir|FDA and TGA approved|10.1128/JVI.01348-19|\-|
|Evusheld|Tixagevimab and Cilgavimab|FDA and TGA approved|\-|Not in default database|
|Regikrona|Regdanvimab|FDA and TGA approved|\-|Not in default database|
|\-|Bamlanivimab and Etesevimab|FDA and TGA approved|\-|Not in default database|
|Ronapreve|Casirivimab and Imdevimab|FDA and TGA approved|\-|Not in default database|

Database Date: 22nd April 2022

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
--lineage, -l [Folder] adds Lineage data to resistance list
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

## Nomenclature
(S)ARS-CoV-2 (A)ntimicro(B)ial (RES)istance 

We promise we didn't fat finger the B instead of the V
