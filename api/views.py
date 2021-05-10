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


class ContactUpdateView(APIView):
    permission_classes=[IsAuthenticated]

    def post(self,request,*args, **kwargs):
        data=request.data
        user=request.user

        try:
            contact=user.contacts.filter(custom_id=kwargs['custom_id'])

            if not contact:
                raise Contact.DoesNotExist

            contact=contact[0]

            country_code=data['country_code']
            full_name=data['full_name']
            phone_number=data['phone_number']

            contact.country_code=country_code
            contact.full_name=full_name
            contact.phone_number=phone_number

            if data.get('is_favorite'):
                contact.is_favorite=data['is_favorite']

            contact.save()

            return JsonResponse({
                'full_name':contact.full_name,
                "custom_id":contact.custom_id,
                'country_code':contact.country_code,
                'phone_number':contact.phone_number,
                'is_favorite':contact.is_favorite
            },status=201)

        except KeyError as e:
            error_message=f'{e.args[0]} is a required field'

            return JsonResponse({
                e.args[0]:[error_message]
            },status=400)

        except Contact.DoesNotExist:
            return HttpResponseBadRequest('This contact does not exist')

        except:
            return HttpResponseBadRequest()

    
    def delete(self,request,*args, **kwargs):
        id = kwargs['custom_id']

        try:
            user=request.user
            contact=user.contacts.filter(custom_id=id)

            if not contact:
                raise Contact.DoesNotExist

            contact[0].delete()

            return JsonResponse({
                'detail' :'Contact successfullt deleted'           },status=204)
        except Contact.DoesNotExist:
            return HttpResponseBadRequest('This contact does not exist')
        except:
            return HttpResponseBadRequest()

class ContactSearchView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request,*args, **kwargs):
        user=request.user
        contacts=list(user.contacts.filter(full_name__contains=kwargs['full_name']).values())

        return JsonResponse({
            'search_matches':contacts,
            "search_length":len(contacts)
        })


        