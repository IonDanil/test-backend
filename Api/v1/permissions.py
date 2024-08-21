from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import BasePermission, SAFE_METHODS

from courses.models import Course, Group
from modelUsers.models import Subscription


def make_payment(request, course_id):
    user = request.user

    try:
        course = Course.objects.get(id=course_id, is_available=True)
    except Course.DoesNotExist:
        return Response({'detail': 'Курс не доступен или не существует.'}, status=status.HTTP_404_NOT_FOUND)

    if user.balance < course.price:
        return Response({'detail': 'Недостаточно бонусов.'}, status=status.HTTP_400_BAD_REQUEST)

    # Списываем бонусы
    user.balance -= course.price
    user.save()

    # Создаем подписку на курс
    group = Group.objects.order_by('?').first()  # Случайное распределение в одну из 10 групп
    Subscription.objects.create(user=user, course=course, group=group)

    return Response({'detail': 'Оплата прошла успешно, доступ к курсу открыт.'}, status=status.HTTP_200_OK)


class IsStudentOrIsAdmin(BasePermission):
    """
    Разрешает доступ админам и студентам, если они имеют доступ к объекту.
    """

    def has_permission(self, request, view):
        return request.user.is_staff or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Проверяем, является ли пользователь админом или студентом с доступом к курсу
        return request.user.is_staff or obj.subscriptions.filter(user=request.user).exists()

class ReadOnlyOrIsAdmin(BasePermission):
    """
    Разрешает только чтение для студентов и полный доступ для админов.
    """

    def has_permission(self, request, view):
        return request.user.is_staff or request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.method in SAFE_METHODS