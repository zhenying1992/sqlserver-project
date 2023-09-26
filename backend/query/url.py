from django.urls import path
from query.view import bmView, columnView, dataView, logoutView, loginView, createView, userView, usersView, \
    zyColumnView, zyDataView, xmView, updateView

urlpatterns = [
    path('users', usersView),
    path('user', userView),
    path('login', loginView),
    path('logout', logoutView),
    path('create-user', createView),
    path('update-user', updateView),

    path('bm', bmView),
    path('xm', xmView),
    path('column', columnView),
    path('data', dataView),

    path('zy/column', zyColumnView),
    path('zy/data', zyDataView),
]
