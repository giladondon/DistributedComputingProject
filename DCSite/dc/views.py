from django.shortcuts import render
from django.http import HttpResponse
from .forms import submit_feature
import os


def submit_feature_response(request):
	return HttpResponse("Hello world you are submitting a feature")


def access_feature_response(request):
	return HttpResponse("Hello world you are accessing a feature")


def get_feature(request):
	if request.method == 'POST':
		form = submit_feature(request.POST)
		if form.is_valid():
			process_name = form.cleaned_data['process_name']
			trim_func = form.cleaned_data['trim_func']
			map_func = form.cleaned_data['map_func']
			reduce_func = form.cleaned_data['reduce_func']
			return HttpResponseRedirect('/thanks/')

	else:
		form = submit_feature()

	return render(request, os.path.dirname(os.path.realpath(__file__)) + os.sep + os.sep.join(['templates', 'SubmitFeature', 'SubmitFeat.html']))