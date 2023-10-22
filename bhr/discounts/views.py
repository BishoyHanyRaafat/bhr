from django.shortcuts import render
from .models import Point,Voucher
import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

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
    vouchers = Voucher.objects.filter(user=request.user).order_by("value")
    for voucher in vouchers:
        if voucher.is_used:
            pass
        else:
            date =  voucher.expire_date - datetime.date.today()
            voucher_object.append({"value":voucher.value,"date":date.days,"id":voucher.voucher_id})
    return render(request, 'vouchers.html',{"vouchers":voucher_object})