"""
Kurstop.uz — bitta faylda to'liq Django ilova
Ishlatish: python manage.py migrate && python manage.py shell -c "import kurstop_all; kurstop_all.seed()"
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'kurstop-change-me-in-production-2026')
DEBUG = os.environ.get('DEBUG', 'True').lower() in ('1', 'true', 'yes')
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')
if os.environ.get('RENDER_EXTERNAL_HOSTNAME'):
    ALLOWED_HOSTS.append(os.environ['RENDER_EXTERNAL_HOSTNAME'])

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'kurstop_all',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'kurstop_all'
WSGI_APPLICATION = 'kurstop_all.application'
LANGUAGE_CODE = 'uz'
TIME_ZONE = 'Asia/Tashkent'
USE_I18N = True
USE_TZ = True
STATIC_URL = '/static/'
STATIC_ROOT = str(BASE_DIR / 'staticfiles')
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

_db_url = os.environ.get('DATABASE_URL')
if _db_url:
    import dj_database_url
    DATABASES = {'default': dj_database_url.config(default=_db_url, conn_max_age=600)}
else:
    DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': str(BASE_DIR / 'db.sqlite3')}}

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [],
    'APP_DIRS': False,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ],
        'loaders': [],  # set below after template strings
    },
}]

# ── Templates ──
T_HOME = '''<!DOCTYPE html>
<html lang="uz"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Kurstop.uz</title><script src="https://cdn.tailwindcss.com"></script>
<script>tailwind.config={theme:{extend:{colors:{brand:{600:'#16a34a',700:'#15803d'}}}}}</script></head>
<body class="bg-slate-50 text-slate-800">
{% if messages %}{% for m in messages %}<div class="fixed top-4 right-4 bg-brand-600 text-white px-4 py-2 rounded-xl z-50 text-sm">{{ m }}</div>{% endfor %}{% endif %}
<header class="bg-white border-b sticky top-0 z-40"><div class="max-w-5xl mx-auto px-4 h-14 flex justify-between items-center">
<a href="/" class="font-black text-lg">Kurstop<span class="text-brand-600">.uz</span></a>
<nav class="flex gap-4 text-sm"><a href="/">Bosh</a><a href="/kurslar/">Kurslar</a></nav></div></header>
<section class="text-center py-14 px-4"><h1 class="text-4xl font-black mb-3">Bilimni <span class="text-brand-600">Kurstop.uz</span> bilan quring</h1>
<p class="text-slate-600 mb-6">Repetitor va onlayn kurslar bir joyda</p>
<a href="/kurslar/" class="bg-brand-600 text-white px-6 py-3 rounded-xl font-bold">Onlayn kurslar</a></section>
<section class="max-w-5xl mx-auto px-4 pb-12">
<h2 class="text-2xl font-extrabold mb-4">O'qituvchilar ({{ tutor_count }})</h2>
<form class="flex flex-wrap gap-2 mb-6" method="get">
<select name="subject" onchange="this.form.submit()" class="border rounded-lg p-2 text-sm"><option value="all">Fan</option>
{% for s in subjects %}<option value="{{ s.slug }}" {% if cur_s == s.slug %}selected{% endif %}>{{ s.name }}</option>{% endfor %}</select>
<select name="region" onchange="this.form.submit()" class="border rounded-lg p-2 text-sm"><option value="all">Hudud</option>
{% for r in regions %}<option value="{{ r.slug }}" {% if cur_r == r.slug %}selected{% endif %}>{{ r.name }}</option>{% endfor %}</select>
</form>
<div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
{% for t in tutors %}
<div class="bg-white border rounded-2xl p-4">
<div class="font-bold">{{ t.name }}</div>
<div class="text-xs mt-1"><span class="bg-green-50 text-brand-600 px-2 py-0.5 rounded">{{ t.subject.name }}</span>
<span class="bg-slate-100 px-2 py-0.5 rounded">{{ t.format }}</span></div>
<div class="text-xs text-slate-500 mt-2">{{ t.region.name }} · {{ t.experience_years }} yil · ★ {{ t.rating }}</div>
<div class="flex justify-between items-center mt-3">
<span class="font-black text-brand-600">{{ t.price }} so'm</span>
<form method="post" action="/booking/">{% csrf_token %}
<input type="hidden" name="tutor_id" value="{{ t.id }}">
<input type="hidden" name="student_name" value="Mehmon">
<input type="hidden" name="phone" value="+998900000000">
<input type="hidden" name="preferred_datetime" value="2026-12-01T10:00">
<button class="text-xs bg-brand-600 text-white px-3 py-1.5 rounded-lg">Yozilish</button>
</form></div></div>
{% empty %}<p class="text-slate-500">Ustoz yo'q — seed ishga tushiring</p>{% endfor %}
</div>
<div class="mt-12 bg-white border rounded-2xl p-6 max-w-md mx-auto">
<h3 class="font-bold mb-3">Bog'lanish</h3>
<form method="post" action="/contact/" class="space-y-2">{% csrf_token %}
<input name="name" required placeholder="Ism" class="w-full border rounded-lg p-2 text-sm">
<input name="phone" required placeholder="Telefon" class="w-full border rounded-lg p-2 text-sm">
<textarea name="message" required placeholder="Xabar" class="w-full border rounded-lg p-2 text-sm" rows="3"></textarea>
<button class="w-full bg-brand-600 text-white font-bold py-2 rounded-lg">Yuborish</button>
</form></div>
</section>
<footer class="text-center text-xs text-slate-400 py-6">&copy; 2026 Kurstop.uz</footer>
</body></html>'''

T_COURSES = '''<!DOCTYPE html>
<html lang="uz"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Kurslar</title><script src="https://cdn.tailwindcss.com"></script>
<script>tailwind.config={theme:{extend:{colors:{brand:{600:'#16a34a'}}}}}</script></head>
<body class="bg-slate-50"><header class="bg-white border-b"><div class="max-w-5xl mx-auto px-4 h-14 flex justify-between items-center">
<a href="/" class="font-black">Kurstop<span class="text-brand-600">.uz</span></a><a href="/" class="text-sm">← Orqaga</a></div></header>
<main class="max-w-5xl mx-auto px-4 py-8"><h1 class="text-2xl font-extrabold mb-6">Onlayn kurslar</h1>
<div class="grid sm:grid-cols-2 gap-4">
{% for c in courses %}
<a href="/kurslar/{{ c.slug }}/" class="bg-white border rounded-2xl p-5 hover:shadow-md block">
<div class="text-xs text-brand-600 font-semibold">{{ c.subject.name }}</div>
<div class="font-bold text-lg mt-1">{{ c.title }}</div>
<p class="text-sm text-slate-500 mt-1">{{ c.short_description }}</p>
<div class="font-black text-brand-600 mt-3">{{ c.price }} so'm</div></a>
{% empty %}<p>Kurs yo'q</p>{% endfor %}
</div></main></body></html>'''

T_DETAIL = '''<!DOCTYPE html>
<html lang="uz"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{{ course.title }}</title><script src="https://cdn.tailwindcss.com"></script>
<script>tailwind.config={theme:{extend:{colors:{brand:{600:'#16a34a'}}}}}</script></head>
<body class="bg-slate-50"><header class="bg-white border-b"><div class="max-w-5xl mx-auto px-4 h-14 flex justify-between items-center">
<a href="/kurslar/" class="text-sm">← Kurslar</a><span class="font-black">Kurstop<span class="text-brand-600">.uz</span></span></div></header>
{% if messages %}{% for m in messages %}<div class="max-w-5xl mx-auto px-4 pt-3"><div class="bg-brand-600 text-white px-4 py-2 rounded-xl text-sm">{{ m }}</div></div>{% endfor %}{% endif %}
<main class="max-w-5xl mx-auto px-4 py-8 grid md:grid-cols-3 gap-6">
<div class="md:col-span-2"><h1 class="text-3xl font-extrabold">{{ course.title }}</h1>
<p class="text-slate-600 mt-3">{{ course.description }}</p>
<h2 class="font-bold mt-6 mb-2">Darslar</h2>
{% for l in lessons %}<div class="bg-white border rounded-lg p-3 mb-2 text-sm">{{ l.order }}. {{ l.title }} ({{ l.duration_minutes }} daq)</div>{% endfor %}
</div>
<div class="bg-white border rounded-2xl p-5 h-fit">
<div class="text-2xl font-black text-brand-600 text-center">{{ course.price }} so'm</div>
<form method="post" action="/kurslar/{{ course.slug }}/xarid/" class="mt-4 space-y-2">{% csrf_token %}
<input name="name" required placeholder="Ism" class="w-full border rounded-lg p-2 text-sm">
<input name="phone" required placeholder="Telefon" class="w-full border rounded-lg p-2 text-sm">
<button class="w-full bg-brand-600 text-white font-bold py-2.5 rounded-xl">Xarid (demo)</button>
</form></div></main></body></html>'''

T_CABINET = '''<!DOCTYPE html>
<html lang="uz"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Kabinet</title><script src="https://cdn.tailwindcss.com"></script>
<script>tailwind.config={theme:{extend:{colors:{brand:{600:'#16a34a'}}}}}</script></head>
<body class="bg-slate-50"><header class="bg-white border-b"><div class="max-w-xl mx-auto px-4 h-14 flex justify-between items-center">
<a href="/" class="font-black">Kurstop<span class="text-brand-600">.uz</span></a></div></header>
<main class="max-w-xl mx-auto px-4 py-8">
<div class="bg-white border rounded-2xl p-5 mb-4"><h1 class="font-bold text-xl">{{ course_title }}</h1>
<div class="text-3xl font-black text-brand-600 mt-2">{{ percent }}%</div></div>
{% for p in progress %}
<div class="bg-white border rounded-xl p-3 mb-2 flex justify-between items-center text-sm">
<span>{% if p.done %}✓ {% endif %}{{ p.title }}</span>
{% if not p.done %}<form method="post" action="/kabinet/{{ eid }}/dars/{{ p.lid }}/">{% csrf_token %}
<button class="bg-brand-600 text-white text-xs px-2 py-1 rounded">Yakunlash</button></form>{% endif %}
</div>{% endfor %}
</main></body></html>'''

TEMPLATES[0]['OPTIONS']['loaders'] = [(
    'django.template.loaders.locmem.Loader',
    {'home.html': T_HOME, 'courses.html': T_COURSES, 'detail.html': T_DETAIL, 'cabinet.html': T_CABINET},
)]

# ── AppConfig so Django recognizes this module as an app ──
from django.apps import AppConfig

class KurstopConfig(AppConfig):
    name = 'kurstop_all'
    label = 'kurstop_all'
    verbose_name = 'Kurstop'

default_app_config = 'kurstop_all.KurstopConfig'

# ── Models ──
from django.db import models


class Region(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    def __str__(self): return self.name


class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    def __str__(self): return self.name


class Tutor(models.Model):
    name = models.CharField(max_length=150)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    format = models.CharField(max_length=20, default='Onlayn')
    experience_years = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField()
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=5.0)
    is_active = models.BooleanField(default=True)
    def __str__(self): return self.name


class Booking(models.Model):
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    student_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    preferred_datetime = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Course(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    price = models.PositiveIntegerField()
    is_published = models.BooleanField(default=True)
    def __str__(self): return self.title


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=1)
    duration_minutes = models.PositiveIntegerField(default=15)


class Order(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    guest_name = models.CharField(max_length=150)
    guest_phone = models.CharField(max_length=20)
    amount = models.PositiveIntegerField()
    status = models.CharField(max_length=20, default='paid')
    created_at = models.DateTimeField(auto_now_add=True)


class Enrollment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    guest_phone = models.CharField(max_length=20)
    progress_percent = models.PositiveIntegerField(default=0)
    enrolled_at = models.DateTimeField(auto_now_add=True)


class LessonProgress(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)


# ── Views ──
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.urls import path
from django.contrib import admin
from datetime import datetime


def home(request):
    qs = Tutor.objects.filter(is_active=True).select_related('subject', 'region')
    cs, cr = request.GET.get('subject', 'all'), request.GET.get('region', 'all')
    if cs != 'all': qs = qs.filter(subject__slug=cs)
    if cr != 'all': qs = qs.filter(region__slug=cr)
    return render(request, 'home.html', {
        'tutors': qs, 'tutor_count': qs.count(),
        'subjects': Subject.objects.all(), 'regions': Region.objects.all(),
        'cur_s': cs, 'cur_r': cr,
    })


@require_POST
def booking(request):
    tid = request.POST.get('tutor_id')
    if tid:
        t = get_object_or_404(Tutor, pk=tid)
        pref = request.POST.get('preferred_datetime', '')
        try: dt = datetime.fromisoformat(pref)
        except Exception: dt = timezone.now()
        Booking.objects.create(
            tutor=t,
            student_name=request.POST.get('student_name', 'Mehmon'),
            phone=request.POST.get('phone', ''),
            preferred_datetime=dt,
        )
        messages.success(request, 'Yozilish qabul qilindi!')
    return redirect('/')


@require_POST
def contact(request):
    ContactMessage.objects.create(
        name=request.POST.get('name', ''),
        phone=request.POST.get('phone', ''),
        message=request.POST.get('message', ''),
    )
    messages.success(request, 'Xabar yuborildi!')
    return redirect('/')


def courses(request):
    return render(request, 'courses.html', {
        'courses': Course.objects.filter(is_published=True).select_related('subject'),
    })


def course_detail(request, slug):
    c = get_object_or_404(Course, slug=slug)
    return render(request, 'detail.html', {'course': c, 'lessons': c.lessons.order_by('order')})


@require_POST
def purchase(request, slug):
    c = get_object_or_404(Course, slug=slug)
    name = request.POST.get('name', '').strip()
    phone = request.POST.get('phone', '').strip()
    if not name or not phone:
        messages.error(request, 'Ism va telefon majburiy')
        return redirect(f'/kurslar/{slug}/')
    order = Order.objects.create(course=c, guest_name=name, guest_phone=phone, amount=c.price)
    enr = Enrollment.objects.create(course=c, order=order, guest_phone=phone)
    for les in c.lessons.all():
        LessonProgress.objects.create(enrollment=enr, lesson=les)
    messages.success(request, 'Kurs xarid qilindi!')
    return redirect(f'/kabinet/{enr.id}/')


def cabinet(request, eid):
    enr = get_object_or_404(Enrollment, pk=eid)
    items = []
    for p in enr.progress.select_related('lesson').order_by('lesson__order'):
        items.append({'title': p.lesson.title, 'lid': p.lesson_id, 'done': p.is_completed})
    done = sum(1 for i in items if i['done'])
    total = len(items) or 1
    return render(request, 'cabinet.html', {
        'course_title': enr.course.title, 'percent': int(done / total * 100),
        'progress': items, 'eid': eid,
    })


@require_POST
def mark_done(request, eid, lid):
    enr = get_object_or_404(Enrollment, pk=eid)
    LessonProgress.objects.filter(enrollment=enr, lesson_id=lid).update(is_completed=True)
    messages.success(request, 'Dars yakunlandi!')
    return redirect(f'/kabinet/{eid}/')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('booking/', booking),
    path('contact/', contact),
    path('kurslar/', courses),
    path('kurslar/<slug:slug>/', course_detail),
    path('kurslar/<slug:slug>/xarid/', purchase),
    path('kabinet/<int:eid>/', cabinet),
    path('kabinet/<int:eid>/dars/<int:lid>/', mark_done),
]

for _m in [Region, Subject, Tutor, Booking, ContactMessage, Course, Lesson, Order, Enrollment, LessonProgress]:
    try:
        admin.site.register(_m)
    except Exception:
        pass

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application


def seed():
    from django.utils.text import slugify
    for n in ['Toshkent', "Farg'ona", 'Samarqand', 'Andijon', 'Namangan', 'Buxoro']:
        Region.objects.get_or_create(name=n, defaults={'slug': slugify(n)})
    for n in ['Matematika', 'Ingliz tili', 'Fizika', 'Dasturlash', 'Kimyo']:
        Subject.objects.get_or_create(name=n, defaults={'slug': slugify(n)})
    data = [
        ('Anvar Karimov', 'Matematika', 'Toshkent', 'Onlayn', 7, 80000, 4.9),
        ('Malika Ahmedova', 'Ingliz tili', "Farg'ona", 'Onlayn', 5, 70000, 5.0),
        ('Sardor Salimov', 'Dasturlash', 'Toshkent', 'Onlayn', 6, 120000, 4.9),
        ('Jahongir Tursunov', 'Fizika', 'Samarqand', 'Oflayn', 10, 90000, 4.8),
    ]
    for name, sub, reg, fmt, exp, price, rat in data:
        Tutor.objects.get_or_create(name=name, defaults={
            'subject': Subject.objects.get(name=sub),
            'region': Region.objects.get(name=reg),
            'format': fmt, 'experience_years': exp, 'price': price, 'rating': rat,
        })
    if not Course.objects.filter(slug='python-asoslari').exists():
        c = Course.objects.create(
            title='Python asoslari', slug='python-asoslari',
            subject=Subject.objects.get(name='Dasturlash'),
            description='Python noldan amaliy kurs.', short_description='6 haftalik Python',
            price=450000, is_published=True,
        )
        for i, t in enumerate(['Kirish', 'O\'zgaruvchilar', 'Funksiyalar', 'Loyiha'], 1):
            Lesson.objects.create(course=c, title=t, order=i, duration_minutes=20)
    if not Course.objects.filter(slug='ielts-speaking').exists():
        c = Course.objects.create(
            title='IELTS Speaking 7.0+', slug='ielts-speaking',
            subject=Subject.objects.get(name='Ingliz tili'),
            description='Speaking strategiyalari.', short_description='IELTS Speaking',
            price=380000, is_published=True,
        )
        for i, t in enumerate(['Part 1', 'Part 2', 'Part 3'], 1):
            Lesson.objects.create(course=c, title=t, order=i, duration_minutes=25)
    print('SEED OK:', Tutor.objects.count(), 'tutors,', Course.objects.count(), 'courses')
