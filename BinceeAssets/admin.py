from django.contrib import admin

# Register your models here.
from BinceeAssets.models import *
from user.models import *


admin.site.register(BinceeEntities)
admin.site.register(RealTimeLocationData)

admin.site.register(User)
admin.site.register(Role)

