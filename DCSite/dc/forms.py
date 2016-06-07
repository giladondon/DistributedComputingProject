from django import forms


class submit_feature(forms.Form):
	process_name = forms.CharField(label='ProcessName', max_length=14)
	trim_func = forms.TextInput()
	map_func = forms.TextInput()
	reduce_func = forms.TextInput()