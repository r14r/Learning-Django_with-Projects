from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.urls import reverse_lazy
from .models import Company, Job, Application
from .forms import JobForm, ApplicationForm


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
        jtype = self.request.GET.get('type')
        if jtype:
            qs = qs.filter(job_type=jtype)
        return qs


class JobDetailView(DetailView):
    model         = Job
    template_name = 'job_board/job_detail.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            ctx['applied'] = Application.objects.filter(
                job=self.object, applicant=self.request.user
            ).exists()
        return ctx


class JobCreateView(LoginRequiredMixin, CreateView):
    model         = Job
    form_class    = JobForm
    template_name = 'job_board/job_form.html'
    success_url   = reverse_lazy('job_board:employer-dashboard')

    def form_valid(self, form):
        form.instance.company = self.request.user.company
        return super().form_valid(form)


@login_required
def apply_view(request, pk):
    job = get_object_or_404(Job, pk=pk, is_active=True)
    if Application.objects.filter(job=job, applicant=request.user).exists():
        return redirect('job_board:detail', pk=pk)
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            app           = form.save(commit=False)
            app.job       = job
            app.applicant = request.user
            app.save()
            return redirect('job_board:my-applications')
    else:
        form = ApplicationForm()
    return render(request, 'job_board/apply.html', {'job': job, 'form': form})


@login_required
def employer_dashboard(request):
    company = get_object_or_404(Company, owner=request.user)
    jobs    = company.jobs.prefetch_related('applications')
    return render(request, 'job_board/employer_dashboard.html', {'company': company, 'jobs': jobs})


@login_required
def applicant_dashboard(request):
    apps = Application.objects.filter(applicant=request.user).select_related('job__company')
    return render(request, 'job_board/my_applications.html', {'applications': apps})


@login_required
def update_status(request, pk, status):
    app = get_object_or_404(Application, pk=pk, job__company__owner=request.user)
    if status in dict(Application.STATUS):
        app.status = status
        app.save()
    return redirect('job_board:employer-dashboard')
