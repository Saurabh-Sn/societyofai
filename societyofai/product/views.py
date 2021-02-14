from django.shortcuts import render
from django.views.generic import ListView, DetailView, View
from  .models import Product
# Create your views here.


class HomeView(ListView):
    model = Product
    paginate_by = 10
    template_name = "home.html"
