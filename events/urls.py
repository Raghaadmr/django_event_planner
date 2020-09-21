from django.urls import path
from .views import Login, Logout, Signup, home, dashboard, event_detail, event_create, event_update, event_delete

urlpatterns = [
	path('', home, name='home'),
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
	path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/<int:event_id>/', event_detail, name='event-detail'),

    path('dashboard/create', event_create, name='event-create'),
    path('dashboard/<int:event_id>/update/', event_update, name='event-update'),
    path('dashboard/<int:event_id>/delete/', event_delete, name='event-delete'),


]
