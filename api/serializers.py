from rest_framework import serializers
from django.contrib.auth.models import User
from events.models import Event,TicketsHolder


class LoginSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['username']


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name',]

    def create(self, validated_data):
        new_user = User(**validated_data)
        new_user.set_password(new_user.password)
        new_user.save()
        return new_user


class EventSerializer(serializers.ModelSerializer):
	class Meta:
		model = Event
		fields = '__all__'


class CreateEventSerializer(serializers.ModelSerializer):
	class Meta:
		model = Event
		fields = ['name', 'date' ,'location','description']


class EventUpdateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Event
		fields = ['name', 'date' ,'location','description']


class OrganizerSerializer(serializers.ModelSerializer):
	event_organizer= serializers.SerializerMethodField()

	class Meta:
		model= Event
		fields=['event_organizer','name', 'date ','location', 'seats']

	def get_event_organizer(self, obj):
		return obj.event_organizer.username


class TicketSerializer(serializers.ModelSerializer):
	event = serializers.SerializerMethodField()

	class Meta:
		model= TicketsHolder
		exclude=['guest']

	def get_event(self, obj):
		return (obj.event.name)


class TicketHolderSerializer(serializers.ModelSerializer):
	TicketHolder=serializers.SerializerMethodField()

	class Meta:
		model= TicketsHolder
		fields=['user']

	def get_TicketHolder(self, obj):
		return (obj.TicketHolder.first_name+" "+obj.TicketHolder.last_name)


class TicketHolderEventSerializer(serializers.ModelSerializer):
		TicketHolder=serializers.SerializerMethodField()
		class Meta:
			model=Event
			fields=['name', 'date' ]

		def get_TicketHolder(self,obj):
			myevent = obj.gustevent.all()
			return TicketHolderSerializer(myevent,many=True).data
