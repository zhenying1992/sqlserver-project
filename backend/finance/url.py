from django.urls import path
from .views import loginView

urlpatterns = [
    path('login', loginView),
    # path('log', ),
    # path('connect/server',),
    # path('connect/database', ),
    # path('period/task', ),
]



