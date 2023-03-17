from db import get_connection

try:
    connection=get_connection()
    with connection.cursor() as cursor:
        cursor.execute('call CONSULTAR_ALUMNOS()')
        resultset = cursor.fetchall()
        for row in resultset:
            print(row)
    connection.close()
except Exception as ex:
    print('ERROR')

try:
    connection=get_connection()
    with connection.cursor() as cursor:
        cursor.execute('CALL CONSULTAR_ALUMNO(%s)',(8))
        resultset = cursor.fetchall()
        for row in resultset:
            print(row)
    connection.close()
except Exception as ex:
    print('ERROR')

try:
    connection=get_connection()
    with connection.cursor() as cursor:
        cursor.execute('CALL AGREGAR_MAESTRO(%s, %s, %s)', ('Christian','Ruiz','cruiz@gmail.com'))
    connection.commit()
    connection.close()
except Exception as ex:
    print('ERROR')