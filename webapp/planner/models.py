from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import timedelta, datetime
import time
import pytz
import warnings

class CalendarBlock(models.Model):
    '''
    Abstract model representing a block of time on the planner/calendar. Includes Task, Event
    '''

    name = models.CharField("Name", max_length=50, db_index=True)
        # optional first positional arg = human readable name
    notes = models.TextField(default="")
    addDate = models.DateTimeField("Time When Block was Created", default=timezone.now)

    # The user to which this block belongs
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
        # NOTES:
        #   - Used ForeignKey so that if associated user is deleted then their blocks are also deleted (that's what the
        #       on_delete parameter does), but may need to switch to ManyToManyField for task/event sharing (so a single block
        #       can be associated with multiple users if, for example, the creating user invites other users onto the task/event)
        #   - Since there is a default of None, be sure to check that users aren't None before dealing with them

    class Meta:
        abstract = True


    #returns addDate in Eastern time
    def getAddDate(self):
        if self.addDate is None:
            warnings.warn('some attributes are None')
            return None
        return CustomDateTime(self.addDate).convertTZ()


class Task(CalendarBlock):
    '''
    A task that must be scheduled
    '''

    class Meta:
        #earliest() gets first result, meaning earliest addDate is selected; dueDate = tiebreaker
        get_latest_by = ['addDate', 'dueDate']

        #priority order of fields to use when ordering Task objects
        #this order prioritizes (in this order): earliest addDate, earliest dueDate, greatest expTime,
            #and name is ascending order
        ordering = ['addDate', 'dueDate', '-expTime', 'name', ]


    # NOTE: Django auto adds an auto-incrementing 'id' field --> create a field and set primary_key=True
        # to create custom id fields for tasks
    # ALSO: can specify IDs when saving Tasks to database

    category = models.CharField(max_length=5, choices = [
        ('Ex', 'Exercise'),
        ('Leis', 'Leisure'),
        ('House', 'Household'),
        ('Pers', 'Personal'),
        ('Work', 'Work'),
        ('', 'None'),
        ], default='')

    dueDate = models.DateTimeField("Due Date",
        help_text="Enter by when this task must be completed in the following format: YYYY-MM-DD HH:MM")
    expTime = models.DurationField("Expected Time for Completion",
        help_text="Enter the amount of time you expect to need to complete this task in the following format: HH:MM:SS")



    '''List containing tuples of length 3

        Collectively, the list represents all the times at which this task is scheduled
        Each tuple represents a time at which the task is scheduled in the user's planner
        Each tuple contains (in this order):
            1. A DateTimeField representing the start time at which this particular instance is scheduled
            2. A DurationField representing for how long this particular instance is scheduled
            3. A BooleanField representing whether this particular instance was scheduled effectively

        Assuming (for now) multiple tasks can be scheduled during the same istance, this represents a many-to-many
            relationship (one task maps to many times, and a time can map to multiple tasks). Since this maps both ways,
            you can list all the ScheduleInstances associated with a particular Task as well as all Tasks associated
            with a particular ScheduleInstance.
        The times field will map to ScheduleInstance objects containing the fields described above.
        To determine whether a task was effectively scheduled, use the function defined below (towards end of Task class),
            which returns the proportion of ScheduledInstances of that task that were considered effectively-scheduled.
              --> NOTE: since we may not receive feedback on particular (or any) instances, this method may not some
                  instances in the proportion or possibly even return None
              --> An alternative solution to using this method would be to store a boolean at the beginning of the list
                  that represents whether the Task was scheduled effectively (and we could use any number of ways to set
                  this value). To do this the times field would need to map to a class that contains a single boolean
                  as well as a mapping to the ScheduleInstance objects.
    '''
    times = models.ManyToManyField('ScheduleInstance', db_table='Scheduled Times')

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Task {self.name} (Category: {self.category}), due {self.getDueDate()} with expected time {self.expTime}'

    #returns expTime in minutes
    def getExpTime(self):
        if self.expTime is None:
            warnings.warn('some attributes are None')
            return None
        return self.expTime.seconds / 60
        # return timedelta(minutes = self.expTime * 10**(-6) / 60)


    #returns dueDate in Eastern time
    def getDueDate(self):
        if self.dueDate is None:
            warnings.warn('some attributes are None')
            return None
        return CustomDateTime(self.dueDate).convertTZ()

    #returns time from now til due date
    def timeTilDue(self):
        if self.dueDate is None:
            warnings.warn('some attributes are None')
            return None
        return self.dueDate - timezone.now()

    #returns None if no feedback was received, otherwise returns proportion of instances that were effectively-scheduled
    def effectiveTask(self):
        count = 0
        num_effective = 0

        for instance in self.times.all():
            if instance is not None:
                count += 1
                if instance.effective:
                    num_effective += 1

        if count == 0:
            return None
        return num_effective / count


    #saves a task to the database by first checking its validity and then using Django's save method
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)   #calls Django's save()



class CustomDateTime(datetime):
    def __new__(cls, dt, tz=None):
        return super().__new__(cls, year=dt.year, month=dt.month, day=dt.day, hour=dt.hour, \
            minute=dt.minute, second=dt.second, microsecond=dt.microsecond)

    def __init__(self, dt, tz=None):
        # self.year = dt.year
        # self.month = dt.month
        # self.day = dt.day
        # self.hour = dt.hour
        # self.minute = dt.minute
        # self.second = dt.second
        # self.microsecond = dt.microsecond
        if tz is None:
            if dt.tzinfo is not None:
                self.timezone = str(dt.tzinfo)
            else:
                self.timezone = dt.timezone if isinstance(dt, CustomDateTime) else 'US/Eastern'
        else:
            self.timezone = str(tz)

        self.altered = False
        self.orig = dt
        super().__init__()


    def changeTimeZone(self, newTimeZone):
        if newTimeZone is None:
            warnings.warn('newTimeZone received is none, doing nothing and returning self')
        else:
            self.timezone = newTimeZone
            self.altered = True
        return self

    #if inplace is True, changes timezone of self and returns self
    #if inplace is False, returns CustomDateTime object with altered timezone (does not change self)
    def convertTZ(self, newTimeZone='US/Eastern', inplace=False):
        if newTimeZone is None:
            warnings.warn('newTimeZone received is none, doing nothing and returning self')
            return self

        if newTimeZone == self.timezone:
            return self

        try:
            new = pytz.timezone(newTimeZone)
        except UnknownTimeZoneError:
            warnings.warn('invalid timezone passed in, doing nothing and returning existing self')
            return self

        orig = pytz.timezone(self.timezone)
        new_dt = self.replace(tzinfo=orig).astimezone(new)

        if inplace:
            self = CustomDateTime(new.normalize(new_dt), tz=str(new))
            self.altered = True
            return self
        else:
            temp = CustomDateTime(new.normalize(new_dt), tz=str(new))
            return temp


        # if self.timezone != 'UTC':
        #     import warnings
        #     raise warnings.warn('self is not in UTC, doing nothing and returning existing self')
        # else:
        #     self.hour -= 4 if time.localtime().tm_isdst == 1 else 5
        #     if self.hour <= 0:
        #         self.hour += 24
        #         self.day -= 1

        #     self.changeTimeZone("US/Eastern")
        #     self.altered = True
        # return self


    def __add__(self, other):
        orig_tz = self.timezone
        result = super().__add__(other)
        return CustomDateTime(result, tz=orig_tz)

    #toString, excluded microseconds attribute
    def __str__(self):
        return f'{self.month:02}/{self.day:02}/{self.year:04} {self.hour:02}:{self.minute:02}:{self.second:02} ({self.timezone})'

    def __repr__(self):
        return str(self)


class ScheduleInstance(models.Model):
    '''
    One time for which a Task is scheduled
    '''

    class Meta:
        ordering = ['startTime', 'duration', 'effective']
        unique_together = ['startTime',]

    startTime = models.DateTimeField("Start time of this scheduled instance")
    duration = models.DurationField("Duration of this scheduled instance")
    effective = models.BooleanField("Whether this instance was scheduled effectively", default=None)
        # ^ give a default of True if None gives errors

    def __str__(self):
        return f'Scheduled Instance at {CustomDateTime(self.startTime).convertTZ()} for {self.duration}'

    def __repr__(self):
        return str(self)


class Event(CalendarBlock):
    '''
    An already-existing event that is scheduled at a specific time. Tasks cannot be scheduled during events.
    '''

    class Meta:
        ordering = ['startTime', 'duration', ]

    startTime = models.DateTimeField("Start Time",
        help_text="Enter the time at which this event starts in the following format: YYYY-MM-DD HH:MM")
    duration = models.DurationField("Duration",
        help_text="Enter for how long this event will last in the following format: HH:MM:SS")


    #returns startTime in Eastern time
    def getStartTime(self):
        if self.startTime is None:
            warnings.warn('some attributes are None')
            return None
        return CustomDateTime(self.startTime).convertTZ()

    #calculates and returns the ending time in ET
    def getEndTime(self):
        if self.startTime is None or self.duration is None:
            warnings.warn('some attributes are None')
            return None
        # start = self.getStartTime()
        # return CustomDateTime(dt=(start + self.duration), tz=start.timezone).convertTZ()
        return CustomDateTime(dt=(self.getStartTime() + self.duration)).convertTZ()

    #calculates and returns the ending time in UTC
    def getEndTimeUTC(self):
        if self.startTime is None or self.duration is None:
            warnings.warn('some attributes are None')
            return None
        return self.startTime + self.duration

    def __repr__(self):
        return f'Event {self.name}, from {self.getStartTime()} to {self.getEndTime()} (duration: {self.duration})'

    def __str__(self):
        return f'Event {self.name}, from {self.getStartTime()} to {self.getEndTime()}'

    #saves an event to the database by first checking its validity and then using Django's save method
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)   #calls Django's save()




# class AddTaskForm(UserCreationForm):
#     email = forms.EmailField()

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']
