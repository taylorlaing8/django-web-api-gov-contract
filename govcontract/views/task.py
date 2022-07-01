from django.shortcuts import render
from django.db.models import Sum
from django.forms.models import model_to_dict

from rest_framework import generics
import logging

from govcontract.services.taskServices import get_palt_actual, get_end_date, get_prev_task, get_start_date, save_parent
from ..models import Task, Contract, Status
from ..serializers import TaskSerializer, ContractSerializer, ContractListSerializer
from rest_framework.permissions import IsAuthenticated

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime

# class TaskCreate(generics.CreateAPIView):
#     permission_classes = (IsAuthenticated,)
#     queryset = (Task.objects.all(),)
#     serializer_class = TaskSerializer


# class TaskList(generics.ListAPIView):
#     permission_classes = (IsAuthenticated,)
#     queryset = Task.objects.all().order_by('contract_id', 'order_id')
#     serializer_class = TaskSerializer

class TaskList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        tasks = Task.objects.all().order_by('contract_id', 'order_id')
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        task = request.data
        task['palt_actual'] = get_palt_actual(task['start_date'], task['end_date'])

        serializer = TaskSerializer(data=task)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        task = self.get_object(pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        task = self.get_object(pk)
        contract = task.contract_id
        parent_task = task.task_id

        # If status changed, update it and check if task is a subtask to update parent as well
        if (request.data['status'] != task.status):
            request.data['status_updated'] = datetime.now()

            if (parent_task != None):
                parent_task.status = Status.INCOMPLETE
                tasks = Task.objects.filter(task_id=parent_task.id).order_by('order_id')
                for tsk in tasks:
                    if (tsk.id == task.id): tsk.status = request.data['status']
                    if (tsk.status != parent_task.status and parent_task.status != Status.INPROGRESS):
                        parent_task.status = tsk.status

                parent_task.save()

        # If business days changed, start looping through tasks to update start/end dates
        if(request.data['bus_days'] != task.bus_days):
            par_or_task = task if parent_task == None else parent_task
            tasks = Task.objects.filter(contract_id=contract.id).order_by('order_id').filter(order_id__gte=par_or_task.order_id)

            # Get all tasks AFTER this task
            get_day_count = Task.objects.filter(contract_id=contract.id).order_by('order_id').filter(order_id__lt=par_or_task.order_id).filter(task_id__isnull=True).aggregate(Sum('bus_days'))
            day_count = get_day_count['bus_days__sum'] if get_day_count['bus_days__sum'] is not None else 0

            task.end_date = get_end_date(task.start_date, request.data['bus_days'], day_count)
            task.palt_actual = get_palt_actual(task.start_date, task.end_date)

            # Save parents as you go through the list
            p_task = None
            # Store previous task to access start date based on its end date
            prev_task = par_or_task

            for tsk in tasks:
                # If it is the root task
                if(tsk.task_id is None):
                    # If parent has already been set before and needs to be saved
                    if(p_task is not None):
                        p_task.end_date = prev_task.end_date
                        p_task.save()
                        prev_task = p_task
                        p_task = None

                    # If it is a parent
                    if(len(tsk.get_all_tasks()) > 1):
                        # Set parent to current task & initialize data
                        p_task = tsk
                        p_task.status = None
                        p_task.palt_plan = 0
                        p_task.palt_actual = 0
                        p_task.bus_days = 0
                        p_task.status = None
                        p_task.start_date = None
                        p_task.end_date = None
                        continue

                # ADD CALCULATIONS TO AGGREGATE PARENT TOTALS IN THIS IF BLOCK
                if(p_task is not None):

                    # Calculations
                    tsk.start_date = get_start_date(prev_task.end_date, day_count)
                    tsk.end_date = get_end_date(tsk.start_date, tsk.bus_days, day_count)
                    tsk.palt_actual = get_palt_actual(tsk.start_date, tsk.end_date)

                    # If this is the first task within parent subtasks
                    if((tsk.order_id - 1) == p_task.order_id):
                        p_task.status = tsk.status
                        p_task.start_date = tsk.start_date

                    if(tsk.id == task.id):
                        if(request.data['status'] != p_task.status and p_task.status != Status.INPROGRESS):
                            p_task.status = request.data['status']
                        p_task.palt_plan += task.palt_plan
                        p_task.palt_actual += task.palt_actual
                        p_task.bus_days += request.data['bus_days']

                        prev_task = task
                        day_count += request.data['bus_days']
                        continue
                    elif(tsk.order_id <= task.order_id):
                        if(tsk.status != p_task.status and p_task.status != Status.INPROGRESS):
                            p_task.status = tsk.status
                        p_task.palt_plan += tsk.palt_plan
                        p_task.palt_actual += tsk.palt_actual
                        p_task.bus_days += tsk.bus_days

                        prev_task = tsk
                        day_count += tsk.bus_days
                        continue

                if(tsk.id == task.id):
                    prev_task = task
                    day_count += request.data['bus_days']
                    continue

                # Calculations
                tsk.start_date = get_start_date(prev_task.end_date, day_count)
                tsk.end_date = get_end_date(tsk.start_date, tsk.bus_days, day_count)
                tsk.palt_actual = get_palt_actual(tsk.start_date, tsk.end_date)

                day_count += tsk.bus_days

                tsk.save()
                prev_task = tsk

                if(p_task is not None):
                    if(tsk.status != p_task.status and p_task.status != Status.INPROGRESS):
                        p_task.status = tsk.status
                    p_task.palt_plan += tsk.palt_plan
                    p_task.palt_actual += tsk.palt_actual
                    p_task.bus_days += tsk.bus_days


            request.data['end_date'] = task.end_date
            request.data['palt_actual'] = task.palt_actual
        
        task_serializer = TaskSerializer(task, data=request.data)
        if task_serializer.is_valid(raise_exception=True):
            task_serializer.save()
            return Response(task_serializer.data)
        return Response(task_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        task = self.get_object(pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
