import psycopg2


host = "localhost"
dbname = "workday"
user = "postgres"
password = "12340987"

try:
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host
    )
    print("Подключение к базе данных установлено.")

    cursor = conn.cursor()

    cursor.execute("select * from datas")
    res = cursor.fetchall()
    print(res)

except Exception as e:
    print("Ошибка при подключении или выполнении запроса:", e)