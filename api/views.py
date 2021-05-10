from api.models import Contact
from django.http.response import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

class ContactView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request,*args, **kwargs):
        user=request.user

        contacts=user.contacts.values()

        return JsonResponse({'contacts': list(contacts)})

    def post(self,request,*args, **kwargs):
        data=request.data 
        user=request.user
        try:
            country_code=data['country_code']
            full_name=data['full_name']
            phone_number=data['phone_number']

            custom_id=len(user.contacts.all())+1

            new_contact=Contact.objects.create(
                full_name=full_name,
                country_code=country_code,
                phone_number=phone_number,
                custom_id=custom_id
            )

            if data.get('is_favorite'):
                new_contact.is_favorite=data['is_favorite']
                new_contact.save()

            user.contacts.add(new_contact)

            return JsonResponse({
                'full_name':new_contact.full_name,
                "custom_id":new_contact.custom_id,
                'country_code':new_contact.country_code,
                'phone_number':new_contact.phone_number
            },status=201)
        except KeyError as e:
            error_message=f'{e.args[0]} is a required field'

            return JsonResponse({
                e.args[0]:[error_message]
            },status=400)

