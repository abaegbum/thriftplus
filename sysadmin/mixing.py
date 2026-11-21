


import os
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver


class FileCleanupMixin:
    """
    Mixin that ensures files are deleted from the filesystem
    when a model instance is updated or deleted.
    """

    @classmethod
    def setup_file_cleanup(cls):
        """Register signals for this model class."""

        @receiver(post_delete, sender=cls)
        def _delete_file_on_delete(sender, instance, **kwargs):
            for field in instance._meta.get_fields():
                if hasattr(field, "upload_to"):
                    file_field = getattr(instance, field.name)
                    if file_field and hasattr(file_field, "path") and os.path.isfile(file_field.path):
                        os.remove(file_field.path)

        @receiver(pre_save, sender=cls)
        def _delete_old_file_on_change(sender, instance, **kwargs):
            if not instance.pk:
                return
            try:
                old_instance = sender.objects.get(pk=instance.pk)
            except sender.DoesNotExist:
                return

            for field in instance._meta.get_fields():
                if hasattr(field, "upload_to"):
                    old_file = getattr(old_instance, field.name)
                    new_file = getattr(instance, field.name)
                    if old_file and old_file != new_file:
                        if hasattr(old_file, "path") and os.path.isfile(old_file.path):
                            os.remove(old_file.path)