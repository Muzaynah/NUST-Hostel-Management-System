#authentication.py

import mysql.connector
from config import db_config


def authenticate_user(username, password):
    user =''
    #establishing a connection and then running queries to see if the username entered is of a staff/student
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    query = "SELECT * FROM student WHERE sUsername = '"+username+"' and sPassword = '"+password+"';"
    cursor.execute(query)
    result = cursor.fetchall()
    
    if(len(result)>0):
        return 'student'
    else:
        query = "SELECT * FROM manager WHERE mUsername == '"+username+"' and mPassword == '"+password+"';"
        cursor.execute(query)
        result = cursor.fetchall()
        if(len(result)>0):
            return 'manager'
    return 'invalid'
    # return (username == 'admin' or username == 'student') and password == '1234'