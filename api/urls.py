from django.urls import path
from api import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/login/', TokenObtainPairView.as_view(), name='api-login'),
    path('api/signup/', views.SignUp.as_view(), name='api-signup'),
    path('api/event/', views.EventView.as_view(), name='api-event'),
    path('api/create/', views.CreateEventView.as_view(), name='api-create'),
    path('api/organizer/event/', views.EventOrganizerView.as_view(), name='api-event-organizer'),
    path('api/update/events/<int:event_id>/', views.UpdateEventView.as_view(), name='api-update'),
    path('api/ticketholder/event/', views.TicketHolderEvent.as_view(), name='api-user'),
	path('api/<int:event_id>/ticketholder/', views.TicketHolderView.as_view(), name='api-ticketholder'),
	path('api/<int:event_id>/ticket/', views.BookView.as_view(), name='api-book'),


]
