from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate
from django.shortcuts import HttpResponse

def start(request):
        return redirect('account/')