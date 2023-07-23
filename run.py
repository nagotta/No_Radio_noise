'''
アプリケーションを起動するためのスクリプト。
'''
from ep1_app import app 

if __name__ == '__main__':
    app.run(debug=True)