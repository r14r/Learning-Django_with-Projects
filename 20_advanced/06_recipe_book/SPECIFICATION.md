# Specification: Recipe Book

**Level:** Advanced  
**Project:** 06_recipe_book  
**Description:** Recipe website with ingredients and categories

---

## 1. Overview

Build a recipe-sharing website where users can publish recipes with ingredients,
step-by-step instructions, preparation times, and category tags.

## 2. Goals

- Model recipes with many ingredients, a preparation workflow and rich content
- Build a search-and-filter recipe browser
- Allow authenticated users to save favourite recipes
- Calculate nutrition totals from per-ingredient data

## 3. Functional Requirements

| # | Feature | Priority |
|---|---------|----------|
| 1 | Browse recipes (list, search, category filter) | Must |
| 2 | Recipe detail: ingredients, steps, times, servings | Must |
| 3 | Create / edit / delete own recipes | Must |
| 4 | Upload recipe photo | Must |
| 5 | Ingredient list with quantities and units | Must |
| 6 | Category/cuisine tags | Should |
| 7 | Save favourites | Should |
| 8 | Rating and reviews | Could |

## 4. Data Model

```
Category
├── id   : AutoField
├── name : CharField(max_length=100, unique=True)
└── slug : SlugField(unique=True)

Recipe
├── id           : AutoField
├── title        : CharField(max_length=200)
├── slug         : SlugField(unique=True)
├── author       : ForeignKey(User)
├── categories   : ManyToManyField(Category)
├── description  : TextField
├── image        : ImageField(upload_to='recipes/')
├── prep_time    : PositiveIntegerField (minutes)
├── cook_time    : PositiveIntegerField (minutes)
├── servings     : PositiveIntegerField
├── instructions : TextField
├── published    : BooleanField(default=False)
└── created_at   : DateTimeField(auto_now_add=True)

Ingredient
├── id         : AutoField
├── recipe     : ForeignKey(Recipe, related_name='ingredients')
├── name       : CharField(max_length=100)
├── quantity   : DecimalField
├── unit       : CharField(max_length=50)
└── order      : PositiveIntegerField
```

## 5. URL Structure

| URL | View | Name |
|-----|------|------|
| `/` | RecipeListView | `recipe_book:list` |
| `/category/<slug>/` | RecipeListView | `recipe_book:category` |
| `/recipe/<slug>/` | RecipeDetailView | `recipe_book:detail` |
| `/recipe/create/` | RecipeCreateView | `recipe_book:create` |
| `/recipe/<slug>/edit/` | RecipeUpdateView | `recipe_book:update` |
| `/recipe/<slug>/delete/` | RecipeDeleteView | `recipe_book:delete` |
| `/my-recipes/` | MyRecipesView | `recipe_book:my-recipes` |

## 6. Acceptance Criteria

- [ ] Ingredient formset validates quantities and units
- [ ] Only published recipes appear in the public list
- [ ] Search by title or ingredient name works
- [ ] Author can toggle publish status
- [ ] At least 10 tests pass
