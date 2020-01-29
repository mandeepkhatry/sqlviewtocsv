# sqlviewtocsv

-----
SQLViewToCSV exports data from a sql query to csv. 
-----

## config
-----

```
All configurations needed.
Eg:
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

```

## root
-----

```
Root path where CSV is to be created.
Eg:
root = "./"

```


## progress
-----

```
Progress(date) upto which data has been exported to csv.
Eg:
progress = "2020-01-28"

```

### Server (command)
```
go run server/server.go

```


**Command to run **
```
python main.py
```

