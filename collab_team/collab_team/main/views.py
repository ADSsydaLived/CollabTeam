from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaultfilters import title
from django.utils import translation

from .models import Project, Comment
from .translations import translations
from .forms import ProjectForm, UserRegisterForm, CommentForm


# Create your views here.
def home(request):
    return render(request, 'home.html')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES,
                           current_language=request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME, 'ru'))
        if form.is_valid():
            project = form.save(commit=False)
            project.author = request.user
            project.save()
            messages.success(request,
                             translations[request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME, 'ru')]['success_message'])
            return redirect('project_list')
    else:
        form = ProjectForm(current_language=request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME, 'ru'))

    # Определите текущий язык
    current_language = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME, 'ru')  # По умолчанию 'ru'

    # Получите переводы для текущего языка
    current_translations = translations.get(current_language, translations['ru'])  # По умолчанию 'ru'

    return render(request, 'create_project.html', {
        'form': form,
        'translations': current_translations,
    })


def logout_view(request):
    logout(request)
    return redirect('home')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт для {username} создан! Теперь вы можете войти в систему.')
            return redirect('login')  # Замените 'login' на фактический URL или имя URL
        else:
            # Вывод ошибок в консоль для отладки
            print(form.errors)
    else:
        form = UserRegisterForm()

    # Возвращаем форму с ошибками, если они есть
    return render(request, 'register.html', {'form': form})


def home(request):
    return render(request, 'home.html')


def set_language(request):
    if request.method == 'POST':
        user_language = request.POST.get('language')
        if user_language:  # Проверяем, что язык задан
            translation.activate(user_language)
            response = HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, user_language)
            messages.success(request, 'Язык успешно изменён!')
            return response
        else:
            messages.error(request, 'Выберите язык.')
    return redirect('/')


def get_translations(request):
    user_language = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME, 'ru')
    return translations.get(user_language, translations['ru'])


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'cover_image']
        labels = {
            'title': '',
            'description': '',
            'cover_image': ''
        }

    def __init__(self, *args, **kwargs):
        current_language = kwargs.pop('current_language', 'ru')
        super().__init__(*args, **kwargs)

        # Устанавливаем метки для каждого поля на основе текущего языка
        self.fields['title'].label = translations[current_language]['title_label']
        self.fields['description'].label = translations[current_language]['description_label']


@login_required
def project_list(request):
    query = request.GET.get('q')
    projects = Project.objects.all().order_by('-id')
    if query:
        # Фильтрация проектов по названию или описанию
        projects = projects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    paginator = Paginator(projects, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'project_list.html', {
        'page_obj': page_obj,
        'translations': get_translations(request),
        'query': query
    })

@login_required
def project_detail(request, project_id):
    project = Project.objects.get(id=project_id)
    comments = project.comments.all()
    transl = get_translations(request)  # Получаем переводы в зависимости от языка

    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.project = project
            comment.author = request.user
            comment.save()
            return redirect('project_detail', project_id=project.id)
    else:
        form = CommentForm()

    return render(request, 'project_detail.html', {
        'project': project,
        'comments': comments,
        'form': form,
        'translations': transl,  # Передаем переводы в шаблон
    })


def close_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if project.author == request.user:
        project.is_closed = True
        project.save()
        return JsonResponse({'status': 'success', 'message': 'Проект закрыт!'})
    else:
        return JsonResponse({'status': 'error', 'message': 'У вас нет прав для закрытия этого проекта.'}, status=403)


def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if project.author == request.user:
        project.delete()
        messages.success(request, "Проект успешно удалён!")
    else:
        messages.error(request, "У вас нет прав для удаления этого проекта.")

    return redirect('project_list')


def add_comment(request, project_id):
    global form
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('project_detail', project_id=project_id)
    return render(request, 'project_detail.html', {'form': form})
