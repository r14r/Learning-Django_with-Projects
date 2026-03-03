from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Job


class JobListView(ListView):
    template_name       = 'job_board/job_list.html'
    context_object_name = 'jobs'
    paginate_by         = 15

    def get_queryset(self):
        qs = Job.objects.filter(is_active=True).select_related('company')
        q  = self.request.GET.get('q')
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))
        loc = self.request.GET.get('location')
        if loc:
            qs = qs.filter(location__icontains=loc)
        return qs


class JobDetailView(DetailView):
    model         = Job
    template_name = 'job_board/job_detail.html'