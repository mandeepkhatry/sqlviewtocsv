from plugins.viewfetcher import ViewFetcher


config = {
    "database"              : "mysql",
    "dbapi"                 : "pymysql",
    "user"                  : "root",
    "password"              : "rootpasswordgiven",
    "host"                  : "localhost",
    "dbname"                : "employee",
    "account_number"        :  "1",
    "query"                 : "select * from myaccount where (id = :account_num) and (reg_date > :start_date and reg_date < :end_date)",
    "from_date"             : "2020-01-28"
}

root = "./"

progress = {"to_date" : "2020-01-23"}

vf = ViewFetcher(config)
print(vf.run(root,progress))