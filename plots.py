
# ----------------------------------------- #
#                                           #
#  TITLE:   FRANK APP EVALUATION DASHBOARD  #
#  PURPOSE: Data Visualizatoins             #
#  AUTHOR:  Craig Hansen                    #
#  DATE:    06 Mar 2021                     #
# ----------------------------------------- #


# -- Import Python Libraries -- #
from getdata import *
import streamlit as st
import plotly.express as px
import plotly.graph_objs as go
import numpy as np

# -- Daily Counts Bar Chart --- #

def DailyBarChart(data):
    fig = px.bar(data, x='Date', 
                      y='USERID', 
                      labels=dict(Date="Date", USERID="Participants (n)"))
    fig.update_layout(title='Number of distinct participants each day')
    fig.update_layout(width=1600, height=400, xaxis_range=['2021-01-01', '2021-06-01'])
    st.plotly_chart(fig)

def DailyBarChartUser(data):
    fig = px.bar(data, x='Date', 
                      y='USERID',
                      color='USERGROUP', 
                      labels=dict(Date="Date", USERID="Participants (n)"))
    fig.update_layout(title='Number of distinct participants each day (By User Group)')
    fig.update_layout(width=1700, height=400, xaxis_range=['2021-01-01', '2021-06-01'])
    st.plotly_chart(fig)

# -- Histograms of each emotion (facet grid) -- #

def Histogram(data, xvalue):
    fig = px.histogram(data, x=xvalue, 
                            facet_col="Emotion", 
                            histnorm="percent",
                            nbins=10,
                            opacity=0.5)
    fig.update_layout(title='Histogram of each emotion')
    fig.update_layout(width=1500, height=400)
    # Get rid of the "Emotion="
    for a in fig.layout.annotations:
        a.text = a.text.split("=")[1]
    st.plotly_chart(fig)

def HistogramUser(data, xvalue):
    fig = px.histogram(data, x=xvalue, 
                            facet_col="Emotion", 
                            histnorm="percent",
                            color="USERGROUP",
                            nbins=10,
                            opacity=0.5)
    fig.update_layout(title='Histogram of each emotion (By User Group)')
    fig.update_layout(width=1600, height=400)
    # Get rid of the "Emotion="
    for a in fig.layout.annotations:
        a.text = a.text.split("=")[1]
    st.plotly_chart(fig)

# -- Correlation plot of the emotions -- #

def CorrHeatmap(data, emotionslist):
    corr = data[emotionslist].corr(method='spearman')
    mask = np.triu(np.ones_like(corr, dtype=bool))
    corr_mask = corr.mask(mask)
    ticklist = emotionslist
    ticklabels = ['Anger', 'Disgust', 'Fear', 'Joy', 'Sadness']
    fig = go.Figure(data=go.Heatmap(
                        z=corr_mask.values,
                        y=corr_mask.index.values,
                        x=corr_mask.columns.values,
                        colorscale = px.colors.diverging.RdBu,
                        zmin=-1, zmax=1,
                        xgap=3,
                        ygap=3))
    fig.update_xaxes(tickmode='array',
                        tickvals=ticklist,
                        ticktext=ticklabels)
    fig.update_yaxes(tickmode='array',
                        tickvals=ticklist,
                        ticktext=ticklabels)
    fig.update_layout(title="Correlation Heatmap", yaxis_autorange='reversed', template='plotly_white')
    st.plotly_chart(fig)

def SentCorrHeatmap(data, emotionslist):
    corr = data[emotionslist].corr(method='spearman')
    mask = np.triu(np.ones_like(corr, dtype=bool))
    corr_mask = corr.mask(mask)
    ticklist = emotionslist
    ticklabels = ['Anger', 'Disgust', 'Fear', 'Joy', 'Sadness', 'Word Count', 'Polarity', 'Subjectivity']
    fig = go.Figure(data=go.Heatmap(
                        z=corr_mask.values,
                        y=corr_mask.index.values,
                        x=corr_mask.columns.values,
                        colorscale = px.colors.diverging.RdBu,
                        zmin=-1, zmax=1,
                        xgap=3,
                        ygap=3))
    fig.update_xaxes(tickmode='array',
                        tickvals=ticklist,
                        ticktext=ticklabels)
    fig.update_yaxes(tickmode='array',
                        tickvals=ticklist,
                        ticktext=ticklabels)
    fig.update_layout(title="Correlation Heatmap", yaxis_autorange='reversed', template='plotly_white')
    st.plotly_chart(fig)


# -- Scatter matrix of emotions -- #

def ScatterMatrix(data, emotionslist, rangelist):
    fig = px.scatter_matrix(data, dimensions=emotionslist,
                                    labels=dict({emotionslist[0]:'Anger', emotionslist[1]:'Disgust', emotionslist[2]:'Fear', emotionslist[3]:'Joy', emotionslist[4]:'Sadness'}),
                                    color="USERGROUP"
                            )
    fig.update_layout(title='Scatter matrix of each emotion')
    fig.update_layout(width=1000, height=800)
    fig.update_layout({"xaxis"+str(i+1): dict(range = rangelist) for i in range(5)})
    fig.update_layout({"yaxis"+str(i+1): dict(range = rangelist) for i in range(5)})

    st.plotly_chart(fig)

# -- Strip plot -- #

def StripUser(data):
    fig = px.strip(data, x="USERGROUP", 
                         y="Difference",
                         color='USERGROUP',
                         facet_col="Emotion")
    fig.update_layout(title='Strip plot of difference in area under the curve')
    fig.update_layout(width=1600, height=400)
    for a in fig.layout.annotations:
        a.text = a.text.split("=")[1]
    st.plotly_chart(fig)


# -- Animated Bar Plot of Cummulative Emotions -- #

def BarChartCumAnimated(data):
    fig = px.bar(data, 
                    x='Emotion', 
                    y='CumEmotion', 
                    color='Emotion',
                    animation_group='Emotion',
                    animation_frame=data['Date'].astype(str),
                    range_y=[0, (0.1*data.CumEmotion.max()) + (data.CumEmotion.max())],
                    labels=dict(CumEmotion='Cummulative sum', Emotion='Emotion')
                    )
    fig.update_layout(title='Cummulative emotions across the study period')
    fig.update_layout(width=1500, height=500)
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 5
    st.plotly_chart(fig)

# -- Scatter plot with linear regression (survey probabilities vs. algorithm probabilities) -- #

def ScatterReg(data):
    fig = px.scatter(data, 
                    x="Survey", 
                    y="Algorithm",
                    facet_col="Emotion", 
                    trendline="ols")

    fig.update_layout(title='Scatter plot of Survey vs. Algorithm')
    fig.update_layout(width=1600, height=400)
    for a in fig.layout.annotations:
        a.text = a.text.split("=")[1]
    st.plotly_chart(fig)

def ScatterRegUser(data):
    fig = px.scatter(data, 
                    x="Survey", 
                    y="Algorithm",
                    facet_col="Emotion",
                    color='USERGROUP', 
                    trendline="ols")

    fig.update_layout(title='Scatter plot of Survey vs. Algorithm (By User Group)')
    fig.update_layout(width=1700, height=400)
    for a in fig.layout.annotations:
        a.text = a.text.split("=")[1]
    st.plotly_chart(fig)

# -- Horizontal bar chart of differences (categorised) in probability

def HorBarProbDiffs(data):
    fig = px.bar(data, y='Difference', 
                            x="Percentage",
                            color='USERGROUP',
                            barmode='group',
                            facet_col='Emotion')
    fig.update_layout(title='Bar chart of the difference (categorised %) in area under the curve (BY User Group)')
    fig.update_layout(width=1600, height=400)
    for a in fig.layout.annotations:
        a.text = a.text.split("=")[1]
    st.plotly_chart(fig)
