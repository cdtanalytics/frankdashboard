
# ----------------------------------------- #
#                                           #
#  TITLE:   FRANK APP EVALUATION DASHBOARD  #
#  PURPOSE: Functions                       #
#  AUTHOR:  Craig Hansen                    #
#  DATE:    06 Mar 2021                     #
# ----------------------------------------- #


# -- Import Python Libraries -- #

import pandas as pd
import numpy as np

from getdata import *
from functions import *
from plots import *

# -- Percentiles -- #

def q25(x):
    return x.quantile(0.25)

def q50(x):
    return x.quantile(0.5)

def q75(x):
    return x.quantile(0.75)

    # Overall for each emotion
def summarystats(data, emotions_list):
    return data[emotions_list].describe().round(2).T
     
    # Group by user group for each emotion
def summarystats_groupby(data, emotions_list):
    return data.groupby('USERGROUP')[emotions_list].agg(['count', 'mean', 'std', 'min', 'max']).round(2)

# Subtitles with the same stylings
def subtitles(var):
    return st.markdown(f'<p style="font-family:sans-serif; color:Blue; font-size: 24px;">{var}</p>', unsafe_allow_html=True)
