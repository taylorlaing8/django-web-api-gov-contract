from numpy import source
from rest_framework import serializers
from ..models import Contract, Task
from .poc import PointOfContactSerializer
from .task import TaskListSerializer

class ContractSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=255)
    sub_title = serializers.CharField(max_length=255, allow_null=True)
    slug = serializers.CharField(max_length=255)
    type = serializers.CharField(max_length=55)
    ucid = serializers.CharField(max_length=55)     # Unique Contract ID
    status = serializers.CharField(max_length=2)
    value = serializers.FloatField()    # In millions of dollars (i.e. 455.53 = $455.53M)
    ss_leads = serializers.ListField(child = serializers.IntegerField(), write_only=True)
    start_date = serializers.DateField(allow_null=True)
    # end_date = serializers.DateField(allow_null=True)
    need_date = serializers.DateField(allow_null=True)
    award_date = serializers.DateField(allow_null=True)
    cycle_code = serializers.CharField(max_length=15)
    pop_date = serializers.DateField(allow_null=True)
    g_o_p = serializers.IntegerField()
    g_t_p = serializers.IntegerField()
    g_tr_p = serializers.IntegerField()
    g_fr_o_p = serializers.IntegerField()
    g_fr_t_p = serializers.IntegerField()
    g_fr_tr_p = serializers.IntegerField()
    g_fr_fr_p = serializers.IntegerField()
    g_fr_fv_p = serializers.IntegerField()
    pocs = serializers.ListField(child = serializers.IntegerField(), write_only=True)
    # tasks = serializers.SerializerMethodField()

    class Meta:
        model = Contract
        fields = ('__all__')

    def to_representation(self, instance):
        self.fields['pco'] =  PointOfContactSerializer(read_only=True)
        self.fields['buyer'] =  PointOfContactSerializer(read_only=True)
        self.fields['admin_pco'] =  PointOfContactSerializer(read_only=True)
        self.fields['admin_buyer'] =  PointOfContactSerializer(read_only=True)

        self.fields['ss_leads'] = PointOfContactSerializer(many=True, read_only=True)
        self.fields['pocs'] = PointOfContactSerializer(many=True, read_only=True)

        return super(ContractSerializer, self).to_representation(instance)
    
    # def get_tasks(self, instance):
    #     tasks = Task.objects.filter(contract_id=instance.id, task_id=None).order_by('order_id')
    #     serializer = TaskListSerializer(tasks, many=True)
    #     return serializer.data

class ContractListSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=255)
    sub_title = serializers.CharField(max_length=255, allow_null=True)
    slug = serializers.CharField(max_length=255)
    type = serializers.CharField(max_length=55)
    ucid = serializers.CharField(max_length=55)     # Unique Contract ID
    status = serializers.CharField(max_length=2)
    value = serializers.FloatField()    # In millions of dollars (i.e. 455.53 = $455.53M)
    start_date = serializers.DateField(allow_null=True)
    need_date = serializers.DateField()
    award_date = serializers.DateField()
    cycle_code = serializers.CharField(max_length=15)

    class Meta:
        model = Contract
        fields = ('id', 'title', 'sub_title', 'slug', 'type', 'ucid', 'status', 'value', 'need_date', 'award_date', 'cycle_code', 'start_date')

class ContractTasksSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=255)
    sub_title = serializers.CharField(max_length=255, allow_null=True)
    slug = serializers.CharField(max_length=255)
    ucid = serializers.CharField(max_length=55)     # Unique Contract ID
    status = serializers.CharField(max_length=2)
    tasks = serializers.SerializerMethodField()
    pocs = serializers.ListField(child = serializers.IntegerField(), write_only=True)

    class Meta:
        model = Contract
        fields = ('id', 'title', 'sub_title', 'slug', 'ucid', 'status', 'tasks', 'pocs')

    def to_representation(self, instance):
        self.fields['pocs'] = PointOfContactSerializer(many=True, read_only=True)

        return super(ContractTasksSerializer, self).to_representation(instance)

    def get_tasks(self, instance):
        tasks = Task.objects.filter(contract_id=instance.id, task_id=None).order_by('order_id')
        serializer = TaskListSerializer(tasks, many=True)
        return serializer.data