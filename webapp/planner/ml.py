# ML script

from .models import Task
from django.utils import timezone


class WeightedAverage:

    tasks = {}
    # Maps tasks to their priority ratings
    prs = {}

    def fill_tasks(user_tasks):
        '''
        Fills the tasks dictionary with the current user's tasks' info and populates the prs dict

        Params:
            user_tasks = current users tasks
        '''

        for task in user_tasks:
            tasks[task.id] = {
                'Due Date': task.dueDate, 'Prefer Date': task.preferDate, 'Exp Time': task.expTime,
                'Category': task.category, 'Add Date': task.addDate,
            }
            prs[task.id] = 0


    def generate_priority(task, date):
        '''
        Generate the priority rating of the given task and store it in the prs dict
        Only takes into account time til due and time til prefer
        TTEBREAKERS (if needed): expTime, and then (if necessary) addDate
            ^ use these when interpreting the results of the

        Params:
            task = task whose PR to calculate
            date = date on which to calculate the PR
        '''
        pr =


    def timeToPrefer(id, date):
        '''
        Calculates the amt of time from given date til user-specified preferred date

        Params:
            id = given task's id
            date = given date to check

        Returns:
            boolean: whether preferred date is given day
            timedelta: difference between preferred date and given date
        '''
        preferDate = tasks[id]['Prefer Date']
        prefer_today = preferDate.year == date.year and preferDate.month == date.month and preferDate.day = date.day
        return prefer_today, preferDate - date

    def timeToDue(id, date):
        '''
        Calculates the amt of time from a given date til due date

        Params:
            id = given task's id
            date = given date
        '''
        return tasks[id]['Due Date'] - date
