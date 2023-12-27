#authentication.py

import mysql.connector
from config import db_config


def authenticate_user(username, password):
    user =''
    #establishing a connection and then running queries to see if the username entered is of a staff/student
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    query = "SELECT cms FROM student WHERE sUsername = '"+username+"' and sPassword = '"+password+"';"
    cursor.execute(query)
    result = cursor.fetchall()
    
    if(len(result)>0):
        cms=result[0]
        return ('student',cms)
    
    query = "SELECT MID FROM manager WHERE mUsername = '"+username+"' and mPassword = '"+password+"';"
    cursor.execute(query)
    result = cursor.fetchall()
    if(len(result)>0):
        manager_id = result[0]
        return ('manager',manager_id)
    return ('invalid',None)
    # return (username == 'admin' or username == 'student') and password == '1234'