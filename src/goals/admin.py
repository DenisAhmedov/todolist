from django.contrib import admin

from goals.models import GoalCategory, Goal


@admin.register(GoalCategory)
class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'is_deleted')
    search_fields = ('title',)
    list_display_links = ('title',)
    list_filter = ('is_deleted',)
    readonly_fields = ('created', 'updated')


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'user', 'category', 'status', 'priority')
    search_fields = ('title',)
    list_display_links = ('title', 'description')
    list_filter = ('status', 'priority')
    readonly_fields = ('created', 'updated')

