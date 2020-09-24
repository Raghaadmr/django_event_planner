from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView,CreateAPIView,RetrieveUpdateAPIView
from .serializers import ( SignUpSerializer, EventSerializer, CreateEventSerializer,
EventOrganizerSerializer, TicketSerializer, EventUpdateSerializer, UserEventSerializer, UserSerializer )
from rest_framework.permissions import IsAuthenticated , IsUserAdmin
from rest_framework.filters import SearchFilter,OrderingFilter
from datetime import datetime
from .permissions import IsUser, IsAdmin
from events.models import Event,TicketsHolder


class SignUp(CreateAPIView):
	serializer_class = SignUpSerializer


class EventView(ListAPIView):
	queryset =  Event.objects.filter(date__gt=datetime.today())
	serializer_class = EventSerializer
	filter_backends = [SearchFilter,OrderingFilter]
	search_fields = ['name', 'description','event_organizer__username']


class CreateEventView(CreateAPIView):
	permission_classes = [IsAuthenticated, IsAdmin]
	serializer_class = CreateEventSerializer
	def perform_create(self, serializer):
		serializer.save(organizer=self.request.user)


class TicketHolderEvent(ListAPIView):
	serializer_class = TicketSerializer
	permission_classes = [IsAuthenticated, IsUser]

	def get_queryset(self):
		query = TicketsHolder.objects.filter(guest=self.request.user)
		return query


class UpdateEventView(RetrieveUpdateAPIView):
	queryset =  Event.objects.all()
	serializer_class = EventUpdateSerializer
	permission_classes = [IsAuthenticated, IsAdmin]
	lookup_field = 'id'
	lookup_url_kwarg = 'event_id'


class EventOrganizerView(ListAPIView):
	serializer_class = EventOrganizerSerializer
	queryset= Event.objects.all()
	filter_backends = [SearchFilter,OrderingFilter]
	search_fields = ['name', 'description','event_organizer__username']


class BookView(CreateAPIView):
	serializer_class = TicketSerializer
	permission_classes = [IsAuthenticated,]
	def perform_create(self,serializer):
		serializer.save(user=self.request.user, event_id=self.kwargs['event_id'])


class TicketHolderView(RetrieveAPIView):
	serializer_class = TicketHolderEventSerializer
	permission_classes = [IsAuthenticated, IsAdmin]
	lookup_field = 'id'
	lookup_url_kwarg = 'event_id'
	queryset=Event.objects.all()
