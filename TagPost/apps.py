from django.apps import AppConfig


class TagpostConfig(AppConfig):
    name = 'TagPost'
    def ready(self):
        import TagPost.signals