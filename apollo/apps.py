from django.apps import AppConfig


class ApolloConfig(AppConfig):
    name = 'apollo'
    def ready(self):
        import apollo.signals