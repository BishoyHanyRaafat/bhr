from django.shortcuts import render
from .models import Point,Voucher
import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import qrcode
from PIL import Image
import os
from io import BytesIO
import base64
from django.contrib.auth.decorators import user_passes_test

def user_is_admin(user):
    return user.is_superuser
# Create your views here.

# 300 -> 20$
# 600 -> 50$
# 950 -> 100$
# 1500 -> 150$
points_to_vouchers = {300 : 20,
                        600 : 50,
                        950 : 100,
                        1500 : 150}
voucher_to_points = {20 : 300,
                    50 : 600,
                    100 : 950,
                    150 : 1500}
def get_qr(voucher_id):
    logo = Image.open(os.path.join(
        os.path.abspath(os.getcwd()), 
        'projects',"templates","static","assets",'logo_no_slag.png')).convert("RGBA")
    logo = logo.resize((60, 60))
    qr = qrcode.QRCode()
    qr.add_data({"voucher_id":voucher_id})
    qr.make(fit=True)
    img = qr.make_image().convert('RGB')
    pos = ((img.size[0] - logo.size[0]) // 2, (img.size[1] - logo.size[1]) // 2)
    img.paste(logo,pos)
    image_io = BytesIO()
    img.save(image_io, format='PNG')
    qr_image_base64 = base64.b64encode(image_io.getvalue()).decode('utf-8')
    return qr_image_base64
def get_total_points(user_id):
    points = Point.objects.filter(user=user_id)
    total = 0
    for point in points:
        if point.expire_date < datetime.date.today():
            point.delete()
        else:
            total += point.value
    return total
@login_required(login_url='/login/')
def discounts(request):
    return render(request, 'discounts.html')


@login_required(login_url='/login/')
def moneyback(request):
    total = get_total_points(request.user.id)
    try:
        current_step = [points_to_vouchers[key] for key in points_to_vouchers if key <= total][-1]
        if current_step == 150:
            current_step = 100
    except:
        current_step = 0
    try:
        key_next = [key for key in points_to_vouchers if key > total][0]
        next_step = points_to_vouchers[key_next]
    except:
        key_next = list(points_to_vouchers.keys())[-1]
        next_step = points_to_vouchers[key_next]
    progress_bar =  total/key_next
    return render(request, 'moneyback.html',{"total_points":total,
                                             'steps':[current_step,next_step],
                                             "progress_bar":int(progress_bar*100),
                                             "vouchers":points_to_vouchers})
@login_required(login_url='/login/')
def new_voucher(request,voucher): 
    total_points = get_total_points(request.user.id)
    try: 
        voucher_to_points[voucher]
    except:
        return HttpResponse("Error: Invalid voucher <br> <a href='/discounts'>Back</a>")
    if voucher_to_points[voucher] > total_points:
        return HttpResponse("Error: Not enough points <br> <a href='/discounts'>Back</a>")
    else:
        point_objects = Point.objects.filter(user=request.user.id).order_by("expire_date")
        points_removed = 0
        points_to_remove = voucher_to_points[voucher]
        for point_object in point_objects:
            if points_to_remove > points_removed:
                points_removed += point_object.value
                expire_date = point_object.expire_date
                point_object.delete()
            else:
                break
        remainder = points_removed - points_to_remove
        if remainder != 0:
            Point(user=request.user,value=remainder,expire_date=expire_date).save()
        expire_date = datetime.date.today() + datetime.timedelta(days=7)
        Voucher(user=request.user,value=voucher,expire_date=expire_date).save()
        return render(request, 'new_voucher.html',{"voucher":voucher})

@login_required(login_url='/login/')
def vouchers(request):
    voucher_object = []
    img = ""
    vouchers = Voucher.objects.filter(user=request.user).order_by("value")
    for voucher in vouchers:
        if voucher.is_used:
            pass
        else:
            date =  voucher.expire_date - datetime.date.today()
            voucher_object.append({"value":voucher.value,"date":date.days,"voucher_id":voucher.voucher_id})
    if request.method == 'POST' and request.POST.get('voucher_id').strip() != "":
        voucher_id = request.POST.get('voucher_id')
        img = get_qr(voucher_id)
    return render(request, 'vouchers.html',{"vouchers":voucher_object,"qr_image":img })

        

@user_passes_test(user_is_admin)
def voucher_admin(request,voucher_id):
    voucher = Voucher.objects.filter(voucher_id=voucher_id).first()
    voucher.date = voucher.expire_date - datetime.date.today()
    voucher.date = voucher.date.days
    if request.method == "POST":
        action = request.POST.get('action')
        if action == "revoke":
            voucher.is_used = True
            voucher.save()
        elif action == "unrevoke":
            voucher.is_used = False
            voucher.save()
    return render(request, 'voucher_admin.html', {'voucher':voucher})