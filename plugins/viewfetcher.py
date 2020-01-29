from sqlalchemy import create_engine
from sqlalchemy import text
import csv
import os
from pathlib import Path
import hashlib
from datetime import date
import uuid


def configure_engine(config):
    con_string = '{database}+{dbapi}://{user}:{password}@{host}/{dbname}'.format(database=config["database"],dbapi=config["dbapi"],user=config["user"],password=config["password"],host=config["host"],dbname=config["dbname"])
    engine = create_engine(con_string)
    return engine

def _configure_db_connection(config):
    engine = configure_engine(config)
    return engine.connect(), engine

#GetFileSize takes filepath as input and returns size of file in bytes
def GetFileSize(path):
    filesize = os.path.getsize(path)
    return filesize


#CheckIfFileExists takes filepath as input and returns boolean value
def CheckIfFileExists(path):
    if Path(path).is_file():
        return True
    else:
        return False

#FindMD5Checksum takes filepath as input and returns md5 hash of the file
def FindMD5Checksum(path):
    md5hash = hashlib.md5(open(path,'rb').read()).hexdigest()
    return md5hash
    


class ViewFetcher(object):
    def __init__(self,config):
        self.config = config
        self.dbconnection, self.engine = _configure_db_connection(config)

    #CreateDynamicSQL takes config as input and returns the dynamic sql created
    def create_dynamic_sql(self, progress):
        if progress == None:
            progress = self.config["start_date"]

        today_date = date.today()
        account_parts = ' OR '.join(["{account_field_name}='{account_number}'".format(account_field_name=self.config['account_field_name'], account_number=account_number) for account_number in self.config['account_numbers']])

        query = "select {fields} from {view} where ({account_query}) and ({txn_date_field_name} >= '{progress}' and {txn_date_field_name} < '{today}')"
        query = query.format(fields = ','.join(self.config["fields"]), view = self.config["view_name"], account_query = account_parts, account_field = self.config["account_field_name"], txn_date_field_name = self.config["txn_date_field_name"], progress = progress, today = today_date)
        return query

    #ExecuteSQL takes db connection instance and query as input, executes query and returns engine result
    def execute_sql(self,query):
        sql = text(query)
        result = self.dbconnection.execute(sql)
        return result
    
    #WriteCsvFile takes filename and engine result as input and writes to file
    def write_csv_file(self, fname,result):
        data = [list(x) for x in result]
        with open(fname, 'w') as w_file:

            wr = csv.writer(w_file, delimiter=',')
            columns = result.keys()
                #add column names if new file is created
            wr.writerow(columns)

            #actual data
            wr.writerows(data)

        w_file.close
    
    def run(self, root, progress):
    
        sql_query = self.create_dynamic_sql(progress)

        result = self.execute_sql(sql_query)

        path = "{root}{name}.csv".format(root = root,name=uuid.uuid4().hex)
        self.write_csv_file(path, result)

        filesize = GetFileSize(path)
        md5hash = FindMD5Checksum(path)
        progress = str(date.today())

        self.dbconnection.close()
        self.engine.dispose()

        response = {"file": path, "md5hash" : md5hash, "filesize" : filesize, "progress" : progress}

        return response




    

        
    
    
    