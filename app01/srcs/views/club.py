from django.shortcuts import render, redirect
from app01.models import Club
from app01.utils.page_nav import PageNav
from app01.srcs.forms.form import ClubModelForm


def club_list(req):
    """社团列表"""
    search_data_dict = {}
    search_data = req.GET.get("q", "")
    
    if search_data:
        search_data_dict["name__contains"] = search_data
    
    queryset = Club.objects.filter(**search_data_dict).order_by("-create_time")
    page_nav_obj = PageNav(req, queryset)
    page_queryset = page_nav_obj.page_queryset
    page_nav_string = page_nav_obj.get_html()
    
    content = {
        "queryset": page_queryset,
        "page_nav_string": page_nav_string,
        "search_data": search_data,
    }
    return render(req, "club/club_list.html", content)


def club_add(req):
    """添加社团"""
    if req.method == "GET":
        form = ClubModelForm()
        return render(req, "club/club_add.html", {"form": form})
    else:
        form = ClubModelForm(data=req.POST)
        if form.is_valid():
            form.save()
            return redirect("/club/list")
        else:
            return render(req, "club/club_add.html", {"form": form})


def club_delete(req):
    """删除社团"""
    nid = req.GET.get("nid")
    Club.objects.filter(club_id=nid).delete()
    return redirect("/club/list")


def club_edit(req, nid):
    """编辑社团"""
    row_obj = Club.objects.filter(club_id=nid).first()
    if req.method == "GET":
        form = ClubModelForm(instance=row_obj)
        return render(req, "club/club_edit.html", {"form": form})
    
    form = ClubModelForm(data=req.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect("/club/list")
    return render(req, "club/club_edit.html", {"form": form})

