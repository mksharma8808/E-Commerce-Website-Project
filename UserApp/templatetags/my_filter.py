from django import template
from UserApp.models import Customer
from AdminApp.models import Product
from AdminApp.models import Category
register=template.Library()

@register.filter
def Currency(val):
    return "₹"+str(int(val))

@register.filter
def Check(product,cart):
    ks=cart.keys()
    for k in ks:
        if product.id==int(k):
            return True
    return False

@register.filter
def Qty_Product(product,pcart):
    try:
        ks=list(pcart.keys())
        ks=ks[1:]
        for k in ks:
            if product.id==int(k):
                return pcart[k]
        return 1
    except:
        return 1

@register.filter
def Filtercategory(id):
    try:
        cobj=Category.objects.get(id=id)
        return cobj.name
    except:
        return False

@register.filter
def CategoryName(cid):
    cobj=Category.objects.get(id=cid)
    return cobj.name
        
        
@register.filter
def Qtyindex_Product(product,pcart):
    try:
        ks=list(pcart.keys())
        for k in ks:
            if product.id==int(k):
                if pcart[k]<=product.item_qty:
                    return pcart[k]
                else:
                    return product.item_qty
        return 1
    except:
        return 1
    
@register.filter    
def Check_Qty(product,pid):
    try:
        ks=list(pid.keys())
        for k in ks:
            if product.id == int(k):
                if product.item_qty>pid[k]:
                    return True
                else:
                    return False
        return True
    except:
        return True

@register.filter
def Counter(cart):
    try:
        l=len(cart.keys())
        if l>0:
            return l
    except:
        return False
    
@register.filter
def CheckButton(product,index):
    try:
        ls=list(index.keys())
        # ls=ls[1:]
        for k in ls:
            if product.id == int(k):
                return True
        else:
            False
    except:
        return False

@register.filter
def Button(button,product):
    try:
        key=button.keys()
        if str(product.id) in key:
            return True
        return False
    except:
        return False
    
@register.filter
def Image(cid):
    try:
        cobj=Customer.objects.get(id=cid)
        return cobj.image.url
    except:
        return 0

@register.filter
def CustName(cid):
    cobj=Customer.objects.get(id=cid)
    return cobj.name.split(' ')[0]

@register.filter
def CustPhone(cid):
    cobj=Customer.objects.get(id=cid)
    return cobj.phone

@register.filter
def CustEmail(cid):
    cobj=Customer.objects.get(id=cid)
    return cobj.email

@register.filter
def CustFname(cid):
    cobj=Customer.objects.get(id=cid)
    return cobj.fname

@register.filter
def CustAdd(cid):
    cobj=Customer.objects.get(id=cid)
    return cobj.address

@register.filter
def Gender(cid):
    obj=Customer.objects.get(id=cid)
    if obj.gender=="male":
        return "mr"
    return "miss"

@register.filter
def GenderCheck(cid):
    obj=Customer.objects.get(id=cid)
    return obj.gender

@register.filter
def UserImage(cid):
    return cid.image.url

@register.filter
def Cust(cid):
    cobj=Customer.objects.get(id=cid)
    return cobj.name

@register.filter
def CatName(cname,prodname):
    if str(cname)==str(prodname):
        return False
    else:
        return True
    
@register.filter
def Icon(msg):
    if str(msg)=="warning":
        return "exclamation-triangle"
    elif str(msg)=="info":
        return "info-circle"
    elif str(msg)=="success":
        return "check-circle"
    elif str(msg)=="danger":
        return "exclamation-octagon"
    elif str(msg)=="light":
        return "star"
    elif str(msg)=="dark":
        return "folder"
    elif str(msg)=="secondary":
        return "collection"
    else:
        return 0
    
    
@register.filter
def CheckId(id):
    obj=Product.objects.get(id=int(id))
    return obj.id

@register.filter
def CheckName(id):
    obj=Product.objects.get(id=int(id))
    return obj.name

@register.filter
def CheckPrice(id):
    obj=Product.objects.get(id=int(id))
    return Currency(obj.price)

@register.filter
def CheckCategory(id):
    obj=Product.objects.get(id=int(id))
    return obj.Category

@register.filter
def CheckQty(id,index):
    qty=index[id]
    return qty

@register.filter
def Total(id,cart):
    qty=cart[id]
    pobj=Product.objects.get(id=int(id))
    t=int(qty)*pobj.price
    return Currency(t)

@register.filter
def CheckIndex(index,product):
    try:
        ks=list(index.keys())
        for k in ks:
            if product.id == int(k):
                return True
        else:
            return False
    except:
        return False
    
    
@register.filter
def Subtotal(cart,custcart):
    try:
        ks=list(cart.keys())
        s=0
        for k in ks:
           s=s+int(Total(k,custcart)[1:])
        return Currency(s)
    except:
        return 0
    
@register.filter
def Discount(cart,custcart):
    price=Subtotal(cart,custcart)
    p=int(price[1:])
    return Currency(str((p*5)//100))

@register.filter
def TotalAmount(cart,custcart):
    price=Subtotal(cart,custcart)
    dis=Discount(cart,custcart)
    pri=int(price[1:])
    disc=int(dis[1:])
    return Currency(str(pri-disc))
    
@register.filter
def QtyProduct(product,pid):
    ks=list(pid.keys())
    for k in ks:
        if product.id==int(k):
            if pid[k]<product.item_qty:
                return product.item_qty-pid[k]
            else:
                return 0
    return product.item_qty

@register.filter
def CheckCats(cats,c):
    # cobj=Category.objects.all()
    if c.id != cats:
        return True
    return False

@register.filter
def FilterName(name):
    name = name.split(" ")
    name = ' '.join(name[1:])
    return name

@register.filter
def TitleName(name):
    name = name.split(" ")
    return name[0]

@register.filter
def FirstName(name):
    name = name.split(" ")
    return name[1]

@register.filter
def LastName(name):
    name = name.split(" ")
    return name[0]