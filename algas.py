import time
from sys import getsizeof
import random
import matplotlib.pyplot as plt
import mysql.connector
import matplotlib.pyplot as plt


sizes1 = range(1, 1441) #1 Usuário

try:
    db_connection = mysql.connector.connect(
        host='localhost',
        user="root",
        password="rafa2507",
        database="transacao_isabella")

    cursor = db_connection.cursor()
    
    print("\n\n---- With Memoryview ----")
    vwMemory = []

    for n in sizes1:
        data = random.randint(60, 101)
        b = memoryview(b'data')
        start = time.time()
        max_mem = 0
        min_mem = 0
        while b:
            if n == len(str(b)):
                max_mem = getsizeof(b) - getsizeof('')
            elif len(str(b)) == 1:
                min_mem = getsizeof(b) - getsizeof('')
            b = str(b)[1:]
        stop = time.time()
        
        final = stop-start
        print(
            f'Transação {n} {final} - Max mem {max_mem} KB - Min mem {min_mem} B')
        vwMemory.append(final)

        query = "INSERT INTO memory(transacao, tempo_exec, max_mem, min_mem) " \
                "VALUES(%s,%s,%s,%s)"
        args = (n, final, max_mem, min_mem)

        cursor.execute(query, args)
        db_connection.commit()

        query = "INSERT INTO dados(frequencia) " \
                "VALUES(%s)"
        args = (data, )

        cursor.execute(query, args)
        db_connection.commit()
        



        
    
    print("Iniciando transações\n\n")
    print("---- Without Memoryview ----")
    vwWithoutMemory= []

    for n in sizes1:
        data = random.randint(60, 101)
        b = data
        start = time.time()
        max_mem = 0
        min_mem = 0
#         frequencia = random.randint(60, 101)
        while b:
            if n == len(str(b)):
                max_mem = getsizeof(b) - getsizeof('')
            elif len(str(b)) == 1:
                min_mem= getsizeof(b) - getsizeof('')
            b = str(b)[1:]
        stop = time.time()
        final = stop - start
        max_mem = max_mem/10**3
        print(
            f'Transação {n} {final} - Max mem {max_mem} KB - Min mem {min_mem} B')
        vwWithoutMemory.append(final)

        query = "INSERT INTO transaction_memory(transacao, tempo_exec, max_mem, min_mem) " \
                "VALUES(%s,%s,%s,%s)"
        args = (n, final, max_mem, min_mem)

        cursor.execute(query, args)
        db_connection.commit()

        query = "INSERT INTO dados(frequencia) " \
                "VALUES(%s)"
        args = (data, )

        cursor.execute(query, args)
        db_connection.commit()


    plt.plot(vwWithoutMemory, 'x-', label='Without Memoryview')
    plt.plot(vwMemory, 'o--', label='With Memoryview')
    plt.xlabel('Size of Bytearray')
    plt.ylabel('Time (s)')
    plt.legend()
    plt.show()
        
finally:
    db_connection.close()
    