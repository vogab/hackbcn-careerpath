from django.urls import path
from .views import *

urlpatterns = [
    path('', landing_page, name='landing'),
    path('form/', upload_image, name='upload-form'),
    path('list/', image_list_view, name='image-list'),
    path('detail/<int:pk>/', image_detail_view, name='image-detail'),
    path('delete/<int:pk>/', image_delete_view, name='image-delete'),
    # REQUESTS
    path('request/', new_request, name='new-request'),
    path('requests/', requests, name='requests'),
    path('request/<int:pk>/', request_detail, name='request-detail'),
    path('test/', test_view, name='test-view'),
    path('test2/', test_view2, name='test-view2'),
]
