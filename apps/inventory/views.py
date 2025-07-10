from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import ProductForm
from .models import Product


class ProductListView(ListView):
    model = Product
    template_name = "inventory/product_list.html"
    context_object_name = "products"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().order_by("nome")
        search_query = self.request.GET.get("search", None)
        filter_type = self.request.GET.get("filter", None)

        if search_query:
            queryset = queryset.filter(Q(nome__icontains=search_query))

        if filter_type:
            if filter_type == "normal":
                queryset = queryset.filter(estoque__gt=5)
            elif filter_type == "low":
                queryset = queryset.filter(estoque__lte=5, estoque__gt=0)
            elif filter_type == "out":
                queryset = queryset.filter(estoque=0)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_products = Product.objects.all()
        context["low_stock_count"] = all_products.filter(
            estoque__lte=5, estoque__gt=0
        ).count()
        context["out_of_stock_count"] = all_products.filter(estoque=0).count()
        context["total_stock"] = sum(product.estoque for product in all_products)

        context["search_query"] = self.request.GET.get("search", "")
        context["current_filter"] = self.request.GET.get("filter", "")
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "inventory/product_detail.html"
    context_object_name = "product"


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = "inventory/product_form.html"
    success_url = reverse_lazy("inventory:product_list")

    def form_valid(self, form):
        messages.success(self.request, "Product created successfully.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_create_form"] = True
        return context


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "inventory/product_form.html"
    success_url = reverse_lazy("inventory:product_list")

    def form_valid(self, form):
        messages.success(self.request, "Product updated successfully.")
        return super().form_valid(form)


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("inventory:product_list")
    context_object_name = "product"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()

        product_name = self.object.nome
        self.object.delete()

        messages.success(
            self.request, f"Produto '{product_name}' excluído com sucesso."
        )

        return HttpResponseRedirect(success_url)


@require_POST
@csrf_protect
def adjust_stock(request):
    try:
        product_id = request.POST.get("product_id")
        operation = request.POST.get("operation")
        quantity = int(request.POST.get("quantity", 0))

        if not all([product_id, operation, quantity]):
            return JsonResponse(
                {"success": False, "message": "Dados incompletos fornecidos."}
            )

        product = get_object_or_404(Product, pk=product_id)

        if operation == "add":
            product.estoque += quantity
            action = "adicionadas"
        elif operation == "subtract":
            if product.estoque < quantity:
                return JsonResponse(
                    {"success": False, "message": "Quantidade insuficiente em estoque."}
                )
            product.estoque -= quantity
            action = "removidas"
        else:
            return JsonResponse({"success": False, "message": "Operação inválida."})

        product.save()

        return JsonResponse(
            {
                "success": True,
                "message": f"{quantity} unidades {action} do estoque de {product.nome}.",
                "new_stock": product.estoque,
            }
        )

    except ValueError:
        return JsonResponse(
            {"success": False, "message": "Quantidade deve ser um número válido."}
        )
    except Product.DoesNotExist:
        return JsonResponse({"success": False, "message": "Produto não encontrado."})
    except Exception:
        return JsonResponse({"success": False, "message": "Erro interno do servidor."})
