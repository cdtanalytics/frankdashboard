
# ----------------------------------------- #
#                                           #
#  TITLE:   FRANK APP EVALUATION DASHBOARD  #
#  PURPOSE: Main App                        #
#  AUTHOR:  Craig Hansen                    #
#  DATE:    06 Mar 2021                     #
#                                           #
# ----------------------------------------- #


# -- IMPORT LIBRARIES -- #

import streamlit as st
import pandas as pd
import seaborn as sns


# -- SET STYLES -- #

st.set_page_config(page_title="FRANK App", layout="wide")

sns.set(style='darkgrid', font_scale=1.1)
pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 1000)

# -- IMPORT LOCAL LIBRARIES -- #

from getdata import *
from functions import *
from plots import *

# ---------- MAIN PAGE ---------- #

def main():

    # - HEADING - #
    st.markdown("<h1 style='text-align: center; color: black; font-size:60px;'>FRANK APP EVALUATION</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: black; font-size:30px;'>Select results from the menu below</p>", unsafe_allow_html=True)
 
    st.write('---')

    # - DASHBOARD 1: RAW DATA - #

    st.title("RAW DATA")
    st.write("Descriptive statistics on the raw data values")

    # Summary information on the raw data
    st.header("SELECT FROM MENU")

    # All data
    summaryInfo = st.beta_expander("Summary Information")
    with summaryInfo:
        
        subtitles("All Data: Summary Information")
        st.write(df_info)
        st.write('---')

        subtitles("Daily Participation (n participants)")
        st.write("Note: Plots by User Group can be toggled by clicking on the User Group in the legend")

        # Daily Moods
        st.write('DAILY MOODS')
        DailyBarChart(mds_daily_cnts)
        DailyBarChartUser(mds_daily_usergrp_cnts)

        # DEQ
        st.write('DEQ')
        DailyBarChart(deq_daily_cnts)
        DailyBarChartUser(deq_daily_usergrp_cnts)

        # Keyboard Input
        st.write('KEYBOARD INPUT')
        DailyBarChart(algo_daily_cnts)
        DailyBarChartUser(algo_daily_usergrp_cnts)

    # Daily Moods
    mds_raw = st.beta_expander("Daily Moods")
    with mds_raw:

        subtitles("Descriptive statistics on emotions")
        st.write("All")
        st.write(summarystats(df_mds, mds_emotlist))
        st.write("By User Group")
        st.write(summarystats_groupby(df_mds,mds_emotlist))

        st.write('---')

        st.write("Note: Plots by User Group can be toggled by clicking on the User Group in the legend")

        Histogram(df_mds_long, 'Value')
        HistogramUser(df_mds_long, 'Value')

        mds_col1, mds_col2 = st.beta_columns(2)

        with mds_col1:
            CorrHeatmap(df_mds, mds_emotlist)
        with mds_col2:
            st.write('---')
            st.write('---')
            corrs = mds_corr(df_mds, mds_emotlist)
            st.write(corrs)

        ScatterMatrix(df_mds, mds_emotlist, [0,11])
        BarChartCumAnimated(df_mds_cum)

        st.write('---')

    # DEQ
    deq_raw = st.beta_expander("DEQ")
    with deq_raw:
        subtitles("Descriptive statistics on emotions")
        st.write("All")
        st.write(summarystats(df_deq, deq_emotlist))
        st.write("By User Group")
        st.write(summarystats_groupby(df_deq, deq_emotlist))

        st.write('---')

        st.write("Note: Plots by User Group can be toggled by clicking on the User Group in the legend")

        Histogram(df_deq_long, 'Value')
        HistogramUser(df_deq_long, 'Value')

        deq_col1, deq_col2 = st.beta_columns(2)

        with deq_col1:
            CorrHeatmap(df_deq, deq_emotlist)
        with deq_col2:
            st.write('---')
            st.write('---')
            corrs = deq_corr(df_deq, deq_emotlist)
            st.write(corrs)

        ScatterMatrix(df_deq, deq_emotlist, [0, 30])
        BarChartCumAnimated(df_deq_cum)

        st.write('---')

    # Keyboard input
    kb_raw = st.beta_expander("Keyboard Input")
    with kb_raw:
        subtitles("Descriptive statistics on emotions")
        st.write("All")
        st.write(summarystats(df_algo, algo_emotlist))
        st.write("By User Group")
        st.write(summarystats_groupby(df_algo, algo_emotlist))

        st.write('---')

        st.write("Note: Plots by User Group can be toggled by clicking on the User Group in the legend")

        Histogram(df_algo_long, 'Value')
        HistogramUser(df_algo_long, 'Value')

        kb_col1, kb_col2 = st.beta_columns(2)

        with kb_col1:
            CorrHeatmap(df_algo, algo_emotlist)
        with kb_col2:
            st.write('---')
            st.write('---')
            corrs = kb_corr(df_algo, algo_emotlist)
            st.write(corrs)

        ScatterMatrix(df_algo, algo_emotlist, [0, 1])
        BarChartCumAnimated(df_algo_cum)

    st.write('---')


    # - DASHBOARD 2: DATA ANALYSES - #

    st.title("MATCHED DATA")
    st.write("The Daily Moods and DEQ data were linked to the Keyboard Input data by matching on date and the time of the input")

    st.header("SELECT FROM MENU")

        # Daily Moods
    prob_diff_mds = st.beta_expander("Daily Moods + Keyboard Input")
    with prob_diff_mds:

        subtitles("Scatter Plot: Raw Values for Survey vs. Algorithm (records matched 30 min +/-)")
        ScatterReg(matched_raw_long[(matched_raw_long['source']=='MDS') & (matched_raw_long['timing']=="30 min +/-")])
        ScatterRegUser(matched_raw_long[(matched_raw_long['source']=='MDS') & (matched_raw_long['timing']=="30 min +/-")])

        subtitles("Scatter Plot: Probabitilities for Survey vs. Algorithm (records matched 30 min +/-)")
        ScatterReg(matched_probs_long[(matched_probs_long['source']=='MDS') & (matched_probs_long['timing']=="30 min +/-")])
        ScatterRegUser(matched_probs_long[(matched_probs_long['source']=='MDS') & (matched_probs_long['timing']=="30 min +/-")])

        subtitles("Histogram: Differences in Probability by User Group (records matched 30 min +/-)")
        Histogram(p_diffs_mds[p_diffs_mds['timing']=="30 min +/-"], 'Difference')
        HistogramUser(p_diffs_mds[p_diffs_mds['timing']=="30 min +/-"], 'Difference')

        subtitles("Strip Plot: Differences in Probability by User Group (records matched 30 min +/-)")
        StripUser(p_diffs_mds[p_diffs_mds['timing']=="30 min +/-"])

        subtitles("Bar Chart: Differences in Probability (categorised) by User Group (records matched 30 min +/-)")
        HorBarProbDiffs(p_diffs_mds_grp[p_diffs_mds_grp['timing']=="30 min +/-"])

    # DEQ
    prob_diff_deq = st.beta_expander("DEQ + Keyboard Input")
    with prob_diff_deq:

        subtitles("Scatter Plot: Raw Values for Survey vs. Algorithm (records matched 30 min +/-)")
        ScatterReg(matched_raw_long[(matched_raw_long['source']=='DEQ') & (matched_raw_long['timing']=="30 min +/-")])
        ScatterRegUser(matched_raw_long[(matched_raw_long['source']=='DEQ') & (matched_raw_long['timing']=="30 min +/-")])

        subtitles("Scatter Plot: Probabitilities for Survey vs. Algorithm (records matched 30 min +/-)")
        ScatterReg(matched_probs_long[(matched_probs_long['source']=='DEQ') & (matched_probs_long['timing']=="30 min +/-")])
        ScatterRegUser(matched_probs_long[(matched_probs_long['source']=='DEQ') & (matched_probs_long['timing']=="30 min +/-")])

        subtitles("Histogram: Differences in Probability by User Group (records matched 30 min +/-)")
        Histogram(p_diffs_deq[p_diffs_deq['timing']=="30 min +/-"], 'Difference')
        HistogramUser(p_diffs_deq[p_diffs_deq['timing']=="30 min +/-"], 'Difference')

        subtitles("Strip Plot: Differences in Probability by User Group (records matched 30 min +/-)")
        StripUser(p_diffs_deq[p_diffs_deq['timing']=="30 min +/-"])

        subtitles("Bar Chart: Differences in Probability (categorised) by User Group (records matched 30 min +/-)")
        HorBarProbDiffs(p_diffs_deq_grp[p_diffs_deq_grp['timing']=="30 min +/-"])


if __name__ == "__main__":
    main()
