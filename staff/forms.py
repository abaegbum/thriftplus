from django import forms




class staffform(forms.Form):
	email = forms.EmailField(label = 'Staff Email',widget = forms.TextInput(attrs={'required':'required'}))


class fieldofficerfform(forms.Form):
	email = forms.EmailField(label = 'Staff Email',widget = forms.TextInput(attrs={'required':'required'}))



