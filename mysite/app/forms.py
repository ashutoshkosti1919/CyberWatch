from django import forms
class RFIDForm(forms.Form):
    rfid_code = forms.CharField(max_length=50, label='RFID Code')
class ServiceForm(forms.Form):
    pass
