from django.db import models


# Create your models here.
class User(models.Model):
    def _str__(self):
        return self.username

    username = models.CharField(max_length=100)
    password = models.TextField()
    created_time = models.TimeField(auto_now_add=True)
    email = models.EmailField(max_length=225, null=True)
    has_confirmed = models.BooleanField(default=False)


class ConfirmString(models.Model):
    code = models.CharField(max_length=256)
    user = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + ":" + self.code

    class Meta:
        ordering = ['-c_time']
        verbose_name = "ConfirmationCode"
        verbose_name_plural = "ConfirmationCodes"
