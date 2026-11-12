from django.shortcuts import render
from dotenv import load_dotenv
import os
from uc.models import underconstruction 

load_dotenv()

class underconstructionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        print('One time Initialization')

    # def __call__(self, request):
    #     print('This is before view')
    #     # response = self.get_response(request)
    #     response = render(request, 'uc/underc.html')
    #     print('This is after view')
    #     return response

    def __call__(self, request):
       if request.user.is_staff:
              return self.get_response(request)

       uc_key = os.environ.get('MAINTENANCE_BYPASS_KEY')
       if 'u' in request.GET and request.GET['u'] == uc_key:
           request.session['bypass_maintenance'] = True
           request.session.set_expiry(0)  # Set session expiry to browser close
       if request.session.get('bypass_maintenance'):
           return self.get_response(request)
       try :
           uc =  underconstruction.objects.first()
           if uc and uc.is_under_construction:
               context = {
                   'uc_note' : uc.uc_note,
                   'uc_duration' : uc.uc_duration,
               }
               return render(request, 'uc/underc.html', context)
       except :
           pass
       return self.get_response(request)