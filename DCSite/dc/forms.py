from django import forms


class submit_dc(forms.Form):
	process_name = forms.CharField(max_length=14)
	trim_func = forms.CharField(widget=forms.Textarea)
	map_func = forms.CharField(widget=forms.Textarea)
	reduce_func = forms.CharField(widget=forms.Textarea)


class run_dc(forms.Form):
	process_code = forms.CharField(max_length=32)
	parameter = forms.CharField(widget=forms.Textarea)
	machines_count = forms.CharField(max_length=2)