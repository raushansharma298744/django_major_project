from django.db import models
class Ticket(models.Model):
   
    title=models.CharField()
    description=models.TextField()
    priority=models.CharField()
    status=models.CharField()
    created_at=models.DateTimeField()
    updated_at=models.DateTimeField()
    def __str__(self):
        return self.title
