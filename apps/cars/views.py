from django.http import HttpResponse
from django.db.models import Q
from django.views import generic
from . import models
from django.template.loader import render_to_string


class IndexView(generic.ListView):
    model = models.Car
    template_name = "cars/list.html"
    paginate_by = 10
    ordering = ['name']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["page"] = {
            "paginate_by": self.paginate_by,
        }

        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        keyword = self.request.GET.get('s', '')
        if keyword:
            filter_args = Q(name__icontains=keyword) | Q(color__name__icontains=keyword)
            # if keyword contains numbers
            num_search = [int(s) for s in keyword.split() if s.isnumeric()]
            if num_search:
                filter_args |= Q(length__in=num_search) | Q(weight__in=num_search) | Q(velocity__in=num_search)

            queryset = queryset.filter(filter_args)

        return queryset

    def get(self, request, *args, **kwargs):
        # download as xml
        if request.GET.get("download", None) is not None:
            return self.download_as_xml(self.get_queryset())

        return super().get(request, *args, **kwargs)

    @staticmethod
    def download_as_xml(cars):
        response = HttpResponse(content_type='application/xml')
        response['Content-Disposition'] = 'attachment; filename="cars.xml"'

        # Build XML data dynamically based on cars
        xml_data = render_to_string("cars/xml.html", {"cars": cars})

        response.write(xml_data)
        return response
