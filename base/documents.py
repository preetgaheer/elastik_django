from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Cook, MenuItems


@registry.register_document
class CookDocument(Document):
    menu_items = fields.NestedField(properties={
        'name': fields.TextField(),
        'id': fields.IntegerField(),
    })
    location = fields.GeoPointField(attr='location_field_indexing')

    def prepare_menu_items(self, instance):
        menu_items_list = instance.menuitems_set.all()
        ingredients_list = [{
            'id': item.pk,
            'name': item.name
        } for item in menu_items_list]
        return ingredients_list

    class Index:
        name = 'cook'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    class Django:
        model = Cook
        fields = [
            'id',
            'name'
        ]
        related_models = [MenuItems]

    def get_queryset(self):
        """Not mandatory but to improve performance we can select related in
            one sql request"""
        return super(CookDocument, self).get_queryset().prefetch_related(
            'menuitems_set')
    
    def get_instances_from_related(self, realted_obj):
        pass
        # if isinstance(realted_obj, MenuItems):
        #     return realted_obj
