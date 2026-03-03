# Specification: Job Board

**Level:** Advanced  
**Project:** 10_job_board  
**Description:** Post and search job listings with applications

---

## 1. Overview

Build a job board where companies can post vacancies and job seekers can
search, apply, and track their application status.

## 2. Goals

- Separate Company and JobSeeker roles with different dashboards
- Model jobs with location, salary range, type (full-time/part-time/remote)
- Allow applicants to attach a resume and cover letter
- Let employers accept or reject applications

## 3. Functional Requirements

| # | Feature | Priority |
|---|---------|----------|
| 1 | Post, edit, delete job listings (employers) | Must |
| 2 | Search jobs by keyword, location, type | Must |
| 3 | Apply to a job with resume + cover letter | Must |
| 4 | Employer dashboard: view applications | Must |
| 5 | Accept / reject applications | Must |
| 6 | Applicant dashboard: track applications | Should |
| 7 | Email notification on application status change | Could |

## 4. Data Model

```
Company
├── id      : AutoField
├── owner   : OneToOneField(User)
├── name    : CharField
├── website : URLField
├── logo    : ImageField
└── bio     : TextField

Job
├── id          : AutoField
├── company     : ForeignKey(Company)
├── title       : CharField
├── description : TextField
├── location    : CharField
├── job_type    : CharField choices=[full_time, part_time, remote, contract]
├── salary_min  : DecimalField(null=True)
├── salary_max  : DecimalField(null=True)
├── is_active   : BooleanField(default=True)
└── posted_at   : DateTimeField(auto_now_add=True)

Application
├── id           : AutoField
├── job          : ForeignKey(Job)
├── applicant    : ForeignKey(User)
├── cover_letter : TextField
├── resume       : FileField(upload_to='resumes/')
├── status       : CharField choices=[pending, accepted, rejected]
└── applied_at   : DateTimeField(auto_now_add=True)
```

## 5. URL Structure

| URL | View | Name |
|-----|------|------|
| `/` | JobListView | `job_board:list` |
| `/job/<pk>/` | JobDetailView | `job_board:detail` |
| `/job/create/` | JobCreateView | `job_board:create` |
| `/job/<pk>/apply/` | apply_view | `job_board:apply` |
| `/dashboard/` | EmployerDashboard | `job_board:employer-dashboard` |
| `/my-applications/` | ApplicantDashboard | `job_board:my-applications` |
| `/application/<pk>/status/<status>/` | update_status | `job_board:update-status` |

## 6. Acceptance Criteria

- [ ] Only active jobs appear in the public list
- [ ] Applicant cannot apply to the same job twice
- [ ] Employer can only manage their own jobs
- [ ] Resume upload stores files securely
- [ ] At least 10 tests pass
