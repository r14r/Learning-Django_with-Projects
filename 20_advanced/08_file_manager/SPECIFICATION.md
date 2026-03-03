# Specification: File Upload Manager

**Level:** Advanced  
**Project:** 08_file_manager  
**Description:** Upload, organise and serve files securely

---

## 1. Overview

Build a secure file management application where authenticated users can upload
files, organise them into folders, and share or download them.

## 2. Goals

- Handle multi-file uploads with progress indication
- Organise files into nested folder structures
- Enforce per-user storage quotas
- Serve files securely via Django (not direct static URLs)

## 3. Functional Requirements

| # | Feature | Priority |
|---|---------|----------|
| 1 | Upload one or multiple files | Must |
| 2 | Create and navigate folders | Must |
| 3 | Download files via a protected view | Must |
| 4 | Delete files and folders | Must |
| 5 | File type validation (no executables) | Must |
| 6 | Show file size, upload date, MIME type | Should |
| 7 | Search by filename | Should |
| 8 | Share file with a time-limited public link | Could |

## 4. Data Model

```
Folder
├── id         : AutoField
├── name       : CharField(max_length=255)
├── owner      : ForeignKey(User)
├── parent     : ForeignKey('self', null=True, blank=True)
└── created_at : DateTimeField(auto_now_add=True)

UploadedFile
├── id         : AutoField
├── owner      : ForeignKey(User)
├── folder     : ForeignKey(Folder, null=True, blank=True)
├── original_name : CharField(max_length=255)
├── file       : FileField(upload_to=user_upload_path)
├── mime_type  : CharField(max_length=100)
├── size       : BigIntegerField
└── uploaded_at : DateTimeField(auto_now_add=True)
```

## 5. URL Structure

| URL | View | Name |
|-----|------|------|
| `/` | FileListView | `file_manager:list` |
| `/folder/<pk>/` | FolderView | `file_manager:folder` |
| `/upload/` | upload_view | `file_manager:upload` |
| `/download/<pk>/` | download_view | `file_manager:download` |
| `/delete/<pk>/` | delete_file | `file_manager:delete` |
| `/folder/create/` | FolderCreateView | `file_manager:folder-create` |

## 6. Acceptance Criteria

- [ ] Files saved to `media/uploads/<user_id>/`
- [ ] Download URL requires login and owner check
- [ ] File types validated (blocked: .exe, .bat, .sh, .php)
- [ ] At least 8 tests pass
