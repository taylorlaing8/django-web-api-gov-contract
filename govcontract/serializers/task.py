from numpy import source
from rest_framework import serializers
from ..models import Contract, Task
from .poc import PointOfContactSerializer

class TaskSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=255)
    sub_title = serializers.CharField(max_length=255, allow_null=True)
    slug = serializers.CharField(max_length=255)
    status = serializers.CharField(max_length=2)
    task_id = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all(), many=False, allow_null=True)
    contract_id = serializers.PrimaryKeyRelatedField(queryset=Contract.objects.all(), many=False)
    order_id = serializers.IntegerField()
    gate = serializers.IntegerField()
    sub_gate = serializers.IntegerField(allow_null=True)
    palt_plan = serializers.FloatField()
    palt_actual = serializers.IntegerField()
    bus_days = serializers.FloatField(allow_null=True)
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    ssp_date = serializers.DateField(allow_null=True)
    comments = serializers.CharField(max_length=500, allow_null=True)
    tasks = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ('__all__')

    def to_representation(self, instance):
        self.fields['poc'] =  PointOfContactSerializer(read_only=True)

        return super(TaskSerializer, self).to_representation(instance)

    def get_tasks(self, instance):
        tasks = Task.objects.filter(task_id=instance.id).order_by('order_id')
        serializer = TaskSerializer(tasks, many=True)
        return serializer.data
