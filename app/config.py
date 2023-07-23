'''
アプリケーションの設定を行います。
データベースの接続情報などをここに記述します。
'''
DEBUG = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///radios.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True