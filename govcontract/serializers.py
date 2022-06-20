from numpy import source
from rest_framework import serializers
from .models import Position, PointOfContact, Contract, Task


class PositionSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=255)
    department = serializers.CharField(max_length=255)

    class Meta:
        model = Position
        fields = ('__all__')


class PointOfContactSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=55)
    last_name = serializers.CharField(max_length=55)
    email = serializers.EmailField()
    prefix = serializers.CharField(max_length=10)
    title_id = serializers.IntegerField(write_only=True)    # FOR WRITING POC
    title = PositionSerializer(many=False, read_only=True)  # FOR UPDATING POC

    class Meta:
        model = PointOfContact
        fields = ('__all__')


class ContractSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=255)
    sub_title = serializers.CharField(max_length=255, allow_null=True)
    slug = serializers.CharField(max_length=255)
    type = serializers.CharField(max_length=55)
    ucid = serializers.CharField(max_length=55)     # Unique Contract ID
    status = serializers.CharField(max_length=2)
    value = serializers.FloatField()    # In millions of dollars (i.e. 455.53 = $455.53M)
    ss_leads = serializers.ListField(child = serializers.IntegerField(), write_only=True)
    need_date = serializers.DateTimeField()
    award_date = serializers.DateTimeField()
    cycle_code = serializers.CharField(max_length=15)
    pop_date = serializers.DateTimeField()
    g_o_p = serializers.IntegerField()
    g_t_p = serializers.IntegerField()
    g_tr_p = serializers.IntegerField()
    g_fr_o_p = serializers.IntegerField()
    g_fr_t_p = serializers.IntegerField()
    g_fr_tr_p = serializers.IntegerField()
    g_fr_fr_p = serializers.IntegerField()
    g_fr_fv_p = serializers.IntegerField()
    pocs = serializers.ListField(child = serializers.IntegerField(), write_only=True)
    tasks = serializers.SerializerMethodField()

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
    
    def get_tasks(self, instance):
        tasks = Task.objects.filter(contract_id=instance.id, task_id=None).order_by('order_id')
        serializer = TaskSerializer(tasks, many=True)
        return serializer.data

class ContractListSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=255)
    sub_title = serializers.CharField(max_length=255, allow_null=True)
    slug = serializers.CharField(max_length=255)
    type = serializers.CharField(max_length=55)
    ucid = serializers.CharField(max_length=55)     # Unique Contract ID
    status = serializers.CharField(max_length=2)
    value = serializers.FloatField()    # In millions of dollars (i.e. 455.53 = $455.53M)
    ss_leads = serializers.ListField(child = serializers.IntegerField(), write_only=True)
    need_date = serializers.DateTimeField()
    award_date = serializers.DateTimeField()
    cycle_code = serializers.CharField(max_length=15)
    pop_date = serializers.DateTimeField()
    g_o_p = serializers.IntegerField()
    g_t_p = serializers.IntegerField()
    g_tr_p = serializers.IntegerField()
    g_fr_o_p = serializers.IntegerField()
    g_fr_t_p = serializers.IntegerField()
    g_fr_tr_p = serializers.IntegerField()
    g_fr_fr_p = serializers.IntegerField()
    g_fr_fv_p = serializers.IntegerField()

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

        return super(ContractListSerializer, self).to_representation(instance)
    

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
    bus_days = serializers.IntegerField(allow_null=True)
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
    ssp_date = serializers.DateTimeField(allow_null=True)
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
