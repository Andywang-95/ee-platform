from rest_framework import serializers


class FieldSerializer(serializers.Serializer):
    name = serializers.CharField()
    label = serializers.CharField()


class PartTypeSerializer(serializers.Serializer):
    code = serializers.CharField()
    label = serializers.CharField()
    list_fields = FieldSerializer(many=True)
    detail_fields = FieldSerializer(many=True)
    search_fields = serializers.ListField(child=serializers.CharField())
    filter_fields = FieldSerializer(many=True)
    editable_fields = serializers.ListField(child=serializers.CharField())
    remark_field = serializers.CharField()


# A part row is keyed by database column names, which differ per part type, so
# rows are described as free-form objects rather than a fixed set of fields.
class PartPageSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.URLField(allow_null=True)
    previous = serializers.URLField(allow_null=True)
    results = serializers.ListField(child=serializers.DictField())
