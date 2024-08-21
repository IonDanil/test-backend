from django.db.models.signals import post_save
from django.dispatch import receiver


from courses.models import Group
from modelUsers.models import Subscription


@receiver(post_save, sender=Subscription)
def post_save_subscription(sender, instance: Subscription, created, **kwargs):
    """
    Распределение нового студента в группу курса.
    Если создана новая подписка, распределяем студента в одну из существующих групп,
    либо создаем новую группу, если их меньше 10.
    """
    if created:
        groups = Group.objects.all()
        if groups.count() < 10:
            new_group = Group.objects.create(name=f'Group {groups.count() + 1}')
            instance.group = new_group
        else:
            instance.group = groups.order_by('?').first()
        instance.save()