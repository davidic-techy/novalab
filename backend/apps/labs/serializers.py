from rest_framework import serializers
from .models import Simulation, SandboxSession

class SimulationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Simulation
        fields = ['id', 'title', 'slug', 'description', 'lab_type', 'environment_config', 'initial_code']

class SandboxSessionSerializer(serializers.ModelSerializer):
    # We nest the simulation details so the frontend knows what to render
    simulation_title = serializers.CharField(source='simulation.title', read_only=True)
    environment_config = serializers.JSONField(source='simulation.environment_config', read_only=True)

    class Meta:
        model = SandboxSession
        fields = ['id', 'simulation', 'simulation_title', 'code_snapshot', 'status', 'environment_config', 'updated_at']
        read_only_fields = ['simulation', 'status', 'updated_at']