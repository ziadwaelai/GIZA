from django.db import models

class Simulator(models.Model):
    start_date = models.DateTimeField(help_text="Date and time when the DAG should start.")
    interval = models.CharField(
        max_length=50,
        choices=[
            ('secondly', 'Secondly'),
            ('minutely', 'Minutely'),
            ('hourly', 'Hourly'),
            ('daily', 'Daily'),
            ('weekly', 'Weekly'),
            ('monthly', 'Monthly'),

        ],
        help_text="Defines the schedule interval for the DAG."
    )
    kpi_id = models.IntegerField(help_text="ID of the KPI to be used.")

    def __str__(self):
        return f"Simulator {self.id}: Start {self.start_date}, Interval {self.interval}, KPI {self.kpi_id}"
