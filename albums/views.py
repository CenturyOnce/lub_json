from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import AlbumForm
from .utils import save_album_to_file, handle_uploaded_file, get_all_albums
from .models import Album

from django.http import JsonResponse

def ajax_search(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        query = request.GET.get('q', '')
        if query:
            results = Album.objects.filter(title__icontains=query) | Album.objects.filter(artist__icontains=query)
            
            data = [{
                'id': album.id,
                'title': album.title,
                'artist': album.artist,
                'year': album.year,
                'genre': album.genre,
                'tracks': album.tracks
            } for album in results]
            return JsonResponse({'results': data})
        return JsonResponse({'results': []})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def home_view(request):
    display_source = request.GET.get('source', 'db') 
    
    if request.method == 'POST':
        if 'file_upload' in request.FILES:
            is_valid, msg = handle_uploaded_file(request.FILES['file_upload'])
            if is_valid: messages.success(request, msg)
            else: messages.error(request, msg)
            return redirect('home')

        form = AlbumForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            storage = data.pop('storage_type')
            
            if storage == 'file':
                save_album_to_file(data)
                messages.success(request, "Альбом сохранен в JSON-файл.")
            else:
                if Album.objects.filter(title=data['title'], artist=data['artist']).exists():
                    messages.error(request, f"Альбом '{data['title']}' исполнителя '{data['artist']}' уже существует в БД!")
                else:
                    Album.objects.create(**data)
                    messages.success(request, "Альбом успешно добавлен в Базу Данных.")
            
            return redirect('home')
        else:
            messages.error(request, "Ошибка валидации формы.")

    else:
        form = AlbumForm(initial={'storage_type': 'db'})

    if display_source == 'db':
        albums = Album.objects.all().order_by('-id')
        no_data_msg = "В базе данных пока нет альбомов."
    else:
        albums, no_data_msg = get_all_albums()

    context = {
        'form': form,
        'albums': albums,
        'no_data_msg': no_data_msg,
        'display_source': display_source,
        'is_db_source': display_source == 'db'
    }
    return render(request, 'albums/home.html', context)

def edit_album(request, album_id):
    album = Album.objects.get(id=album_id)
    if request.method == 'POST':
        form = AlbumForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if Album.objects.filter(title=data['title'], artist=data['artist']).exclude(id=album_id).exists():
                messages.error(request, "Такой альбом уже существует!")
            else:
                album.title = data['title']
                album.artist = data['artist']
                album.year = data['year']
                album.genre = data['genre']
                album.tracks = data['tracks']
                album.save()
                messages.success(request, "Данные успешно обновлены.")
            return redirect('home')
    else:
        form = AlbumForm(initial={
            'title': album.title, 'artist': album.artist, 'year': album.year,
            'genre': album.genre, 'tracks': album.tracks, 'storage_type': 'db'
        })
    
    return render(request, 'albums/edit_album.html', {'form': form, 'album': album})

def delete_album(request, album_id):
    if request.method == 'POST':
        album = Album.objects.get(id=album_id)
        album.delete()
        messages.success(request, "Запись удалена из базы данных.")
    return redirect('home')