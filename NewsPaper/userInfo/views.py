from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'userInfo/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_an_author'] = self.request.user.groups.filter(name='Author').exists()
        return context
