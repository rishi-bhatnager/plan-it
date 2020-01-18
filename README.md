# PlannerApp

One issue many people face is time management. It's easy to lose focus of work you need to get done, especially when there are so many distractions around. Yes, you can plan rigid blocks of time where you will try finish each task, but it's very easy to fall off of these goals. When you miss one task, usually this snowballs into the rest and destroys the plan for the day.

So how can we fix this? Can we make a scheduling app that is more forgiving of missed deadlines and eases you back into your work instead of falling apart?

To keep things simple for the user, they should just input in a list of things they have to do, the time they expect each task to take, and when each one needs to be done. There would also be N/A options for these parameters if the user either doesn't put anything, or if the task has no due date/expected completion time. An algorithm will then prioritize these for them based on the given due dates, after which the user can re-prioritize if theyso choose.

We can then ask the user how many hours they would like to work for the day, and how stressed they feel. These can be used to optimize the schedule for max likelihood of completion. By using historical data on how the user has felt in the past and comparing that to the success rate of plans we gave them, we can determine which schedules are best. Additionally, we can generalize data across users to determine the ideal default schedule method for each level of stress, then adapt from there based on the specific user.

Now, another system takes all these tasks and maps them onto Google calendar. This way, our processes do not interfere with any plans they already have. We should also allow the user to edit their Google calendar events in case they forgot something and realize a conflict in the schedule we design. To begin with, we should just display their Google calendar with our work events added. Eventually, we can consider making our own calendar UI if the app gains popularity.
