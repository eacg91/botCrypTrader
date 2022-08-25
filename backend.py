import requests
import time, os

os.environ['TZ'] = 'UTC+6'
#time.tzset()  #Linea bloqueada para funcionar en Termux (Android)

class crypto():
    #def __init__(self):
    allBooks = {}

def get_allBooks():
    response = requests.get('https://api.bitso.com/v3/ticker/')
    if response.json()['success'] :
        #crypto.allBooks = response.json()['payload']
        for x in range( len(response.json()['payload']) ):
            i = response.json()['payload'][x]['book']
            crypto.allBooks[i] = response.json()['payload'][x]
        #print(crypto.allBooks[i])
    return response.json()['success']

def search_betweenTwoBooks( a,b,index ) :
    aBooks = []
    bBooks = []
    c = ""
    for x in index :
        if a in x :
            aBooks.append( x )
        elif b in x:
            bBooks.append( x )
    if len(aBooks) > 0 and len(bBooks) > 0:
        for x in aBooks :
            xs0 = x.split('_')[0]
            xs1 = x.split('_')[1]
            for y in bBooks :
                ys0 = y.split('_')[0]
                ys1 = y.split('_')[1]
                if xs0 == ys0 or xs0 == ys1 :
                    c = xs0
                elif xs1 == ys0 or xs1 == ys1 :
                    c = xs1
                if not c == "" :
                    return [x,y,c]
    x = y = "NO Encontrado"
    return [x,y,c]

def convert2(aValue,aCoinName,bCoinName):
    aCoinName = aCoinName.lower()
    bCoinName = bCoinName.lower()
    if not aCoinName == bCoinName :
        book = aCoinName+'_'+bCoinName
        try:
            bValue = aValue * float(crypto.allBooks[book]['last'])
        except:
            book = bCoinName+'_'+aCoinName
            try:
                bValue = aValue / float(crypto.allBooks[book]['last'])
            except:
                cCoinName = search_betweenTwoBooks( aCoinName,bCoinName,crypto.allBooks )[2]
                if not cCoinName == "" :
                    print("*****")
                    cValue = convert2(aValue,aCoinName,cCoinName)
                    bValue = convert2(cValue,cCoinName,bCoinName)
                    print("*****")
                else : 
                    print( "No se puede hacer trading de {} a {} usando Bitso !".format(aCoinName.upper(),bCoinName.upper()) )
                    return 0
    else :
        bValue = aValue
    print(f"{aValue} {aCoinName.upper()} = {bValue} {bCoinName.upper()} ")
    return bValue

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

def test():
	print( "Inicia programa {}".format(time.strftime("%c")) )
	confirmed_balance = get_address_balance('BTC','14HprKtenqJWyMqT236J7i7DN5TArAiQLD')['confirmed_balance']
	while get_allBooks() :
		dateInfo = crypto.allBooks['btc_mxn']['created_at']
		dateInfo = dateInfo.split('T')[0] +" "+ dateInfo.split('T')[1].split('+')[0]
		print(f"\n*******\n Hora de Bitso {dateInfo}")
		#print(crypto.allBooks['btc_mxn']) #imprime el JSON obtenido
		convert2(1,'BTC','USD')
		convert2(1,'ETH','USD')
		convert2(1,'APE','USD')
		convert2(1,'AAVE','USD')
		convert2(1,'USD','MXN')
		convert2(float(confirmed_balance),'BTC','mxn')
		#for x in crypto.allBooks :
		 #   print( "{}) 1 {} = {} {} ".format(x,x.split('_')[0].upper(),crypto.allBooks[x]['last'],x.split('_')[1].upper()) )
		time.sleep(1)
