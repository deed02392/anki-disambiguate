import requests
import json

url = 'http://localhost:8765'

def get_notes_with_shared_values(value, deck_name):
    request_data = {
        'action': 'findNotes',
        'version': 6,
        'params': {
            'query': f'"WordTranslation:*{value}*" "deck:{deck_name}"'
        }
    }

    response = requests.post(url, data=json.dumps(request_data))
    if response.status_code == 200:
        data = response.json()
        return data['result']
    else:
        print('AnkiConnect request failed.')
        return []

def find_cards_with_shared_values(deck_name):
    request_data = {
        'action': 'findNotes',
        'version': 6,
        'params': {
            'query': f'"deck:{deck_name}"'
        }
    }

    response = requests.post(url, data=json.dumps(request_data))
    if response.status_code == 200:
        data = response.json()
        note_ids = data['result']
        shared_values = set()

        for note_id in note_ids:
            request_data = {
                'action': 'notesInfo',
                'version': 6,
                'params': {
                    'notes': [note_id]
                }
            }

            response = requests.post(url, data=json.dumps(request_data))
            if response.status_code == 200:
                data = response.json()
                note_info = data['result'][0]
                word_translation = note_info['fields']['WordTranslation']['value']
                split_values = word_translation.split(',')

                for value in split_values:
                    shared_values.add(value.strip())

        for shared_value in shared_values:
            note_ids_with_value = get_notes_with_shared_values(shared_value, deck_name)
            if len(note_ids_with_value) > 1:
                print(f'Cards with shared value "{shared_value}": {note_ids_with_value}')

    else:
        print('AnkiConnect request failed.')


find_cards_with_shared_values("German Vocabulary")

