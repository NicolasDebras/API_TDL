from Findscrapper import request, RecoveryUrlIMG

# récupère le titre de la page d'apres la balise title 
def recoveryTitle(title):
    return title[5:title.find('</title>')]

def recoveryDesc(tab , index):
    desc = (tab[index])[tab[index].find('content='):]
    while True:
        index = index + 1
        if '">' in tab[index]:
            break
        desc = desc + " " +  tab[index]
    desc = desc + " " +  (tab[index])[:len(tab[index])-2]
    return desc

def recoveryTitleAndDesc(tab):
    dictres = {}
    index = tab.index('  <!-- End Adsense -->')
    i = index
    while True:
        if index+100 == i:
            print("ERROR")
            break
        if '<title>' in tab[i]:
            dictres["TITLE"] = recoveryTitle(tab[i])
        if '<meta name="description"' in tab[i]:
            dictres["DESC"] = recoveryDesc(tab, i)
            break
        i = i + 1
    return dictres

# tri si la page est en version pro ou pas ! 
def parse(txtpage):
    list_content_url = list(txtpage.split('\n'))
    dictres = recoveryTitleAndDesc(list_content_url)
    try:
        index = list_content_url.index('          <div class="offer-service-card ">')
        dictres = NOPro(dictres, list_content_url[index:])
        dictres["ULR_IMG"] = RecoveryUrlIMG(list_content_url[list_content_url.index('              <div class="offer-item-picture" itemprop="provider" itemscope itemtype="https://schema.org/Person">')+1])
    except ValueError:
        dictres = pro(dictres, list_content_url)
    return dictres 

def recoveryPriceNet(priceLine):
    return priceLine[priceLine.find('">')+2:priceLine.find('</div>')]

def recoveryPrice(priceLine):
    return priceLine[priceLine.find("t")+1:priceLine.find("a")]

def recoverylocation(location):
    return location[location.find('">')+2:location.find('</div>')]

def recoveryNUm(btnline):
    return btnline[btnline.find(':'):btnline.find('"><')]

def NOPro(dictres, list_content):
    index = list_content.index('        <div class="offer-content col-md-7 order-md-1">')
    for i in range(0, index):
        if "item-location" in list_content[i]:
            dictres["LOCATION"] = recoverylocation(list_content[i])
        if "price-info mt-3" in list_content[i]:
            dictres["NET_PRICE"] = recoveryPriceNet(list_content[i])
        if "price-info-cesu" in list_content[i]:
            dictres["PRICE"] = recoveryPrice(list_content[i+2])
        if 'ded-phone' in list_content[i]:
            dictres["NUM"] = recoveryNUm(list_content[i])
    return dictres

def pro(dictres, list_content):
    index = list_content.index('        <div class="offer-content col-md-7 order-md-1">')
    for i in range(0, index):
        if 'data-src' in list_content[i]:
            dictres["URL_IMG"] = RecoveryUrlIMG(list_content[i])
        if "price-info mt-3" in list_content[i]:
            dictres["NET_PRICE"] = recoveryPriceNet(list_content[i])
        if "item-location" in list_content[i]:
            dictres["LOCATION"] = recoverylocation(list_content[i])
    return dictres

#crée l'url avec l'id rentré dans la page
def createUrl(id):
    return "https://www.aladom.fr/" + id

def Cselect(id , entityTable):
    url = createUrl(id)
    txtpage = request(url)
    print(url)
    if txtpage != 400:
        print(parse(txtpage))
    return
