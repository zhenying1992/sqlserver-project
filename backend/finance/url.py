from django.urls import path
from .views.user import loginView, logoutView, changePasswordView, createUserView
from .views.task import logView, updateCopyTaskView, updateDeleteTaskView
from .views.tool import serverTestView, databaseTestView, copyFileView, deleteLocalFileView, backupDatabaseView
from .views.system import diskView, cpuView, memoryView, sysView

urlpatterns = [
    path('login', loginView),
    path('logout', logoutView),
    path('change-password', changePasswordView),
    path('create-user', createUserView),

    path('log', logView),
    path('task/update-copy-task', updateCopyTaskView),
    path('task/update-delete-task', updateDeleteTaskView),

    path('server-test', serverTestView),
    path('database-test', databaseTestView),
    path('copy-file', copyFileView),
    path('backup-database', backupDatabaseView),
    path('delete-local-file', deleteLocalFileView),

    path('cpu', cpuView),
    path('memory', memoryView),
    path('disk', diskView),
    path('sys', sysView),
]
