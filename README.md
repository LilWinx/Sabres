![sabres_logo](https://user-images.githubusercontent.com/93765714/167744118-11e06611-6f86-47be-86c9-aeadf2c33adb.png)

# SABRes

A simple tool that scans VCF files for SARS-CoV-2 Antiviral Resistance

The tool takes an iVar (https://github.com/andersen-lab/ivar) output (.tsv) or Varscan (http://varscan.sourceforge.net/) output (.vcf) and parses it for mutations curated in our database. The output will return only the mutation that matches with mutations listed in the database

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

Database Date: 25th May 2022

## How it works
![sabres_flowchart](https://user-images.githubusercontent.com/93765714/184043283-821ca835-d72c-43ff-8609-1ea5f09b2645.png)


## Usage
The tool defaults to drugs that continue to provide effective antiviral suppression against circulating strains.
Example usage

```
python input.py --vcall varscan/ivar [Path to folder with TSV or VCF files]
```

FLAGS

```
--outdir, -o [Folder] optional folder to write output files to
--full, -f uses the full database including drugs that no longer work for Omicron
--lineage, -l [Folder] adds Lineage data to resistance list
--vcall, -v [options: ivar, varscan or medaka]
--input, -i [path] path to folder or file to run on
```

OUTPUT

Generates a list SNPs associated with resistance against SARS-CoV-2 antivirals within the dataset (resistant_isolates.txt).

Counts of strains carrying the type of resistance marker (summary_counts.txt)

A per-isolate snpprofile.tab file is also generated which displays all the per-isolate SNPs a human-readable format with any accompanying resistance markers.

The "Note" column denotes whether the resistance marker has been confirmed in wild-type virus.
- observed  mutation has been observed in circulating SARS-CoV-2 genomes but has no in vitro results
- predicted mutation predicted to have resistance functionaility but has not been tested or observed
- confirmed mutation has been observed and confirmed in vitro to confer resistance

## Dependencies
Pandas https://pandas.pydata.org/

## Future Additions
 - Continuous updates as resistance markers are identified

## Nomenclature
(S)ARS-CoV-2 (A)ntimicro(B)ial (RES)istance

We promise we didn't fat finger the B instead of the V
