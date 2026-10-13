from django.urls import path

from apps.parts import views

app_name = 'parts'

urlpatterns = [
    path('', views.PartListView.as_view(), name='list'),
    path('types/', views.PartTypeListView.as_view(), name='types'),
    path(
        'types/<str:code>/filter-options/',
        views.PartFilterOptionsView.as_view(),
        name='filter-options',
    ),
    path('<int:pk>/', views.PartDetailView.as_view(), name='detail'),
]
