from django.urls import path
from .views.user import loginView, logoutView, changePasswordView
from .views.task import taskView, serverView, getCronTaskView, createCronTaskView, deleteCronTaskView, logView
from .views.tool import serverTestView, databaseTestView

urlpatterns = [
    path('login', loginView),
    path('logout', logoutView),
    path('change-password', changePasswordView),
    path('tasks', taskView),
    path('server', serverView),
    path('get-cron-task', getCronTaskView),
    path('create-cron-task', createCronTaskView),
    path('delete-cron-task', deleteCronTaskView),
    path('log', logView),
    path('server-test', serverTestView),
    path('database-test', databaseTestView),
]



