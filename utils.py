import datetime as dt
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import connect as cn
import mysqlactions as mysql
import platform


import twlsms as twl

### Authorized columns



def jsonfname ():
    now = dt.datetime.now()
    dtstring = now.strftime("%d_%m_%Y_%H_%M_%S")
    filname = "notflattendata" + dtstring +".json"
    fullpath = "./unflatten_data/" + filname
    return fullpath

def returnurl():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    return url

def prms(cur):
    if cur ==1:
        parameters = {
          'start':'1',
          'limit':'5000',
          'convert':'USD'
        }
        return parameters
    else:
        parameters = {
            'start' : '1',
            'limit' : '5000',
            'convert' : 'BTC'
        }
        return parameters

def headers():
    headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': '492b9d81-0f94-4449-90b1-3fe1ff9b29ff',
    }
    return headers





def callcms(cur):
    session = Session()
    session.headers.update(headers())
    try:
      response = session.get(returnurl(), params=prms(cur))
      data = json.loads(response.texll)
      # with open(jsonfname(), "w") as temp_data:
      #   temp_data.write(str(data))
      return (data)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(e)


# def dimscolumns():
#     authcolumns = ["id", "name", "symbol", "tags", "max_supply", "circulating_supply", "total_supply", "cmc_rank"]
#     return authcolumns
#
#
# def quotecolumns():
#     cols =["price", "volume_24h", "percent_change_1h", "percent_change_24h", "market_cap", "last_updated"]
#     return cols

def setobj(obj, conversiontype):
    if conversiontype ==1:
        rnd = 3
    else:
        rnd = 10
    if not obj:
        return str('null')
    if obj == 'None':
        return str('null')
    elif type(obj) == int:
        return str(obj)
    elif type(obj) == float:
        newobj = round(obj, rnd)
        return  newobj
    elif type(obj) == str:
        if "T" in obj and ":" in obj:
            newobj = obj.replace("T", " ")
            newobjstr = str(newobj)[:19]
            return str("'" + newobjstr.replace("'", "") + "'")
        else:
            return str("'" + obj.replace("'", "") + "'")
    elif type(obj) == list:
        if obj == []:
            return str('null')
        newobj = obj[0]
        return str("'" + newobj +"'")
    else:
        return str(obj)


def getsql(arr, conversion_type):
    if platform.system() == 'Windows':
        sql = "INSERT INTO mrr_test.fact_30_min_raw_data VALUES\n"
    else:
        sql = "INSERT INTO mrr.fact_30_min_raw_data VALUES\n"
    if conversion_type == 1:
        contype = "USD"
    else:
        contype = "BTC"

    islast_row = 0
    for dict in arr:
        islast_row += 1
        insertrow = '('
        insertvlues = [str(setobj(dict["id"], conversion_type)),
                       str(conversion_type),
                       str(setobj(dict["name"], conversion_type)),
                       str(setobj(dict["symbol"], conversion_type)),
                       str(setobj(dict["tags"], conversion_type)),
                       str(setobj(dict["max_supply"], conversion_type)),
                       str(setobj(dict["circulating_supply"], conversion_type)),
                       str(setobj(dict["total_supply"], conversion_type)),
                       str(setobj(dict["cmc_rank"], conversion_type)),
                       str(setobj(dict["quote"][contype]["price"], conversion_type)),
                       str(setobj(dict["quote"][contype]["volume_24h"], conversion_type)),
                       str(setobj(dict["quote"][contype]["percent_change_1h"], conversion_type)),
                       str(setobj(dict["quote"][contype]["percent_change_24h"], conversion_type)),
                       str(setobj(dict["quote"][contype]["market_cap"], conversion_type)),
                       str(setobj(dict["quote"][contype]["last_updated"], conversion_type))
                     ]
        txtvals = ",".join(insertvlues)
        rtoadd = insertrow + txtvals + ")"
        if len(arr) != islast_row:
            rtoadd += ',\n'
        sql += rtoadd
    return sql



def execmngsql(query_id, is_return=0):
    sql = "select query_str from mng.environment_queries where query_id = " + str(query_id)
    execsql = cn.connect(sql, 1)[0]
    print("I Execute the query", execsql)
    if is_return == 0:
        cn.connect(execsql, is_return)
        return(execsql)
    else:
        isdata = cn.connect(sql, is_return)[0]
        data = cn.connect(isdata, is_return)[0]
        if not data:
            print("The query return no data")
            return 0
        else:
            print("Here are the results for the query")
            return data

def load_cmc_data(cur):
    # Download new data
    if cur == "USD":
        curid = 1
    else:
        curid = 2

    fulldata = callcms(curid)

    # Isolate only the relevant data
    crpdata = fulldata["data"]
    # Prepare the insert sql statement
    sql = getsql(crpdata, curid)
    mysql.qryexec(sql)
    print("Data successfully load to mysql")

# Return only the sql to execute



# twl.sendsms()
# execmngsql(2, 0)
# execmngsql(1, 0)

# test = execmngsql(3, 1)
# print(test)

