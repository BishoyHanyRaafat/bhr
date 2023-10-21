from django.shortcuts import render
from .models import Point
import datetime
# Create your views here.

# 300 -> 20$
# 600 -> 50$
# 950 -> 100$
# 1500 -> 150$
points_to_vouchers = {300 : 20,
                        600 : 50,
                        950 : 100,
                        1500 : 150}
def discounts(request):
    points = Point.objects.filter(user=request.user.id)
    total = 0
    for point in points:
        if point.expire_date < datetime.date.today():
            continue
        else:
            total += point.value
    try:
        current_step = [points_to_vouchers[key] for key in points_to_vouchers if key <= total][0]
    except:
        current_step = 0
    try:
        key_next = [key for key in points_to_vouchers if key > total][0]
        next_step = points_to_vouchers[key_next]
    except:
        next_step = points_to_vouchers[points_to_vouchers.keys()[-1]]
        key_next = points_to_vouchers.keys()[-1]
    progress_bar =  total/key_next
    
    return render(request, 'discounts.html',{"total_points":total,
                                             'steps':[current_step,next_step],
                                             "progress_bar":int(progress_bar*100),
                                             "vouchers":points_to_vouchers})