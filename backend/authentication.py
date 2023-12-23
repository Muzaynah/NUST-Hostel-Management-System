#authentication.py

def authenticate_user(username, password):
    # Your authentication logic here
    return (username == 'admin' or username == 'student') and password == '1234'