"""
URL configuration for cms_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

from rest_framework.routers import DefaultRouter
from core.views import ProgramViewSet, TopicViewSet, TermViewSet, LessonViewSet
from core.catalog_views import list_catalog_programs, get_catalog_program, get_catalog_lesson

router = DefaultRouter()
router.register(r'programs', ProgramViewSet)
router.register(r'topics', TopicViewSet)
router.register(r'terms', TermViewSet)
router.register(r'lessons', LessonViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('catalog/programs/', list_catalog_programs, name='catalog-programs'),
    path('catalog/programs/<uuid:id>/', get_catalog_program, name='catalog-program-detail'),
    path('catalog/lessons/<uuid:id>/', get_catalog_lesson, name='catalog-lesson-detail'),
]

