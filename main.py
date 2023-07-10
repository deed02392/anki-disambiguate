import requests
import json

url = 'http://localhost:8765'

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
        word_note_map = {}

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
                    word = value.strip()
                    if word not in word_note_map:
                        word_note_map[word] = set()
                    word_note_map[word].add(note_id)

        for word, note_ids_with_value in word_note_map.items():
            if len(note_ids_with_value) > 1:
                print(f'Cards with shared value "{word}": {note_ids_with_value}')

    else:
        print('AnkiConnect request failed.')


find_cards_with_shared_values("German Vocabulary")

