from django.views.generic import TemplateView, ListView, DetailView


from safemasks.resources.models import Product, Supplier


class IndexView(TemplateView):
    template_name = "index.html"


class ProductListView(ListView):
    model = Product
    template_name = "product_list_view.html"


class TrustedProductView(ListView):
    model = Product
    template_name = "trusted_product_view.html"


class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail_view.html"


class SupplierListView(ListView):
    model = Supplier
    template_name = "supplier_list_view.html"


class SupplierDetailView(DetailView):
    model = Supplier
    template_name = "supplier_detail_view.html"
