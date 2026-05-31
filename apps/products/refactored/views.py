# from django.shortcuts import render

# Create your views here.
# from django.views.generic import ListView
# from .models import Product

# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from .forms import ProductForm, ManufacturingForm, OwnerForm


# class ProductListView(ListView):
#     model = Product
#     paginate_by = 10
#     template_name = "product/list.html"


# @login_required
# def product_create(request):
#     if request.method == "POST":
#         product_form = ProductForm(request.POST, request.FILES)
#         manufacturing_form = ManufacturingForm(request.POST)
#         owner_form = OwnerForm(request.POST)

#         if all(
#             [
#                 product_form.is_valid(),
#                 manufacturing_form.is_valid(),
#                 owner_form.is_valid(),
#             ]
#         ):
#             product = product_form.save(commit=False)
#             product.user = request.user
#             product.save()

#             manufacturing = manufacturing_form.save(commit=False)
#             manufacturing.product = product
#             manufacturing.save()

#             owner = owner_form.save(commit=False)
#             owner.product = product
#             owner.save()

#             return redirect("dashboard")

#     else:
#         product_form = ProductForm()
#         manufacturing_form = ManufacturingForm()
#         owner_form = OwnerForm()

#     return render(
#         request,
#         "product/create.html",
#         {
#             "product_form": product_form,
#             "manufacturing_form": manufacturing_form,
#             "owner_form": owner_form,
#         },
#     )
