from django.db import models


class EventType(models.Model):
    EXPENSE = 'EX'
    INCOME = 'IN'
    CHANGE = 'CH'
    EVENT_TYPES = (
        (EXPENSE, 'Expense'),
        (INCOME, 'Income'),
        (CHANGE, 'Change')
    )
