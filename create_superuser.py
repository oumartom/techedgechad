import os
import django

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "techEdgeWebSite.settings"
)

django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

user, created = User.objects.get_or_create(
    username=username,
    defaults={
        "email": email
    }
)

user.email = email
user.is_staff = True
user.is_superuser = True
user.set_password(password)
user.save()

if created:
    print("Superuser créé :", username)
else:
    print("Mot de passe superuser réinitialisé :", username)
