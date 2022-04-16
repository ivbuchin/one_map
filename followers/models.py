from django.conf import settings
from django.db import models


# Модель подписки
class Follow(models.Model):
    user_from = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rel_from_set'
    )
    user_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rel_to_set'
    )
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

        def __str__(self):
            return f"{self.user_from} follows {self.user_to}"
