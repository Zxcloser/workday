import pandas as pd
import psycopg2


def main():
    host = "localhost"
    dbname = "workday"
    user = "postgres"
    password = "12340987"

    df_holiday = pd.read_excel('Календарь.xlsx',  sheet_name='Доп выходной', header=None)
    df_holiday.columns = ["Дата"]

    df_work = pd.read_excel('Календарь.xlsx', sheet_name='Доп рабочий день', header=None)
    df_work.columns = ["Дата"]

    df_weekend = pd.read_excel('Календарь.xlsx', sheet_name='Сб, вс')

    df = pd.DataFrame(columns=["Дата", 'Значение'])

    for data in df_weekend["Дата"]:
        dff = pd.DataFrame()

        for data_holiday in df_holiday["Дата"]:
            if data == data_holiday:
                dff = pd.DataFrame([{'Дата': data.strftime('%Y-%m-%d'), 'Значение': 'Праздник'}])
                df = pd.concat([df, dff], ignore_index=True)
                break

        for data_work in df_work["Дата"]:
            if data == data_work:
                dff = pd.DataFrame([{'Дата': data.strftime('%Y-%m-%d'), 'Значение': 'Отработка'}])
                df = pd.concat([df, dff], ignore_index=True)
                break

        if len(dff) == 0:
            if (df_weekend['Сб, вс'].loc[df_weekend['Дата'] == data].iloc[0]) == 1:
                dff = pd.DataFrame([{'Дата': data.strftime('%Y-%m-%d'), 'Значение': 'Выходной'}])
                df = pd.concat([df, dff], ignore_index=True)
            else:
                dff = pd.DataFrame([{'Дата': data.strftime('%Y-%m-%d'), 'Значение': 'Рабочий день'}])
                df = pd.concat([df, dff], ignore_index=True)

    try:
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host
        )
        print("Подключение к базе данных установлено.")

        cursor = conn.cursor()

        for data in df.iterrows():
            cursor.execute(f"select id from type_day where name = '{data[1]['Значение']}'")
            res = cursor.fetchone()
            cursor.execute(f"insert into spec_day(data, date_type_id) values('{data[1]['Дата']}', {res[0]})")
            conn.commit()

    except Exception as e:
        print("Ошибка при подключении или выполнении запроса:", e)


if __name__ == '__main__':
    main()