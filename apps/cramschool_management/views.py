# views.py

from django.shortcuts import redirect, render
from .models import Info

def cramschool_list(request):
    info = Info.objects.all()
    return render(request, 'cramschool_list.html', {"Info": info})

# def update_address(request, school_id):
#     if request.method == 'POST':
#         new_address = request.POST.get('new_address')
#         if new_address:
#             school = Info.objects.get(id=school_id)
#             school.address = new_address
#             school.save()
#             return redirect('cramschool_list')
#     return redirect('cramschool_list')  # 如果提交的新地址为空，也重定向到列表页面
