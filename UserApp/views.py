from django.shortcuts import render,redirect
from .models import Customer,Address
from AdminApp.models import Category,Product
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.views import View
from django.contrib import messages
from django.db.models import Max,Avg,Min
from media.time_date import t1
import random
from django.conf import settings
from django.core.mail import send_mail

# Create your views here.

def pricetest(request,prods):
    amt=prods.aggregate(Max('price'))
    val=amt['price__max']
    amt['price__max']=amt['price__max']//4
    amt['price__max1']=amt['price__max']+1
    amt['price__max2']=amt['price__max']*2
    amt['price__max3']=amt['price__max']*2+1
    request.session['firstprice']="0-"+str(amt['price__max'])
    request.session['secondprice']=str(amt['price__max1'])+"-"+str(amt['price__max2'])
    request.session['thirdprice']=str(amt['price__max3'])+"-"+str(val)
    return amt
    
class Index(View):
    def get(self,request):
        cats=Category.objects.all()
        prods=Product.objects.all()
        if prods:
            amt=pricetest(request,prods)
        else:
            amt=None
        cat1=request.session.get('cat1')
        if cat1:
            del request.session['cat1']
        price1=request.session.get('price1')
        if price1:
            del request.session['price1']
        data={'category':cats,'prods':prods,'pri':amt}
        return render(request,"usersite/index.html",data)

def add(request):
    if request.method=="GET":
        id = request.GET.get('id')
        qty = request.GET.get('qty')
        index = request.session.get('index',{})
        index[id] = qty
        request.session['index'] = index
    return HttpResponseRedirect("/")

# from django.http import HttpResponseRedirect

def customeradd(request):
    if request.method == "GET":
        # Fetch 'id' and 'qty' from GET parameters
        product_id = request.GET.get('id')
        qty = request.GET.get('qty')

        # print("Product ID:", product_id)
        # print("Quantity:", qty)

        # Handle session cart
        pcart = request.session.get('pcart', {})

        # Store quantity in the session cart using the product ID as key
        pcart[product_id] = qty
        request.session['pcart'] = pcart

        return HttpResponseRedirect("/profile/")
    
def update_customeradd(request):
    if request.method == "GET":
        # Fetch 'id' and 'qty' from GET parameters
        product_id = request.GET.get('id')
        qty = request.GET.get('qty')

        # print("Product ID:", product_id)
        # print("Quantity:", qty)

        # Handle session cart
        pcart = request.session.get('pcart', {})

        # Store quantity in the session cart using the product ID as key
        pcart[product_id] = qty
        request.session['pcart'] = pcart

        return HttpResponseRedirect("/profile/viewcart/")

def update_add(request):
    if request.method == "GET":
        # Fetch 'id' and 'qty' from GET parameters
        product_id = request.GET.get('id')
        qty = request.GET.get('qty')

        # print("Product ID:", product_id)
        # print("Quantity:", qty)

        # Handle session cart
        index = request.session.get('index', {})

        # Store quantity in the session cart using the product ID as key
        index[product_id] = qty
        request.session['index'] = index

        return HttpResponseRedirect("/viewcart/")

 
    
class Signup_view(View):
    def get(self, request):
        data = Category.objects.all()
        return render(request, "usersite/signup.html", {'cats': data})

    def post(self, request):
        try:
            email = request.POST.get('email')  # Fetching the first name
            password = request.POST.get('password')  # Fetching the last name
            confirmpassword = request.POST.get('confirmpassword')
            username = request.POST.get('username')
            
            if Customer.objects.filter(email__iexact=email).exists():
                return JsonResponse({'success': False, 'message': 'Email already exists. Please use a different email or log in.'}, status=200)
            
            if not password or not confirmpassword or not email or not username:
                return JsonResponse({'success': False, 'message': "All fields are required."}, status=200)
            if password != confirmpassword:
                # print("hiii")
                return JsonResponse({'success': False, 'message': "Password not match..."}, status=200)
            otp=random.randint(100000,999999)
            print(otp)
            subject = "This message related to Create New User for E-Commerce Website"
            message = f"OTP is {otp}"
            request.session['str_otp'] = str(otp)
            request.session['newuserpass'] = password
            request.session['newusername'] = username
            request.session['newemail'] = email
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]
            # send_mail(subject, message, from_email, recipient_list)
            # cobj = Customer(
            #     name = username,
            #     email = email,
            #     password = password,
            # )
            # cobj.save()
            return JsonResponse({'status': 'success', 'message': 'For Registration successfully! Click OK to go to the Verification page.'}, status=200)
        except Exception as e:
            # Catch any other exceptions and return a generic error message
            return JsonResponse({'success': False, 'message': 'An error occurred during registration. Please try again.'}, status=500)
            
    
class NewUser_verify_otp_view(View):    
    def get(self, request):
        cats = Category.objects.all()
        return render(request, "usersite/verify_otp.html", {'cats': cats})
    def post(self, request):
            otp = request.POST.get("otp")
            get_otp=request.session.get('str_otp')
            if otp == get_otp:
                del request.session['str_otp']
                # otp=random.randint(100000,999999)
                subject = "Congrates! Welcome to Successfully Create New User for E-Commerce Website"
                password = request.session.get('newuserpass')
                username = request.session.get('newusername')
                newemail = request.session.get('newemail')
                message = "Your Username : "+username+" , Your Password : " + password
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [newemail]
                
                # send_mail(subject, message, from_email, recipient_list)
                cobj = Customer(
                    name = username,
                    email = newemail,
                    password = password,
                )
                cobj.save()
                return JsonResponse({'success': True, 'redirect_url': '/login/', 'message': "Successfully created New Account Check Your Email"})
            else:
                return JsonResponse({'success': False, 'message': "OTP does not match"})
            
class Login_view(View):
    def get(self,request):
        user=request.session.get('cuser')
        if user:
            return HttpResponseRedirect('/profile/')
        cats=Category.objects.all()
        return render(request,"usersite/customerlogin.html",{'cats':cats})
    def post(self,request):
        try:
            uname = request.POST.get('username')
            if uname.endswith('@gmail.com') or uname.endswith('@rediffmail.com') or uname.endswith('@yahoomail.com'):
                pass
            else:
                custobj=Customer.objects.get(name=uname)
                uname=custobj.email
            pwd = request.POST.get('password')
            cobj = Customer.objects.get(email=uname)
            if cobj:
                if pwd == cobj.password:
                    if uname == cobj.email:
                        request.session['customer_instance'] = cobj.id
                        otp=random.randint(100000,999999)
                        request.session['str_otp']=str(otp)
                        print(otp)
                        subject = "This message Related to Login E-Commerce Website"
                        message = f"Your OTP is {otp}" 
                        from_email = settings.EMAIL_HOST_USER
                        recipient_list = [uname]
        
                        # send_mail(subject, message, from_email, recipient_list)
                        return JsonResponse({'status': 'success', 'redirect_url': '/login_verify_otp/', 'message': "OTP Send ! Please Check Your Registered Email-ID"})
                    else:
                        return JsonResponse({'status': 'error', 'message': 'Invalid username!'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Invalid Password!'})
            return JsonResponse({'status': 'error', 'message': 'Invalid credentials!'})

        except Customer.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Invalid Email!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

class Logout_view(View):
    def get(self,request):
        cat1=request.session.get('cat1')
        if cat1:
            del request.session['cat1']
        price=request.session.get('price1')
        if price:
            del request.session['price1']
        cuser=request.session.get('cuser')
        if cuser:
            del request.session['cuser']
            del request.session['cid']
        return HttpResponseRedirect('/')
        
class Login_verify_otp_view(View):
    def get(self,request):
        cats = Category.objects.all()
        return render(request,"usersite/loginVerify_otp.html",{'cats':cats})
    def post(self,request):
        otp = request.POST.get("otp")
        get_otp=request.session.get('str_otp')
        if otp == get_otp:
            del request.session['str_otp']
            customer_instance = request.session.get('customer_instance')
            obj = Customer.objects.get(id=customer_instance)
            request.session['cuser'] = obj.email
            request.session['cid'] = obj.id
            index = request.session.get('index')
            if index:
                request.session['pid'] = index
                request.session['pcart'] = index
                del request.session['index']
            cat1 = request.session.get('cat1')
            if cat1:
                del request.session['cat1']
            return JsonResponse({'success': True, 'redirect_url': '/profile/', 'message': "Login Successfully"})
        else:
            return JsonResponse({'success': False, 'message': "OTP does not match"})

        
# class Send_mail_view(View):
#     def get(self,request):
#         cats=Category.objects.all()
#         return render(request,"usersite/forget.html",{'cats':cats,'otp':"msg"})
#     def post(self,request):
#         otp=request.POST.get("otp")
#         print(otp,str_otp)
#         if otp==str_otp:
#             return redirect('/login/forget/reset_password/')
#         else:
#             messages.warning(request,"OTP Not Matched")
#             return redirect("/login/send_mail/")

class Forget_password_view(View):
    def get(self, request):
        cats = Category.objects.all()
        return render(request, "usersite/forget.html", {'cats': cats})
    def post(self, request):
        try:
            email = request.POST.get('email')
            request.session['em'] = email
            cobj = Customer.objects.get(email = email)
            if cobj:
                otp = random.randint(100000, 999999)
                request.session['str_otp']=str(otp)
                subject = "This message related to forget password"
                message = f"OTP is {otp}"
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [email]
                send_mail(subject, message, from_email, recipient_list)
                return JsonResponse({'success': True, 'message': 'OTP sent successfully', 'redirect_url': '/login/send_mail/'})
        except Customer.DoesNotExist:
            return JsonResponse({'success': False, 'message': "Email ID doesn't exist"})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

class Send_mail_view(View):
    def get(self, request):
        cats = Category.objects.all()
        return render(request, "usersite/check_otp.html", {'cats': cats})
    def post(self, request):
            otp = request.POST.get("yourotp")
            if otp == request.session['str_otp']:
                del request.session['str_otp']
                return JsonResponse({'success': True, 'redirect_url': '/login/forget/reset_password/'})
            else:
                return JsonResponse({'success': False, 'message': "OTP does not match"})
            
class Resend_mail_view(View):
    def post(self,request):
        try:
            email = request.session.get('em')
            cobj = Customer.objects.get(email = email)
            if cobj:
                otp = random.randint(100000, 999999)
                request.session['str_otp'] = str(otp)
                subject = "This message related to forget password"
                message = f"OTP is {otp}"
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [email]
                send_mail(subject, message, from_email, recipient_list)
                return JsonResponse({'success': True, 'message': 'OTP sent successfully', 'redirect_url': '/login/send_mail/'})
        except:
            return JsonResponse({'success': False,'message': 'Email Id not Exist'})
    def get(self,request):
        return redirect('/login/forget/')
    # def get(self,request):
    #     cats=Customer.objects.all()
    #     return render(request,"usersite/check_otp.html",{'cats':cats})

# class Reset_password_view(View):
#     def get(self,request):
#         cats=Category.objects.all()
#         return render(request,"usersite/reset_password.html",{'cats':cats})
#     def post(self,request):
#         newpass=request.POST.get('password')
#         conf_pass=request.POST.get('confirm_pass')
#         # print(str_email,type(str_email))
#         str_email=request.session['em']
#         if newpass==conf_pass:
#             obj=Customer.objects.get(email=str_email)
#             cobj=Customer(id=obj.id,name=obj.name,fname=obj.fname,email=obj.email,phone=obj.phone,cpass=newpass,image=obj.image,gender=obj.gender,address=obj.address)
#             cobj.save()
#             print("POP up box")
#             del request.session['em']
#             return HttpResponseRedirect('/login/')
#         else:
#             messages.warning(request,"New Password and Confirmed Password does not matched")
#             return HttpResponseRedirect('/login/forget/reset_password/')

class Reset_password_view(View):
    def get(self, request):
        cats = Category.objects.all()
        return render(request, "usersite/reset_password.html", {'cats': cats})

    def post(self, request):
        newpass = request.POST.get('password')
        conf_pass = request.POST.get('confirm_pass')
        str_email = request.session['em']
        if newpass == conf_pass:
            obj = Customer.objects.get(email = str_email)
            obj.cpass = newpass  # Update the password field directly
            obj.save()
            del request.session['em']
            return JsonResponse({'success': True, 'message': 'Password reset successfully!'})
        else:
            return JsonResponse({'success': False, 'message': 'New Password and Confirmed Password do not match'})
        
class Customer_profile_view(View):
    def get(self,request):
        try:
            cats=Category.objects.all()
            prods=Product.objects.all()
            if prods:
                amt=pricetest(request,prods)
            else:
                amt=None
            # cat1=request.session.get('cat1')
            # if cat1:
            #     del request.session['cat1']
            data={'category':cats,'prods':prods,'pri':amt}
            return render(request,"usersite/customerindex.html",data)
        except Exception as msg:
            return HttpResponse(msg)
    
class Filter_category_index_view(View):
    def post(self,request):
        try:
            id = request.POST.get('id')
            cats=Category.objects.all()
            prods=Product.objects.filter(Category=int(id))
            if prods:
                amt=pricetest(request,prods)
                # obj=cats.get(id=int(id))
                request.session['cat1'] = id
            else:
                return HttpResponseRedirect('/')
            price=request.session.get('price1')
            if price:
                del request.session['price1'] 
            data={'category':cats,'prods':prods,'pri':amt,'index1':"msg"}
            return render(request,"usersite/index.html",data)
        except:
            return HttpResponse("Something mistake")
    def get(self,request):
        prods = Product.objects.all()
        cats = Category.objects.all()
        amt = pricetest(request,prods)
        data = {'prods': prods, 'category': cats, 'pri': amt}
        return render(request,"usersite/index.html",data)
    
# from django.template.loader import render_to_string


class Filter_category_view(View):        
    def post(self,request):
        try:
            id = request.POST.get('id')
            cats=Category.objects.all()
            prods=Product.objects.filter(Category=int(id))
            if prods:
                amt=pricetest(request,prods)
                # obj=cats.get(id=int(id))
                request.session['cat1'] = id
            else:
                return HttpResponseRedirect('/profile/')
            price=request.session.get('price1')
            if price:
                del request.session['price1'] 
            data={'category':cats,'prods':prods,'pri':amt,'index1':"msg"}
            return render(request,"usersite/customerindex.html",data)
        except:
            return HttpResponse("Something mistake")
    def get(self,request):
        user = request.session.get('cuser')
        if not user:
            return redirect('/login/')
        prods = Product.objects.all()
        cats = Category.objects.all()
        amt = pricetest(request,prods)
        data = {'prods': prods, 'category': cats, 'pri': amt}
        return render(request,"usersite/customerindex.html",data)
       
class PriceFilterIndex_view(View):
    def post(self,request):
        price = request.POST.get("price")
        cats=Category.objects.all()
        cat1=request.session.get('cat1')
        if cat1:
            prods=Product.objects.filter(Category=cat1)
        else:
            prods=Product.objects.all()
        amt=pricetest(request,prods)
        request.session['price1'] = price
        if price:
            price = price.split("-")
            min1 = int(price[0])
            max1 = int(price[1])
            prods=prods.filter(price__range=(min1,max1))
        data={'category':cats,'prods':prods,'pri':amt}
        return render(request,"usersite/index.html",data)
    def get(self,request):
        prods = Product.objects.all()
        cats = Category.objects.all()
        amt = pricetest(request,prods)
        data = {'prods': prods, 'category': cats, 'pri': amt}
        return render(request,"usersite/index.html",data)
        
        
class PriceFilter_view(View):
    def post(self,request):
        price = request.POST.get("price")
        cats=Category.objects.all()
        cat1=request.session.get('cat1')
        if cat1:
            prods=Product.objects.filter(Category=cat1)
        else:
            prods=Product.objects.all()
        amt=pricetest(request,prods)
        request.session['price1'] = price
        if price:
            price = price.split("-")
            min1 = int(price[0])
            max1 = int(price[1])
            prods=prods.filter(price__range=(min1,max1))
        data={'category':cats,'prods':prods,'pri':amt}
        return render(request,"usersite/customerindex.html",data)
    def get(self,request):
        user = request.session.get('cuser')
        if not user:
            return HttpResponseRedirect('/login/')
        prods = Product.objects.all()
        cats = Category.objects.all()
        amt = pricetest(request,prods)
        data = {'prods': prods, 'category': cats, 'pri': amt}
        return render(request,"usersite/customerindex.html",data)
    
# class Index_view(View):
#     def get(self,request):
#         print("say hii")
        
# import json

class Add_to_cart_view(View):
    def post(self,request):
        addcart_id=request.POST.get('pid')
        if addcart_id:
            data=self.add_in_cart(request,addcart_id)
        # data=addcart_id
        val=request.session.get('cat1')
        price1=request.session.get('price1')
        if val:
            if price1:
                return JsonResponse({'redirect_url': f'/price/{price1}/','data':data})
            return JsonResponse({'redirect_url': f'/filter/{str(val)}/','data':data})
        else:
            if price1:
                return JsonResponse({'redirect_url': f'/price/{price1}/','data':data})
            return JsonResponse({'redirect_url': '/','data':data})    
    def add_in_cart(self,request,product_id):
        index=request.session.get('index',{})
        index[product_id]=1
        request.session['index']=index
        prod = Product.objects.get(id=product_id)
        # Serialize the product instance
        prod_data = {
            'img': prod.image.url,  # Ensure you have the url if image is an ImageField
            'name': prod.name,
            'des': prod.des,
            'qty': prod.item_qty,
            'rate': prod.price,
            'item': 1
        }
        return prod_data
        
class CustomerAdd_to_cart_view(View):
    def post(self,request):
        addcart_id = request.POST.get('pid')
        if addcart_id:
            data = self.add_in_cart(request,addcart_id)
        return JsonResponse({'data':data})  
    def add_in_cart(self,request,product_id):
        pcart = request.session.get('pcart',{})
        pcart[product_id] = 1
        request.session['pcart'] = pcart
        prod = Product.objects.get(id = product_id)
        # Serialize the product instance
        prod_data = {
            'img': prod.image.url,  # Ensure you have the url if image is an ImageField
            'name': prod.name,
            'des': prod.des,
            'qty': prod.item_qty - 1,
            'rate': prod.price,
            'item': 1
        }
        return prod_data
    
class Customer_update_cart_view(View):
    def post(self,request):
        updatecart_id = request.POST.get('pid')
        if updatecart_id:
            data = self.update_incart(request,updatecart_id)
        return JsonResponse({'data': data})
    def update_incart(self,request,product_id):
        pcart = request.session.get('pcart')
        item = pcart[product_id]
        # request.session['pcart']=pcart
        prod = Product.objects.get(id=product_id)
        qty = int(prod.item_qty) - int(item)
        # qty = prod.item_qty
        # Serialize the product instance
        prod_data = {
            'img': prod.image.url,  # Ensure you have the url if image is an ImageField
            'name': prod.name,
            'des': prod.des,
            'qty': qty,
            'rate': prod.price,
            'item': item
        }
        return prod_data

class update_cart_view(View):
    def post(self,request):
        updatecart_id = request.POST.get('pid')
        if updatecart_id:
            data = self.update_incart(request,updatecart_id)
        return JsonResponse({'data': data})
    def update_incart(self,request,product_id):
        index = request.session.get('index')
        item = index[product_id]
        # request.session['pcart']=pcart
        prod = Product.objects.get(id=product_id)
        qty = int(prod.item_qty) - int(item)
        # qty = prod.item_qty
        # Serialize the product instance
        prod_data = {
            'img': prod.image.url,  # Ensure you have the url if image is an ImageField
            'name': prod.name,
            'des': prod.des,
            'qty': qty,
            'rate': prod.price,
            'item': item
        }
        return prod_data

# class Customer_addproduct_view(View):
#     def post(self,request):
#         pcart=request.session.get('pcart',{})
#         cat1=request.session.get('cat1')
#         price1=request.session.get('price1')
#         add_product_id=request.POST.get('addcart',None)
#         less_product_id=request.POST.get('removecart',None)
#         if pcart:
#             ks=pcart.keys()
#             if add_product_id in ks:
#                 qty=pcart[add_product_id]
#                 pcart[add_product_id]=qty+1
#             elif less_product_id in ks:
#                 qty=pcart[less_product_id]
#                 if qty<2:
#                     pcart.pop(less_product_id)
#                 else:
#                     pcart[less_product_id]=qty-1
#         request.session['pcart']=pcart
#         if cat1:
#             if price1:
#                 return redirect('/profile/price/'+price1+'/')
#             return redirect('/profile/filter/'+str(cat1)+'/')
#         else:
#             if price1:
#                 return redirect('/profile/price/'+price1+'/')
#             return redirect('/profile/')
    
# class Index_addproduct_view(View):
#     def post(self,request):
#         index=request.session.get('index',{})
#         cat1=request.session.get('cat1')
#         price1=request.session.get('price1')
#         add_product_id=request.POST.get('addcart',None)
#         less_product_id=request.POST.get('removecart',None)
#         if index:
#             ks=index.keys()
#             if add_product_id in ks:
#                 qty=index[add_product_id]
#                 index[add_product_id]=qty+1
#             elif less_product_id in ks:
#                 qty=index[less_product_id]
#                 if qty<2:
#                     index.pop(less_product_id)
#                 else:
#                     index[less_product_id]=qty-1
#         request.session['index']=index
#         if cat1:
#             if price1:
#                 return redirect('/price/'+price1+'/')
#             return redirect('/filter/'+str(cat1)+'/')
#         else:
#             if price1:
#                 return redirect('/price/'+price1+'/')
#             return redirect('/')   

# class Index_addproduct_view(View):
#     def post(self, request):
#         index = request.session.get('index', {})
#         cat1 = request.session.get('cat1')
#         price1 = request.session.get('price1')
#         add_product_id = request.POST.get('addcart')
#         less_product_id = request.POST.get('removecart')
#         if add_product_id:
#             items=self.add_product_to_cart(index, add_product_id)
#         if less_product_id:
#             self.remove_product_from_cart(index, less_product_id)
#         request.session['index'] = index
#         redirect_url = self.get_redirect_url(cat1, price1)
#         prod = Product.objects.get(id=add_product_id)
#         # Serialize the product instance
#         prod_data = {
#             'img': prod.image.url,  # Ensure you have the url if image is an ImageField
#             'name': prod.name,
#             'des': prod.des,
#             'qty': prod.item_qty,
#             'rate': prod.price,
#             'item': items 
#         }
#         return JsonResponse({'redirect_url': redirect_url, 'index': index, 'data':prod_data})
#     def add_product_to_cart(self, index, product_id):
#         if product_id in index:
#             index[product_id] += 1
#         else:
#             index[product_id] = 1
#         return index[product_id]
#     def remove_product_from_cart(self, index, product_id):
#         if product_id in index:
#             if index[product_id] > 1:
#                 index[product_id] -= 1
#             else:
#                 index.pop(product_id)
#     def get_redirect_url(self, cat1, price1):
#         if cat1:
#             if price1:
#                 return f'/price/{price1}/'
#             return f'/filter/{cat1}/'
#         else:
#             if price1:
#                 return f'/price/{price1}/'
#             return '/'
# from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
# def confirm_action(request):
#     if request.method == 'POST':
#         # return HttpResponse("success")
#         return JsonResponse({'status': 'success', 'message': 'Action confirmed'})
#     return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
    # return HttpResponse("say hii")


    
class Viewcart_view(View):
    def get(self,request):
        cats=Category.objects.all()
        pcart=request.session.get('pcart')
        print(pcart)
        if not pcart:
            # messages.warning(request,"No items in cart!!!")
            data={'cats':cats,'pcart':pcart,'msg':"congrates"}
        else:
            data={'cats':cats,'pcart':pcart}
        return render(request,"usersite/viewcart.html",data)
    
    
# class Customer_less_item_incart_view(View):
#     def post(self,request):
#         pid=request.POST.get('pid')
#         pcart=request.session.get('pcart')
#         item=int(pcart[pid])
#         if item==1:
#             # messages.warning(request,"Quantity must be 1 !!")
#             # index.pop(pid)
#             del pcart[pid]
#             request.session['pcart']=pcart
#             return JsonResponse({'success': False, 'message': 'This items deleted...','redirect_url': '/profile/viewcart/'}, status=200)
#         else:    
#             item=item-1
#             pcart[pid]=str(item)
#         request.session['pcart']=pcart
#         return JsonResponse({'success': True, 'redirect_url': '/profile/viewcart/'},status=200)
#     def get(self,request):
#         user=request.session.get('cuser')
#         if not user:
#             return HttpResponseRedirect('/login/')
#         return redirect('/profile/viewcart/')

# class Customer_add_item_incart(View):
#     def post(self,request):
#         pid=request.POST.get('pid')
#         pcart=request.session.get('pcart')
#         item=int(pcart[pid])
#         product_reference=Product.objects.get(id=pid)
#         if item<product_reference.item_qty:
#             item=item+1
#             pcart[pid]=str(item)
#             request.session['pcart']=pcart
#             return JsonResponse({'success': True, 'redirect_url': '/profile/viewcart/'}, status=200)
#         return JsonResponse({'success': False, 'message': 'Items Empty...'}, status=200)
#     def get(self,request):
#         user=request.session.get('cuser')
#         if not user:
#             return HttpResponseRedirect('/login/')
#         return redirect('/profile/viewcart/')


class Customer_delete_item_incart(View):
    def post(self, request):
        pid = request.POST.get('pid')
        pcart = request.session.get('pcart', {})
        if pid in pcart:
            del pcart[pid]
            request.session['pcart'] = pcart
            if not pcart:
                messages.warning(request, "No items in cart!!!")
                return JsonResponse({'success': True, 'empty_cart': True})
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'message': 'Item not found in cart'})
    def get(self,request):
        user=request.session.get('cuser')
        if not user:
            return HttpResponseRedirect('/login/')
        return redirect('/profile/viewcart/')

    
class Viewcart_Index_view(View):
    def get(self,request):
        cats=Category.objects.all()
        index=request.session.get('index')
        # for k,v in request.session.items():
        #     print(k,"=>",v)
        data={'cats':cats,'index':index}
        if not index:
            # messages.warning(request,"No items in cart!!!")
            # data.update({'messages':"hello"})
            # del data['index']
            data['msg']="empty_cart"
        return render(request,"usersite/indexcart.html",data)

# class Add_item_incart(View):
#     def post(self,request):
#         pid=request.POST.get('pid')
#         index=request.session.get('index')
#         item=int(index[pid])
#         product_reference=Product.objects.get(id=pid)
#         if item<product_reference.item_qty:
#             item=item+1
#             index[pid]=str(item)
#             request.session['index']=index
#             return JsonResponse({'success': True, 'redirect_url': '/viewcart/'}, status=200)
#         return JsonResponse({'success': False, 'message': 'Items Empty...'}, status=200)
#     def get(self,request):
#         return redirect('/viewcart/')


# class Less_item_incart(View):
#     def post(self,request):
#         pid=request.POST.get('pid')
#         index=request.session.get('index')
#         item=int(index[pid])
#         if item==1:
#             # messages.warning(request,"Quantity must be 1 !!")
#             # index.pop(pid)
#             del index[pid]
#             request.session['index']=index
#             return JsonResponse({'success': False, 'message': 'This items deleted...','redirect_url': '/viewcart/'}, status=200)
#         else:    
#             item=item-1
#             index[pid]=str(item)
#         request.session['index']=index
#         return JsonResponse({'success': True, 'redirect_url': '/viewcart/'},status=200)
#     def get(self,request):
#         return redirect('/viewcart/')   

class Delete_item_incart(View):
    def post(self, request):
        pid = request.POST.get('pid')
        index = request.session.get('index', {})
        if pid in index:
            del index[pid]
            request.session['index'] = index
            if not index:
                messages.warning(request, "No items in cart!!!")
                return JsonResponse({'success': True, 'empty_cart': True})
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'message': 'Item not found in cart'})
    def get(self,request):
        return redirect('/viewcart/')
        

# class Delete_item_incart(View):
#     def get(self,request,pid):
#         index=request.session.get('index')
#         # index=request.session.get('button')
#         cats=Category.objects.all()
#         # index.pop(pid)
#         del index[pid]
#         # index=request.session.get('index')
#         # index.pop(cartid)
#         # request.session['cartindex']=cart
#         request.session['index']=index
#         if not index:
#             messages.warning(request,"No items in cart!!!")
#         # return redirect('/viewcart/')
#         data={'cats':cats,'index':index}
#         return render(request,"usersite/indexcart.html",data)


        
class Checkout_view(View):
    def post(self,request):
        # cats=Category.objects.all()
        # for k,v in request.session.items():
        #     print(k,"=>",v)
        # address = Address.objects.get(id=id)
        # if not pcart:
        #     messages.warning(request,"Empty Cart!!")
        # data = {'msg':"congrates"}
        id = request.POST.get('addid')
        pcart = request.session.get('pcart')
        request.session['address_id'] = id
        return render(request,"usersite/checkout.html",{'pcart': pcart})
    def get(self,request):
        user=request.session.get('cuser')
        if not user:
            return HttpResponseRedirect('/login/')
        return redirect('/profile/viewcart/address/')
    
class Invoice_view(View):
    def get(self,request):
        user=request.session.get('cuser')
        if not user:
            return HttpResponseRedirect('/login/')
        # cats=Category.objects.all()
        # prods=Product.objects.all()
        # pcart=request.session.get('pcart')
        # data={'cats':cats,'pcart':pcart}
        try:
            pcart = request.session.get('pcart')
            id = request.session.get('address_id')
            address = Address.objects.get(id = id)
            return render(request,"usersite/invoice.html",{'pcart': pcart, 'address': address})
        except:
            return redirect('/profile/viewcart/checkout/')
    
from django.core.mail import EmailMessage

class DownloadInvoice_view(View):
    def post(self,request):
        try:
            # id = request.session.get('cid')
            # print(id)
            # cobj = Customer.objects.get(id = id)
            subject = "This is Your Product Invoice"
            message = "Generated by Nature E-Commerce"
            from_to = settings.EMAIL_HOST_USER
            recipient_list = ['mksharma8808@gmail.com']
            obj = EmailMessage(subject=subject , body = message ,from_email = from_to ,to = recipient_list)
            obj.attach_file("media/invoice_pdf/E-Commerce Website.pdf")
            obj.send()
            return JsonResponse({'success': True, 'message': "send to"})
        except Exception as msg:
            return JsonResponse({'error': False, 'message': str(msg)})
            # return HttpResponse(str(msg))
        

class Address_view(View):
    def get(self,request):
        user = request.session.get('cuser')
        if not user:
            return HttpResponseRedirect('/login/')
        id = request.session.get('cid')
        address = Address.objects.filter(cust_reference = id)
        return render(request,"usersite/address.html",{'address': address})

ref = None

class EditAddress_view(View):
    def post(self,request):
        id = request.POST.get('addid')
        request.session['update_address_id'] = id
        address = Address.objects.get(id = id)
        # request.session['update_customer_id'] = address.cust_reference
        global ref
        ref = address.cust_reference
        return render(request,"usersite/EditAddress.html",{'address': address})
    def get(self,request):
        try:
            user=request.session.get('cuser')
            if not user:
                return HttpResponseRedirect('/login/')
            # id = request.POST.get('addid')
            id = request.session.get('update_address_id')
            address = Address.objects.get(id = id)
            # request.session['update_customer_id'] = address.cust_reference
            # global ref
            # ref = address.cust_reference
            return render(request,"usersite/EditAddress.html",{'address': address})
        except:
            return HttpResponseRedirect('/profile/viewcart/address/')

class UpdateAddress_view(View):
    def post(self,request):
        title = request.POST.get("title")
        first_name = request.POST.get("first-name")
        last_name = request.POST.get("last-name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        postal = request.POST.get("postal")
        id = request.session.get('update_address_id')
        cname = f'{title} {first_name} {last_name}'
        add_obj=Address(id=id,cname=cname,phone=phone,address=address,city=city,state=state,postal=postal,cust_reference=ref)
        add_obj.save()
        return HttpResponseRedirect('/profile/viewcart/address/')
 
class Product_detail_view(View):
    def get(self,request):
        return render(request,"usersite/product_detail.html") 
    
class NewAddress_create_view(View):
    def get(self,request):
        user=request.session.get('cuser')
        if not user:
            return HttpResponseRedirect('/login/')
        return render(request,"usersite/newaddress.html")
    def post(self,request):
        title = request.POST.get("title")
        first_name = request.POST.get("first-name")
        last_name = request.POST.get("last-name")
        # email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        # address2 = request.POST.get("address2")
        city = request.POST.get("city")
        state = request.POST.get("state")
        postal = request.POST.get("postal")
        id=request.session.get('cid')
        obj=Customer.objects.get(id=id)
        cname=f'{title} {first_name} {last_name}'
        add_obj=Address(cname=cname,phone=phone,address=address,city=city,state=state,postal=postal,cust_reference=obj)
        add_obj.save()
        return HttpResponseRedirect('/profile/viewcart/address/')
        
from UserApp.models import Profile 

class Customerprofile_view(View):
    def get(self,request):
        # cats=Category.objects.all()
        # data={'cats':cats,'msg':"hello"}
        return render(request,"usersite/profile.html")

class ChangeImg_view(View):
    def post(self,request):
        try:
            id = request.session['cid']
            im = request.FILES['profileImage']
            cobj = Customer.objects.get(id = id)
            pobj = Profile.objects.get(reference = cobj)
            pobj.image = im
            # pobj.save()
        except:
            pobj = Profile(name=' ', fname=' ', image=im, address=' ', phone=' ', gender=' ', reference=cobj)
            # print("confirm")
        else:
            pass
        finally:
            pobj.save()
            return redirect('/profile/details/')
        

class DeleteImg_view(View):
    def get(self,request):
        try:
            id = request.session['cid']
            cobj = Customer.objects.get(id = id)
            pobj = Profile.objects.get(reference = cobj)
            pobj.image.delete()
        except:
            pass
        finally:
            return redirect('/profile/details/')
        
    # def get(self,request):
    #     cats=Category.objects.all()
    #     data={'cats':cats,'msg1':"congrates",'msg':"hello"}
    #     return render(request,"usersite/profile.html",data)
class ChangeProfile_view(View):
    def post(self,request):
        try:
            id = request.session['cid']
            cobj = Customer.objects.get(id = id)
            n = request.POST.get('fullName')
            fn = request.POST.get('fatherName')
            ph = request.POST.get('phone')
            add = request.POST.get('address')
            g = request.POST.get('gender')
            reference = Profile.objects.get(reference = cobj)
            # To update profile table
            obj = Profile(id=reference.id, name=n, fname=fn, phone=ph, address=add, gender=g, reference=cobj, image=reference.image)
            # obj.save()
            # return redirect('/profile/details/')
        except:
            obj = Profile(name=n, fname=fn, phone=ph, address=add, gender=g, reference=cobj)
        finally:
            obj.save()
            return redirect('/profile/details/')
    
# class Changepwd_view(View):
#     def post(self,request):
#         id = request.session['cid']
#         cobj = Customer.objects.get(id = id)
#         cpass=request.POST.get('currentPassword')
#         # print(cobj.cpass,type(cobj.cpass))
#         # print(cpass,type(cpass))
#         if str(cpass) != cobj.password:
#             messages.warning(request,"Invalid Current Password")
#             return redirect('/profile/profile_details/')
#         newpass=request.POST.get('newPassword')
#         renewpass=request.POST.get('renewPassword')
#         if newpass != renewpass:
#             messages.warning(request,"Invalid Re-new Password")
#             return redirect('/profile/profile_details/')
#         obj=Customer(id=id,cpass=newpass,name=cobj.name,fname=cobj.fname,email=cobj.email,image=cobj.image,phone=cobj.phone,gender=cobj.gender,address=cobj.address)
#         obj.save()
#         messages.success(request,"Successfully Changed")
#         return redirect('/profile/profile_details/')
    
class Changepwd_view(View):
    def post(self, request):
        id = request.session['cid']
        cobj = Customer.objects.get(id=id)
        cpass = request.POST.get('currentPassword')
        
        if str(cpass) != cobj.password:
            return JsonResponse({"message": "Invalid Current Password"}, status=400)
        
        newpass = request.POST.get('newPassword')
        renewpass = request.POST.get('renewPassword')
        
        if newpass != renewpass:
            return JsonResponse({"message": "Invalid Re-new Password"}, status=400)
        
        cobj.password = newpass
        cobj.save()
        return JsonResponse({"message": "Successfully Changed"}, status=200)    

    
