from django.urls import path
from .views import HomeView, RoadmapListView, RoadmapDetailView, UnitDetailView, JoinRoadmapView, TickCheckbox

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('roadmaps/', RoadmapListView.as_view(), name='roadmap_list'),
    path('roadmaps/<int:pk>', RoadmapDetailView.as_view(), name='roadmap_detail'),
    path('unit/<int:pk>', UnitDetailView.as_view(), name='unit_detail'),
    path('roadmaps/join/<int:pk>', JoinRoadmapView.as_view(), name='join_roadmap'),
    path('items/check/<int:pk>', TickCheckbox.as_view(), name='tick_checkbox')
]