import json
import random

from werkzeug.datastructures import ImmutableMultiDict

clients = {
    'uniq_id': {'login': 'pass'},
}


def authorization(form: ImmutableMultiDict) -> (bool, int):
    uniq_id = 1
    while uniq_id in clients:
        uniq_id = random.randint(1, 100)

    for client in clients.values():
        if form['login'] in client.keys() \
                and form['pass'] in client.values():
            for client_id in clients:
                if clients[client_id] == {form['login']: form['pass']}:
                    return client_id

        elif form['login'] in client.keys():
            if form['pass'] != client[form['login']]:
                return False

    clients.update({uniq_id: {form['login']: form['pass']}})

    with open(f'client_{uniq_id}_cpu_load.csv', 'w') as file:
        file.write(f'{uniq_id};cpu\n')
        return uniq_id
