import pymysql

conn = pymysql.connect(host='127.0.0.1', user='root', password='root', database='club')
cursor = conn.cursor()

# 修改数据库默认字符集
cursor.execute("ALTER DATABASE club CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
print("数据库字符集已修改为 utf8mb4")

# 获取所有表名并转换
cursor.execute("SHOW TABLES")
tables = [t[0] for t in cursor.fetchall()]
for table in tables:
    cursor.execute(f"ALTER TABLE `{table}` CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    print(f"已转换表: {table}")

conn.commit()
cursor.close()
conn.close()
print("完成！所有表已转换为 utf8mb4")
