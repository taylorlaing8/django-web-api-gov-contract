from numpy import source
from rest_framework import serializers
from .models import Position, PointOfContact, Contract


class PositionSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=255)
    department = serializers.CharField(max_length=255)

    class Meta:
        model = Position
        fields = ('pk', 'title', 'department')


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
    ss_leads = PointOfContactSerializer(many=True, read_only=True, source="ss_lead_ids")
    ss_lead_ids = serializers.PrimaryKeyRelatedField(many=True, write_only=True, queryset=PointOfContact.objects.all())
    need_date = serializers.DateTimeField()
    award_date = serializers.DateTimeField()
    pco = PointOfContactSerializer(many=False, read_only=True)
    pco_id = serializers.IntegerField(write_only=True)
    buyer = PointOfContactSerializer(many=False, read_only=True)
    buyer_id = serializers.IntegerField(write_only=True)
    admin_pco = PointOfContactSerializer(many=False, read_only=True)
    admin_pco_id = serializers.IntegerField(write_only=True)
    admin_buyer = PointOfContactSerializer(many=False, read_only=True)
    admin_buyer_id = serializers.IntegerField(write_only=True)
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
    pocs = PointOfContactSerializer(many=True, read_only=True, source="poc_ids")
    poc_ids = serializers.PrimaryKeyRelatedField(many=True, write_only=True, queryset=PointOfContact.objects.all())

    class Meta:
        model = Contract
        fields = ('__all__')


class TaskSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=255)
    sub_title = serializers.CharField(max_length=255)
    slug = serializers.CharField(max_length=255)
    status = serializers.CharField(max_length=2)
    task_id = serializers.IntegerField()  # FIX MEEEEEEE !!!! TASK FOREIGN KEY INTEGER
    contract_id = (
        serializers.IntegerField()
    )  # FIX MEEEEEEE !!!! CONTRACT FOREIGN KEY INTEGER
    order_id = serializers.IntegerField()
    gate = serializers.IntegerField()
    sub_gate = serializers.IntegerField()
    palt_plan = serializers.FloatField()
    bus_days = serializers.IntegerField()
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
    ssp_date = serializers.DateTimeField()
    poc = serializers.IntegerField()  # FIX MEEEEEEE !!!! POC FOREIGN KEY INTEGER
    comments = serializers.CharField(max_length=500)
    tasks = (
        serializers.IntegerField()
    )  # TaskSerializer()                      # FIX MEEEEEEE !!!! MANY TASKS THAT RELATES TO ITSELF
    # tasks = TaskSerializer(many=True)

    # def create(self,validated_data):
    #     return Task.objects.create(**validated_data)
