from kiteconnect import KiteConnect

api_key = open('algo/config/api_key.txt','r').read()
api_secret = open('algo/config/api_secret.txt','r').read()
access_token = open('algo/config/access_token.txt','r').read()
try:
    kite = KiteConnect(api_key=api_key)

    ## Uncomment if ACCESS KEY is generated.
    # kite.set_access_token(access_token)

    ## first time in a day.
    print(kite.login_url())
    token = input('ENTER THE TOKEN: ')
    data = kite.generate_session(token, api_secret=api_secret)
    kite.set_access_token(data["access_token"])
    print(data["access_token"])
    with open('algo/config/access_token.txt','w') as at:
      at.write(data["access_token"])
except Exception as  e:
    print(e)


ltp = kite.ltp(['NSE:SBIN'])
print(ltp)

print('SUCCESSFULLY GENERATED TOKEN:- AND SAVED IN A FILE..')