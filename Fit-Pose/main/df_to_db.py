# Imports
import pandas as pd
import psycopg2
from .models import Session

# Converts dictionary to dataframe
def dataframer(reps):

    # Saving relevant values as list
    rep_no = list(range(1, reps['count']+1))

    time = list(reps['time'].values())[:reps['count']]
    time = [round(x,1) for x in time] # Rounding values to single decimal point

    correct_form = list(reps['correct_form'].values())[:reps['count']]
    correct_form = [round(x,1) for x in correct_form]

    wrong_form = list(reps['wrong_form'].values())[:reps['count']]
    wrong_form = [round(x,1) for x in wrong_form]

    session_id = list(Session.objects.latest('id').id for x in time)

    # Storing lists in a dataframe
    data = [rep_no, time, correct_form, wrong_form, session_id]
    columns = ['rep_no', 'time', 'correct_form', 'wrong_form', 'session_id']

    df = pd.DataFrame(data, columns).transpose()
    df['session_id'] = df['session_id'].astype(int)
    df.to_csv('exercise_stats.csv',  header=False, index=False)

    return df

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
