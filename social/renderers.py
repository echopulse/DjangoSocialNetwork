from rest_framework.relations import (
    HyperlinkedRelatedField,
    HyperlinkedIdentityField,
)
from rest_framework.renderers import JSONRenderer
from collection_json import Collection, Data, Item, Link


class CollectionJsonRenderer(JSONRenderer):
    media_type = 'application/vnd.collection+json'
    format = 'collection+json'

    __link_cls__ = (HyperlinkedIdentityField, HyperlinkedRelatedField)

    def _is_field_hyperlink(self, field, value):
        for cls in self.__link_cls__:
            if isinstance(value, cls):
                return True
        return False

    def _infer_cj(self, data, serializer, **kwargs):
        """Renders a collection inferred from the data and serializer provided.

        :param data dict: Dictionary to render.
        :param serializer Serializer: Serializer use for the data provided.
        :param href str: URI to use for this resource.
        """
        href = kwargs.get("href", "")

        # is there an identity fields

        # which fields are related links
        link_fields = [field for field, obj in serializer.fields.items() if self._is_field_hyperlink(field, obj)]

        # generate the remaining fields
        if isinstance(data, dict):
            data = [data]

        def item_data(row):
            for field, value in row.items():
                yield Data(field, value)

        def item_links(row):
            for field in link_fields:
                yield Link(field, row[field])

        items = (Item(data=item_data(row), links=item_links(row)) for row in data)
        return Collection(href, items=items)

    def render(self, data, media_type=None, renderer_context=None):
        #Renders the data to collection+json hypermedia format
        if isinstance(data, Collection):
            data = data.to_dict()
        else:
            view = renderer_context["view"]
            serializer = getattr(view, "get_serializer", None)
            if not serializer:
                raise TypeError("Unable to generate a Collection+JSON object")
            request = renderer_context["request"]
            collection = self._infer_cj(data, serializer(),
                                        href=request.build_absolute_uri())
            data = collection.to_dict()

        return super(CollectionJsonRenderer, self).render(data, media_type,
                                                          renderer_context)
