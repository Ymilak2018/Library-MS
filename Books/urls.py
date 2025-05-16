from django.urls import path
from .views import addsub, addauth, addbook, viewsub, viewbooks, viewauth, delsub, delauth, editsubs, editauth, \
    viewsubbooks, delbook, editbook, bookreq, reqapp, reqdec, trackusers, search_result

urlpatterns = [
    path('addbook/', addbook, name='addbook'),
    path('addsub/', addsub, name='addsub'),
    path('addauth/', addauth, name='addauth'),
    path('viewsub/', viewsub, name='viewsub'),
    path('viewbooks/', viewbooks, name='viewbooks'),
    path('viewauth/', viewauth, name='viewauth'),
    path('delsub/<int:id>/', delsub, name='delsub'),
    path('delauth/<int:id>/', delauth, name='delauth'),
    path('delbook/<int:id>', delbook, name='delbook'),
    path('editsubs/<int:id>/', editsubs, name="editsubs"),
    path('editauth/<int:id>/', editauth, name="editauth"),
    path('editbook/<int:id>/', editbook, name="editbook"),
    path('viewsubbooks/<int:id>/', viewsubbooks, name="viewsubbooks"),
    path('userrequests/', bookreq, name="userrequests"),
    path('userrequests1/<int:id>/', reqapp, name='reqapp'),
    path('userrequests2/<int:id>/', reqdec, name='reqdec'),
    path('useractivity/', trackusers, name='useractivity'),
    path('searchbooks', search_result, name='search_result')
]