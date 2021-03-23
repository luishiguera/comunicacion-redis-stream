import time
from walrus import Database as RedisDatabase

redis_conn = RedisDatabase(host='localhost', port=6379, db=0, decode_responses=True)

cg = redis_conn.consumer_group('cg-energy', 'data-entry')

while True:
    print('Ciclo infinito cada 1 segundo')
    messages = cg.data_entry.read()
    for message in messages:
        msg_id = message[0]
        data = message[1]['data']
        cg.data_entry.ack(msg_id)
        print(message)
    print(f'Pendientes {cg.data_entry.pending()}')
    time.sleep(1) # Cada 1 segundo