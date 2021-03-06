
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
        
        st.write('---')

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
        CorrHeatmap(df_mds, mds_emotlist)
        corrs = mds_corr(df_mds, mds_emotlist)
        st.dataframe(corrs)
        st.write('---')
  
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
        CorrHeatmap(df_deq, deq_emotlist)
        corrs = deq_corr(df_deq, deq_emotlist)
        st.dataframe(corrs)
        st.write('---')

        st.write("The following plot is a scatter matrix of each emotion - toggle the USERGROUP in the legend to see individual groups.")
        ScatterMatrix(df_deq, deq_emotlist, [0, 30])

        st.write("The following plot is an animated bar chart of the amount each emotion grows across the study period. It is the cummulative growth of each emotion.")
        BarChartCumAnimated(df_deq_cum)

        st.write('---')

    # Keyboard input
    kb_raw = st.beta_expander("Keyboard Input")
    with kb_raw:
        # Raw data
        subtitles("Keyboard Input (Raw Data): Descriptive statistics on emotions")
        st.write("All")
        st.write(summarystats(sentiment, kb_emotlist))
        st.write("By User Group")
        st.write(summarystats_groupby(sentiment, kb_emotlist))
        st.write('---')
        
        st.write("The plots below are histograms of the Keyboard Input raw data for each emotion. All emotions are skewed with more values towards zero.")
        Histogram(df_sent_long, 'Value')

        st.write("The plot below is the same as above, but stratified by User Group - toggle the USERGROUP in the legend to see individual groups.")
        HistogramUser(df_sent_long, 'Value')
        
        st.write("The following plot is a scatter matrix of each emotion - toggle the USERGROUP in the legend to see individual groups.")
        ScatterMatrix(sentiment, kb_emotlist2, [0, 1])
        
        subtitles("Keyboard Input (Raw Data): Mean emotions based on the emoji identified in the text")
        st.write("The website http://www.unicode.org/emoji/charts/full-emoji-list.html was scraped for all emoji text, and then the Keyboard Input text was scanned for each emoji.")
        st.write("The following shows the mean scores for each emotion based on the type of emoji identified. The [] represents records where no emoji was identified.")
        emoji_mean = sentiment[['Anger_Input', 'Disgust_Input', 'Fear_Input', 'Joy_Input', 'Sadness_Input', 'emoji']].groupby('emoji').mean().round(4)
        emoji_count = sentiment.groupby('emoji')['emoji'].agg({'count'})
        emoji_stats = pd.merge(emoji_count, emoji_mean, on='emoji')
        st.dataframe(emoji_stats)
        st.write('---')
        
        subtitles("Keyboard Input (Raw Data): Sentiment Analysis on the Input Text and comparing it to the algorithm scores")
        
        st.write("The following plot is a scatter plot comparing the algorithm scores compared to the sentiment analysis (polarity) - toggle the USERGROUP in the legend to see individual groups.")
        ScatterRegUser2(df_kb_pol)
        
        st.write("The following shows the correlations between the raw algorithm scores and the sentiment analysis of the keyboard text, along with word count and subjectivity.")
        st.write("Polarity: Ranges from -1.0 to 1.0 for negative to positive sentiment. You would expect text that has a high score for Joy would have more positive sentiment.")
        st.write("Subjectivity: Ranges from 0.0 to 1.0. It is an indication of how much subjectivity there is in the text. This is good for identifying text that shows opinions.")
        st.write("")
        st.write("The results show that sentiment is negatively correlated with Fear and Sadnes, and positively correlated with Joy, however these are weak correlations.")
        st.write("It can also be observed that word count is positively correlated with Fear, meaning that the more words the higher the Fear score. Word count is also strongly correlated with subjectivity.")
        
        SentCorrHeatmap(sentiment, kb_sent_emotlist)
        corrs = kb_sent_corr(sentiment, kb_sent_emotlist)
        st.dataframe(corrs)
        
        st.write('---')

        # Rolled up records
        subtitles("Keyboard Input (Rolled up records): Descriptive statistics on emotions")
        st.write("In the raw data there are mutliple records for each participant, date, and time. These records were 'rolled up' in preparation for the matching with DAILY MOODS and DEQ.")
        st.write("---")
        st.write("All")
        st.write(summarystats(df_algo, algo_emotlist))
        st.write("By User Group")
        st.write(summarystats_groupby(df_algo, algo_emotlist))
        st.write('---')

        st.write("The plots below are histograms of the Keyboard Input raw data for each emotion. All emotions are skewed with more values towards zero.")
        Histogram(df_algo_long, 'Value')

        st.write("The plot below is the same as above, but stratified by User Group - toggle the USERGROUP in the legend to see individual groups.")
        HistogramUser(df_algo_long, 'Value')

        st.write("Below is a correlation plot of the Keyboard Input data for each emotion. Anger is positively correlated mostly with Digust. Sadness is mostly correlated with Fear. Interestingly Joy is positively correlated with Disgust.")
        CorrHeatmap(df_algo, algo_emotlist)
        corrs = kb_corr(df_algo, algo_emotlist)
        st.dataframe(corrs)
        st.write('---')

        ScatterMatrix(df_algo, algo_emotlist, [0, 1])

        st.write("The following plot is an animated bar chart of the amount each emotion grows across the study period. It is the cummulative growth of each emotion.")
        BarChartCumAnimated(df_algo_cum)

        st.write('---')


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
        subtitles("Matched Records (from Rolled Up): Values for Survey vs. Algorithm (records matched 30 min +/-)")
        st.write("The plots below are scatter plots showing the algorithm scores against the matched DAILY MOODS scores with a regression line.")
        ScatterReg(matched_raw_long[(matched_raw_long['source']=='MDS') & (matched_raw_long['timing']=="30 min +/-")])
        st.write("The plot below is the same as above, but stratified by User Group - toggle the USERGROUP in the legend to see individual groups.")
        ScatterRegUser(matched_raw_long[(matched_raw_long['source']=='MDS') & (matched_raw_long['timing']=="30 min +/-")])

            # Scatterplots - probabilities
        subtitles("Matched Records (from Rolled Up): Probabitilities for Survey vs. Algorithm (records matched 30 min +/-)")
        st.write("The following plots are similar to those above, but this time we look at the probability (area under the curve). The perfect outcome here would be a diagonal line from bottom left to top right.")
        ScatterReg(matched_probs_long[(matched_probs_long['source']=='MDS') & (matched_probs_long['timing']=="30 min +/-")])
        st.write("The plot below is the same as above, but stratified by User Group - toggle the USERGROUP in the legend to see individual groups.")
        ScatterRegUser(matched_probs_long[(matched_probs_long['source']=='MDS') & (matched_probs_long['timing']=="30 min +/-")])

            # Histograms - difference in probabilities
        subtitles("Matched Records (from Rolled Up): Differences in Probability by User Group (records matched 30 min +/-)")
        st.write("The following plots are histograms of the difference between the probabilities (area under the curve) for algrorithm and DAILY MOODS. The ideal results would show less difference and therefore a higher proportion towards zero.")
        Histogram(p_diffs_mds[p_diffs_mds['timing']=="30 min +/-"], 'Difference')
        st.write("The plot below is the same as above, but stratified by User Group - toggle the USERGROUP in the legend to see individual groups.")
        HistogramUser(p_diffs_mds[p_diffs_mds['timing']=="30 min +/-"], 'Difference')

            # Strip plot differences in probabilities
        st.write("The following plots are strip plots, which show the scattered distribution of the differences in probabilities between the algorithm and matched DAILY MOODS.")
        StripUser(p_diffs_mds[p_diffs_mds['timing']=="30 min +/-"])

            # Bar chart - differences in probabilities
        st.write("The following plots show the percentage of records categorised by the differences in probabilities (bins = 0.10). The ideal result would show a higher percentage in the <0.10 group.")
        HorBarProbDiffs(p_diffs_mds_grp[p_diffs_mds_grp['timing']=="30 min +/-"])

             # Correlation heatmap
        subtitles("Matched Records (from Raw): Values for DAILY MOODS, Word Count, Polarity, Subjectivity (records matched 30 min +/-)")
        st.write("The following shows the correlations between the DAILY MOODS and the sentiment analysis of the matched keyboard text, along with word count and subjectivity.")
        st.write("Polarity: Ranges from -1.0 to 1.0 for negative to positive sentiment. You would expect text that has a high score for Joy would have more positive sentiment.")
        st.write("Subjectivity: Ranges from 0.0 to 1.0. It is an indication of how much subjectivity there is in the text. This is good for identifying text that shows opinions.")
        
        mask1 = (df_matches_sent['timing'] =="30 min +/-") & (df_matches_sent['source']=="MDS")
        SentCorrHeatmap(df_matches_sent[mask1], srvy_sent_emotlist)
        corrs = srvy_sent_corr(df_matches_sent[mask1], srvy_sent_emotlist)
        st.dataframe(corrs)
        st.write('---')

        subtitles("Same as above, where subjectivity is > 0.5")
        mask1 = (df_matches_sent['timing'] =="30 min +/-") & (df_matches_sent['source']=="MDS") & (df_matches_sent['subjectivity']>=0.5)
        SentCorrHeatmap(df_matches_sent[mask1], srvy_sent_emotlist)
        corrs = srvy_sent_corr(df_matches_sent[mask1], srvy_sent_emotlist)
        st.dataframe(corrs)
        st.write('---')

        subtitles("Same as above, where subjectivity is > 0.7")
        mask1 = (df_matches_sent['timing'] =="30 min +/-") & (df_matches_sent['source']=="MDS") & (df_matches_sent['subjectivity']>=0.7)
        SentCorrHeatmap(df_matches_sent[mask1], srvy_sent_emotlist)
        corrs = srvy_sent_corr(df_matches_sent[mask1], srvy_sent_emotlist)
        st.dataframe(corrs)
        st.write('---')

        subtitles("Same as above, where word count is > 5")
        mask1 = (df_matches_sent['timing'] =="30 min +/-") & (df_matches_sent['source']=="DEQ") & (df_matches_sent['word_count']>=5)
        SentCorrHeatmap(df_matches_sent[mask1], srvy_sent_emotlist)
        corrs = srvy_sent_corr(df_matches_sent[mask1], srvy_sent_emotlist)
        st.dataframe(corrs)
        st.write('---')

        subtitles("Same as above, where word count is > 10")
        mask1 = (df_matches_sent['timing'] =="30 min +/-") & (df_matches_sent['source']=="DEQ") & (df_matches_sent['word_count']>=10)
        SentCorrHeatmap(df_matches_sent[mask1], srvy_sent_emotlist)
        corrs = srvy_sent_corr(df_matches_sent[mask1], srvy_sent_emotlist)
        st.dataframe(corrs)
        st.write('---')

    # DEQ
    prob_diff_deq = st.beta_expander("DEQ + Keyboard Input")
    with prob_diff_deq:

            # Scatterplots
        subtitles("Matched Records (from Rolled Up): Values for Survey vs. Algorithm (records matched 30 min +/-)")
        st.write("The plots below are scatter plots showing the algorithm scores against the matched DEQ scores with a regression line.")
        ScatterReg(matched_raw_long[(matched_raw_long['source']=='DEQ') & (matched_raw_long['timing']=="30 min +/-")])
        st.write("The plot below is the same as above, but stratified by User Group - toggle the USERGROUP in the legend to see individual groups.")
        ScatterRegUser(matched_raw_long[(matched_raw_long['source']=='DEQ') & (matched_raw_long['timing']=="30 min +/-")])

            # Scatterplot probabilities
        subtitles("Matched Records (from Rolled Up): Probabitilities for Survey vs. Algorithm (records matched 30 min +/-)")
        st.write("The following plots are similar to those above, but this time we look at the probability (area under the curve). The perfect outcome here would be a diagonal line from bottom left to top right.")
        ScatterReg(matched_probs_long[(matched_probs_long['source']=='DEQ') & (matched_probs_long['timing']=="30 min +/-")])
        st.write("The plot below is the same as above, but stratified by User Group - toggle the USERGROUP in the legend to see individual groups.")
        ScatterRegUser(matched_probs_long[(matched_probs_long['source']=='DEQ') & (matched_probs_long['timing']=="30 min +/-")])

            # Histogram - differences in probabilities
        subtitles("Matched Records (from Rolled Up): Differences in Probability by User Group (records matched 30 min +/-)")
        st.write("The following plots are histograms of the difference between the probabilities (area under the curve) for algrorithm and DEQ. The ideal results would show less difference and therefore a higher proportion towards zero.")
        Histogram(p_diffs_deq[p_diffs_deq['timing']=="30 min +/-"], 'Difference')
        st.write("The plot below is the same as above, but stratified by User Group - toggle the USERGROUP in the legend to see individual groups.")
        HistogramUser(p_diffs_deq[p_diffs_deq['timing']=="30 min +/-"], 'Difference')
       
            # Strip plot - differences in probabilities
        st.write("The following plots are strip plots, which show the scattered distribution of the differences in probabilities between the algorithm and matched DEQ.")
        StripUser(p_diffs_deq[p_diffs_deq['timing']=="30 min +/-"])

            # Bar chart - differences in probabilities
        st.write("The following plots show the percentage of records categorised by the differences in probabilities (bins = 0.10). The ideal result would show a higher percentage in the <0.10 group.")
        HorBarProbDiffs(p_diffs_deq_grp[p_diffs_deq_grp['timing']=="30 min +/-"])

            # Correlation heatmap
        subtitles("Matched Records (from Raw): Values for DEQ, Word Count, Polarity, Subjectivity (records matched 30 min +/-)")
        st.write("The following shows the correlations between the DEQ and the sentiment analysis of the matched keyboard text, along with word count and subjectivity.")
        st.write("Polarity: Ranges from -1.0 to 1.0 for negative to positive sentiment. You would expect text that has a high score for Joy would have more positive sentiment.")
        st.write("Subjectivity: Ranges from 0.0 to 1.0. It is an indication of how much subjectivity there is in the text. This is good for identifying text that shows opinions.")
        sentmds_col1, sentmds_col2 = st.beta_columns([3,1])
        mask2 = (df_matches_sent['timing'] =="30 min +/-") & (df_matches_sent['source']=="DEQ")
        SentCorrHeatmap(df_matches_sent[mask2], kb_sent_emotlist)
        corrs = kb_sent_corr(df_matches_sent[mask2], kb_sent_emotlist)
        st.dataframe(corrs)
        st.write('---')

        subtitles("Same as above, where subjectivity is > 0.5")
        mask1 = (df_matches_sent['timing'] =="30 min +/-") & (df_matches_sent['source']=="DEQ") & (df_matches_sent['subjectivity']>=0.5)
        SentCorrHeatmap(df_matches_sent[mask1], kb_sent_emotlist)
        corrs = kb_sent_corr(df_matches_sent[mask1], kb_sent_emotlist)
        st.dataframe(corrs)
        st.write('---')

        subtitles("Same as above, where subjectivity is > 0.7")
        mask1 = (df_matches_sent['timing'] =="30 min +/-") & (df_matches_sent['source']=="DEQ") & (df_matches_sent['subjectivity']>=0.7)
        SentCorrHeatmap(df_matches_sent[mask1], kb_sent_emotlist)
        corrs = kb_sent_corr(df_matches_sent[mask1], kb_sent_emotlist)
        st.dataframe(corrs)
        st.write('---')
            
        subtitles("Same as above, where word count is > 5")
        mask1 = (df_matches_sent['timing'] =="30 min +/-") & (df_matches_sent['source']=="DEQ") & (df_matches_sent['word_count']>=5)
        SentCorrHeatmap(df_matches_sent[mask1], kb_sent_emotlist)
        corrs = kb_sent_corr(df_matches_sent[mask1], kb_sent_emotlist)
        st.dataframe(corrs)
        st.write('---')

        subtitles("Same as above, where word count is > 10")
        mask1 = (df_matches_sent['timing'] =="30 min +/-") & (df_matches_sent['source']=="DEQ") & (df_matches_sent['word_count']>=10)
        SentCorrHeatmap(df_matches_sent[mask1], kb_sent_emotlist)
        corrs = kb_sent_corr(df_matches_sent[mask1], kb_sent_emotlist)
        st.dataframe(corrs)
        st.write('---')

if __name__ == "__main__":
    main()
