# otf-event-service

# Task Manager
## Overview

The **__Task Manager__**effectively polls for scheduled tasks to be handled. Every task is scheduled by a
separate entity. It reads a timestream of scheduled tasks and when the datetime is for a tasks has passed
and is in the ready state, the manager will start micro tasks. These **__MicroTasks__** are essentially short lived
cron jobs (coroutines) that run every so often.

## Example
Say for example we want to keep track of the box score for a basketball game.
There is a daily cronjob that will check the game schedules for the day. It will send all the game schedules to
the database. The Task Manager will check the database every minute to see if any new tasks have been scheduled for
processing.

Once a game has started, the manager will find the task associated with that game and create a MircoTask to keep
track of the boxscores as the game is live. The Task Manager will start a new MicroTask coroutine with a TaskID and
enter the task as **Started** in the database.

The MicroTask will then poll for the game information every 10 minutes until the game is over.

## MicroTasks
These micro tasks are ran when the Task Manager finds a task in the database that is ready to run.
You can think of these as workers.
Once this process starts, the database adds a new row to make it known that the task has started.
This change in state allows the Task Manager to know not to try to run it again.
Each MicroTask is a cron job and is timed to run periodically. This frees the Task Manger up for
scheduling purposes.

Each MicroTask is assigned a TaskID to keep track of what scheduled main task it belongs to. As
it polls for information, it will create its own events. These events are what are sent out to
other services for processing. A MicroTaskID and the main TaskID are both attached to these events.
The MicroTaskID is for the MicroTask that handles the events and the main TaskID every new event
sent out.

## How Orchestration works
The Task Manager is only responsible for checked scheduled tasks and creating MicroTasks.
There can be multiple instances of the manager running at once, but since it relies on a consistent
timestream data store there will never be duplicates of tasks running.

A MicroTask is created in the sense that a new subprocess should start spitting out new events to
outside services. However, the instances of MicroTasks are always running. They subscribe to a
queue and wait patiently for a message to come in from the Task Manager. When a message comes in,
it will create a coroutine for it and run it periodically. The MicroTask will then end itself once
it has completed its mission.

The two services share the same databases. There are only two databases. One is for all task related
events that have occurred in the system. The other is for information related to how a task is structured.
Why two databases?

## No SQL database and Timestreams
### No SQL
The two databases are to help separate concerns. The No SQL database is for information that will rarely change, and is
directly related to the structure of a task. Let us consider that for every task there will potentially be a task type
that is either defined by us or the user.
For exmaple, if we want to keep track of period scores for a game, that will be its own task type. We can call it
'GAME_PERIOD_SCORE_TASK'. This task needs to be associated with the http url to poll and the number of seconds wed want
to poll this. Since this would be considered mutable, it doesn't fit the use case of a time stream. However, this data
will rarely change unless the polling needs to be increased or decreased. This Task can also be soft deleted.
This allows us to slowly structure how a task is made and processed.

### Timestream
The timestream database is only for tracking the state of tasks. A task can be in multiple states as it traverses all the
backend services. It could be in a **READY** state when we schedule for it. It could be in a **STARTED** state as multiple
services work on the task. It could also either be in a **FINISHED** or **FAILED** state depending on the circumstances of
the processing. The Photo Service could fail, but the Caption service might succeed in creating a caption. All these states
must be considered as a task is worked on. If an outside service needs to update the state of a task, it will always go through
the Task Manager. MicroTasks only worry about making tasks. The Manager will take into account if a task is successful based on
the incoming progress of other services.

 

```mermaid
flowchart TD
    CronJob1[Sports Api Daily Schedules Job] --> |Polls Sports Api Daily for game schedules| TaskData[(Tasks)]
    TaskManager{Task Manager} <--> |Starts tasks when datetime is reached| TaskData
    TaskManager <--> |Sends tasks for processing and gets event states back| Services((Other Services))
    subgraph MicroTasks
    TaskManager --> |starts up tasks to poll apis for events| MicroTask1[MicroTask]
    TaskManager --> MicroTask2[MicroTask]
    TaskManager --> MicroTask3[MicroTask]
    end
    MicroTask1 --> |writes more tasks if found| TaskData
    MicroTask2 --> |writes more tasks if found| TaskData
    MicroTask3 --> |writes more tasks if found| TaskData
```