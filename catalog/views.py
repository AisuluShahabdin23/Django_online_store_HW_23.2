from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin, UserPassesTestMixin
from django.forms import inlineformset_factory
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy, reverse

from catalog.forms import ProductForm, VersionForm, ProductModerForm
from catalog.models import Product, Version  # , Category
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from catalog.services import cache_category


# def home(request):
#     category_list = Category.objects.all()
#     context = {
#         'object_list': category_list,
#         'title': 'Главная'
#     }
#     return render(request, 'catalog/home.html', context)


class ProductListView(PermissionRequiredMixin, ListView):
    model = Product
    template_name = 'catalog/home.html'
    permission_required = 'catalog.product'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return cache_category()


def contacts(request):
    context = {
        'title': 'Контакты',
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'Name: {name}\n Phone: {phone}\n Message: {message}')
    return render(request, 'catalog/contacts.html', context)


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'catalog/product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['version'] = Version.objects.filter(product=self.kwargs['pk'])
        return context


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        if form.is_valid:
            new_product = form.save()
            new_product.user = self.request.user
            new_product.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    permission_required = 'catalog.update'
    success_url = reverse_lazy('catalog:home')

    def get_success_url(self):
        return reverse('catalog.update', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        else:
            return self.form_invalid(form)
        return super().form_valid(form)

    # def test_func(self):
    #     if self.request.user.is_staff:
    #         return False
    #     return self.request.user == Product.objects.get(pk=self.kwargs['pk']).user

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if (self.request.user != self.object.user and not self.request.user.is_staff
                and not self.request.user.is_superuser and self.request.user.has_perm('catalog.product_published')):
            raise Http404
        return self.object

    def get_form_class(self):
        if self.request.user.is_staff:
            return ProductModerForm
        return ProductForm


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:home')


class VersionListView(LoginRequiredMixin, ListView):
    model = Version
