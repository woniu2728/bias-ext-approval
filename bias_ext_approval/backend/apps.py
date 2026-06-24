from django.apps import AppConfig

class ApprovalExtensionConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "bias_ext_approval.backend"
    label = "approval"
