import pymysql

passwords = ['', 'root', 'admin', 'password', '12345', '123456']
success_pwd = None

for pwd in passwords:
    try:
        conn = pymysql.connect(host='localhost', user='root', password=pwd)
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS homemade_food;")
        conn.commit()
        conn.close()
        success_pwd = pwd
        print(f"SUCCESS:{pwd}")
        break
    except Exception as e:
        pass

if success_pwd is None:
    print("FAILED")
