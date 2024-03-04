from django.urls import path
from EcommerceApp import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from .forms import LoginForm,MyPasswordResetForm,MyPasswordChangeForm,MySetPasswordForm

urlpatterns = [
    path('',views.home,name="home"),
    path('about/',views.about,name="about"),
    path('contact/',views.contact,name="contact"),
    path("category/<slug:val>",views.CategoryView.as_view(), name="category"),
    path("category-title/<val>",views.CategoryTitle.as_view(), name="category-title"),
    path("product-details/<int:pk>",views.ProductDetail.as_view(), name="product-detail"),
    path("profile/",views.ProfileView.as_view(), name="profile"),
    path("address/",views.address, name="address"),
    path("updateAddress/<int:pk>",views.UpdateAddress.as_view(), name="update-address"),
    # add to cart urls
    path("add-to-cart/",views.add_to_cart, name="add-to-cart"),
    path("cart/",views.show_cart, name="show-cart"),
    path("checkout/",views.Checkout.as_view(), name="checkout"),
    path("pluscart/",views.plus_cart, name="pluscart"),
    path("minuscart/",views.minus_cart, name="minuscart"),
    path("removecart/",views.remove_cart, name="removecart"),

    # login authentication urls
    path('registration/',views.CustomerRegView.as_view(), name='registration'),
    path('login/',auth_view.LoginView.as_view(template_name='login.html', authentication_form=LoginForm),name='login'),
    path('password-change/',auth_view.PasswordChangeView.as_view(template_name='password_change.html',success_url='/password-change-done')
         ,name='password-change'),
    path('password-change-done/',auth_view.PasswordChangeView.as_view(template_name='password_change_done.html',form_class=MyPasswordChangeForm),
         name='password-change-done'),
    path('logout/',auth_view.LogoutView.as_view(next_page='login'),name='logout'),
    # password reset urls
    path('password-reset/',auth_view.PasswordResetView.as_view(template_name='password_reset.html',form_class=MyPasswordResetForm),name='password-reset'),
    path('password-reset/done/',auth_view.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),name='password-reset-done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_view.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html', form_class=MySetPasswordForm),
         name='password-reset-confirm'),
    path('password-reset-complete/',auth_view.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name='password-reset-complete'),

] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)