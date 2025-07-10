from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        abstract = True


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class SoftDeleteModel(TimeStampedModel):
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Deletado em")

    objects = models.Manager()
    active_objects = ActiveManager()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.is_active = False
        self.deleted_at = timezone.now()
        self.save(using=using)

    def hard_delete(self, using=None, keep_parents=False):
        super().delete(using=using, keep_parents=keep_parents)
