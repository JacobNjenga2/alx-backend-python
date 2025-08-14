import django_filters
from .models import Message  # adjust import as needed

class MessageFilter(django_filters.FilterSet):
    # Example: filter by sender, conversation, sent_at range
    sender = django_filters.CharFilter(field_name="sender__username", lookup_expr='iexact')
    conversation = django_filters.NumberFilter(field_name="conversation__id")
    sent_after = django_filters.DateTimeFilter(field_name="sent_at", lookup_expr='gte')
    sent_before = django_filters.DateTimeFilter(field_name="sent_at", lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['sender', 'conversation', 'sent_after', 'sent_before']
