import pymysql

DB_CONFIG = {
    'host':'localhost',
    'user':'app_user',
    'password':'123456',
    'database':'批记录',
    'charset':'utf8mb4'
}

def 获取连接():
    return pymysql.connect(**DB_CONFIG)

def 初始化数据库():
    连接 = 获取连接()
    游标 = 连接.cursor()
    游标.execute('''
        CREATE TABLE IF NOT EXISTS 批记录(
            批号 VARCHAR(50),
            收率 FLOAT,
            结果 VARCHAR(10),
            日期 DATE
        )
    ''')
    游标.execute('''
		CREATE TABLE IF NOT EXISTS users(
	 	   id INT AUTO_INCREMENT PRIMARY KEY,
	 	   username VARCHAR(50) UNIQUE NOT NULL,
	  	   password_hash VARCHAR(200) NOT NULL,
		   created_at DATETIME DEFAULT CURRENT_TIMESTAMP
		)
    ''')
    连接.commit()
    连接.close()

def 读取所有数据():
    初始化数据库()
    连接 = 获取连接()
    游标 = 连接.cursor()
    游标.execute('select * from 批记录')
    数据 = 游标.fetchall()
    连接.close()
    return 数据

def 追加记录(批号,收率,结果,日期):
    if 日期 is None:
         from datetime import datetime
         日期 = datetime.now().date().strptime('%Y-%m-%d')
    初始化数据库()
    连接 = 获取连接()
    游标 = 连接.cursor()
    游标.execute(
        'INSERT INTO 批记录 (批号,收率,结果,日期) VALUES (%s,%s,%s,%s)',
        (批号,收率,结果,日期)
    )
    连接.commit()
    连接.close()

def 执行查询(sql,参数 = None):
    连接 = 获取连接()
    游标 = 连接.cursor()
    游标.execute(sql,参数 or ())
    数据 = 游标.fetchall()
    连接.close()
    return 数据

def 执行插入(sql,参数):
    连接 = 获取连接()
    游标 = 连接.cursor()
    游标.execute(sql,参数)
    连接.commit()
    连接.close()

