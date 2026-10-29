from django.apps import AppConfig


class DriverConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'driver'
    verbose_name = 'Водій'

    def ready(self):
        import driver.templatetags.custom_filters_signs  # Регистрируем фильтры