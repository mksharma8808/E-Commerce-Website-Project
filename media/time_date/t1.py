import datetime
import os
from django.conf import settings
from AdminApp.models import Product

def time_date():
    try:
        fp=open(settings.BASE_DIR/"media/time_date/minute.txt","r")
        fp1=open(settings.BASE_DIR/"media/time_date/minute1.txt","w")
        data=fp.readline()
        val=data.split(",")
        t=datetime.datetime.now()
        if int(val[1])<3:
            d=str(int(val[1])+1)
            fp1.write("c,"+d+",\n")
            fp1.close()
            fp.close()
            os.remove(settings.BASE_DIR/"media/time_date/minute.txt")
            os.rename(settings.BASE_DIR/"media/time_date/minute1.txt",settings.BASE_DIR/"media/time_date/minute.txt")
            data="Attemped "+d+" failed Check your username & password!!"
            return (data,int(d))
        elif int(val[1])==3:
            dt=datetime.datetime.now()+datetime.timedelta(minutes=5)
            hour=t.strftime("%I")
            fp1.write("attemp,4,hour,"+hour+",min,"+str(dt.minute)+",sec,"+str(dt.second)+",\n")
            fp.close()
            fp1.close()
            os.remove(settings.BASE_DIR/"media/time_date/minute.txt")
            os.rename(settings.BASE_DIR/"media/time_date/minute1.txt",settings.BASE_DIR/"media/time_date/minute.txt")
            data="You are 5 min block"
            return (data,4)
    
        else:
            if int(val[3])>=int(t.strftime("%I")) and int(val[5])>=int(t.minute):
                fp1.close()
                os.remove(settings.BASE_DIR/"media/time_date/minute1.txt")
                data="You are blocked"
                return (data,5)
            else:
                fp.close()
                fp1.close()
                os.remove(settings.BASE_DIR/"media/time_date/minute.txt")
                os.remove(settings.BASE_DIR/"media/time_date/minute1.txt")
                data="Timer out Admin!!"
                return (data,0)
    except:
        fp=open(settings.BASE_DIR/"media/time_date/minute.txt","w")
        fp.write("c,1,\n")
        fp.close()
        data="Attemped 1 failed Check your username & password!!"
        return (data,1)


def check_time():
    try:
        fp=open(settings.BASE_DIR/"media/time_date/minute.txt","r")
        data=fp.readline()
        t=datetime.datetime.now()
        val=data.split(",")
        if int(val[3])>=int(t.strftime("%I")) and int(val[5])>=int(t.minute):
            data="You are blocked"
            return (data,1)
        else:
            fp.close()
            os.remove(settings.BASE_DIR/"media/time_date/minute.txt")
            data="success"
            return (data,2)
    except:
        data="success"
        return (data,0)
    
    
def Mansoon():
    dt=datetime.datetime.now()
    mon=int(dt.strftime("%m"))
    if mon>=12 and mon<=2:
        return 'winter'
    elif mon>=3 and mon<=5:
        return 'summer'
    elif mon>=6 and mon<=9:
        return 'rainy season'
    else:
        return 'retreating'
    # return prods