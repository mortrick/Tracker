# Connect to mysql with python
import pymysql
from logs import dynamic_log as dl
from keys import conf

dbconf = conf.dbconf()

def getqrystr(numb, retval=1, env='test'):
    if env != 'test':
        sql = "select query_str from mng.environment_queries where query_id = " + str(numb) + " limit 1"
    else:
        sql = "select query_str from mng_test.environment_queries where query_id = " + str(numb) + " limit 1"
    db = pymysql.connect(dbconf[0], dbconf[1], dbconf[2])
    cursor = db.cursor()
    cursor.execute(sql)
    if retval == 1:
        data = cursor.fetchone()
        for row in data:
            qry = row
        if env == 'test':
            qry = qry.replace("{env}", '_test')
            db.close()
            return qry
        else:
            qry = qry.replace("{env}", '')
            db.close()
            return qry
    else:
        data = cursor.fetchall()
        for row in data:
            if type(row) == tuple:
                txt = row[0]
            else:
                txt = row
            db.close()
            return txt


def qryexec(numb, retval=0, run_id=0, debugmode=0, env='test'):
    if not numb:
        return None
    db = pymysql.connect(dbconf[0], dbconf[1], dbconf[2])
    cursor = db.cursor()
    if type(numb) == int:
        if retval == 1:
            qry = getqrystr(numb, retval=1, env=env)
            cursor.execute(qry)
            # Add Debug
            dl.writelog(dl.logpath(run_id), "Successfully execute the query :" + '\n' + qry[:1500], debugmode)
            ans = cursor.fetchone()
            db.close()
            # Add debug
            dl.writelog(dl.logpath(run_id), "Successfully executed and the results are : " + '\n' + str(ans[:1500]), debugmode)
            return ans
        elif retval == 2:
            qry = getqrystr(numb, retval=2, env=env)
            cursor.execute(qry)
            ans = cursor.fetchall()
            db.close()
            dl.writelog(dl.logpath(run_id), "Successfully executed and the results are : " + '\n' + str(ans[:1500]), debugmode)
            return ans
        else:
            qry = getqrystr(numb, retval=1, env=env) # mean
            cursor.execute(qry)
            db.commit()
            db.close()
            dl.writelog(dl.logpath(run_id), "Successfully execute and commit the sql : " + '\n' + qry[:1500], debugmode)
    else:
        try:
            cursor.execute(numb)
            dl.writelog(dl.logpath(run_id), 'The query bellow successfully executed \n' + numb[:1500], debugmode)
        except pymysql.err as e :
            msg = "Couldnt execute the query " + 'Failed to execute the the sql ' + numb + '\n Because of an error ' + e
            dl.writelog(dl.logpath(run_id), msg[:1500], debugmode)
            print(msg)
        if retval == 1:
            ans = cursor.fetchone()
            db.close()
            return ans
        elif retval == 2:
            ans = cursor.fetchall()
            db.close()
            return ans
        else:
            db.commit()
            db.close()


def updateprocesslog(run_id=0, env='unknown', debugmode=0):
    sql = 'insert into mng.process_execution_log (run_id, env,debug_mode)'
    values = 'values ('+str(run_id)+',' + "'" +env + "'" +',' + str(debugmode) + ')'
    finsql = sql + values
    qryexec(numb=finsql, retval=0, run_id=run_id, debugmode=debugmode, env=env)
