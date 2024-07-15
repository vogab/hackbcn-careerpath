import json
from django.urls import reverse
from .models import UploadedImage, Request
from .forms import RequestForm, ImageUploadForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .tasks import some_async_function
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login


def landing_page(request):
    return render(request, 'uploader/landing.html')


def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('landing')
    else:
        form = ImageUploadForm()
    return render(request, 'uploader/upload.html', {'form': form})


def image_list_view(request):
    images = UploadedImage.objects.all()
    return render(request, 'uploader/image_list.html', {'images': images})


def image_detail_view(request, pk):
    image = UploadedImage.objects.get(pk=pk)
    return render(request, 'uploader/image_detail.html', {'image': image})


def image_delete_view(request, pk):
    image = UploadedImage.objects.get(pk=pk)
    image.delete()
    return HttpResponse('Image deleted successfully')


# REQUESTS

@login_required(login_url='/accounts/login')
def new_request(request):
    """
    View for creating a new request for career path recommendations
    """
    if request.method == 'POST':
        form = RequestForm(request.POST, request.FILES)
        form.instance.user = request.user
        if form.is_valid():
            form.save()
            return redirect(reverse('request-detail', args=[form.instance.pk]))
    else:
        if len(Request.objects.filter(user=request.user)) >= 5:
            messages.error(request, 'You have reached the maximum number of requests allowed. Please delete some requests before creating new ones.')
            return HttpResponse('You have reached the maximum number of requests allowed. Thanks for using our demo webpage.')
        form = RequestForm()
    return render(request, 'uploader/new_request.html', {'form': form})


@login_required(login_url='/accounts/login')
def requests(request):
    """
    View for listing all requests
    """
    requests = Request.objects.all().order_by('-uploaded_at').filter(user=request.user)
    for req in requests:
        req.data = {}
        try:
            req.data = json.loads(req.response.strip('```json').strip('```'))
        except json.JSONDecodeError:
            pass
    return render(request, 'uploader/requests.html', {'requests': requests})


@login_required(login_url='/accounts/login')
def request_detail(request, pk):
    """
    View for displaying a single request
    """
    my_request = Request.objects.filter(user=request.user).get(pk=pk)
    data = {}
    try:
        data = json.loads(my_request.response.strip('```json').strip('```'))
    except json.JSONDecodeError:
        pass
    return render(request, 'uploader/request_detail.html', {'request': my_request, 'data': data})


def test_view(request):
    return HttpResponse(some_async_function())

def test_view2(request):
    return HttpResponse("TEST")


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            # Automatically log in the user
            user = authenticate(username=username, password=form.cleaned_data.get('password1'))
            if user is not None:
                login(request, user)
                return redirect('landing')
            else:
                messages.error(request, 'There was an error logging in. Please try again.')
            return redirect('login')
    else:
        # If more than 50 users already exist, don't allow new registrations
        if len(User.objects.all()) > 50:
            messages.error(request, 'Sorry, we have reached the maximum number of users allowed for this site.')
            return HttpResponse('Sorry, we have reached the maximum number of users allowed for this site.')
        form = UserCreationForm()
    return render(request, 'uploader/register.html', {'form': form})