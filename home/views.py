from django.views.generic import TemplateView
from django.views.generic import DetailView
from django.http import HttpResponseForbidden
from django.views.generic.edit import FormMixin
from home.forms import ProfileSport
from django.shortcuts import render
from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied

class IsUserAciveMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_active:
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied('Permission denied') 


class Profile(IsUserAciveMixin, TemplateView):
    template_name = 'account/profile.html'

    def get(self, request, *args, **kwargs):
        form = ProfileSport(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = ProfileSport(instance=request.user, 
                            data=request.POST, 
                            files=request.FILES)
        if form.is_valid():
            form.save()
        return render(request, self.template_name, {'form': form})

        