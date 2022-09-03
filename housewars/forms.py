from django.forms import (CharField, ChoiceField, EmailField, EmailInput, Form,
                          ModelChoiceField, ModelForm, Select,
                          TextInput, ValidationError)
from smart_selects.form_fields import ChainedModelChoiceField

from .models import Activity, House, PointsEntry, UserEntry


class UserEntryForm(Form):
    first_name = CharField(widget=TextInput(attrs={
        'class': 'form-control',
        'id': 'first-name',
        'placeholder': 'First Name'
    }))
    last_name = CharField(widget=TextInput(attrs={
        'class': "form-control",
        'id': 'last-name',
        'placeholder': 'Last Name'
    }))
    email = EmailField(widget=EmailInput(attrs={
        'class': "form-control",
        'id': 'email',
        'placeholder': 'Email'
    }))
    grade = ChoiceField(choices=UserEntry.GradeChoices, widget=Select(attrs={
        'class': "form-select",
        'id': 'grade',
        'placeholder': 'Grade'
    }))
    house = ModelChoiceField(House.objects.all(), widget=Select(attrs={
        'class': "form-select",
        'id': 'house',
        'placeholder': 'House'
    }))

    def clean(self):
        email = self.cleaned_data['email']
        # Verify that email domain matches the school's
        if ('@slps.org' not in email):
            raise ValidationError("Please use your school email")
        # Verify that no other email with that domain exists
        if UserEntry.objects.filter(email=email).exists():
            raise ValidationError(
                "A signup with this email already exists, if you want to change your signups, please email cpatino8605@slps.org")


class ActivityForm(Form):
    activity1 = ModelChoiceField(Activity.objects.all(), widget=Select(attrs={
        'class': "form-select",
        'id': 'activity1',
        'placeholder': 'Activity 1'
    }))
    activity2 = ModelChoiceField(Activity.objects.all(), required=False, widget=Select(attrs={
        'class': "form-select",
        'id': 'activity2',
        'placeholder': 'Activity 2'
    }))

    def clean(self):
        data = self.cleaned_data

        activity1 = data.get('activity1')
        activity2 = data.get('activity2')

        # Verify that there are 60 minutes of activities selected
        if activity1:
            if activity2 and activity1.time + activity2.time != 60:
                raise ValidationError(
                    "Please pick activities adding up to one hour.")
            elif not activity2 and activity1.time != 60:
                raise ValidationError(
                    "Please pick activities adding up to one hour.")
            else:
                super().clean()
        else:
            raise ValidationError("Please select an activity.")


class PointsEntryForm(ModelForm):
    class Meta:
        model = PointsEntry
        fields = '__all__'
        widgets = {
            'house': Select(attrs={
                'class': "form-select",
                'id': 'house',
                'placeholder': 'House'
            }),
            'password': TextInput(attrs={
                'class': 'form-control',
                'id': 'first-name',
                'placeholder': 'Password',
                'type': 'password'
            })
        }

    def __init__(self, *args, **kwargs):
        super(PointsEntryForm, self).__init__(*args, **kwargs)
        self.fields['activity'].widget.attrs.update({'class': 'form-select'})
        self.fields['award'].widget.attrs.update({'class': 'form-select'})
