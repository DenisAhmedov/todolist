from django.urls import path

from goals.views import GoalCategoryCreateView, GoalCategoryListView, GoalCategoryView, GoalView, GoalListView, \
    GoalCreateView, GoalCommentCreateView, GoalCommentListView, GoalCommentView, BoardCreateView, BoardView, \
    BoardListView

urlpatterns = [
    path('goal_category/create', GoalCategoryCreateView.as_view(), name='create-category'),
    path('goal_category/list', GoalCategoryListView.as_view(), name='category-list'),
    path('goal_category/<pk>', GoalCategoryView.as_view(), name='category-detail'),

    path('goal/create', GoalCreateView.as_view(), name='create-goal'),
    path('goal/list', GoalListView.as_view(), name='goal-list'),
    path('goal/<pk>', GoalView.as_view(), name='goal-detail'),

    path('goal_comment/create', GoalCommentCreateView.as_view(), name='create-comment'),
    path('goal_comment/list', GoalCommentListView.as_view(), name='comment-list'),
    path('goal_comment/<pk>', GoalCommentView.as_view(), name='comment-detail'),

    path('board/create', BoardCreateView.as_view(), name='create-board'),
    path('board/list', BoardListView.as_view(), name='board-list'),
    path('board/<pk>', BoardView.as_view(), name='board-detail'),
]
