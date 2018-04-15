# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 08:25:50 2018

"""
# import libraries
import urllib
import pandas as pd

# Read in csv file with unique image identifiers (exported from Knime workflow)
df = pd.read_csv('Filename')

#loop through the data to download all images from the dimu media servers
for i in df.itertuples():
    urllib.request.urlretrieve("https://dms01.dimu.org/image/" + i[1] + "?", i[1] + ".jpg")