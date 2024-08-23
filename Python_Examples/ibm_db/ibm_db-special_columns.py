#! /usr/bin/python3
#-------------------------------------------------------------------------------------------------#
#  NAME:     ibm_db-special_columns.py                                                            #
#                                                                                                 #
#  PURPOSE:  This program is designed to illustrate how to use the ibm_db.special_columns() API.  #
#                                                                                                 #
#            Additional APIs used:                                                                #
#                 ibm_db.fetch_assoc()                                                            #
#                                                                                                 #
#  USAGE:    Log in as a Db2 database instance user (for example, db2inst1) and issue the         #
#            following command from a terminal window:                                            #
#                                                                                                 #
#            ./ibm_db-special_columns.py                                                          #
#                                                                                                 #
#-------------------------------------------------------------------------------------------------#
#                      DISCLAIMER OF WARRANTIES AND LIMITATION OF LIABILITY                       #
#                                                                                                 #
#  (C) COPYRIGHT International Business Machines Corp. 2018, 2019 All Rights Reserved             #
#  Licensed Materials - Property of IBM                                                           #
#                                                                                                 #
#  US Government Users Restricted Rights - Use, duplication or disclosure restricted by GSA ADP   #
#  Schedule Contract with IBM Corp.                                                               #
#                                                                                                 #
#  The following source code ("Sample") is owned by International Business Machines Corporation   #
#  or one of its subsidiaries ("IBM") and is copyrighted and licensed, not sold. You may use,     #
#  copy, modify, and distribute the Sample in any form without payment to IBM, for the purpose    #
#  of assisting you in the creation of Python applications using the ibm_db library.              #
#                                                                                                 #
#  The Sample code is provided to you on an "AS IS" basis, without warranty of any kind. IBM      #
#  HEREBY EXPRESSLY DISCLAIMS ALL WARRANTIES, EITHER EXPRESS OR IMPLIED, INCLUDING, BUT NOT       #
#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.    #
#  Some jurisdictions do not allow for the exclusion or limitation of implied warranties, so the  #
#  above limitations or exclusions may not apply to you. IBM shall not be liable for any damages  #
#  you suffer as a result of using, copying, modifying or distributing the Sample, even if IBM    #
#  has been advised of the possibility of such damages.                                           #
#-------------------------------------------------------------------------------------------------#

# Load The Appropriate Python Modules
import sys         # Provides Information About Python Interpreter Constants, Functions, & Methods
import ibm_db      # Contains The APIs Needed To Work With Db2 Databases

#-------------------------------------------------------------------------------------------------#
# Import The Db2ConnectionMgr Class Definition, Attributes, And Methods That Have Been Defined    #
# In The File Named "ibm_db_tools.py"; This Class Contains The Programming Logic Needed To        #
# Establish And Terminate A Connection To A Db2 Server Or Database                                #
#-------------------------------------------------------------------------------------------------#
from ibm_db_tools import Db2ConnectionMgr

#-------------------------------------------------------------------------------------------------#
# Import The ipynb_exit Class Definition, Attributes, And Methods That Have Been Defined In The   #
# File Named "ipynb_exit.py"; This Class Contains The Programming Logic Needed To Allow "exit()"  #
# Functionality To Work Without Raising An Error Or Stopping The Kernel If The Application Is     #
# Invoked In A Jupyter Notebook                                                                   #
#-------------------------------------------------------------------------------------------------#
from ipynb_exit import exit

# Define And Initialize The Appropriate Variables
dbName = "SAMPLE"
userID = "db2inst1"
passWord = "db2inst1"
dbConnection = None
schemaName = userID.upper()
tableName = "EMPLOYEE"
resultSet = False
dataRecord = False
sqlDataTypes = {0 : "SQL_UNKNOWN_TYPE", 1 : "SQL_CHAR", 2 : "SQL_NUMERIC", 3 : "SQL_DECIMAL",
    4 : "SQL_INTEGER", 5 : "SQL_SMALLINT", 6 : "SQL_FLOAT", 7 : "SQL_REAL", 8 : "SQL_DOUBLE",
    9 : "SQL_DATETIME", 12 : "SQL_VARCHAR", 16 : "SQL_BOOLEAN", 19 : "SQL_ROW", 
    91 : "SQL_TYPE_DATE", 92 : "SQL_TYPE_TIME", 93 : "SQL_TYPE_TIMESTAMP",
    95 : "SQL_TYPE_TIMESTAMP_WITH_TIMEZONE", -8 : "SQL_WCHAR", -9 : "SQL_WVARCHAR",
    -10 : "SQL_WLONGVARCHAR", -95 : "SQL_GRAPHIC", -96 : "SQL_VARGRAPHIC",
    -97 : "SQL_LONGVARGRAPHIC", -98 : "SQL_BLOB", -99 : "SQL_CLOB", -350 : "SQL_DBCLOB",
    -360 : "SQL_DECFLOAT", -370 : "SQL_XML", -380 : "SQL_CURSORHANDLE", -400 : "SQL_DATALINK",
    -450 : "SQL_USER_DEFINED_TYPE"}

# Create An Instance Of The Db2ConnectionMgr Class And Use It To Connect To A Db2 Database
conn = Db2ConnectionMgr('DB', dbName, '', '', userID, passWord)
conn.openConnection()
if conn.returnCode is True:
    dbConnection = conn.connectionID
else:
    conn.closeConnection()
    exit(-1)

# Attempt To Retrieve Information About Unique Row Identifier Columns That Have Been 
# Defined For The Table Specified
print("Obtaining information about unique row identifier columns that have been")
print("defined for the " + schemaName + "." + tableName + " table ... ", end="")
try:
    resultSet = ibm_db.special_columns(dbConnection, None, schemaName, tableName, 0)

except Exception:
    pass

# If The Information Desired Could Not Be Retrieved, Display An Error Message And Exit
if resultSet is False:
    print("\nERROR: Unable to obtain the information desired\n.")
    conn.closeConnection()
    exit(-1)

# Otherwise, Complete The Status Message
else:
    print("Done!\n")

# As Long As There Are Records (That Were Produced By The ibm_db.special_columns API), ...
noData = False
loopCounter = 1
while noData is False:

    # Retrieve A Record And Store It In A Python Dictionary
    try:
        dataRecord = ibm_db.fetch_assoc(resultSet)
    except:
        pass

    # If The Data Could Not Be Retrieved Or If There Was No Data To Retrieve, Set The
    # "No Data" Flag And Exit The Loop  
    if dataRecord is False:
        noData = True

    # Otherwise, Display The Information Retrieved
    else:

        # Display Record Header Information
        print("Primary key/unique index " + str(loopCounter) + " details:")
        print("___________________________________")

        # Display The Information Stored In The Data Record Retrieved
        print("Column name            : {}" .format(dataRecord['COLUMN_NAME']))
        print("Data type              : {}" .format(dataRecord['TYPE_NAME']))
        print("SQL data type          : ", end="")
        print(sqlDataTypes.get(dataRecord['DATA_TYPE']))
        print("Column size            : {}" .format(dataRecord['COLUMN_SIZE']))
        print("Buffer size            : {}" .format(dataRecord['BUFFER_LENGTH']))
        print("Scale (decimal digits) : {}" .format(dataRecord['DECIMAL_DIGITS']))

        print("Scope                  : ", end="")
        if dataRecord['SCOPE'] == 0:
            print("Row ID is valid only while the\n" + " " * 25, end="")
            print("cursor is positioned on the row")
        elif dataRecord['SCOPE'] == 1:
            print("Row ID is valid for the\n" + " " * 25, end="")
            print("duration of the transaction")
        elif dataRecord['SCOPE'] == 2:
            print("Row ID is valid for the\n" + " " * 25, end="")
            print("duration of the connection")

        # Increment The loopCounter Variable And Print A Blank Line To Separate The
        # Records From Each Other
        loopCounter += 1
        print()

# Close The Database Connection That Was Opened Earlier
conn.closeConnection()

# Return Control To The Operating System
exit()
