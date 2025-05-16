from django.urls import path

from .views import userdb, listedsubs, listedbooks, bookissueform, returnbooks, returnbooks1, editprofile

urlpatterns = [
    path('userdb/', userdb, name='userdb'),
    path('listedsubs/', listedsubs, name='listedsubs'),
    path('listedbooks/<int:id>/', listedbooks, name="listedbooks"),
    path('bookissueform/<int:id>', bookissueform, name="bookissueform"),
    path('returnbooks', returnbooks, name='returnbooks'),
    path('returnbooks1/<int:id>', returnbooks1, name='returnbooks1'),
    path('editprofile/<int:id>', editprofile, name="editprofile")
]