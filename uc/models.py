from django.db import models

class underconstruction(models.Model):
    is_under_construction = models.BooleanField(default=True)
    uc_note = models.TextField(
        blank=True, null=True, help_text="Note to display on the under construction page"
    )
    uc_duration = models.DateTimeField(
        blank=True, null=True, help_text="Estimated duration of the under construction period"
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Under Construction : {self.is_under_construction} - Note: {self.uc_note} - Duration: {self.uc_duration} - Updated: {self.updated_at}"