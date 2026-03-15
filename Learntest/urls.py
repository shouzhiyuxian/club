"""Learntest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from app01 import views
from app01.srcs.views import myadmin, account, club, member, activity, registration, department, role, recruitment, member_portal

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index),
    
    # 登录相关
    path("login/", account.login),
    path("logout/", account.logout),
    
    # 管理员相关
    path("myadmin/list", myadmin.myadmin_list),
    path("myadmin/add", myadmin.myadmin_add),
    path("myadmin/<nid>/edit/", myadmin.myadmin_edit),
    path("myadmin/delete/", myadmin.myadmin_delete),
    path("myadmin/<nid>/reset/", myadmin.myadmin_reset_pwd),
    
    # 社团管理
    path("club/list", club.club_list),
    path("club/add", club.club_add),
    path("club/<int:nid>/edit/", club.club_edit),
    path("club/delete/", club.club_delete),
    path("club/transfer/", club.club_transfer),
    
    # 部门管理
    path("department/list", department.department_list),
    path("department/add", department.department_add),
    path("department/<int:nid>/edit/", department.department_edit),
    path("department/delete/", department.department_delete),
    
    # 角色管理
    path("role/list", role.role_list),
    path("role/add", role.role_add),
    path("role/<int:nid>/edit/", role.role_edit),
    path("role/delete/", role.role_delete),
    
    # 成员管理
    path("member/list", member.member_list),
    path("member/add", member.member_add),
    path("member/<nid>/edit/", member.member_edit),
    path("member/delete/", member.member_delete),
    path("member/<nid>/reset/", member.member_reset_pwd),
    
    # 活动管理
    path("activity/list", activity.activity_list),
    path("activity/add", activity.activity_add),
    path("activity/<int:nid>/edit/", activity.activity_edit),
    path("activity/<int:nid>/detail/", activity.activity_detail),
    path("activity/delete/", activity.activity_delete),
    
    # 活动报名管理
    path("registration/list", registration.registration_list),
    path("registration/add", registration.registration_add),
    path("registration/<int:nid>/edit/", registration.registration_edit),
    path("registration/delete/", registration.registration_delete),
    
    # 招新管理
    path("recruitment/list", recruitment.recruitment_list),
    path("recruitment/add", recruitment.recruitment_add),
    path("recruitment/<int:nid>/edit/", recruitment.recruitment_edit),
    path("recruitment/delete/", recruitment.recruitment_delete),
    path("recruitment/applications/", recruitment.application_list),
    path("recruitment/applications/add/", recruitment.application_add),
    path("recruitment/applications/<int:nid>/edit/", recruitment.application_edit),
    path("recruitment/applications/delete/", recruitment.application_delete),
    path("recruitment/applications/<int:nid>/approve/", recruitment.application_approve),
    # 成员端（普通成员/社长个人视角）
    path("member/profile/", member_portal.member_profile),
    path("member/change-password/", member_portal.member_change_password),
    path("member/my-registrations/", member_portal.my_registrations),
    path("member/activities/", member_portal.activities_can_register),
    path("member/activities/<int:activity_id>/register/", member_portal.do_register),
]
