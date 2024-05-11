from django.shortcuts import render, HttpResponseRedirect, redirect

from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout

from django.urls import reverse_lazy, reverse

from django.contrib import messages

from .models import BusRoute

class RouteListView(ListView):
    model = BusRoute
    template_name = 'route_list.html'
    context_object_name = 'routes'

    def get_context_data(self):

        context = super().get_context_data()

        if 'route' in self.request.GET:
            context['searched_route'] = self.request.GET.get('route')
            context['routes'] = context['routes'].filter(bus_route_name__icontains = self.request.GET.get('route'))

        return context

route_list = RouteListView.as_view()


class RouteCreateView(PermissionRequiredMixin, CreateView):

    permission_required = ["bus_locater_app.add_busroute",]

    model = BusRoute
    template_name = 'route_list.html'
    fields = ['bus_route_name','bus_number']

    def get_context_data(self):
        context = super().get_context_data()

        context['routes'] = BusRoute.objects.all()
        context['create'] = 'create'

        if 'route' in self.request.GET:
            context['searched_route'] = self.request.GET.get('route')
            context['routes'] = context['routes'].filter(bus_route_name__icontains = self.request.GET.get('route'))


        return context

    def form_valid(self,form):

        bus_route_name = self.request.POST.get('bus_route_name')
        bus_number = self.request.POST.get('bus_number')

        messages.success(
            self.request,
            f'route {bus_route_name} with bus {bus_number} has been successfully added'
        )

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('route-create')

route_create = RouteCreateView.as_view()

class UpdateBusRouteView(PermissionRequiredMixin, UpdateView):

    permission_required = ["bus_locater_app.change_busroute",]

    model = BusRoute
    fields = ['bus_route_name','bus_number']
    template_name = 'route_list.html'

    def form_valid(self,form):
        print(self.request.POST)

        bus_route_name = self.request.POST.get('bus_route_name')
        bus_number = self.request.POST.get('bus_number')

        messages.success(
            self.request,
            f'route {bus_route_name} with bus {bus_number} has been successfully updated'
        )

        return super().form_valid(form)

    def get_context_data(self):
        context = super().get_context_data()

        context['routes'] = BusRoute.objects.all()

        return context

    def get_success_url(self):

        return reverse_lazy('route-create')

route_update = UpdateBusRouteView.as_view()

class DeleteBusRouteView(PermissionRequiredMixin, DeleteView):

    permission_required = ["bus_locater_app.delete_busroute"]

    model = BusRoute
    template_name = 'route_list.html'
    

    def post(self, request, *args, **kwargs):

        self.object = self.get_object()
        form = self.get_form()

        messages.success(
            self.request,
            f'Route "{self.object.bus_route_name}" with bus {self.object.bus_number} has been successfully deleted'
        )

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('route-create')

route_delete = DeleteBusRouteView.as_view()

class customLoginView(LoginView):

    template_name = 'accounts/login.html'
    fields = '__all__'
    
    def get_success_url(self):
        return reverse_lazy('route-create')

    

login_view = customLoginView.as_view()


def logout_view(request):
    logout(request)

    return redirect('route-list')
