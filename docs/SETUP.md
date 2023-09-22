# Task Scheduler Setup

I use Windows Task Scheduler, and below is my current setup:

## General

When running the task, use the following user account: (my `$env:USERNAME`)

- [x] Run whether user is logged on or not

### Triggers

| Trigger   | Details               | Status  |
| --------- | --------------------- | ------- |
| Daily     | At 12:00 AM every day | Enabled |
| At log on | At log on of any user | Enabled |

### Actions

| Action          | Program/script | Arguments    | Start in          |
| --------------- | -------------- | ------------ | ----------------- |
| Start a program | path\to\poetry | run counters | path\to\this\repo |

### Conditions

- [x] Start only if the following network connection is available: Any connection

### Settings

- [x] Allow task to be run on demand
- [x] Stop the task if it runs longer than: 1 hour
- [x] If the running task does not end when requested, force it to stop

If tha task is already running, then the following rule applies: Do not start a new instance
