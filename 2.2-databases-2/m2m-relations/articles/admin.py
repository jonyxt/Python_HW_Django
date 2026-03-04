from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError

from .models import Article, Tag, Scope


class ScopeInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        main_count = 0
        seen_tags = set()
        for form in self.forms:
            if form.cleaned_data.get('is_main'):
                main_count += 1
            if form.cleaned_data.get('DELETE', False):
                continue
            tag = form.cleaned_data.get('tag')
            if not tag:
                continue
            if tag in seen_tags:
                raise ValidationError("Нельзя добавлять один и тот же тег несколько раз для одной статьи.")
            seen_tags.add(tag)

        if main_count > 1:
            raise ValidationError('У одной статьи может быть только один главный тэг')

        if main_count == 0:
            raise ValidationError('У статьи должен быть главный тэг')


class ScopesInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormSet

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopesInline]

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass