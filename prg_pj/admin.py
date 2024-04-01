from django.contrib import admin

# Register your models here.
from .models import Question    # .앞에 붙으면 같은 경로에 있는 폴더
from .models import Choice    # .앞에 붙으면 같은 경로에 있는 폴더

admin.site.register(Question)
admin.site.register(Choice)