
# ----------------------------------------- #
#                                           #
#  TITLE:   FRANK APP EVALUATION DASHBOARD  #
#  PURPOSE: Data Preparation                #
#  AUTHOR:  Craig Hansen                    #
#  DATE:    06 Mar 2021                     #
# ----------------------------------------- #


# -- Import Python Libraries -- #

import pandas as pd
import streamlit as st


# -- Load the data -- #

@st.cache
def load_data(sheet):
    raw_data = pd.read_excel('Frank_Round2_Analyses.xlsx', sheet_name=sheet)
    return raw_data

df_mds = load_data('frank.moods')
df_deq = load_data('frank.deq')
df_algo = load_data('frank.kb_rolledup')
df_mds_deq = load_data('frank.deq_moods_timing')
df_matches_ru = load_data('matches_rolledup')
df_matches_sent = load_data('sentmatches')

@st.cache
def load_sentdata():
    raw_data = pd.read_csv('sentiment_analysis.csv')
    return raw_data

sentiment = load_sentdata()
sentiment.rename(columns={'userId':'USERID', 'userGroup':'USERGROUP'}, inplace=True)

# -- Create a dataframe that has all the summary information from the different datasets -- #

d = {'Dataset'      : ['Daily Moods', 'DEQ', 'Keyboard'], 

     'Records'      : [len(df_mds.index), 
                      len(df_deq.index), 
                      len(df_algo.index)],

     'Participants' : [df_mds['USERID'].nunique(), 
                      df_deq['USERID'].nunique(), 
                      df_algo['USERID'].nunique()],

     'Frank'        : [df_mds[df_mds['USERGROUP']=='Frank']['USERID'].nunique(), 
                      df_deq[df_deq['USERGROUP']=='Frank']['USERID'].nunique(), 
                      df_algo[df_algo['USERGROUP']=='Frank']['USERID'].nunique()],

     'FrankKeyboard': [df_mds[df_mds['USERGROUP']=='FrankKeyboard']['USERID'].nunique(), 
                      df_deq[df_deq['USERGROUP']=='FrankKeyboard']['USERID'].nunique(), 
                      df_algo[df_algo['USERGROUP']=='FrankKeyboard']['USERID'].nunique()],

     'Keyboard'     : [df_mds[df_mds['USERGROUP']=='Keyboard']['USERID'].nunique(), 
                      df_deq[df_deq['USERGROUP']=='Keyboard']['USERID'].nunique(), 
                      df_algo[df_algo['USERGROUP']=='Keyboard']['USERID'].nunique()],

     'Min Date'     : [df_mds['mds_srvy_date'].min(), 
                       df_deq['deq_srvy_date'].min(), 
                       df_algo['kb_input_date'].min()],

     "Max Date"     : [df_mds['mds_srvy_date'].max(), 
                       df_deq['deq_srvy_date'].max(), 
                       df_algo['kb_input_date'].max()]
                       
    }

df_info = pd.DataFrame(data=d)


# -- Create lists of emotions for various data manipulations/calculations -- #

emotions = ['Anger', 'Disgust', 'Fear', 'Joy', 'Sadness']

users = ['FrankKeyboard', 'Keyboard', 'Frank']

mds_emotlist = ['ANGER_SURVEY', 'DISGUST_SURVEY', 'FEAR_SURVEY', 'JOY_SURVEY', 'SADNESS_SURVEY']
mds_emotlist_z = ['z_Anger_Survey', 'z_Disgust_Survey', 'z_Fear_Survey', 'z_Joy_Survey', 'z_Sadness_Survey']
mds_emotlist_p = ['p_anger_Survey', 'p_disgust_Survey', 'p_fear_Survey', 'p_joy_Survey', 'p_sadness_Survey']

deq_emotlist = ['anger', 'disgust', 'fear', 'joy', 'sadness']
deq_emotlist_z = ['z_anger', 'z_disgust', 'z_fear', 'z_joy', 'z_sadness']
deq_emotlist_p = ['p_Anger', 'p_disgust', 'p_fear', 'p_joy', 'p_sadness']

algo_emotlist = ['Anger_input', 'Disgust_input', 'Fear_input', 'Joy_input', 'Sadness_input']
algo_emotlist_z = ['z_Anger_input', 'z_Disgust_input', 'z_Fear_input', 'z_Joy_input', 'z_Sadness_input']
algo_emotlist_p = ['p_anger_input', 'p_disgust_input', 'p_fear_input', 'p_joy_input', 'p_sadness_input']

dff_emotlist_p = ['diff_p_anger', 'diff_p_disgust', 'diff_p_fear', 'diff_p_joy', 'diff_p_sadness']
dff_emotlist_p_grp = ['diff_p_anger_grp', 'diff_p_disgust_grp', 'diff_p_fear_grp', 'diff_p_joy_grp', 'diff_p_sadness_grp']

timings = ["30 min +/-", "60 min +/-", "90 min +/-", "120 min +/", "150 min +/", "180 min +/"]

srvy_sent_emotlist = ['anger', 'disgust', 'fear', 'joy', 'sadness', 'word_count', 'polarity', 'subjectivity']
kb_sent_emotlist = ['Anger_Input', 'Disgust_Input', 'Fear_Input', 'Joy_Input', 'Sadness_Input', 'word_count', 'polarity', 'subjectivity']
kb_emotlist = ['Anger_Input', 'Disgust_Input', 'Fear_Input', 'Joy_Input', 'Sadness_Input', 'word_count']
kb_emotlist2 = ['Anger_Input', 'Disgust_Input', 'Fear_Input', 'Joy_Input', 'Sadness_Input']

# -- Create a dataset of the dates by Emotion and User Group -- #

dates_by_emotion = pd.DataFrame()
for emotion in emotions:
    dates = pd.date_range('20210101','20210531')
    df = pd.DataFrame(data=dates, columns=['Date'])
    df['Emotion'] = emotion
    dates_by_emotion = dates_by_emotion.append(df)

dates_by_emotion_user = pd.DataFrame()
for emotion in emotions:
    for user in users:
        dates = pd.date_range('20210101','20210531')
        df = pd.DataFrame(data=dates, columns=['Date'])
        df['Emotion'] = emotion
        df['USERGROUP'] = user
        dates_by_emotion_user = dates_by_emotion_user.append(df)


# -- Participant counts (daily) -- #

    # Daily Moods
mds_daily_cnts = df_mds.groupby('mds_srvy_date').agg({"USERID": "nunique"})
mds_daily_cnts = mds_daily_cnts.reset_index()
mds_daily_cnts.rename(columns={'mds_srvy_date': 'Date'}, inplace=True)
    # DEQ
deq_daily_cnts = df_deq.groupby('deq_srvy_date').agg({"USERID": "nunique"})
deq_daily_cnts = deq_daily_cnts.reset_index()
deq_daily_cnts.rename(columns={'deq_srvy_date': 'Date'}, inplace=True)
    # Keyboard
algo_daily_cnts = df_algo.groupby('kb_input_date').agg({"USERID": "nunique"})
algo_daily_cnts = algo_daily_cnts.reset_index()
algo_daily_cnts.rename(columns={'kb_input_date': 'Date'}, inplace=True)


# -- Participant counts (USERGROUP and daily) -- #

    # Daily Moods
mds_daily_usergrp_cnts = df_mds.groupby(['USERGROUP','mds_srvy_date']).agg({"USERID": "nunique"})
mds_daily_usergrp_cnts = mds_daily_usergrp_cnts.reset_index()
mds_daily_usergrp_cnts.rename(columns={'mds_srvy_date': 'Date'}, inplace=True)
    # DEQ
deq_daily_usergrp_cnts = df_deq.groupby(['USERGROUP','deq_srvy_date']).agg({"USERID": "nunique"})
deq_daily_usergrp_cnts = deq_daily_usergrp_cnts.reset_index()
deq_daily_usergrp_cnts.rename(columns={'deq_srvy_date': 'Date'}, inplace=True)
    # Keyboard
algo_daily_usergrp_cnts = df_algo.groupby(['USERGROUP','kb_input_date']).agg({"USERID": "nunique"})
algo_daily_usergrp_cnts = algo_daily_usergrp_cnts.reset_index()
algo_daily_usergrp_cnts.rename(columns={'kb_input_date': 'Date'}, inplace=True)


# -- Emotions long file (raw values) -- #

    # Daily Moods
df_mds_long = df_mds.melt(id_vars=['USERID', 'USERGROUP'], 
                        value_vars=mds_emotlist,
                        var_name='Emotion', value_name='Value')
df_mds_long["Emotion"].replace({'ANGER_SURVEY':'Anger', 'DISGUST_SURVEY':'Disgust', 'FEAR_SURVEY':'Fear', 'JOY_SURVEY':'Joy', 'SADNESS_SURVEY':'Sadness'}, inplace=True)
    # DEQ
df_deq_long = df_deq.melt(id_vars=['USERID', 'USERGROUP'], 
                        value_vars=deq_emotlist,
                        var_name='Emotion', value_name='Value')
df_deq_long["Emotion"].replace({'anger':'Anger', 'disgust':'Disgust', 'fear':'Fear', 'joy':'Joy', 'sadness':'Sadness'}, inplace=True)
    # Keyboard
df_algo_long = df_algo.melt(id_vars=['USERID', 'USERGROUP'], 
                        value_vars=algo_emotlist,
                        var_name='Emotion', value_name='Value')
df_algo_long["Emotion"].replace({'Anger_input':'Anger', 'Disgust_input':'Disgust', 'Fear_input':'Fear', 'Joy_input':'Joy', 'Sadness_input':'Sadness'}, inplace=True)

df_sent_long = sentiment.melt(id_vars=['USERID', 'USERGROUP'], 
                        value_vars=kb_emotlist2,
                        var_name='Emotion', value_name='Value')
df_sent_long["Emotion"].replace({'Anger_Input':'Anger', 'Disgust_Input':'Disgust', 'Fear_Input':'Fear', 'Joy_Input':'Joy', 'Sadness_Input':'Sadness'}, inplace=True)

# -- Cummulative Emotions long file -- #

    # Daily Moods
df_mds_cum = df_mds.melt(id_vars=['mds_srvy_date'], 
                  value_vars=mds_emotlist,
                  var_name='Emotion', value_name='Value')
df_mds_cum["Emotion"].replace({'ANGER_SURVEY':'Anger', 'DISGUST_SURVEY':'Disgust', 'FEAR_SURVEY':'Fear', 'JOY_SURVEY':'Joy', 'SADNESS_SURVEY':'Sadness'}, inplace=True)
df_mds_cum.rename(columns={'mds_srvy_date': 'Date'}, inplace=True)
df_mds_cum = pd.merge(dates_by_emotion, df_mds_cum, how='left', on=['Date', 'Emotion']).fillna(0)
df_mds_cum['CumEmotion'] = df_mds_cum.groupby(['Emotion'])['Value'].cumsum()
    # DEQ
df_deq_cum = df_deq.melt(id_vars=['deq_srvy_date'], 
                  value_vars=deq_emotlist,
                  var_name='Emotion', value_name='Value')
df_deq_cum["Emotion"].replace({'anger':'Anger', 'disgust':'Disgust', 'fear':'Fear', 'joy':'Joy', 'sadness':'Sadness'}, inplace=True)
df_deq_cum.rename(columns={'deq_srvy_date': 'Date'}, inplace=True)
df_deq_cum = pd.merge(dates_by_emotion, df_deq_cum, how='left', on=['Date', 'Emotion']).fillna(0)
df_deq_cum['CumEmotion'] = df_deq_cum.groupby(['Emotion'])['Value'].cumsum()
    # Keyboard Innput
df_algo_cum = df_algo.melt(id_vars=['kb_input_date'], 
                  value_vars=algo_emotlist,
                  var_name='Emotion', value_name='Value')
df_algo_cum["Emotion"].replace({'Anger_input':'Anger', 'Disgust_input':'Disgust', 'Fear_input':'Fear', 'Joy_input':'Joy', 'Sadness_input':'Sadness'}, inplace=True)
df_algo_cum.rename(columns={'kb_input_date': 'Date'}, inplace=True)
df_algo_cum = pd.merge(dates_by_emotion, df_algo_cum, how='left', on=['Date', 'Emotion']).fillna(0)
df_algo_cum['CumEmotion'] = df_algo_cum.groupby(['Emotion'])['Value'].cumsum()


# -- Create datasets for the differences in probability in the matched data -- #

    # Daily Moods
myTemp = df_matches_ru[df_matches_ru['source']=='MDS'][['USERID', 'USERGROUP', "timing", "diff_p_anger", "diff_p_disgust", "diff_p_fear", "diff_p_joy", "diff_p_sadness"]]
p_diffs_mds = myTemp.melt(id_vars=['USERID', 'USERGROUP', "timing"], 
                        value_vars=["diff_p_anger", "diff_p_disgust", "diff_p_fear", "diff_p_joy", "diff_p_sadness"],
                        var_name='Emotion', value_name='Difference')
p_diffs_mds["Emotion"].replace({'diff_p_anger':'Anger', 'diff_p_disgust':'Disgust', 'diff_p_fear':'Fear', 'diff_p_joy':'Joy', 'diff_p_sadness':'Sadness'}, inplace=True)
del myTemp

    # DEQ
myTemp = df_matches_ru[df_matches_ru['source']=='DEQ'][['USERID', 'USERGROUP', "timing", "diff_p_anger", "diff_p_disgust", "diff_p_fear", "diff_p_joy", "diff_p_sadness"]]
p_diffs_deq = myTemp.melt(id_vars=['USERID', 'USERGROUP', "timing"], 
                        value_vars=["diff_p_anger", "diff_p_disgust", "diff_p_fear", "diff_p_joy", "diff_p_sadness"],
                        var_name='Emotion', value_name='Difference')
p_diffs_deq["Emotion"].replace({'diff_p_anger':'Anger', 'diff_p_disgust':'Disgust', 'diff_p_fear':'Fear', 'diff_p_joy':'Joy', 'diff_p_sadness':'Sadness'}, inplace=True)
del myTemp

# -- Difference in Probabilities (grouped) -- #

    # Daily Moods
myTemp = df_matches_ru[df_matches_ru['source']=='MDS'][['USERID', 'USERGROUP', "timing", "diff_p_anger_grp", "diff_p_disgust_grp", "diff_p_fear_grp", "diff_p_joy_grp", "diff_p_sadness_grp"]]
p_diffs_mds_grp = myTemp.melt(id_vars=['USERID', 'USERGROUP', 'timing'], 
                  value_vars=dff_emotlist_p_grp,
                  var_name='Emotion', value_name='Difference')
p_diffs_mds_grp["Emotion"].replace({'diff_p_anger_grp':'Anger', 'diff_p_disgust_grp':'Disgust', 'diff_p_fear_grp':'Fear', 'diff_p_joy_grp':'Joy', 'diff_p_sadness_grp':'Sadness'}, inplace=True)

p_diffs_mds_grp = p_diffs_mds_grp.groupby(['USERGROUP', 'timing', 'Emotion', 'Difference']).size().reset_index()
p_diffs_mds_grp['total'] = p_diffs_mds_grp.groupby(['USERGROUP', 'timing', 'Emotion'])[0].transform('sum')
p_diffs_mds_grp['Percentage'] = ((p_diffs_mds_grp[0]/p_diffs_mds_grp['total'])*100).round(2)
del myTemp

    # DEQ
myTemp = df_matches_ru[df_matches_ru['source']=='DEQ'][['USERID', 'USERGROUP', "timing", "diff_p_anger_grp", "diff_p_disgust_grp", "diff_p_fear_grp", "diff_p_joy_grp", "diff_p_sadness_grp"]]
p_diffs_deq_grp = myTemp.melt(id_vars=['USERID', 'USERGROUP', 'timing'], 
                  value_vars=dff_emotlist_p_grp,
                  var_name='Emotion', value_name='Difference')
p_diffs_deq_grp["Emotion"].replace({'diff_p_anger_grp':'Anger', 'diff_p_disgust_grp':'Disgust', 'diff_p_fear_grp':'Fear', 'diff_p_joy_grp':'Joy', 'diff_p_sadness_grp':'Sadness'}, inplace=True)

p_diffs_deq_grp = p_diffs_deq_grp.groupby(['USERGROUP', 'timing', 'Emotion', 'Difference']).size().reset_index()
p_diffs_deq_grp['total'] = p_diffs_deq_grp.groupby(['USERGROUP', 'timing', 'Emotion'])[0].transform('sum')
p_diffs_deq_grp['Percentage'] = ((p_diffs_deq_grp[0]/p_diffs_deq_grp['total'])*100).round(2)
del myTemp

# -- Probabilities as a long file with the survey as one column and the algorithm as one column. Used in regression -- #

    # Raw Values
emot_survey_long = df_matches_ru.melt(id_vars=['USERID', 'USERGROUP', 'timing', 'source'], 
                        value_vars=["anger", "disgust", "fear", "joy", "sadness"],
                        var_name='Emotion', value_name='Survey')
emot_survey_long["Emotion"].replace({'anger':'Anger', 'disgust':'Disgust', 'fear':'Fear', 'joy':'Joy', 'sadness':'Sadness'}, inplace=True)

emot_algo_long = df_matches_ru.melt(id_vars=['USERID', 'USERGROUP', 'timing', 'source'], 
                        value_vars=["max_anger_input", "max_disgust_input", "max_fear_input", "max_joy_input", "max_sadness_input"],
                        var_name='Emotion', value_name='Algorithm')
emot_algo_long["Emotion"].replace({'max_anger_input':'Anger', 'max_disgust_input':'Disgust', 'max_fear_input':'Fear', 'max_joy_input':'Joy', 'max_sadness_input':'Sadness'}, inplace=True)

matched_raw_long = pd.merge(emot_survey_long, emot_algo_long['Algorithm'], left_index=True, right_index=True)

    # Probabilities
p_survey_long = df_matches_ru.melt(id_vars=['USERID', 'USERGROUP', 'timing', 'source'], 
                        value_vars=["p_Anger", "p_disgust", "p_fear", "p_joy", "p_sadness"],
                        var_name='Emotion', value_name='Survey')
p_survey_long["Emotion"].replace({'p_Anger':'Anger', 'p_disgust':'Disgust', 'p_fear':'Fear', 'p_joy':'Joy', 'p_sadness':'Sadness'}, inplace=True)

p_algo_long = df_matches_ru.melt(id_vars=['USERID', 'USERGROUP', 'timing', 'source'], 
                        value_vars=["max_p_anger_input", "max_p_disgust_input", "max_p_fear_input", "max_p_joy_input", "max_p_sadness_input"],
                        var_name='Emotion', value_name='Algorithm')
p_algo_long["Emotion"].replace({'max_p_anger_input':'Anger', 'max_p_disgust_input':'Disgust', 'max_p_fear_input':'Fear', 'max_p_joy_input':'Joy', 'max_p_sadness_input':'Sadness'}, inplace=True)

matched_probs_long = pd.merge(p_survey_long, p_algo_long['Algorithm'], left_index=True, right_index=True)





