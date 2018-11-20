from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('about/', views.AboutPageView.as_view(), name='about'),
    path('sites/', views.SiteListView.as_view(), name='sites'),
    path('sites/<int:pk>/', views.SiteDetailView.as_view(), name='site_detail'),

    # adding paths for country area
    path('country_area/', views.CountryAreaListView.as_view(), name='country_area'),
    path('country_area/<int:pk>/', views.CountryAreaDetailView.as_view(), name='country_area_detail'),

    # adding paths for form
    path('sites/new/', views.SiteCreateView.as_view(), name='site_new'),
    path('sites/<int:pk>/delete/', views.SiteDeleteView.as_view(), name='site_delete'),
    path('sites/<int:pk>/update/', views.SiteUpdateView.as_view(), name='site_update'),

    # adding path for filter
    path('sites/filter/', views.SiteFilterView.as_view(), name='site_filter')
]
