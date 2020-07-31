from django.views.generic import TemplateView, ListView, DetailView

from safemasks.masks_auth.mixins import ReviewedRequiredMixin
from safemasks.resources.models import Product, Supplier


class IndexView(TemplateView):
    template_name = "index.html"


class ProductListView(ReviewedRequiredMixin, ListView):
    model = Product
    template_name = "product_list_view.html"


class ProductDetailView(ReviewedRequiredMixin, DetailView):
    model = Product
    template_name = "product_detail_view.html"


class TrustedSuppliersView(ListView):
    model = Supplier
    template_name = "trusted_suppliers_view.html"


class SupplierListView(ReviewedRequiredMixin, ListView):
    model = Supplier
    template_name = "supplier_list_view.html"


class SupplierDetailView(ReviewedRequiredMixin, DetailView):
    model = Supplier
    template_name = "supplier_detail_view.html"
