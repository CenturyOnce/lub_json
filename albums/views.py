from django.shortcuts import render
from .forms import AlbumForm
from .utils import save_album_to_file, handle_uploaded_file, get_all_albums

def home_view(request):
    context = {'message': '', 'is_error': False, 'albums': [], 'no_data_message': ''}
    
    if request.method == 'POST':
        if 'file_upload' in request.FILES:
            uploaded_file = request.FILES['file_upload']
            is_valid, message = handle_uploaded_file(uploaded_file)
            context['message'] = message
            context['is_error'] = not is_valid
            
        elif 'form_submit' in request.POST:
            form = AlbumForm(request.POST)
            if form.is_valid():
                save_album_to_file(form.cleaned_data)
                context['message'] = "Данные успешно сохранены в JSON файл."
                context['is_error'] = False
            else:
                context['message'] = "Ошибка валидации формы. Проверьте введенные данные."
                context['is_error'] = True
                context['form'] = form

    if 'form' not in context:
        context['form'] = AlbumForm()

    albums, no_data_msg = get_all_albums()
    if albums is not None:
        context['albums'] = albums
    else:
        context['no_data_message'] = no_data_msg

    return render(request, 'albums/home.html', context)