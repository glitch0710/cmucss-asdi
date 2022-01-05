from django.db import models

class CustomerFeedback(models.Model):
    fullname = models.CharField(max_length=200, blank=True)
    customer_type = models.CharField(max_length=300, null=False)
    person_transacted = models.CharField(max_length=200, blank=True)
    rate1 = models.IntegerField(default=0)
    rate2 = models.IntegerField(default=0)
    rate3 = models.IntegerField(default=0)
    rate4 = models.IntegerField(default=0)
    comment = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.fullname
