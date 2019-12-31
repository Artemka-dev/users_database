from django.shortcuts import render, redirect
from django.http import HttpResponse

def redirect_to(request):
	return redirect("login")