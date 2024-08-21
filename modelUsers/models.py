from django.contrib.auth.models import AbstractUser
from django.db import models

from courses.models import Course, Group


class CustomUser(AbstractUser):
    """Кастомная модель пользователя - студента."""

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=250,
        unique=True
    )
    balance = models.PositiveIntegerField(
        default=1000,
        verbose_name='Баланс (бонусы)',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-id',)

    def __str__(self):
        return self.get_full_name()

    def has_access_to_course(self, course):
        return Subscription.objects.filter(user=self, course=course).exists()


class Balance(models.Model):
    """Модель баланса пользователя."""

    user = models.OneToOneField(
        CustomUser,
        related_name='user_balance',
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    amount = models.PositiveIntegerField(
        default=1000,
        verbose_name='Баланс (бонусы)',
    )

    class Meta:
        verbose_name = 'Баланс'
        verbose_name_plural = 'Балансы'
        ordering = ('-id',)

class Subscription(models.Model):
    """Модель подписки пользователя на курс."""

    user = models.ForeignKey(
        CustomUser,
        related_name='subscriptions',
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    course = models.ForeignKey(
        Course,
        related_name='subscriptions',
        on_delete=models.CASCADE,
        verbose_name='Курс'
    )
    group = models.ForeignKey(
        Group,
        related_name='subscriptions',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Группа'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('-id',)

    def __str__(self):
        return f'{self.user} - {self.course}'