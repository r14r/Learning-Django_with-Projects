import os
from django.views.generic import ListView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse, Http404
from django.urls import reverse_lazy
from .models import Folder, UploadedFile

BLOCKED_EXTENSIONS = {'.exe', '.bat', '.sh', '.php', '.ps1', '.vbs'}


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


class FolderView(LoginRequiredMixin, ListView):
    template_name       = 'file_manager/file_list.html'
    context_object_name = 'files'

    def get_queryset(self):
        folder = get_object_or_404(Folder, pk=self.kwargs['pk'], owner=self.request.user)
        self.folder = folder
        return UploadedFile.objects.filter(owner=self.request.user, folder=folder)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['folders']        = Folder.objects.filter(owner=self.request.user, parent=self.folder)
        ctx['current_folder'] = self.folder
        return ctx


class FolderCreateView(LoginRequiredMixin, CreateView):
    model         = Folder
    fields        = ['name', 'parent']
    template_name = 'file_manager/folder_form.html'
    success_url   = reverse_lazy('file_manager:list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


@login_required
def upload_view(request):
    if request.method == 'POST':
        folder_pk = request.POST.get('folder')
        folder    = None
        if folder_pk:
            folder = get_object_or_404(Folder, pk=folder_pk, owner=request.user)
        for f in request.FILES.getlist('files'):
            ext = os.path.splitext(f.name)[1].lower()
            if ext not in BLOCKED_EXTENSIONS:
                UploadedFile.objects.create(
                    owner=request.user, folder=folder,
                    original_name=f.name, file=f,
                    mime_type=f.content_type, size=f.size,
                )
    return redirect('file_manager:list')


@login_required
def download_view(request, pk):
    uf = get_object_or_404(UploadedFile, pk=pk, owner=request.user)
    try:
        return FileResponse(
            open(uf.file.path, 'rb'), as_attachment=True, filename=uf.original_name
        )
    except FileNotFoundError:
        raise Http404


@login_required
def delete_file(request, pk):
    uf = get_object_or_404(UploadedFile, pk=pk, owner=request.user)
    if request.method == 'POST':
        uf.file.delete(save=False)
        uf.delete()
    return redirect('file_manager:list')