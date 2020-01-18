# PlannerApp

One issue many people face is time management. It's easy to lose focus of work you need to get done, especially when there are so many distractions around. Yes, you can plan rigid blocks of time where you will try finish each task, but it's very easy to fall off of these goals. When you miss one task, usually this snowballs into the rest and destroys the plan for the day.

So how can we fix this? Can we make a scheduling app that is more forgiving of missed deadlines and eases you back into your work instead of falling apart?

To keep things simple for the user, they should just input in a list of things they have to do, the time they expect each task to take, and when each one needs to be done. There would also be N/A options for these parameters if the user either doesn't put anything, or if the task has no due date/expected completion time. An algorithm will then prioritize these for them based on the given due dates, after which the user can re-prioritize if theyso choose.

We can then ask the user how many hours they would like to work for the day, and how stressed they feel. These can be used to optimize the schedule for max likelihood of completion. By using historical data on how the user has felt in the past and comparing that to the success rate of plans we gave them, we can determine which schedules are best. Additionally, we can generalize data across users to determine the ideal default schedule method for each level of stress, then adapt from there based on the specific user.

Now, another system takes all these tasks and maps them onto Google calendar. This way, our processes do not interfere with any plans they already have. We should also allow the user to edit their Google calendar events in case they forgot something and realize a conflict in the schedule we design. To begin with, we should just display their Google calendar with our work events added. Eventually, we can consider making our own calendar UI if the app gains popularity.


Here is the general app process I'm imagining:
 
User logs into their Google account upon opening the app for the first time.
Survey questions (first time only, but answers can be changed at any time):
When do you usually get to bed?
When do you usually wake up?
When do you like to work?
The app now creates a 24-hour vector (with values between 0 and 1?) that represents how desirable each hour is for work. Of course, the time period while the user is asleep should be assigned to 0 always. Times while other events on the Google      calendar are going on should also be assigned 0. The remaining hours are assigned value based partially on how productive the average person is, and in part on the time during which the user claims to be productive.
At the start of the day, the user is prompted by app to put down all specific things they need to do. Order is not important.
User specifies their events by putting them into bullets, giving time expected per task and due date.
User is asked two questions:
How long would you like to work for today? (Notify user if they select amount larger than available hours in the day)
How stressed/fatigued do you feel today?
App then priority ranks these tasks in order of due date and presents this new list to the user.
User can now change these priorities if they wish.*
The default algorithm would insert the events in order of priority into the available hours on the calendar. While this may sound straightforward, there is some compromise that comes into play here. The next available hour may not be the most      desirable one (like if it's morning and the user claims to enjoy working at night). A reasonable principle would be to insert the most important work into the most desirable time slot. Additionally, I would imagine that users who claim to be stressed can benefit by doing an easy task first. Easiness would in this case be defined by how long the task is expected to take.
At any point, the user can update their list by adding or removing a task. If they remove a task, this data should be kept, as it informs us of how accurately they were      able to predict the time it took them. There is one issue here. The user may not be crossing off the task right upon completion. The app should assign some probability to this based on how close it is to the expected completion time, and how close it is to other tasks being crossed off. For example two tasks being crossed off within seconds would make it extremely likely that the first one is not an accurate time of completion. There is also the reasonable chance that the user does not cross off tasks until morning. Again, these are most likely not the times of completion and should therefore be marked as outliers before analysis.
The app takes these completion times and gives the user the option to update their planner. In settings this could be made a default.
If the user does not cross off all tasks before they begin the next day, the app will mark this down, noting the success of the plan. We then regularize this based on how      stressed the user said they were feeling, for that (not the schedule), could have been the reason for failure. If all tasks were crossed off, this was a success and can be used as a positive example for the machine learning.
Now we must get into the task of the machine learning. This needs to recognize trends behind user completion. We need to find out which configurations of a given set of tasks lead to the best productivity. If we know what productivity previous      task arrangements have caused in the past, we can infer what plans will yield the highest performance in the future. There are multiple ways we could go about this…
 
Option 1:
 
Somehow vectorize the schedule and put it into a neural net that outputs some productivity index for that arrangement. Train this net enough and we will be able to test all possible schedules to see which is the best. How can a schedule be vectorized? This is pretty much the most important theoretical question we would need to figure out. Too many features and the model will be inefficient; too few and it will not be able to find patterns. Each schedule takes in x tasks for the day. It is constrained by the number of hours the user has specified and the number of hours of the tasks. Other than that, it can presumably arrange the tasks in several ways. A schedule is characterized by how much it prioritizes early due dates, how well
 
Option 2:
 
We learn features about each individual, and insert those into a generic planning algorithm. For example, if a person seems to work well in the evening, those times are given priority. So this requires an input vector that begins as the average person and is tweaked with new data. This vector would include things like how stressed the user is on average, the time of day they work best, and how efficient they tend to be. This would necessitate a handmade algorithm that prioritizes based on these features. The upshot is that this requires essentially no complex training. Simply altering vectors by some set percentage each day would be sufficient to encapsulate changes in the user.

Option 3:

We construct a probability tensor (3D matrix) for each individual. This tensor defines how likely the user is to do work in each hour (or maybe half hour) of the day, in each category, and in each state of stressed-ness. This begins as the average tensor and eventually becomes customized with time. We can see how often a user did tasks they were assigned, and then adjust the tensor accordingly. Now, this tensor would be 24xnxm, where n and m are number of categories and number of stressed levels respectively. These two values will probably be in the realm of 5, so our tensor will have about 600 values in it. That will take a lot of training to figure out, as each day only gives a few data points. Perhaps trends can be inferred, and changes can be made to tensor positions that were never actually tested. For example if someone tends to do well in the morning regardless of task category, we can extend this probability to tasks that weren’t necessarily tested themselves.
