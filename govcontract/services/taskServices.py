from datetime import datetime, timedelta, date
import copy
import math

from govcontract.serializers.task import TaskSerializer
from ..models import Holiday, Task

def format_date(d):
    if (isinstance(d, date)):
        return d
    elif (isinstance(d, datetime)):
        return d.date()
    else:
        return datetime.strptime(d, '%Y-%m-%d').date()

def get_prev_task(task):
    order_id = task.order_id if task.order_id != task.task_id else (task.order_id - 1)
    prev_task = Task.objects.filter(contract_id=task.contract_id).filter(order_id=order_id).get()
    return prev_task

def get_palt_actual(start_date, end_date):
    start = copy.deepcopy(start_date)
    end = copy.deepcopy(end_date)
    return (end - start).days + 1

def get_start_date(prev_end_date, day_count):
    start_date = copy.deepcopy(prev_end_date)

    if(day_count % 1 == 0):
        start_date += timedelta(days=1)

    while(start_date.weekday() > 4):
        start_date += timedelta(days=1)

    holidays = Holiday.objects.all().order_by('date').filter(observed__gte=start_date)
    for holiday in holidays:
        if(holiday.observed <= start_date):
            start_date += timedelta(days=1)

    return start_date

def get_end_date(start_date, bus_days, day_count):
    next_date = copy.deepcopy(start_date)
    holidays = Holiday.objects.all().order_by('date').filter(observed__gt=start_date)

    floor_days = math.floor(bus_days)

    for x in range(floor_days):
        next_date += timedelta(days=1)

        if(next_date.weekday() > 4):
            next_date += timedelta(days=2)

    # Add a day but if this condition met, remove that artificially added day
    if(day_count % 1 == 0 and bus_days % 1 == 0):
        next_date -= timedelta(days=1)

    for holiday in holidays:
        if(holiday.observed <= next_date):
            next_date += timedelta(days=1)

    while(next_date.weekday() > 4):
        next_date += timedelta(days=1)

    return next_date

def save_parent(p_task):
    task_serializer = TaskSerializer(data=p_task)

    if task_serializer.is_valid():
        task_serializer.save()