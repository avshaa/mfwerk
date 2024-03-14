from rest_framework import serializers
from .models import Part

class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = ["id", "name", "mf_id", "org_file", "branded_file", "branded_file_url", "drawing_id", "material", "part_ids", "weight", "designation", "general_tolerances", "completed", "timestamp", "updated", "user"]