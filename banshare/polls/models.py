from django.db import models

# Create your models here.
class Au_thor(models.Model):
    name = models.CharField(max_length=200)    
    def __str__(self):
        return self.name

class Com_pany(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Al_bum(models.Model):
    author = models.ForeignKey(Au_thor, on_delete=models.CASCADE, null=True)
    company = models.ForeignKey(Com_pany, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)    
    def __str__(self):
        return self.name
        
class So_ng(models.Model):
    album = models.ForeignKey(Al_bum, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

#from polls.models import Au_thor, Com_pany, Al_bum, So_ng
#a = Au_thor(name='lockdoor')
#c = Com_pany(name='grammy')
#b = Al_bum(name='hello', author=a, company=c)

