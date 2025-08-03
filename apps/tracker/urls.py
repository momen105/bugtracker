from django.urls import path
from .views import *

urlpatterns = [
    
    # project
    path('project/', ProjectCRUDView.as_view(), name='project'),
   
    # comment
    path('comment/', CommentCRUDView.as_view(), name='comment'),
    
    # Bug
    path('bug/', BugCRUDView.as_view(), name='bug'),
    path("bugs/assigned/", AssignedBugsView.as_view(), name="assigned-bugs"),

]

