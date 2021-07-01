
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
        
        fig = go.Figure(data=[go.Table(
        header=dict(values=list(df.columns),
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[df_info,
                   fill_color='lavender',
                   align='left'))])
        st.plotly_chart(fig)
        
        
        st.write('---')

        subtitles("Daily Participation (n participants)")

        # Daily Moods
        st.header('DAILY MOODS')
        st.write("The plot below shows the daily number of participants across the study period for DAILY MOODS data. There are two main periods of participation.")
        DailyBarChart(mds_daily_cnts)

        st.write("The plot below is the same as above, but stratified by User Group - toggle the USERGROUP in the legend to see individual groups.")
        DailyBarChartUser(mds_daily_usergrp_cnts)

        # DEQ
        st.header('DEQ')
        st.write("The plot below shows the daily number of participants across the study period for DEQ data. There are two main periods of participation.")
        DailyBarChart(deq_daily_cnts)

        st.write("The plot below is the same as above, but stratified by User Group - toggle the USERGROUP in the legend to see individual groups.")
        DailyBarChartUser(deq_daily_usergrp_cnts)

        # Keyboard Input
        st.header('KEYBOARD INPUT')
        st.write("The plot below shows the daily number of participants across the study period for Keyboard Input data. There are two main periods of participation.")
        DailyBarChart(algo_daily_cnts)

        st.write("The plot below is the same as above, but stratified by User Group - toggle the USERGROUP in the legend to see individual groups.")
        DailyBarChartUser(algo_daily_usergrp_cnts)

    # Daily Moods
    mds_raw = st.beta_expander("Daily Moods")
    with mds_raw:

        subtitles("Daily Moods: Descriptive statistics on emotions")
        st.write("All")
        st.write(summarystats(df_mds, mds_emotlist))
        st.write("By User Group")
        st.write(summarystats_groupby(df_mds,mds_emotlist))

        st.write('---')

        st.write("The plots below are histograms of the DAILY MOODS raw data for each emotion. All emotions except joy are skewed with more values towards one. Keep in mind that the values for DAILY MOODS ranged from 1-10.")
        Histogram(df_mds_long, 'Value')

        st.write("The plot below is the same as above, but stratified by User Group - toggle the USERGROUP in the legend to see individual groups.")
        HistogramUser(df_mds_long, 'Value')

        st.write("Below is a correlation plot of the DAILY MOODS for each emotion. Anger is positively correlated with Digust, Fear, and Sadness. Joy is negatively correlated with Sadness.")

        mds_col1, mds_col2 = st.beta_columns(2)

        with mds_col1:
            CorrHeatmap(df_mds, mds_emotlist)
        with mds_col2:
            st.write('---')
            st.write('---')
            corrs = mds_corr(df_mds, mds_emotlist)
            st.write(corrs)
  
        st.write("Below is a scatter matrix of each emotion. The limitation of this plot is that it doesn't show how many records are under each data point.")
        st.write("Toggle the USERGROUP in the legend to see individual groups.")
        ScatterMatrix(df_mds, mds_emotlist, [0,11])

        st.write("The following plot is an animated bar chart of the amount each emotion grows across the study period. It is the cummulative growth of each emotion.")
        BarChartCumAnimated(df_mds_cum)

        st.write('---')

    # DEQ
    deq_raw = st.beta_expander("DEQ")
    with deq_raw:
        subtitles("DEQ: Descriptive statistics on emotions")
        st.write("All")
        st.write(summarystats(df_deq, deq_emotlist))
        st.write("By User Group")
        st.write(summarystats_groupby(df_deq, deq_emotlist))

        st.write('---')

        st.write("The plots below are histograms of the DEQ raw data for each emotion. All emotions except joy and sadness are skewed with more values towards one.")
        Histogram(df_deq_long, 'Value')

        st.write("The plot below is the same as above, but stratified by User Group - toggle the USERGROUP in the legend to see individual groups.")
        HistogramUser(df_deq_long, 'Value')

        st.write("Below is a correlation plot of the DEQ data for each emotion. Anger is positively correlated with Digust, Fear, and Sadness. Joy is more negatively correlated with Sadness compared to the same in DAILY MOODS.")

        deq_col1, deq_col2 = st.beta_columns(2)

        with deq_col1:
            CorrHeatmap(df_deq, deq_emotlist)
        with deq_col2:
            st.write('---')
            st.write('---')
            corrs = deq_corr(df_deq, deq_emotlist)
            st.write(corrs)

        ScatterMatrix(df_deq, deq_emotlist, [0, 30])

        st.write("The following plot is an animated bar chart of the amount each emotion grows across the study period. It is the cummulative growth of each emotion.")
        BarChartCumAnimated(df_deq_cum)

        st.write('---')

    # Keyboard input
    kb_raw = st.beta_expander("Keyboard Input")
    with kb_raw:
        subtitles("Keyboard Input: Descriptive statistics on emotions")
        st.write("All")
        st.write(summarystats(df_algo, algo_emotlist))
        st.write("By User Group")
        st.write(summarystats_groupby(df_algo, algo_emotlist))
        st.write('---')

        st.write("The plots below are histograms of the DEQ raw data for each emotion. All emotions are skewed with more values towards zero.")
        Histogram(df_algo_long, 'Value')

        st.write("The plot below is the same as above, but stratified by User Group - toggle the USERGROUP in the legend to see individual groups.")
        HistogramUser(df_algo_long, 'Value')

        st.write("Below is a correlation plot of the Keyboard Input data for each emotion. Anger is positively correlated mostly with Digust. Sadness is mostly correlated with Fear. Interestingly Joy is positively correlated with Disgust.")

        kb_col1, kb_col2 = st.beta_columns(2)

        with kb_col1:
            CorrHeatmap(df_algo, algo_emotlist)
        with kb_col2:
            st.write('---')
            st.write('---')
            corrs = kb_corr(df_algo, algo_emotlist)
            st.write(corrs)

        ScatterMatrix(df_algo, algo_emotlist, [0, 1])

        st.write("The following plot is an animated bar chart of the amount each emotion grows across the study period. It is the cummulative growth of each emotion.")
        BarChartCumAnimated(df_algo_cum)

        st.write('---')

        subtitles("Sentiment Analysis on the Input Text and comparing it to the algorithm scores")
        st.write("The following shows the correlations between the raw algorithm scores and the sentiment analysis of the keyboard text, along with word count and subjectivity.")
        st.write("Polarity: Ranges from -1.0 to 1.0 for negative to positive sentiment. You would expect text that has a high score for Joy would have more positive sentiment.")
        st.write("Subjectivity: Ranges from 0.0 to 1.0. It is an indication of how much subjectivity there is in the text. This is good for identifying text that shows opinions.")
        st.write("")
        st.write("The results show that sentiment is negatively correlated with Fear and Sadnes, and positively correlated with Joy, however these are weak correlations.")
        st.write("It can also be observed that word count is positivly correlated with Fear, meaning that the more words the higher the Fear score. Word is also strongly correlated with subjectivity.")
        
        sentmds_col11, sentmds_col21 = st.beta_columns(2)
        with sentmds_col11:
            SentCorrHeatmap(sentiment, kb_sent_emotlist)
        with sentmds_col21:
            st.write('---')
            st.write('---')
            corrs = kb_sent_corr(sentiment, kb_sent_emotlist)
            st.write(corrs)

    # - DASHBOARD 2: DATA ANALYSES - #

    st.title("MATCHED DATA")
    st.write("In this section we now compare the DAILY MOODS and DEQ with the algorithm by matching the records on date and the time of the input.")
    st.write("The data were matched on a range of windows, starting with 30min +/- (e.g. within a 1hr window) up to 180min +/- (e.g. 3hr window).")
    st.write("After comparing results across windows, it was decided to focus on the 1hr window as there was very little change in results across windows.")

    st.header("SELECT FROM MENU")

        # Daily Moods
    prob_diff_mds = st.beta_expander("Daily Moods + Keyboard Input")
    with prob_diff_mds:

            # Scatterplots
        subtitles("Scatter Plot: Raw Values for Survey vs. Algorithm (records matched 30 min +/-)")
        st.write("The plots below are scatter plots showing the algorithm scores against the matched DAILY MOODS scores with a regression line.")
        ScatterReg(matched_raw_long[(matched_raw_long['source']=='MDS') & (matched_raw_long['timing']=="30 min +/-")])
        st.write("The plot below is the same as above, but stratified by User Group - toggle the USERGROUP in the legend to see individual groups.")
        ScatterRegUser(matched_raw_long[(matched_raw_long['source']=='MDS') & (matched_raw_long['timing']=="30 min +/-")])

            # Scatterplots - probabilities
        subtitles("Scatter Plot: Probabitilities for Survey vs. Algorithm (records matched 30 min +/-)")
        st.write("The following plots are similar to those above, but this time we look at the probability (area under the curve). The perfect outcome here would be a diagonal line from bottom left to top right.")
        ScatterReg(matched_probs_long[(matched_probs_long['source']=='MDS') & (matched_probs_long['timing']=="30 min +/-")])
        st.write("The plot below is the same as above, but stratified by User Group - toggle the USERGROUP in the legend to see individual groups.")
        ScatterRegUser(matched_probs_long[(matched_probs_long['source']=='MDS') & (matched_probs_long['timing']=="30 min +/-")])

            # Histograms - difference in probabilities
        subtitles("Histogram: Differences in Probability by User Group (records matched 30 min +/-)")
        st.write("The following plots are histograms of the difference between the probabilities (area under the curve) for algrorithm and DAILY MOODS. The ideal results would show less difference and therefore a higher proportion towards zero.")
        Histogram(p_diffs_mds[p_diffs_mds['timing']=="30 min +/-"], 'Difference')
        st.write("The plot below is the same as above, but stratified by User Group - toggle the USERGROUP in the legend to see individual groups.")
        HistogramUser(p_diffs_mds[p_diffs_mds['timing']=="30 min +/-"], 'Difference')

            # Strip plot differences in probabilities
        subtitles("Strip Plot: Differences in Probability by User Group (records matched 30 min +/-)")
        st.write("The following plots are strip plots, which show the scattered distribution of the differences in probabilities between the algorithm and matched DAILY MOODS.")
        StripUser(p_diffs_mds[p_diffs_mds['timing']=="30 min +/-"])

            # Bar chart - differences in probabilities
        subtitles("Bar Chart: Differences in Probability (categorised) by User Group (records matched 30 min +/-)")
        st.write("The following plots show the percentage of records categorised by the differences in probabilities (bins = 0.10). The ideal result would show a higher percentage in the <0.10 group.")
        HorBarProbDiffs(p_diffs_mds_grp[p_diffs_mds_grp['timing']=="30 min +/-"])

                    # Correlation heatmap
        subtitles("Correlation Plot: Raw Values for DAILY MOODS, Word Count, Polarity, Subjectivity (records matched 30 min +/-)")
        st.write("The following shows the correlations between the DAILY MOODS and the sentiment analysis of the matched keyboard text, along with word count and subjectivity.")
        st.write("Polarity: Ranges from -1.0 to 1.0 for negative to positive sentiment. You would expect text that has a high score for Joy would have more positive sentiment.")
        st.write("Subjectivity: Ranges from 0.0 to 1.0. It is an indication of how much subjectivity there is in the text. This is good for identifying text that shows opinions.")
        
        sentmds_col1, sentmds_col2 = st.beta_columns(2)
        mask1 = (df_matches_sent['timing'] =="30 min +/-") & (df_matches_sent['source']=="MDS")
        with sentmds_col1:
            SentCorrHeatmap(df_matches_sent[mask1], srvy_sent_emotlist)
        with sentmds_col2:
            st.write('---')
            st.write('---')
            corrs = srvy_sent_corr(df_matches_sent[mask1], srvy_sent_emotlist)
            st.write(corrs)

        subtitles("Same as above, where subjectivity is > 0.5")
        sentmds_col11, sentmds_col21 = st.beta_columns(2)
        mask1 = (df_matches_sent['timing'] =="30 min +/-") & (df_matches_sent['source']=="MDS") & (df_matches_sent['subjectivity']>=0.5)
        with sentmds_col11:
            SentCorrHeatmap(df_matches_sent[mask1], srvy_sent_emotlist)
        with sentmds_col21:
            st.write('---')
            st.write('---')
            corrs = srvy_sent_corr(df_matches_sent[mask1], srvy_sent_emotlist)
            st.write(corrs)

        subtitles("Same as above, where subjectivity is > 0.7")
        sentmds_col11, sentmds_col21 = st.beta_columns(2)
        mask1 = (df_matches_sent['timing'] =="30 min +/-") & (df_matches_sent['source']=="MDS") & (df_matches_sent['subjectivity']>=0.7)
        with sentmds_col11:
            SentCorrHeatmap(df_matches_sent[mask1], srvy_sent_emotlist)
        with sentmds_col21:
            st.write('---')
            st.write('---')
            corrs = srvy_sent_corr(df_matches_sent[mask1], srvy_sent_emotlist)
            st.write(corrs)

        subtitles("Same as above, where word count is > 5")
        sentmds_col11, sentmds_col21 = st.beta_columns(2)
        mask1 = (df_matches_sent['timing'] =="30 min +/-") & (df_matches_sent['source']=="DEQ") & (df_matches_sent['word_count']>=5)
        with sentmds_col11:
            SentCorrHeatmap(df_matches_sent[mask1], srvy_sent_emotlist)
        with sentmds_col21:
            st.write('---')
            st.write('---')
            corrs = srvy_sent_corr(df_matches_sent[mask1], srvy_sent_emotlist)
            st.write(corrs)

        subtitles("Same as above, where word count is > 10")
        sentmds_col11, sentmds_col21 = st.beta_columns(2)
        mask1 = (df_matches_sent['timing'] =="30 min +/-") & (df_matches_sent['source']=="DEQ") & (df_matches_sent['word_count']>=10)
        with sentmds_col11:
            SentCorrHeatmap(df_matches_sent[mask1], srvy_sent_emotlist)
        with sentmds_col21:
            st.write('---')
            st.write('---')
            corrs = srvy_sent_corr(df_matches_sent[mask1], srvy_sent_emotlist)
            st.write(corrs)

    # DEQ
    prob_diff_deq = st.beta_expander("DEQ + Keyboard Input")
    with prob_diff_deq:

            # Scatterplots
        subtitles("Scatter Plot: Raw Values for Survey vs. Algorithm (records matched 30 min +/-)")
        st.write("The plots below are scatter plots showing the algorithm scores against the matched DEQ scores with a regression line.")
        ScatterReg(matched_raw_long[(matched_raw_long['source']=='DEQ') & (matched_raw_long['timing']=="30 min +/-")])
        st.write("The plot below is the same as above, but stratified by User Group - toggle the USERGROUP in the legend to see individual groups.")
        ScatterRegUser(matched_raw_long[(matched_raw_long['source']=='DEQ') & (matched_raw_long['timing']=="30 min +/-")])

            # Scatterplot probabilities
        subtitles("Scatter Plot: Probabitilities for Survey vs. Algorithm (records matched 30 min +/-)")
        st.write("The following plots are similar to those above, but this time we look at the probability (area under the curve). The perfect outcome here would be a diagonal line from bottom left to top right.")
        ScatterReg(matched_probs_long[(matched_probs_long['source']=='DEQ') & (matched_probs_long['timing']=="30 min +/-")])
        st.write("The plot below is the same as above, but stratified by User Group - toggle the USERGROUP in the legend to see individual groups.")
        ScatterRegUser(matched_probs_long[(matched_probs_long['source']=='DEQ') & (matched_probs_long['timing']=="30 min +/-")])

            # Histogram - differences in probabilities
        subtitles("Histogram: Differences in Probability by User Group (records matched 30 min +/-)")
        st.write("The following plots are histograms of the difference between the probabilities (area under the curve) for algrorithm and DEQ. The ideal results would show less difference and therefore a higher proportion towards zero.")
        Histogram(p_diffs_deq[p_diffs_deq['timing']=="30 min +/-"], 'Difference')
        st.write("The plot below is the same as above, but stratified by User Group - toggle the USERGROUP in the legend to see individual groups.")
        HistogramUser(p_diffs_deq[p_diffs_deq['timing']=="30 min +/-"], 'Difference')
       
            # Strip plot - differences in probabilities
        subtitles("Strip Plot: Differences in Probability by User Group (records matched 30 min +/-)")
        st.write("The following plots are strip plots, which show the scattered distribution of the differences in probabilities between the algorithm and matched DEQ.")
        StripUser(p_diffs_deq[p_diffs_deq['timing']=="30 min +/-"])

            # Bar chart - differences in probabilities
        subtitles("Bar Chart: Differences in Probability (categorised) by User Group (records matched 30 min +/-)")
        st.write("The following plots show the percentage of records categorised by the differences in probabilities (bins = 0.10). The ideal result would show a higher percentage in the <0.10 group.")
        HorBarProbDiffs(p_diffs_deq_grp[p_diffs_deq_grp['timing']=="30 min +/-"])

            # Correlation heatmap
        subtitles("Correlation Plot: Raw Values for DEQ, Word Count, Polarity, Subjectivity (records matched 30 min +/-)")
        st.write("The following shows the correlations between the DEQ and the sentiment analysis of the matched keyboard text, along with word count and subjectivity.")
        st.write("Polarity: Ranges from -1.0 to 1.0 for negative to positive sentiment. You would expect text that has a high score for Joy would have more positive sentiment.")
        st.write("Subjectivity: Ranges from 0.0 to 1.0. It is an indication of how much subjectivity there is in the text. This is good for identifying text that shows opinions.")
        sentmds_col1, sentmds_col2 = st.beta_columns(2)
        mask2 = (df_matches_sent['timing'] =="30 min +/-") & (df_matches_sent['source']=="DEQ")
        with sentmds_col1:
            SentCorrHeatmap(df_matches_sent[mask2], kb_sent_emotlist)
        with sentmds_col2:
            st.write('---')
            st.write('---')
            corrs = kb_sent_corr(df_matches_sent[mask2], kb_sent_emotlist)
            st.write(corrs)

        subtitles("Same as above, where subjectivity is > 0.5")
        sentmds_col11, sentmds_col21 = st.beta_columns(2)
        mask1 = (df_matches_sent['timing'] =="30 min +/-") & (df_matches_sent['source']=="DEQ") & (df_matches_sent['subjectivity']>=0.5)
        with sentmds_col11:
            SentCorrHeatmap(df_matches_sent[mask1], kb_sent_emotlist)
        with sentmds_col21:
            st.write('---')
            st.write('---')
            corrs = kb_sent_corr(df_matches_sent[mask1], kb_sent_emotlist)
            st.write(corrs)

        subtitles("Same as above, where subjectivity is > 0.7")
        sentmds_col11, sentmds_col21 = st.beta_columns(2)
        mask1 = (df_matches_sent['timing'] =="30 min +/-") & (df_matches_sent['source']=="DEQ") & (df_matches_sent['subjectivity']>=0.7)
        with sentmds_col11:
            SentCorrHeatmap(df_matches_sent[mask1], kb_sent_emotlist)
        with sentmds_col21:
            st.write('---')
            st.write('---')
            corrs = kb_sent_corr(df_matches_sent[mask1], kb_sent_emotlist)
            st.write(corrs)
            
        subtitles("Same as above, where word count is > 5")
        sentmds_col11, sentmds_col21 = st.beta_columns(2)
        mask1 = (df_matches_sent['timing'] =="30 min +/-") & (df_matches_sent['source']=="DEQ") & (df_matches_sent['word_count']>=5)
        with sentmds_col11:
            SentCorrHeatmap(df_matches_sent[mask1], kb_sent_emotlist)
        with sentmds_col21:
            st.write('---')
            st.write('---')
            corrs = kb_sent_corr(df_matches_sent[mask1], kb_sent_emotlist)
            st.write(corrs)

        subtitles("Same as above, where word count is > 10")
        sentmds_col11, sentmds_col21 = st.beta_columns(2)
        mask1 = (df_matches_sent['timing'] =="30 min +/-") & (df_matches_sent['source']=="DEQ") & (df_matches_sent['word_count']>=10)
        with sentmds_col11:
            SentCorrHeatmap(df_matches_sent[mask1], kb_sent_emotlist)
        with sentmds_col21:
            st.write('---')
            st.write('---')
            corrs = kb_sent_corr(df_matches_sent[mask1], kb_sent_emotlist)
            st.write(corrs)

if __name__ == "__main__":
    main()
