# albums/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import AlbumForm
from .utils import save_album_to_file, handle_uploaded_file, get_all_albums

def home_view(request):
    context = {'albums': [], 'no_data_message': ''}
    
    if request.method == 'POST':
        if 'file_upload' in request.FILES:
            uploaded_file = request.FILES['file_upload']
            is_valid, message_text = handle_uploaded_file(uploaded_file)
            
            if is_valid:
                messages.success(request, message_text)
            else:
                messages.error(request, message_text)
                
            return redirect('home')
            
        elif 'form_submit' in request.POST:
            form = AlbumForm(request.POST)
            if form.is_valid():
                save_album_to_file(form.cleaned_data)
                messages.success(request, "Данные успешно сохранены в JSON файл.")
                return redirect('home')
            else:
                messages.error(request, "Ошибка валидации формы. Проверьте введенные данные.")
                context['form'] = form

    if 'form' not in context:
        context['form'] = AlbumForm()

    albums, no_data_msg = get_all_albums()
    if albums is not None:
        context['albums'] = albums
    else:
        context['no_data_message'] = no_data_msg

    return render(request, 'albums/home.html', context)