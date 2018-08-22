# python-rtklib

## Getting Started
Python-rtklib is used to process emlid's base and rover raw data to position file. Src folder contains executable files of rtklib.

## Dependencies
1. numpy
2. Tkinter
3. zipfile
4. pandas

To install these dependencies, type
```
pip install zipfile
pip install pandas
```

## How to run
To run number of inputs are required from the user
1. Raw zip file of base
2. Raw zip files of rover
3. Position of base

You can select number of base files at once to process all of them.
If position of base is available then make a csv file as given in **Sample_base_position.csv** 

Type
```
python process_rtk.py
```
### User Inputs
1. Select base zip file
2. Select all the rover zip files
3. Select csv file of base position if available otherwise simply select: **No**

## Output as CSV
This will give you position file of each observation. 
Run matlab program to covert from pos file to csv file.

**Note** - If you get a float point then try processing with GUI app. GUI software is updated as compared to CLI software.



