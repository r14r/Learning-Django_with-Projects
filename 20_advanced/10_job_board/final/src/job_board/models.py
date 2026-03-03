from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Company(models.Model):
    owner   = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company')
    name    = models.CharField(max_length=200)
    website = models.URLField(blank=True)
    logo    = models.ImageField(upload_to='logos/', blank=True)
    bio     = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Job(models.Model):
    JOB_TYPES = [
        ('full_time', 'Full Time'), ('part_time', 'Part Time'),
        ('remote', 'Remote'), ('contract', 'Contract'),
    ]
    company     = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='jobs')
    title       = models.CharField(max_length=200)
    description = models.TextField()
    location    = models.CharField(max_length=200)
    job_type    = models.CharField(max_length=20, choices=JOB_TYPES, default='full_time')
    salary_min  = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_max  = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_active   = models.BooleanField(default=True)
    posted_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-posted_at']

    def __str__(self):
        return f'{self.title} at {self.company.name}'

    def get_absolute_url(self):
        return reverse('job_board:detail', kwargs={'pk': self.pk})


class Application(models.Model):
    STATUS = [('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')]

    job          = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    cover_letter = models.TextField()
    resume       = models.FileField(upload_to='resumes/', blank=True)
    status       = models.CharField(max_length=10, choices=STATUS, default='pending')
    applied_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('job', 'applicant')
        ordering        = ['-applied_at']

    def __str__(self):
        return f'{self.applicant.username} → {self.job.title}'
