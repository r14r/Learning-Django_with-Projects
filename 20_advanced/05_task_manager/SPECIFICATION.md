# Specification: Advanced Task Manager

**Level:** Advanced  
**Project:** 05_task_manager  
**Description:** Task manager with priorities, deadlines and filters

---

## 1. Overview

Build a full-featured task management application where users can create, assign and
track tasks with priorities, deadlines, labels and status transitions.

## 2. Goals

- Model tasks with a rich set of fields (priority, status, deadline, assignee)
- Implement filtering and sorting on the task list
- Build a Kanban-style status board
- Track task history/activity log

## 3. Functional Requirements

| # | Feature | Priority |
|---|---------|----------|
| 1 | Create, edit, delete tasks | Must |
| 2 | Priority levels: Low / Medium / High / Critical | Must |
| 3 | Status workflow: Todo → In Progress → Done | Must |
| 4 | Due date with overdue highlighting | Must |
| 5 | Assign task to a user | Must |
| 6 | Filter by status, priority, assignee | Should |
| 7 | Labels/tags on tasks | Should |
| 8 | Task comments/activity log | Should |
| 9 | Dashboard with task counts by status | Could |

## 4. Data Model

```
Label
├── id    : AutoField
├── name  : CharField(max_length=50)
├── color : CharField(max_length=7)  # hex colour
└── owner : ForeignKey(User)

Task
├── id          : AutoField
├── title       : CharField(max_length=200)
├── description : TextField(blank=True)
├── status      : CharField choices=[todo, in_progress, done]
├── priority    : CharField choices=[low, medium, high, critical]
├── due_date    : DateField(null=True, blank=True)
├── owner       : ForeignKey(User, related_name='owned_tasks')
├── assignee    : ForeignKey(User, null=True, related_name='assigned_tasks')
├── labels      : ManyToManyField(Label, blank=True)
└── created_at  : DateTimeField(auto_now_add=True)

Comment
├── id         : AutoField
├── task       : ForeignKey(Task)
├── author     : ForeignKey(User)
├── body       : TextField
└── created_at : DateTimeField(auto_now_add=True)
```

## 5. URL Structure

| URL | View | Name |
|-----|------|------|
| `/` | TaskListView (filterable) | `task_manager:list` |
| `/board/` | board_view (kanban) | `task_manager:board` |
| `/task/<pk>/` | TaskDetailView | `task_manager:detail` |
| `/task/create/` | TaskCreateView | `task_manager:create` |
| `/task/<pk>/edit/` | TaskUpdateView | `task_manager:update` |
| `/task/<pk>/delete/` | TaskDeleteView | `task_manager:delete` |
| `/task/<pk>/status/<status>/` | update_status | `task_manager:update-status` |

## 6. Acceptance Criteria

- [ ] Status transitions work via quick-action buttons on the list/board
- [ ] Overdue tasks highlighted in the UI
- [ ] Filtering by status, priority and assignee works
- [ ] Dashboard shows counts by status
- [ ] At least 10 tests pass
