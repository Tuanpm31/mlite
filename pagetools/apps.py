from django.apps import AppConfig


class PagetoolsConfig(AppConfig):
    name = 'pagetools'

    def ready(self):
        import pagetools.signals