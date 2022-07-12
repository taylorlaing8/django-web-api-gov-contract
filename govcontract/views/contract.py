from govcontract.services.taskServices import format_date, get_end_date, get_palt_actual, get_start_date
from ..models import Contract, Status
from ..serializers import ContractSerializer, ContractListSerializer, ContractOverviewSerializer, TaskSerializer
from rest_framework.permissions import IsAuthenticated

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class ContractList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        contracts = Contract.objects.all().order_by('id')
        serializer = ContractListSerializer(contracts, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        tasks = request.data.pop('tasks')

        contract_serializer = ContractSerializer(data=request.data)

        if contract_serializer.is_valid(raise_exception=True):
            contract_serializer.save()

            if (len(tasks) > 0):
                prev_task = None
                day_count = 0
                order_id = 1
                subtasks = None
                subtask_array = []

                for task in tasks:
                    task['task_id'] = None
                    task['contract_id'] = contract_serializer.data['id']

                    if ('tasks' in task):
                        subtasks = task.pop('tasks')
                    else:
                        subtasks = None

                        if (task['slug'] == tasks[0]['slug']):
                            task['start_date'] = contract_serializer.data['start_date']
                        else:
                            task['start_date'] = get_start_date(format_date(prev_task['end_date']), day_count)
                        task['end_date'] = get_end_date(format_date(task['start_date']), task['bus_days'], day_count)
                        task['palt_actual'] = get_palt_actual(format_date(task['start_date']), format_date(task['end_date']))

                    if (subtasks and len(subtasks) > 0):
                        palt_plan = 0
                        bus_days = 0

                        for subtask in subtasks:
                            subtask['contract_id'] = contract_serializer.data['id']

                            if(subtask['status'] != task['status'] and task['status'] != Status.INPROGRESS):
                                task['status'] = subtask['status']

                            if (task['slug'] == tasks[0]['slug'] and 'start_date' not in task):
                                task['start_date'] = contract_serializer.data['start_date']
                                subtask['start_date'] = task['start_date']
                            elif (subtask['slug'] == subtasks[0]['slug']):
                                task['start_date'] = get_start_date(format_date(prev_task['end_date']), day_count)
                                subtask['start_date'] = task['start_date']

                            if ('start_date' not in subtask):
                                subtask['start_date'] = get_start_date(format_date(prev_task['end_date']) if prev_task else format_date(task['start_date']), day_count)
                            
                            subtask['end_date'] = get_end_date(format_date(subtask['start_date']), subtask['bus_days'], day_count)
                            subtask['palt_actual'] = get_palt_actual(format_date(subtask['start_date']), format_date(subtask['end_date']))

                            subtask_array.append(subtask)
                            prev_task = subtask

                            day_count += subtask['bus_days']
                            palt_plan += subtask['palt_plan']
                            bus_days += subtask['bus_days']


                        task['end_date'] = get_end_date(format_date(task['start_date']), task['bus_days'], day_count)
                        task['palt_actual'] = get_palt_actual(format_date(task['start_date']), format_date(task['end_date']))
                        task['palt_plan'] = palt_plan
                        task['bus_days'] = bus_days

                        palt_plan = 0
                        bus_days = 0
                    else:
                        day_count += task['bus_days']

                    prev_task = task

                    # ADD ORDER ID TO TASKS
                    task['order_id'] = order_id
                    order_id += 1

                    tskSerializer = TaskSerializer(data=task)

                    if tskSerializer.is_valid(raise_exception=True):
                        tskSerializer.save()
                        
                        if (len(subtask_array) > 0):
                            for subtask in subtask_array:
                                subtask['task_id'] = tskSerializer.data['id']
                                subtask['contract_id'] = contract_serializer.data['id']

                                subtask['order_id'] = order_id
                                order_id += 1

                                subtskSerializer = TaskSerializer(data=subtask)

                                if subtskSerializer.is_valid(raise_exception=True):
                                    subtskSerializer.save()

                            subtask_array = []

            return Response(contract_serializer.data, status=status.HTTP_201_CREATED)

        return Response(contract_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class ContractDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Contract.objects.get(pk=pk)
        except Contract.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        contract = self.get_object(pk)
        serializer = ContractSerializer(contract)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        contract = self.get_object(pk)
        serializer = ContractSerializer(contract, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        contract = self.get_object(pk)
        contract.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ContractOverview(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Contract.objects.get(pk=pk)
        except Contract.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        contract = self.get_object(pk)
        serializer = ContractOverviewSerializer(contract)
        return Response(serializer.data)

