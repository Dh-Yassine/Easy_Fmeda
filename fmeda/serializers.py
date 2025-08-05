from rest_framework import serializers
from .models import Project, SafetyFunction, Component, FailureMode

class FailureModeSerializer(serializers.ModelSerializer):
    # Map frontend field names to backend field names
    failure_rate_total = serializers.FloatField(source='Failure_rate_total', required=False)
    is_spf = serializers.BooleanField(source='is_SPF', required=False)
    is_mpf = serializers.BooleanField(source='is_MPF', required=False)
    spf_safety_mechanism = serializers.CharField(source='SPF_safety_mechanism', required=False)
    mpf_safety_mechanism = serializers.CharField(source='MPF_safety_mechanism', required=False)
    spf_diagnostic_coverage = serializers.FloatField(source='SPF_diagnostic_coverage', required=False)
    mpf_diagnostic_coverage = serializers.FloatField(source='MPF_diagnostic_coverage', required=False)

    class Meta:
        model = FailureMode
        fields = '__all__'

class SafetyFunctionSerializer(serializers.ModelSerializer):
    related_components = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = SafetyFunction
        fields = '__all__'

class ComponentSerializer(serializers.ModelSerializer):
    failure_modes = FailureModeSerializer(many=True, read_only=True)
    related_sfs = SafetyFunctionSerializer(many=True, read_only=True)

    class Meta:
        model = Component
        fields = '__all__'

    def create(self, validated_data):
        related_sfs_data = self.context.get('related_sfs', [])
        component = Component.objects.create(**validated_data)
        if related_sfs_data:
            component.related_sfs.set(related_sfs_data)
        return component

    def update(self, instance, validated_data):
        related_sfs_data = self.context.get('related_sfs', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if related_sfs_data is not None:
            instance.related_sfs.set(related_sfs_data)
        return instance

class ProjectSerializer(serializers.ModelSerializer):
    safety_functions = SafetyFunctionSerializer(many=True, read_only=True)
    components = ComponentSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = '__all__' 