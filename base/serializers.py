from .models import Cook
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from .documents import CookDocument
from rest_framework.serializers import SerializerMethodField


class CookSerializer(DocumentSerializer):
    location = SerializerMethodField('get_location')

    class Meta(object):
        """Meta options."""
        model = Cook
        document = CookDocument
        fields = (
            'id',
            'name',
            'menu_items',
        )

    def get_location(self, obj):
        """Represent location value."""
        try:
            return obj.location.to_dict()
        except Exception as e:
            print(e)
