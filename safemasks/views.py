"""Views for the safemasks project
"""

from django.views.generic import TemplateView


class Index(TemplateView):
    template_name = "index.html"
