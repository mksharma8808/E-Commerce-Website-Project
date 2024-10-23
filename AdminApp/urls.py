from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('',views.Index.as_view()),
    path('dashboard/', views.Dashboard_view.as_view(),name="dashboard"),
    path('dashboard/logout/', views.Adminlogout_view.as_view(),name="dashboard/logout"),
    path('dashboard/addcategory/', views.Addcategory_view.as_view(),name="dashboard/addcategory"),
    path('dashboard/addproduct/', views.Addproduct_view.as_view(),name="dashboard/addproduct"),
    path('dashboard/viewproduct/', views.Viewproduct_view.as_view(),name="dashboard/viewproduct"),
    path('dashboard/viewcategory/', views.Viewcategory_view.as_view(),name="dashboard/viewcategory"),
    path('dashboard/viewcustomer/', views.Viewcustomer_view.as_view(),name="dashboard/viewcustomer"),
    path('dashboard/viewproduct/edit/<pid>', views.Edit_product_view.as_view(),name="dashboard/viewproduct/edit"),
    path('dashboard/viewproduct/delete/<pid>', views.Delete_product_view.as_view(),name="dashboard/viewproduct/delete"),
    path('dashboard/viewproduct/view/<pid>', views.Product_view.as_view(),name="dashboard/viewproduct/view"),
    path('dashboard/viewcustomer/profile/<cid>/', views.Customerprofile_view.as_view(),name="dashboard/viewcustomer/profile"),
    path('dashboard/viewcustomer/delprofile/<cid>', views.Delcustomerprofile_view.as_view(),name="dashboard/viewcustomer/delprofile"),
    path('dashboard/viewcategory/catdelete/<cid>', views.Delete_category_view.as_view(),name="dashboard/viewcategory/catdelete"),
    path('dashboard/viewcategory/rename_category/<cid>', views.Rename_category_view.as_view(),name="dashboard/viewcategory/rename_category"),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)