import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='goku@1111',
                             database='auctionms',
                             cursorclass=pymysql.cursors.DictCursor,
                             autocommit=True,
                             )

cursor = connection.cursor()
cursor.execute("select version() as version")
output = cursor.fetchone()
print(f"Using mysql version {output['version']} ...")
