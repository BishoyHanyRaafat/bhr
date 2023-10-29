from django.shortcuts import render,redirect
from .models import Point,Voucher
import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import qrcode
from PIL import Image,ImageDraw,ImageFont
import os
from io import BytesIO
import base64
from users.models import IPAddress
from django.contrib.auth.models import User
from django.templatetags.static import static
from django.conf import settings
# Create your views here.

# 300 -> 20$
# 600 -> 50$
# 950 -> 100$
# 1500 -> 150$
points_to_vouchers = {250 : 10,
                        600 : 50,
                        950 : 100,
                        1500 : 150}
voucher_to_points = {10 : 250,
                    50 : 600,
                    100 : 950,
                    150 : 1500}
def get_qr(url,text=None):
    logo = Image.open(os.path.join(os.path.dirname(settings.BASE_DIR), 'static', "assets/logo_no_slag.png")).convert("RGBA")
    logo = logo.resize((60, 60))
    qr = qrcode.QRCode()
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image().convert('RGB')
    pos = ((img.size[0] - logo.size[0]) // 2, (img.size[1] - logo.size[1]) // 2)
    img.paste(logo,pos)
    if text:
        size = (img.size[0],img.size[1]+50)
        new_image = Image.new('RGB', size, (255, 255, 255))
        draw = ImageDraw.Draw(new_image)
        font = ImageFont.load_default()
        new_image.paste(img, (0, 0))
        offset =  size[0] - font.getlength(text)//3
        draw.multiline_text((offset//2,img.size[1]-20), text, fill="black", font=font,align="center")
        img = new_image
    
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
    user = request.user
    if user.is_authenticated:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            user_ip = x_forwarded_for.split(',')[-1].strip()
        else:
            user_ip = request.META.get('REMOTE_ADDR')
        
        ip, _ = IPAddress.objects.get_or_create(address=user_ip)
        ip.users.add(user)
    return render(request, 'discounts.html')

def user_QR(request,user_id):
    admin_url = request.META['HTTP_HOST'] + "/admin/discounts/voucher/"
    user_link = f'{admin_url}add/?user={user_id}&value={10}'
    user = User.objects.filter(id=user_id).first()
    text = f"Use the QR code when you get any of \nBishoy's services to get a 10$ discount.\n This image was generated by {user.username}"
    img = get_qr(user_link,text)
    image_data = base64.b64decode(img)
    response = HttpResponse(image_data, content_type="image/png")
    
    return response

@login_required(login_url='/login/')
def moneyback(request):
    total = get_total_points(request.user.id)
    return render(request, 'moneyback.html',{"total_points":total,
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
        Voucher(user=request.user,value=voucher).save()
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
        img = get_qr(request.META['HTTP_HOST']+"/discounts/vouchers/admin/"+ voucher_id)
    return render(request, 'vouchers.html',{"vouchers":voucher_object,"qr_image":img })


@login_required(login_url='/admin/login/')
def voucher_admin(request,voucher_id):
    if request.user.is_superuser == False:
        return redirect(f"/admin/login/?next={request.path}")
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
