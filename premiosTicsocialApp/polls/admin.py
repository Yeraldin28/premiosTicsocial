from django.contrib import admin
from .models import Question, Choice
 
class ChoiceInline(admin.StackedInline):
        model = Choice
        extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fields = ["pub_data", "question_text"]
    inlines = [ChoiceInline]
    list_display = ("question_text", "pub_data")
  #  list_filter = []
    search_fields = ["question_text"]
    
    
admin.site.register(Question, QuestionAdmin)
    
