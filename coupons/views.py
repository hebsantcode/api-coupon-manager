import json
import os
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt # type: ignore
from .models import Coupon, EmailUsed, MailchimpEmails
from dotenv import load_dotenv
from .utils.db_ssh import setup_ssh_tunnel

load_dotenv()

# Start tunnel for the listening
tunnel = setup_ssh_tunnel()

SUBSCRIBERS = []

@csrf_exempt
def create(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        code = data.get('code')
        description = data.get('description')
        discount = data.get('discount')
        if Coupon.objects.filter(code=code).count() == 0:
            Coupon.objects.create(code=code, description=description, discount=discount).save()
            return JsonResponse({
                "coupon_code": code,
                "is_created": True
            })
        return JsonResponse({
            "coupon_code": code,
            "is_created": False
        })

@csrf_exempt
def delete(request):
    if request.method == 'DELETE':
        data = json.loads(request.body)
        coupon_id = data.get('couponId')
        coupon = Coupon.objects.get(pk=coupon_id)
        if coupon:
            coupon.delete()
            return JsonResponse({
                "coupon_code": coupon.code,
                "is_deleted": True
            })
        return JsonResponse({
            "coupon_code": coupon.code,
            "is_deleted": False
        })
    
@csrf_exempt
def update(request):
    if request.method == 'PUT':
        data = json.loads(request.body)
        code = data.get('code')
        description = data.get('description')
        discount = data.get('discount')
        coupon = Coupon.objects.filter(pk=3)
        coupon.update(code=code, description=description, discount=discount)
        return JsonResponse({
            "is_updated": True
        })
    
@csrf_exempt    
def get_coupons(request):
    if request.method == 'POST':
        coupons = Coupon.objects.all()
        all_coupons = []
        for coupon in coupons:
            all_coupons.append({
                "id": coupon.pk,
                "code": coupon.code,
                "description": coupon.description,
                "discount": coupon.discount
            })
    return JsonResponse({
        "coupons": all_coupons
    })

@csrf_exempt    
def mailchimp_total_members(request):
    if request.method == 'GET':
        headers = {'Authorization': 'apikey {}'.format(os.environ.get('MAILCHIMP_SECRET_KEY')),}
        url = "https://us18.api.mailchimp.com/3.0/lists/{}".format(os.environ.get('MAILCHIMP_LIST_ID'))
        data = json.loads(requests.get(url=url, headers=headers).text)
        total_members = data.get('stats').get('member_count')
        return JsonResponse({
            "total_members": total_members,
            "total_subscribers": len(SUBSCRIBERS)
        })
        
@csrf_exempt
def maichimp_pagination(request):
    if request.method == 'POST':
        
        data = json.loads(request.body)
        offset = data.get('offset')
        count = data.get('count')
        members_fetched = data.get('members_fetched')
        
        if members_fetched == 0:
            SUBSCRIBERS.clear()
            
        headers = {'Authorization': 'apikey {}'.format(os.environ.get('MAILCHIMP_SECRET_KEY')),}

        url = "https://us18.api.mailchimp.com/3.0/lists/{}/members?offset={}&count={}".format(os.environ.get('MAILCHIMP_LIST_ID'), offset, count)
        data = json.loads(requests.get(url=url, headers=headers).text)
        for sub in data.get('members'):
            SUBSCRIBERS.append({"full_name": sub.get('full_name'), "email_address": sub.get('email_address')})
        
        print(len(SUBSCRIBERS), 'subscribers fetched')
            
        return JsonResponse({
            "offset": offset + 100,
            "members_fetched": len(data.get('members')) + members_fetched
        })

@csrf_exempt    
def is_valid_for_coupons(request):
    if request.method == 'POST' and len(SUBSCRIBERS) > 0:
        data = json.loads(request.body)
        email = data.get('email')
        code = data.get('code')
        
        for sub in SUBSCRIBERS:
            if email.lower() in str(sub.get('email_address')).lower():
                coupon = Coupon.objects.filter(code=code).first()
                if coupon:
                    email_used_entry = EmailUsed.objects.filter(coupon=coupon, email=email).exists()
                    if not email_used_entry:
                        EmailUsed.objects.create(coupon=coupon, email=email)
                        return JsonResponse({
                            "is_valid": True,
                            "coupon_code": coupon.code
                        })
                        
                    return JsonResponse({
                        "is_valid": False,
                        "email": email
                    })
                
                return JsonResponse({
                    "coupon_error": "Coupon {} not exists.".format(code)
                })
        
            return JsonResponse({
                "is_valid": False
            })
        
    return JsonResponse({
        "error": "not data"
    })