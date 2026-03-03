from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Folder, UploadedFile


class FileListView(LoginRequiredMixin, ListView):
    model               = UploadedFile
    template_name       = 'file_manager/file_list.html'
    context_object_name = 'files'

    def get_queryset(self):
        return UploadedFile.objects.filter(owner=self.request.user, folder__isnull=True)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['folders'] = Folder.objects.filter(owner=self.request.user, parent__isnull=True)
        return ctx


@login_required
def upload_view(request):
    if request.method == 'POST':
        for f in request.FILES.getlist('files'):
            UploadedFile.objects.create(
                owner=request.user, original_name=f.name,
                file=f, mime_type=f.content_type, size=f.size,
            )
    return redirect('file_manager:list')