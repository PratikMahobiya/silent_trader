from django.shortcuts import render
from kiteconnect import KiteConnect

# Create your views here.
def Index(request):
  api_key = open('./algo/config/api_key.txt','r').read()
  try:
    kite = KiteConnect(api_key=api_key)
    kite_url = kite.login_url()
  except Exception as  e:
    pass
  context = {'kite_url': kite_url}
  return render(request, 'index.html', context)

def generate_acc_token(request):
  api_key = open('./algo/config/api_key.txt','r').read()
  api_secret = open('./algo/config/api_secret.txt','r').read()
  if request.method == 'POST':
    request_token 		= request.POST.get('request_token','')
    # try:
    kite = KiteConnect(api_key=api_key)
    data = kite.generate_session(request_token, api_secret=api_secret)
    kite.set_access_token(data["access_token"])
    with open('./algo/config/t_token.txt','w') as at:
      at.write(data["access_token"])
    ltp = kite.ltp(['NSE:SBIN'])
    context = {'access_token': data["access_token"], 'SBI_ltp': ltp['NSE:SBIN']['last_price'],'status':'Now you can "REST IN PEACE".'}
    # except Exception as  e:
    #   context = {'status':'Please, Do it once again, My Lord. My Creater. My LUCIFER...'}
    return render(request, 'success.html', context)
  else:
    context = {'success':False,'status':'Please, Do it once again, My Lord. My Creater. My LUCIFER...'}
    return render(request, 'success.html', context)