from rest_framework import serializers
from posts.models import Comment, Post, Follow, Group


class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.username", read_only=True)
    group = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(),
        allow_null=True,
        required=False,
    )

    class Meta:
        model = Post
        fields = ["id", "author", "text", "pub_date", "image", "group"]
        read_only_fields = ["id", "pub_date", "author"]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username"
    )

    class Meta:
        model = Comment
        fields = ["id", "author", "post", "text", "created"]
        read_only_fields = ["author", "post"]


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "title", "slug", "description"]


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.CharField(
        source="user.username",
        read_only=True
    )
    following = serializers.CharField(
        source="following.username",
        read_only=True
    )

    class Meta:
        model = Follow
        fields = ["user", "following"]

    def validate_following(self, value):
        """
        Проверяем, что пользователь не может подписаться на самого себя.
        """
        if self.context["request"].user == value:
            raise serializers.ValidationError(
                "Вы не можете подписаться на себя."
            )
        return value
