###### DB Connection #########
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError, DatabaseError
import pandas as pd 

def sendquery(query,returnQuery,close = False): ## 데이터 프레임을 넣지 않는걸로 쿼리 수정 
    try:
        result = pd.DataFrame()
#         engine = create_engine('postgresql+psycopg2://mc100:sndv1004@rds-mc100.cphntmyw7vkw.ap-northeast-2.rds.amazonaws.com:5432/mc100db', echo = False)
        conn_string = "host='rds-mc100.cphntmyw7vkw.ap-northeast-2.rds.amazonaws.com' dbname='mc100db' user='mc100' password='sndv1004'"
        conn = psycopg2.connect(conn_string)
        cur = conn.cursor()
    
        if returnQuery:
            result = pd.read_sql(query, conn)
        else:
#             print('debug0')
#             print(query)
            cur.execute(query)
#             print('debug1')
            conn.commit()
#             print('debug2')
            

    except IntegrityError as error: 
        print('duplicate key')
#         raise(Exception)
    except psycopg2.DatabaseError as error:
        print('DBconnection error ')
        raise(Exception)
    finally:
        if close:
            print('DBconnection close')
            conn.close()
    
    return result