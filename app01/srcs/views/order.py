# 注意：Order 模型已被移除，此文件已废弃
from django.shortcuts import render, redirect
from django import forms
from django.http import HttpResponse
# from app01.models import Order


def order_list(request):
    # Order 功能已移除
    return HttpResponse("此功能已移除", status=404)

