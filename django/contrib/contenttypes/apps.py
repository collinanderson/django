from django.apps import AppConfig
from django.contrib.contenttypes.checks import (
    check_generic_foreign_keys,
    check_model_name_lengths,
)
from django.core import checks
from django.db.models.signals import post_migrate, pre_migrate
from django.utils.translation import gettext_lazy as _


def lazy_inject_rename_contenttypes_operations(*args, **kwargs):
    from .management import inject_rename_contenttypes_operations

    return inject_rename_contenttypes_operations(*args, **kwargs)


def lazy_create_contenttypes(*args, **kwargs):
    from .management import create_contenttypes

    return create_contenttypes(*args, **kwargs)


class ContentTypesConfig(AppConfig):
    default_auto_field = "django.db.models.AutoField"
    name = "django.contrib.contenttypes"
    verbose_name = _("Content Types")

    def ready(self):
        pre_migrate.connect(lazy_inject_rename_contenttypes_operations, sender=self)
        post_migrate.connect(lazy_create_contenttypes)
        checks.register(check_generic_foreign_keys, checks.Tags.models)
        checks.register(check_model_name_lengths, checks.Tags.models)
