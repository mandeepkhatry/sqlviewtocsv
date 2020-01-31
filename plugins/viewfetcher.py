from sqlalchemy import create_engine
from sqlalchemy import text
import csv
import os
from pathlib import Path
import hashlib
from datetime import date
from datetime import datetime
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

    def compute_start_date(self,progress):
        if progress is None:
            progress = {}

        start_date = progress.get('to_date')
        
        if start_date is None:
            start_date = self.config['from_date']
        return start_date


    def prepare_query(self):

        query = self.config['query'].format()

        return query

    def execute_query(self, progress):
        start_date = self.compute_start_date(progress)
        end_date = date.today()

        acc_no=self.config['account_number']

        sql_query = self.prepare_query()
        #parameters inside query : start_date, end_date, account_num 
        result = self.dbconnection.execute(text(sql_query), start_date=start_date, end_date=end_date, account_num=acc_no)
        
        progress = {'to_date': str(end_date)}
        return result
    
    def run(self, root, progress):
    
        result = self.execute_query(progress)

        path = "{root}{name}.csv".format(root = root,name=uuid.uuid4().hex)
        self.write_csv_file(path, result)

        filesize = GetFileSize(path)
        md5hash = FindMD5Checksum(path)
        progress = str(date.today())

        self.dbconnection.close()
        self.engine.dispose()

        response = {"file": path, "md5hash" : md5hash, "filesize" : filesize, "progress" : progress}

        return response




    

        
    
    
    