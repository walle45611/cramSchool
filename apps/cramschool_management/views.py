# views.py

from django.shortcuts import redirect, render
from .models import Info
from django.core.paginator import Paginator


def cramschool_list(request):
    info_list = Info.objects.all()
    paginator = Paginator(info_list, 10)  # 每页显示 10 个对象
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'cramschool_list.html', {'page_obj': page_obj})

# def update_address(request, school_id):
#     if request.method == 'POST':
#         new_address = request.POST.get('new_address')
#         if new_address:
#             school = Info.objects.get(id=school_id)
#             school.address = new_address
#             school.save()
#             return redirect('cramschool_list')
#     return redirect('cramschool_list')  # 如果提交的新地址为空，也重定向到列表页面
