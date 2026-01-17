from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    username = None                     # We remove username completely

    email = models.EmailField(
        _("email address"),
        unique=True,
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )

    # Minimal extra fields (you can add student_id later)
    full_name = models.CharField(_("full name"), max_length=150, blank=True)
    is_verified_student = models.BooleanField(_("verified student"), default=False)

    USERNAME_FIELD = "email"            # login with email
    REQUIRED_FIELDS = []                # no extra fields needed for createsuperuser

    def __str__(self):
        return self.email