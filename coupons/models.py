from django.db import models

class Coupon(models.Model):
    code = models.CharField(verbose_name='Coupon code', null=False, blank=False, max_length=20)
    description = models.TextField(verbose_name='Description', null=True, blank=True, max_length=200)
    discount = models.IntegerField(verbose_name='Discount', null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)


class EmailUsed(models.Model):
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    email = models.EmailField()

    class Meta:
        unique_together = ('coupon', 'email')
        
class MailchimpEmails(models.Model):
    id= models.AutoField(verbose_name="Customer ID", auto_created=True, primary_key=True)
    name = models.CharField(verbose_name='Customer Name', null=False, blank=False, max_length=99)
    email = models.CharField(verbose_name='Customer Email', null=False, blank=False, max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
