from apscheduler.triggers.cron import CronTrigger

tasks_trigger = {
    'content.based': CronTrigger(
        year="*", month="*", day="*", hour="*", minute="5", second="15"
    ),
    'item.based': CronTrigger(
        year="*", month="*", day="*", hour="*", minute="5", second="10"
    )
}


