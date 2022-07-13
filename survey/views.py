from django.shortcuts import render

# Create your views here.
import os
from django.http import HttpResponse
from .forms import MyfileUploadForm
from .models import file_upload
from zipfile import ZipFile


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def home(request):
    if request.method == 'POST':
        c_form = MyfileUploadForm(request.POST, request.FILES)
        if c_form.is_valid():
            name = c_form.cleaned_data['file_name']
            files = c_form.cleaned_data['files']
            file_upload(file_name=name, my_file=files).save()
            context = {
                'uploaded': False
            }
            return render(request, 'index.html', context)
        else:
            return HttpResponse("error")

    else:

        context = {
            'form': MyfileUploadForm(),
            'uploaded': True
        }

        return render(request, 'index.html', context)


def show_files(request):
    file_name = os.listdir('media')
    folder = ''
    for item in file_name:
        file = str(item)
        if file.split('.')[-1] == 'zip':
            with ZipFile('media/'+file, 'r') as zipObj:
                folder = file.split('.')[0]
                zipObj.extractall('media/data')
                print('File is unzipped in temp folder')

    all_data = file_upload.objects.all()
    image = []
    caption = []
    data = []
    data_files = os.listdir('media/data/'+folder)
    for item in data_files:
        if str(item).split('.')[-1] == 'txt':
            with open('media/data/' + folder + '/' + str(item), 'r') as f:
                content = f.readline()
                caption.append(str(content))
        elif str(item).split('.')[-1] == 'jpg':
            image.append(item)
    for j, k in zip(image, caption):
        data.append((j, k))

    context = {
        'folder': folder,
        'imgss': data,
        'username': all_data[0].file_name
    }
    return render(request, 'view.html', context)



def vote(request):
    user_name = str(request.POST.get('user_name'))
    label = str(request.POST.get('label'))
    filename = str(request.POST.get('filename'))
    if (user_name != 'None') and (user_name != ''):
        save_db(user_name, label, filename)

    return render(request, 'view.html')



def save_db(username, label, filename):
    with open('media/labelling.csv', 'a') as f:
        f.write(','.join([username, label, filename]) + '\n')
