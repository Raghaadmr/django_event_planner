from django.urls import path
from .views import Login, Logout, Signup, home, userdashboard ,dashboard, event_detail, event_create, event_update, event_delete, event_list, book_ticket
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	path('', home, name='home'),
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
	path('dashboard/', dashboard, name='dashboard'),
	path('events/', event_list, name='event-list'),
    path('event/<int:event_id>/ticket', book_ticket, name='ticket'),
	path('userdashboard/', userdashboard, name='userdashboard'),

	#path('profile/<int:user_id>/', profile, name='profile'),
    path('event/<int:event_id>/', event_detail, name='event-detail'),
    path('event/create/', event_create, name='event-create'),
    path('event/<int:event_id>/update/', event_update, name='event-update'),
    path('event/<int:event_id>/delete/', event_delete, name='event-delete'),


]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
