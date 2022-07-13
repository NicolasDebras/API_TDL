import requests
import pprint


#decoup la page avec que ce qui nous interesse 
def parse(content_url):
    list_content_url = list(content_url.split('\n'))
    index = list_content_url.index('    <div class="row offer-list">')
    list_content_url = list_content_url[index:]
    index2 = list_content_url.index('      <div class="row">')
    list_content_url = list_content_url[:index2+1]
    ListRes = findElement(list_content_url)
    return ListRes

#Recupère url de l'image dans la balise <img>
def RecoveryUrlIMG(imgStr):
    list_img = list(imgStr.split(" "))
    for element in list_img:
        if "data-src=" in element:
            return element[element.find("\""):element.rfind("\"")]
    

#Recupère le title dans la balise <img>
def Recoverytitle(imgStr):
    cutStr = imgStr[imgStr.find("alt="):imgStr.find('itemprop=')]
    return cutStr[5:imgStr.rfind('"')]


def RecoveryId(h3str):
    cutstr = h3str[h3str.find("href="):]
    tab = list(cutstr.split('>'))
    return (tab[0])[5:]


#recherche information dans élement 
def findInfoIntoElement(listElement):
    dictInfo = {}
    for i in range(0, len(listElement)):
        if listElement[i] == "    <figure>":
            dictInfo["URL_INFO"] = RecoveryUrlIMG(listElement[i+1])
            dictInfo["TITLE"] = Recoverytitle(listElement[i+1])
        if listElement[i] == '      <i class="fa fa-fw fa-map-marker"></i>':
            dictInfo["PLACE"] = listElement[i+1]
        if "<h3" in listElement[i]:
            dictInfo["ID"] = RecoveryId(listElement[i])
        dictInfo["DESC"] = "a faire"
    return dictInfo

#recherce element
def findElement(listElement):
    ListRes = []
    first = ""
    for i in range(0, len(listElement)):
        if listElement[i] == '        <div class="col-lg-4 col-6 d-flex flex-column my-4 offer-list-item">':
            if first == "":
                first = i
            else:
                ListRes.append(findInfoIntoElement(listElement[first:i]))
                first = i
    printdict(ListRes)
    return ListRes

#prend en paramètre l'url de la page 
def request(url):
    r = requests.get(url)
    if (r.status_code != 200):
        print("erreur")
        return r.status_code
    else:
        return r.content.decode("utf-8")

def printdict(tab):
    print("Number result : " + str(len(tab)) + "\n")
    for element in tab:
        print("========")
        pprint.pprint(element)
        print("========")

#a finir
def locate(cp):
    return "paris-75/"

#fonction qui contruit l'url 
def BuildUrl(type, cp):
    return "https://www.aladom.fr/" + type + "/" + locate(cp)

#fonction qui se lance lors de l'execution de la commande page  
def Cfind(cp, type, entityTable, limit):
    url = BuildUrl(type, cp)
    cp = request(url)
    if cp != 400:
        parse(cp)
    return

#Cfind(78300, "aide-personnes-handicapees")


