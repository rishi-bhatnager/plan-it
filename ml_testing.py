import numpy as np
from datetime import datetime

class Task():
    def __init__(self, category, time, due, s = []):
        self.cat = category # one of [1, 2, 3]
        self.time = time # time user expects in half hours
        self.due = due # date due (year, month, day, half hour)
        self.slots = s # list of time slots


    def __str__(self):
        return "Task {}, which takes {} half hours can be at: {}".format(self.due, self.time, self.slots)

# User data on sleep:

s = [-1, 7] # 11 pm to 7 am

# convert s into 48 half hour format:

for i in range(len(s)):
    s[i] *= 2

# google calendar events defined by their half-hour spans:

g = [[20, 24], [34, 37]]

# put this into a vector (3 is used as num of categories):

x = 0.5 * np.ones((48))

for i in range(len(x)):
    # remove times in google events
    for n in g:
        if n[0] <= i and i <= n[1]:
            x[i] = 0
    # remove times of sleep
    if i >= (48 + s[0]) or i <= s[1]:
        x[i] = 0

print(x)

# make some user tasks:

t = [Task(1, 3, (2020, 1, 19, 39)),
    Task(3, 2, (2020, 1, 20, 22)),
    Task(3, 7, (2020, 1, 22, 0)),
    Task(2, 1, (2020, 1, 19, 36))]

# prioritize tasks based on due date:

# sorry this is a bad way to do this. should optimize later.

now = (2020, 1, 18, 46)
future = (now[0] + 1000, now[1], now[2], now[3])
tasks = []

for i in range(len(t)):
    soonest = Task(1, 1, future)
    for task in t:
        # check to see if this task is sooner than the current soonest
        if task.due[0] < soonest.due[0]:
            soonest = task
        # if year is same:
        elif task.due[0] == soonest.due[0]:
            # check month:
            if task.due[1] < soonest.due[1]:
                soonest = task
            # if month is same:
            elif task.due[1] == soonest.due[1]:
                # check day:
                if task.due[2] < soonest.due[2]:
                    soonest = task
                # if day is same:
                elif task.due[2] == soonest.due[2]:
                    #check the half hour:
                    if task.due[3] < soonest.due[3]:
                        soonest = task
    # move the soonest    
    t.remove(soonest)
    tasks.append(soonest)

# find open slots for each task

# go thru each task
for task in tasks:
    # go thru the list of times
    li = []
    for i in range(len(x)):
        # check if each time is open
        if x[i] != 0:
            # if it is, check that a large enough chunk ahead is too
            free = True
            for n in range(task.time):
                if i + n >= 48:
                    free = False
                    break
                # if at any point there is a 0, this space is not free
                elif x[i + n] == 0:
                    free = False
                    break
            if free:
                li.append(i)
    task.slots = li
    print(task)
            
    



















