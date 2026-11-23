import json
import os
import uuid
from django.conf import settings

def save_album_to_file(album_data):
    data_structure = {"albums": [album_data]}
    filename = f"album_{uuid.uuid4().hex}.json"
    filepath = os.path.join(settings.DATA_DIR, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data_structure, f, ensure_ascii=False, indent=4)
    return filename

def handle_uploaded_file(uploaded_file):
    if not uploaded_file.name.lower().endswith('.json'):
        return False, "Ошибка: разрешены только файлы формата JSON."

    safe_filename = f"upload_{uuid.uuid4().hex}.json"
    filepath = os.path.join(settings.DATA_DIR, safe_filename)

    with open(filepath, 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        if not isinstance(data, dict) or 'albums' not in data:
            raise ValueError("Отсутствует корневой ключ 'albums'.")
            
        for album in data['albums']:
            required_fields = ['title', 'artist', 'year', 'genre', 'tracks']
            if not all(field in album for field in required_fields):
                raise ValueError(f"В данных альбома отсутствуют обязательные поля: {required_fields}")
                
    except (json.JSONDecodeError, ValueError) as e:
        os.remove(filepath)
        return False, f"Файл не прошел валидацию: {str(e)}. Файл удален."
    except Exception as e:
        os.remove(filepath)
        return False, f"Произошла ошибка при чтении файла: {str(e)}. Файл удален."

    return True, f"Файл '{safe_filename}' успешно загружен и сохранен."

def get_all_albums():
    all_albums = []
    
    files = [f for f in os.listdir(settings.DATA_DIR) if f.endswith('.json')]
    
    if not files:
        return None, "На сервере пока нет ни одного файла с данными."

    for filename in files:
        filepath = os.path.join(settings.DATA_DIR, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                all_albums.extend(data.get('albums', []))
        except Exception:
            continue 
            
    return all_albums, None