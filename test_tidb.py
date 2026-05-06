import pymysql

try:
    conn = pymysql.connect(
        host='gateway01.ap-southeast-1.prod.aws.tidbcloud.com',
        port=4000,
        user='37z2smgpS4MzdkK.root',
        password='q2506rE1w7DkrWdJ',
        database='homemade_food',
        ssl={'ssl_verify_cert': False},
    )
    print("SUCCESS! Connected to TiDB Cloud.")
    conn.close()
except Exception as e:
    print(f"FAILED: {e}")
