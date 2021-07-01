
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
    return st.markdown(f'<p style="font-family:sans-serif; color:grey; font-size: 34px;">{var}</p>', unsafe_allow_html=True)

# Spearman correlations

def mds_corr(data, emotions_list):
    corr = data[emotions_list].corr(method='spearman')
    corr.rename(index={'ANGER_SURVEY':'Anger', 'DISGUST_SURVEY':'Disgust', 'FEAR_SURVEY':'Fear', 'JOY_SURVEY':'Joy', 'SADNESS_SURVEY':'Sadness'}, inplace=True)
    corr.rename(columns={'ANGER_SURVEY':'Anger', 'DISGUST_SURVEY':'Disgust', 'FEAR_SURVEY':'Fear', 'JOY_SURVEY':'Joy', 'SADNESS_SURVEY':'Sadness'}, inplace=True)
    return corr

def deq_corr(data, emotions_list):
    corr = data[emotions_list].corr(method='spearman')
    corr.rename(index={'anger':'Anger', 'disgust':'Disgust', 'fear':'Fear', 'joy':'Joy', 'sadness':'Sadness'}, inplace=True)
    corr.rename(columns={'anger':'Anger', 'disgust':'Disgust', 'fear':'Fear', 'joy':'Joy', 'sadness':'Sadness'}, inplace=True)
    return corr

def kb_corr(data, emotions_list):
    corr = data[emotions_list].corr(method='spearman')
    corr.rename(index={'Anger_input':'Anger', 'Disgust_input':'Disgust', 'Fear_input':'Fear', 'Joy_input':'Joy', 'Sadness_input':'Sadness'}, inplace=True)
    corr.rename(columns={'Anger_input':'Anger', 'Disgust_input':'Disgust', 'Fear_input':'Fear', 'Joy_input':'Joy', 'Sadness_input':'Sadness'}, inplace=True)
    return corr

def srvy_sent_corr(data, emotions_list):
    corr = data[emotions_list].corr(method='spearman')
    corr.rename(index={'anger':'Anger', 'disgust':'Disgust', 'fear':'Fear', 'joy':'Joy', 'sadness':'Sadness', 'word_count':'Word Count'}, inplace=True)
    corr.rename(columns={'anger':'Anger', 'disgust':'Disgust', 'fear':'Fear', 'joy':'Joy', 'sadness':'Sadness', 'word_count':'Word Count'}, inplace=True)
    return corr

def kb_sent_corr(data, emotions_list):
    corr = data[emotions_list].corr(method='spearman')
    corr.rename(index={'Anger_Input':'Anger', 'Disgust_Input':'Disgust', 'Fear_Input':'Fear', 'Joy_Input':'Joy', 'Sadness_Input':'Sadness', 'word_count':'Word Count'}, inplace=True)
    corr.rename(columns={'Anger_Input':'Anger', 'Disgust_Input':'Disgust', 'Fear_Input':'Fear', 'Joy_Input':'Joy', 'Sadness_Input':'Sadness', 'word_count':'Word Count'}, inplace=True)
    return corr
