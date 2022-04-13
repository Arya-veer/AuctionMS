from django.shortcuts import redirect
from .models import *

class SuperuserMixin:
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if self.request.user.is_superuser:
                return super().dispatch(request, *args, **kwargs)
        return redirect('login')