from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.serialize import ProfileSerializer
from goals.models import GoalCategory, Goal, GoalComment


class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        read_only_fields = ('id', 'user', 'created', 'updated', 'is_deleted')
        fields = '__all__'


class GoalCategorySerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        read_only_fields = ('id', 'user', 'created', 'updated')
        fields = '__all__'


class GoalCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    category = serializers.PrimaryKeyRelatedField(
        queryset=GoalCategory.objects.filter(is_deleted=False)
    )

    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created', 'updated')

    def validate_category(self, value):
        if value.is_deleted:
            raise ValidationError('not allowed category')
        if value.user != self.context['request'].user:
            raise ValidationError('not owner of category')
        return value


class GoalSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=GoalCategory.objects.filter(is_deleted=False)
    )

    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created', 'updated')

    def validate_category(self, value):
        if value.is_deleted:
            raise ValidationError('not allowed category')
        if value.user != self.context['request'].user:
            raise ValidationError('not owner of category')
        return value


class GoalCommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalComment
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created', 'updated')


class GoalCommentSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = GoalComment
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created', 'updated', 'goal')
