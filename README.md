
![sabres_logo_final_nobackg_smol](https://user-images.githubusercontent.com/93765714/190021979-66b08a76-e84d-4661-a66c-2b95781cdbb2.png)

# SABRes

A simple tool that scans VCF files for SARS-CoV-2 Antiviral Resistance

The tool takes output from [iVar](https://github.com/andersen-lab/ivar) (.tsv), [Varscan](http://varscan.sourceforge.net/) (.vcf), [Medaka](https://github.com/nanoporetech/medaka) (.vcf) [LoFreq](https://csb5.github.io/lofreq/) (.vcf), [Shiver](https://github.com/ChrisHIV/shiver) (.csv), [Ucsc faToVCF (from UShER)](https://anaconda.org/bioconda/ucsc-fatovcf) (.vcf) and parses it for mutations curated in our database as conferring antiviral resistance. 

There are two databases available, a filtered and a global antiviral database (--full). This is because the two dominant circulating strains Delta and Omicron inherently carry resistance markers against existing drugs.
The database was generated using product information sheets for each drug. e.g.
https://www.pfizermedicalinformation.com/en-us/nirmatrelvir-tablets-ritonavir-tablets/clinical-pharmacology

and the curated database collated by Stanford https://covdb.stanford.edu/page/susceptibility-data/


The full database contains mutations against the following drugs:
|Brand Name|Drug Name|Agency Approval|Citation|Notes|
|----------|---------|---------------|--------|-----|
|Veklury|Remdesivir|FDA and TGA approved|10.1371/journal.ppat.1009929, 10.1038/s41467-022-29104-y|\-|
|Xevudy|Sotrovimab|FDA and TGA approved|10.1056/NEJMc2120219, 10.1101/2022.04.06.487325 |\-|
|\-|Bebtelovimab|FDA Only|10.1101/2021.04.30.442182|\-|
|Paxlovid|Nirmatrelvir and Ritonavir|FDA and TGA approved|10.1016/j.bmcl.2022.128629|\-|
|Lagevrio|Molnupiravir|FDA and TGA approved|10.1128/JVI.01348-19|\-|
|Evusheld|Tixagevimab and Cilgavimab|FDA and TGA approved|10.1056/NEJMc2119407|Not in default database|
|Regikrona|Regdanvimab|FDA and TGA approved|10.1056/NEJMc2119407|Not in default database|
|\-|Bamlanivimab and Etesevimab|FDA and TGA approved|10.1056/NEJMc2119407|Not in default database|
|Ronapreve|Casirivimab and Imdevimab|FDA and TGA approved|10.1016/j.bbrc.2021.06.016|Not in default database|

Database Date: 2nd December 2022

## How it works
![sabres_flowchart](https://user-images.githubusercontent.com/93765714/184043283-821ca835-d72c-43ff-8609-1ea5f09b2645.png)


## Installation

Firstly have Python3 installed.

PIP (RECOMMENDED)
```
pip install git+https://github.com/LilWinx/Sabres
```
GITHUB
```
git clone https://github.com/LilWinx/Sabres.git
```

## Usage
The tool defaults to drugs that continue to provide effective antiviral suppression against circulating strains. You can provide it with either a specific file or a directory containing ivar/varscan/medaka output files. 

Please note that if your VCF file was not generated using the Genbank references MN908947.3 or NC_045512.2, the results may be misaligned and provide inaccurate resistance calls.


Example usage

```
sabres --vcall ivar --input ivar_output_file.tsv
sabres --vcall varscan -i varscan_output_file.vcf
```

FLAGS

```
--outdir, -o [Folder] optional folder to write output files to
--full, -f uses the full database including drugs that no longer work for Omicron
--lineage, -l [Folder] adds Lineage data to resistance list
--vcall, -v [options: ivar, varscan, medaka, lofreq, shiver, fatovcf]
--input, -i [path] path to folder or file to run on. (must be a file if using medaka)
```


An optional `merge` subcommand is available for merging multiple SABRes output files (which can contain different column names based on their resistance profiles) into one table. This script can be run by generating a newline-separated text file listing all the files to merge, and running the script as:

```
sabres merge -i sabres_file_list.txt -o output_merged_file.tab
```


OUTPUT

Generates a table of SNPs associated with resistance against SARS-CoV-2 antivirals observed within the dataset for all samples (resistant_samples.tab).

Counts of strains carrying the each resistance marker (summary_counts.txt)

A per-sample snpprofile.tab file is also generated which displays all the per-isolate SNPs a human-readable format with any accompanying resistance markers.

The "Evidence" column denotes whether the resistance marker has been confirmed to confer resistance:
- *High*  mutation has been confirmed to confer resistance using _in vitro_ studies using live SARS-CoV-2 virus
- *Moderate* mutation has either been observed in genomes or reported in case studies but has no in vitro evidence to support.
- *Low* mutation has been predicted in in vitro pseudovirus studies, however, there have been no in vitro studies confirming its conferral to SARS-CoV-2 resistance
- *lineage* mutation is a marker for a specific lineage

CAUTION!
It is up to the user to provide high quality VCF files, as SABRes itself does not perform any quality checking. Any genomes with low coverage over certain regions may result in missed detection of mutations

## Dependencies
- Python == 3.8.13
- Pandas == 2.0.0
- Numpy == 1.23.2

## Future Additions
 - Continuous updates as resistance markers are identified
 - Webtool
 - BCFtools capability

## Nomenclature
(S)ARS-CoV-2 (A)ntimicro(B)ial (RES)istance

We promise we didn't fat finger the B instead of the V


## Citation
Fong, W., Rockett, R.J., Agius, J.E. et al. SABRes: in silico detection of drug resistance conferring mutations in subpopulations of SARS-CoV-2 genomes. BMC Infect Dis 23, 303 (2023). https://doi.org/10.1186/s12879-023-08236-6
