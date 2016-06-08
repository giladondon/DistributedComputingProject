from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from .forms import submit_dc, run_dc
from .models import DCProcess
import os
import uuid


def get_run(request):
	if request.method == 'POST':
		form = run_dc(request.POST)
		if form.is_valid():
			process_code = form.cleaned_data['process_code']
			parameter = form.cleaned_data['parameter']
			machines_count = form.cleaned_data['machines_count']

			directory = os.sep.join(['templates', 'results.html'])
			return render(request, os.path.dirname(os.path.realpath(__file__))+os.sep+directory, 
				{'process_name': 'Hello World', 'result': 'NADA'})

	directory = os.sep.join(['templates', 'RunDC', 'RunDC.html'])
	return render(request, os.path.dirname(os.path.realpath(__file__))+os.sep+directory)


def get_process(request):
	if request.method == 'POST':
		form = submit_dc(request.POST)
		if form.is_valid():
			process_name = form.cleaned_data['process_name']
			trim_func = form.cleaned_data['trim_func']
			map_func = form.cleaned_data['map_func']
			reduce_func = form.cleaned_data['reduce_func']
			process_code = uuid.uuid4().hex
			process = DCProcess.create(process_name, trim_func, map_func, reduce_func, process_code)
			print process

			details_view = os.sep.join(['templates', 'dcDetails.html'])
			return render(request, os.path.dirname(os.path.realpath(__file__))+os.sep+details_view, 
				{'process_name': process_name, 'process_code': process.process_code})

	directory = os.sep.join(['templates', 'SubmitDC', 'SubmitDC.html'])
	return render(request, os.path.dirname(os.path.realpath(__file__))+os.sep+directory)


def not_found(request):
	directory = os.sep.join(['templates', 'pageNotFound.html'])
	return render(request, os.path.dirname(os.path.realpath(__file__))+os.sep+directory)


def home_page(request):
	directory = os.sep.join(['templates', 'dcHome.html'])
	return render(request, os.path.dirname(os.path.realpath(__file__))+os.sep+directory)
