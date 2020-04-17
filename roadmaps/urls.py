from django.urls import path
from .views import HomeView, RoadmapListView, RoadmapDetailView, UnitDetailView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('roadmaps/', RoadmapListView.as_view(), name='roadmap_list'),
    path('roadmaps/<int:pk>', RoadmapDetailView.as_view(), name='roadmap_detail'),
    path('unit/<int:pk>', UnitDetailView.as_view(), name='unit_detail')
]