from django.shortcuts import render,redirect
from .models import Category,Product
from UserApp.models import Customer,Profile
from django.http import HttpResponseRedirect,HttpResponse
from django.views import View
from django.contrib import messages
from django.conf import settings
import os
from media.time_date import t1


class Index(View):
    def get(self,request):
        ad=request.session.get('aduname')
        print(ad)
        if ad:
            return HttpResponseRedirect('/admin/dashboard/')
        return render(request,"adminsite/admin_login.html")
    
    def post(self,request):
        un=request.POST.get('username')
        pwd=request.POST.get('password')
        if un=="admin" and pwd=="1234":
            val=t1.check_time()
            if val[1]==1:
               messages.warning(request,val[0])
            else:
               request.session['aduname']=un
               return redirect('/admin/dashboard/')
            return render(request,"adminsite/admin_login.html")
        val=t1.time_date()
        if val[1]==0:
            messages.warning(request,val[0])
        elif val[1]<3:
            messages.warning(request,val[0])
        elif val[1]==3:
            messages.warning(request,val[0])
        else:
            messages.warning(request,val[0])
        return render(request,"adminsite/admin_login.html")   
            
        
class Dashboard_view(View):
    def get(self,request):
        return render(request,"adminsite/index.html")

class Adminlogout_view(View):
    def get(self,request):
        del request.session['aduname']
        try:
            fp=open(settings.BASE_DIR/"media/time_date/minute.txt")
            if fp:
                os.remove(settings.BASE_DIR/"media/time_date/minute.txt")
            return redirect('/')
        except:
            return redirect('/')

class Addcategory_view(View):
    def get(self,request):
        adm=request.session.get('aduname')
        if not adm:
            return HttpResponseRedirect('/admin/')
        else:
            return render(request,"adminsite/addcategory.html")
    def post(self,request):
        n=request.POST.get('cname')
        cobj=Category.objects.all()
        for c in cobj:
            if c.name == n:
                messages.warning(request,"The category already exists!!")
                return render(request,"adminsite/addcategory.html")
        d=request.POST.get('des')
        obj=Category(name=n,des=d)
        obj.save()
        messages.success(request,"Successfully added!!")
        return render(request,"adminsite/addcategory.html")
        
class Addproduct_view(View):
    def get(self,request):
        ad=request.session.get('aduname')
        if ad:
            cats=Category.objects.all()
            return render(request,"adminsite/addproduct.html",{'cats':cats})
        else:
            return HttpResponseRedirect('/admin/')
    def post(self,request):
        n=request.POST.get('name')
        p=request.POST.get('price')
        qty=request.POST.get('pqty')
        select=request.POST.get('select')
        im=request.FILES['imag']
        des=request.POST.get('des')
        # season=request.POST.get('season')
        comp=request.POST.get('comp')
        cobj=Category.objects.get(id=select)
        pobj=Product(name=n,price=p,image=im,Category=cobj,des=des,item_qty=int(qty),company=comp)
        pobj.save()
        messages.success(request,"Successfully added!!")
        return redirect('/admin/dashboard/addproduct/')
        
    
class Viewproduct_view(View):
    def get(self,request):
        ad=request.session.get('aduname')
        if ad:
            prods=Product.objects.all()
            if not prods:
                messages.warning(request,"Empty product!!!")
            data={'prods':prods}
            return render(request,"adminsite/viewproduct.html",data)
        else:
            return redirect('/admin/')       
    
class Viewcategory_view(View):
    def get(self,request):
        ad=request.session.get('aduname')
        if ad:
            cats=Category.objects.all()
            if not cats:
                messages.warning(request,"Empty Category!!!")
            data={'cats':cats}
            return render(request,"adminsite/viewcategory.html",data)
        else:
            return redirect('/admin/')
    
class Viewcustomer_view(View):
    def get(self,request):
        adm=request.session.get('aduname')
        if not adm:
            return redirect('/admin/')
        cust = Customer.objects.all().values('name','id')
        profile = Profile.objects.all().values('image','reference_id')
        # custid = Customer.objects.all().values()
        # profileid = Profile.objects.all().values()
        # print(list(cust))
        # print(list(profile))
        dict=[]
        for d in cust:
            for pro in profile:
                # if d['id'] == pro['reference_id']:
                d.update(pro)
            dict.append(d)
        # print(dict)
        # print(cust)
        # print(profile)
        data={'val':dict}
        return render(request,"adminsite/viewcustomer.html",data)
        # return HttpResponse("say hii")    

class Edit_product_view(View):    
    def post(self,request,pid):
        n=request.POST.get('name')
        p=request.POST.get('price')
        s=request.POST.get('select')
        im=request.FILES.get('imag',0)
        qty=request.POST.get('pqty')
        season=request.POST.get('season')
        if not im:
            pobj=Product.objects.get(id=pid)
            im=pobj.image
        d=request.POST.get('des')
        cobj=Category.objects.get(id=int(s))
        obj=Product(id=pid,name=n,price=p,image=im,des=d,Category=cobj,item_qty=qty,season=season)
        obj.save()
        return HttpResponseRedirect('/admin/dashboard/viewproduct/')
    def get(self,request,pid):
        prods=Product.objects.get(id=pid)
        cats=Category.objects.all()
        return render(request,"adminsite/admineditproduct.html",{'prods':prods,'cats':cats}) 

class Delete_product_view(View):
    def get(self,request,pid):
        obj=Product.objects.get(id=pid)
        obj.delete()
        prods=Product.objects.all()
        if not prods:
            messages.warning(request,"Empty product table")
        return HttpResponseRedirect('/admin/dashboard/viewproduct/')
 
class Product_view(View):
    def get(self,request,pid):
        cats=Category.objects.all()
        prods=Product.objects.get(id=pid)
        data={'cats':cats,'prods':prods}
        return render(request,"adminsite/productcard.html",data)

class Customerprofile_view(View):
    def get(self,request,cid):
        try:
            customer = Customer.objects.get(id = cid)
            profile = Profile.objects.get(reference = cid)
            # print(profile,type(profile))
            # print(profile.id)
            data = {
                'id': customer.id,
                'image': profile.image,
                'name': profile.name,
                'fname': profile.fname,
                'address': profile.address,
                'email': customer.email
            }
            # print(data)
        except Exception as msg:
            data = {
                'id': customer.id,
                'image': '',
                'name': customer.name,
                'fname': '',
                'address': '',
                'email': customer.email
            }
            print(msg)
            # return HttpResponse("something error found")
        finally:
            return render(request, "adminsite/profile.html", data)
    def post(self,request,cid):
        n=request.POST.get('fullName')
        add=request.POST.get('address')
        cobj=Customer.objects.get(id=cid)
        obj=Customer(id=cid,name=n,fname=cobj.fname,address=add,email=cobj.email,gender=cobj.gender,phone=cobj.phone,cpass=cobj.cpass,image=cobj.image)
        obj.save()
        messages.success(request,"Successfully Changed")
        return redirect('/admin/dashboard/viewcustomer/')
        

class Delcustomerprofile_view(View):
    def get(self,request,cid):
        cust=Customer.objects.get(id=cid)
        cust.delete()
        return redirect('/admin/dashboard/viewcustomer/')

class Delete_category_view(View):
    def get(self,request,cid):
        obj=Category.objects.get(id=cid)
        obj.delete()
        return HttpResponseRedirect('/admin/dashboard/viewcategory/')
    
class Rename_category_view(View):
    def get(self,request,cid):
        cats=Category.objects.get(id=cid)
        return render(request,"adminsite/category_rename.html",{'cats':cats})
    def post(self,request,cid):
        cobj=Category.objects.get(id=cid)
        # old=request.POST.get('catName')
        new=request.POST.get('newcatName')
        obj=Category(id=cobj.id,name=new,des=cobj.des)
        obj.save()
        return HttpResponseRedirect('/admin/dashboard/viewcategory/')
