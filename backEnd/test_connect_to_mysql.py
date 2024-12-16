import pymysql

# 資料庫連線設定
host = ""
port = 3306  # MySQL 預設埠號
user = ""
database = ""
password = ""

try:
    # 建立連線
    connection = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database
    )
    print("資料庫連線成功！")

    # 測試查詢
    with connection.cursor() as cursor:
        cursor.execute("SELECT VERSION();")
        result = cursor.fetchone()
        print(f"MySQL 版本：{result[0]}")

except pymysql.MySQLError as e:
    print(f"資料庫連線失敗：{e}")
finally:
    # 關閉連線
    if 'connection' in locals() and connection.open:
        connection.close()
        print("資料庫連線已關閉。")
