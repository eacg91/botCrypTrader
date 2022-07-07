import requests

def convert(aValue,aCoinName,bCoinName):
    aCoinName = aCoinName.upper()
    bCoinName = bCoinName.upper()
    if not aCoinName == bCoinName :
        book = aCoinName.lower()+'_'+bCoinName.lower()
        response = requests.get('https://api.bitso.com/v3/ticker/?book={}'.format(book))
        if response.json()['success'] :
            json_response = response.json()
            bValue = aValue * float(json_response['payload']['last'])
        else :
            book = bCoinName.lower()+'_'+aCoinName.lower()
            response2 = requests.get('https://api.bitso.com/v3/ticker/?book={}'.format(book))
            if response2.json()['success'] :
                json_response = response2.json()
                bValue = aValue / float(json_response['payload']['last'])
            else :
                print( response.json()['error'] )
                print( response2.json()['error'] )
                return False
    else :
        bValue = aValue
    print("{} {} = {} {}".format(aValue,aCoinName,bValue,bCoinName))

def get_address_balance(network,address) :
    response = requests.get('https://chain.so/api/v2/get_address_balance/{}/{}'.format(network,address))
    if response.json()['status']=="success":
        data = response.json()['data']
        """
        print("Network {} in address {} ".format(data['network'],data['address']) )
        print("Balance confirmado = {} ".format(data['confirmed_balance']) )
        print("Balance por confirmar = {} ".format(data['unconfirmed_balance']) )
        """
        return data
    else:
        return response.json()['status']

confirmed_balance = get_address_balance('BTC','14HprKtenqJWyMqT236J7i7DN5TArAiQLD')['confirmed_balance']
convert(float(confirmed_balance),'BTC','MXN')
convert(1,'APE','mxn')
response = requests.get('https://api.bitso.com/v3/ticker/')
allBooks = response.json()['payload']
dateInfo = allBooks[0]['created_at']
print(allBooks[0])
print(dateInfo)
for x in range( len(allBooks) ):
    bookX = allBooks[x]['book'].upper()
    print( "{}) {} = {} {} ".format(x+1,bookX,allBooks[x]['last'],bookX.split('_')[1]) )