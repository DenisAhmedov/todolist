from django.contrib import admin

from goals.models import GoalCategory


@admin.register(GoalCategory)
class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'is_deleted')
    search_fields = ('title',)
    list_display_links = ('title',)
    list_filter = ('is_deleted',)
    readonly_fields = ('created', 'updated')

