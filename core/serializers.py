from rest_framework import serializers

class BulkCreateSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        model_class = self.child.Meta.model
        items = [model_class(**item) for item in validated_data]
        return model_class.objects.bulk_create(items)

class BulkCreateModelSerializer(serializers.ModelSerializer):
    @classmethod
    def many_init(cls, *args, **kwargs):
        kwargs['child'] = cls()
        return BulkCreateSerializer(*args, **kwargs)