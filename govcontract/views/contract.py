from datetime import datetime
from govcontract.serializers.task import TaskSerializer
from govcontract.services.taskServices import get_palt_actual
from ..models import Contract
from ..serializers import ContractSerializer, ContractListSerializer
from rest_framework.permissions import IsAuthenticated

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class ContractList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        contracts = Contract.objects.all()
        serializer = ContractListSerializer(contracts, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        tasks = request.data.pop('tasks')

        serializer = ContractSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            contract_id = serializer.data['id']

            if (len(tasks) > 0):
                for task in tasks:
                    if ('tasks' in task):
                        subtasks = task.pop('tasks')
                    else:
                        subtasks = None

                    task['task_id'] = None
                    task['contract_id'] = contract_id
                    task['palt_actual'] = get_palt_actual(datetime.strptime(task['start_date'], '%Y-%m-%d'), datetime.strptime(task['end_date'], '%Y-%m-%d'))

                    tskSerializer = TaskSerializer(data=task)

                    if tskSerializer.is_valid(raise_exception=True):
                        tskSerializer.save()
                        
                        if (subtasks and len(subtasks) > 0):
                            for subtask in subtasks:
                                subtask['task_id'] = tskSerializer.data['id']
                                subtask['contract_id'] = contract_id
                                subtask['palt_actual'] = get_palt_actual(datetime.strptime(subtask['start_date'], '%Y-%m-%d'), datetime.strptime(subtask['end_date'], '%Y-%m-%d'))

                                subtskSerializer = TaskSerializer(data=subtask)

                                if subtskSerializer.is_valid(raise_exception=True):
                                    subtskSerializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
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
