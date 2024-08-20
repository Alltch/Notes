from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    image = models.ImageField(
        upload_to='users_images/',
        null=True,
        blank=True,
        verbose_name="Изображение",
        help_text="Изображение пользователя."
    )
    bio = models.TextField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="Биография",
        help_text="Краткая информация о пользователе."
    )

    def __str__(self):
        return self.username


class FriendRequest(models.Model):
    from_user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='sent_requests')
    to_user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='received_requests')
    is_confirmed = models.BooleanField(default=False)
    # Новый флаг для управления активностью запроса
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def accept(self):
        """Подтверждение запроса на добавление в друзья."""
        self.is_confirmed = True
        self.is_active = False
        self.save()

        # Добавление в список друзей
        Friend.objects.create(user=self.from_user, friend=self.to_user)
        Friend.objects.create(user=self.to_user, friend=self.from_user)

    def reject(self):
        """Отклонение запроса на добавление в друзья."""
        self.is_active = False
        self.save()

    def cancel(self):
        """Отмена запроса пользователем."""
        self.delete()

    def __str__(self):
        return f"Request from {self.from_user.username} to {self.to_user.username}"

    class Meta:
        verbose_name_plural = 'Friend Requests'
        verbose_name = 'Friend Request'
        # уникальность запроса между двумя пользователями
        unique_together = ('from_user', 'to_user')
        ordering = ['-created_at']


class Friend(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='friends')
    friend = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='friends_of')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} is friends with {self.friend.username}"

    class Meta:
        verbose_name_plural = 'Friends'
        verbose_name = 'Friend'
        # ensures each friendship is unique
        unique_together = ('user', 'friend')
        ordering = ['-created_at']


class Note(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField(max_length=800)
    is_private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Notes'
        verbose_name = 'Note'
        ordering = ['-created_at']
