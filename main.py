from plugins.viewfetcher import ViewFetcher


config = {
    "database"              : "mysql",
    "dbapi"                 : "pymysql",
    "user"                  : "root",
    "password"              : "rootpasswordgiven",
    "host"                  : "localhost",
    "dbname"                : "employee",
    "date"                  : "",
    "fields"                : ["firstname","email", "reg_date"],
    "account_field_name"    : "id",
    "account_numbers"       : ["1","2","5"],
    "txn_date_field_name"   : "reg_date",
    "view_name"             : "myaccount",
    "start_date"            : "2020-01-28"
}

root = "./"
progress = None

vf = ViewFetcher(config)
print(vf.run(root,progress))