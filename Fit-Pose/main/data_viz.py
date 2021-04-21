# Imports
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import psycopg2

from .pose import *
from .models import Session

# Converts dictionary to dataframe
def dataframer(reps):

    # Saving relevant values as list
    rep_no, time, correct_form, wrong_form, session_id = [], [], [], [], []
    labels = {}
    labels['time'], labels['correct_form'], labels['wrong_form'] = [], [], []

    for i in range(reps['count']):
        rep_no.append(i+1)
        
        time.append(round(reps['time'][i+1],1))
        labels['time'].append(f'{str(time[i])}s')
        
        correct_form.append(round(reps['correct_form'][i],1))
        labels['correct_form'].append(f'{str(correct_form[i])}s')
        
        wrong_form.append(round(reps['wrong_form'][i],1))
        labels['wrong_form'].append(f'{str(wrong_form[i])}s')
        
        session_id.append(Session.objects.latest('id').id)

    # Storing lists in a dataframe
    data = [rep_no, time, correct_form, wrong_form, session_id]
    column_names = ['rep_no', 'time', 'correct_form', 'wrong_form', 'session_id']

    df = pd.DataFrame(data, column_names).transpose()
    df['session_id'] = df['session_id'].astype(int)

    # Adding initial condition of 0s
    zeros = pd.DataFrame([0,0,0,0,Session.objects.latest('id').id],column_names).transpose()
    df = pd.concat([zeros,df], ignore_index=True)

    return df, labels

# Reads csv and inserts into database
def databaser():

    conn_string = 'postgres://postgres:postgres@localhost/fitpose' 
    pg_conn = psycopg2.connect(conn_string)
    cur = pg_conn.cursor()

    insert_sql = '''
    COPY main_stats(rep_no, time, correct_form, wrong_form, session_id)
    FROM '/home/bryan/git_workspace/FitPose/Fit-Pose/exercise_stats.csv'
    DELIMITER ',' CSV;
    '''
    cur.execute(insert_sql)
    # cur.execute('TRUNCATE TABLE main_stats')

    pg_conn.commit()
    cur.close()

# X and Y axis settings
def xaxis_yaxis(num):

    if num == 1:
        xaxis=dict(showline=True,
                linewidth=2,
                linecolor='black',
                mirror=True, # To create border outline
                dtick=1) # Setting x ticks to show each rep count

        yaxis=dict(showline=True,
                linewidth=2,
                linecolor='black',
                mirror=True)
    
    elif num == 2:
        xaxis=dict(showticklabels=False,
                showline=True,
                linewidth=2,
                linecolor='black',
                mirror=True) # To create border outline

        yaxis=dict(showticklabels=False,
                showline=True,
                linewidth=2,
                linecolor='black',
                mirror=True)
    
    return xaxis, yaxis

# Lineplot showing time vs. reps
def lineplot(df, labels):

    xaxis, yaxis = xaxis_yaxis(1)
    fig= go.Figure()

    fig.add_trace(go.Scatter(x=df['rep_no'],
                            y=df['time'],
                            text=labels['time'],
                            hoverinfo='text',
                            line=dict(color='darkviolet',
                                    width=3),
                            stackgroup='one' # To fill color beneath the plotted area
                            ))

    fig.update_layout(title='Time spent doing each rep',
                    xaxis_title='Rep no.',
                    yaxis_title='Time (s)',
                    xaxis=xaxis,
                    yaxis=yaxis,
                    plot_bgcolor='#EAEAF2',
                    font_size=15
                    )
    
    fig.show()
    return fig

# Time vs. Reps iplot comparing correct form to wrong form
def stackplot(df, labels):

    xaxis, yaxis = xaxis_yaxis(1)
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        name='Wrong form',
        x=df['rep_no'],
        y=df['wrong_form'],
        text=labels['wrong_form'],
        hoverinfo='text',
        mode='lines',
        line=dict(width=3,
                color='red'),
        stackgroup='one'
    ))

    fig.add_trace(go.Scatter(
        name='Correct form',
        x=df['rep_no'],
        y=df['correct_form'],
        text=labels['correct_form'],
        hoverinfo='text',
        mode='lines',
        line=dict(width=3,
                color='rgb(111, 231, 219)'),
        stackgroup='one'
    ))

    fig.update_layout(title='Correct form vs. Wrong form with rep progression',
                    xaxis_title='Rep no.',
                    yaxis_title='Time (s)',
                    xaxis=xaxis,
                    yaxis=yaxis,
                    plot_bgcolor='#EAEAF2',
                    font_size=15
                    )
    
    fig.show()
    return fig

# Piechart showing cumulative seconds spent doing correct vs wrong form
def piechart(df, labels):
    total_correct =round(sum(df['correct_form']), 1)
    total_wrong = round(sum(df['wrong_form']), 1)

    x_bar = ['Correct form', 'Wrong form']
    y_bar = [total_correct, total_wrong]
    y_label = [f'{str(x)}s' for x in y_bar]

    form_colors = ['rgba(111, 231, 219, 0.5)', 'rgba(255,0,0,0.5)'] # Using rgba to set different opacity for marker and marker line
    form_line_colors = ['rgba(111, 231, 219, 1)', 'rgba(255,0,0,1)']

    fig = go.Figure(data=[go.Pie(labels=x_bar,
                                values=y_bar)])

    fig.update_traces(hoverinfo='label+percent', 
                    text=y_label,
                    textinfo='text', 
                    textfont_size=20,
                    marker=dict(colors=form_colors, 
                                line=dict(color=form_line_colors, 
                                            width=3))
                    )

    fig.show()
    return fig

def initialize_viz(reps):
    df, labels = dataframer(reps)
    df.to_csv('exercise_stats.csv',  header=False, index=False)
    databaser()
    # lineplot(df, labels)
    # stackplot(df, labels)
    # piechart(df, labels)
