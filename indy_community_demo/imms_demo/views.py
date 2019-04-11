from django.shortcuts import render

# Create your views here.
def profile_view(request):
    return render(request, 'imms_demo/imms_profile.html')

def data_view(request):
    return render(request, 'imms_demo/imms_data.html')

def wallet_view(request):
    return render(request, 'imms_demo/imms_wallet.html')

def conversation_callback(message, prev_type, prev_status):
    print("message callback", prev_type, prev_status, message.conversation_type, message.status)
