from django.conf import settings


def pytest_configure():
    settings.configure(
        MIDDLEWARE_CLASSES=[],
        SECRET_KEY="mqprmJT9uyGvOqtFZZWpDQH2uGgamX83QpsyyvjhHcHqtZJKouNlhHX3Xf2lASPS",
        CACHES={
            "default": {
                "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
                "LOCATION": "unique-snowflake",
            }
        },
        DATABASES={
            "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": "db.sqlite"}
        },
        INSTALLED_APPS=[
            "wagtail.contrib.forms",
            "wagtail.contrib.redirects",
            "wagtail.embeds",
            "wagtail.sites",
            "wagtail.users",
            "wagtail.snippets",
            "wagtail.documents",
            "wagtail.images",
            "wagtail.search",
            "wagtail.admin",
            "wagtail.core",
            "wagtail.contrib.modeladmin",
            "modelcluster",
            "taggit",
            "django.contrib.admin",
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            "django.contrib.messages",
            "django.contrib.staticfiles",
            "wagtail_site_inheritance",
        ],
    )
