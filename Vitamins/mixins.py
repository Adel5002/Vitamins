from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator

class SuperuserRequiredMixin:
    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
