import os

from django.http import HttpResponse, FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.encoding import smart_str
from django.views import View

from Transfer.forms import FileForm
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm, LoginForm
from django.contrib.auth.decorators import login_required

from .models import File, CustomUser


@login_required
def upload_file(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = FileForm(request.POST, request.FILES, request=request)
            if form.is_valid():
                file = form.save(commit=False)
                # set the transfer_to field to the authenticated user
                file.transfer_to = file.transfer_to
                file.save()
                return redirect('home')
        else:
            form = FileForm()
        return render(request, 'upload.html', {'form': form})
    else:
        print("Not Authenticated")


def home(request):
    files = File.objects.all()
    users = CustomUser.objects.all()

    if request.user.is_authenticated:
        email = request.user.email
    else:
        email = 'AnonymousUser'

    return render(request, 'home.html', {'files': files})


def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, email=email, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'registration.html', {'form': form})


def login_view(request):
    template_name = 'login.html'
    context = {}

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)

            if user:
                login(request, user)
                return redirect('home')
            else:
                context['error_message'] = 'Invalid login credentials.'
        else:
            context['error_message'] = 'Invalid login credentials.'
    else:

        form = LoginForm()

    context['form'] = form
    return render(request, template_name, context)


def logoutPage(request):
    logout(request)
    return redirect("home")


# def download(request, pk):
#     obj = File.objects.get(id=pk)
#     filename = obj.file.path
#     response = FileResponse(open(filename, 'rb'))
#     print(filename)
#     return render(request, 'download.html', {'filename': filename})


class DownloadFileView(View):
    def get(self, request, pk):
        # Get the file object from the database
        file = get_object_or_404(File, pk=pk)

        # Build the response
        response = FileResponse(file.file, as_attachment=True)
        file_name = file.file.name.split('/')[-1]
        response['Content-Disposition'] = 'attachment; filename="%s"' % smart_str(file_name)

        # Set the content type based on the file extension
        content_type_map = {
            '.pdf': 'application/pdf',
            '.doc': 'application/msword',
            '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            '.xls': 'application/vnd.ms-excel',
            '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            '.ppt': 'application/vnd.ms-powerpoint',
            '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
            '.txt': 'text/plain',
            '.csv': 'text/csv',
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.gif': 'image/gif',
            '.mp3': 'audio/mpeg',
            '.wav': 'audio/wav',
            '.mp4': 'video/mp4',
            '.mov': 'video/quicktime',
        }
        content_type = content_type_map.get(file_name.lower().rsplit('.', 1)[-1], 'application/octet-stream')
        response['Content-Type'] = content_type

        return response
