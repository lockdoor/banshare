from django.contrib import admin
from .models import Customers, Share_groups, Share_groups_customers

# Register your models here.
admin.site.register(Customers)
admin.site.register(Share_groups)
admin.site.register(Share_groups_customers)
