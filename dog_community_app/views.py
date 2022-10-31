from datetime import datetime

from django.shortcuts import (get_object_or_404,
                              render,
                              HttpResponseRedirect)

from django.views.generic.edit import (CreateView, UpdateView, DeleteView, FormView)
from django.views.generic.detail import DetailView


# Create your views here.

from django.http import HttpResponse

from django.views.generic.list import ListView

from django.views import View

# class MyView(View):
#     def get(self, request):
#         # <view logic>
#         return HttpResponse('result')

# class GeeksCreate(CreateView):
#     # specify the model for create view
#     model = GeeksModel
#     # specify the fields to be displayed
#     fields = ['title', 'description']
#     def form_valid(self, form) -> HttpResponse:
#         form.save()
#         return HttpResponseRedirect("/")

# class GeeksList(ListView):
#     # specify the model for list view
#     model = GeeksModel

# class GeeksDetailView(DetailView):
#     # specify the model to use
#     model = GeeksModel

# class GeeksUpdateView(UpdateView):
#     # specify the model you want to use
#     model = GeeksModel
 
#     # specify the fields
#     fields = [
#         "title",
#         "description"
#     ]
 
#     # can specify success url
#     # url to redirect after successfully
#     # updating details
#     success_url ="/get/"

# class GeeksDeleteView(DeleteView):
#     # specify the model you want to use
#     model = GeeksModel
     
#     # can specify success url
#     # url to redirect after successfully
#     # deleting object
#     success_url ="/get/"

# class GeeksFormView(FormView):
#     # specify the Form you want to use
#     form_class = GeeksForm
     
#     # specify name of template
#     template_name = "geeks / geeksmodel_form.html"
 
#     # can specify success url
#     # url to redirect after successfully
#     # updating details
#     success_url ="/thanks/"

# function based

def home_view(request):
    return render(request, "index.html")
def aboutus_view(request):
    return render(request, "aboutus.html")
def breedinfo_view(request):
    return render(request, "breedinfo.html")
def reportadog(request):
    return render(request, "reportadog.html")
def meetup_view(request):
    return render(request, "meetup.html")
def adoption_view(request):
    return render(request, "adoption.html")
def contact_view(request):
    return render(request, "contact.html")


