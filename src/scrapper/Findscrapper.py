import requests
import pprint


def reveryUrlnav(lineurl):
    return lineurl[lineurl.find('href="'):lineurl.rfind('">')]

def nav(tabres, content):
    try:
        index = content.index('  <ul class="pagination">')
        content = content[index:]
        index2 = content.index('</nav>')
        tabUrl = []
        for i in range(0, index2):
            if 'href' in content[i] and 'ala-chevron-right' not in content[i]:
                tabUrl.append("https://www.aladom.fr" + reveryUrlnav(content[i])[6:])
        for element in tabUrl:
            r = request(element)
            if r != 404:
                tabres = tabres + parse(r)
        return tabres
    except ValueError:
        return tabres

def recoveryDesc(tab , index):
    desc = (tab[index])[tab[index].find('">'):]
    while True:
        index = index + 1
        if '</' in tab[index]:
            break
        desc = desc + " " +  tab[index]
    desc = desc + " " +  (tab[index])[:len(tab[index])-2]
    desc = desc[:len(desc)-5]
    return desc + "..."

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
            dictInfo["TITLE"] = Recoverytitle(listElement[i+1]).replace('&#x27;', "'")
        if listElement[i] == '      <i class="fa fa-fw fa-map-marker"></i>':
            dictInfo["PLACE"] = listElement[i+1]
        if "<h3" in listElement[i]:
            dictInfo["ID"] = RecoveryId(listElement[i])
        if "description" in listElement[i]:
            dictInfo["DESC"] = recoveryDesc(listElement, i)
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
    ListRes.append(findInfoIntoElement(listElement[first:]))
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

def choose(tab):
    print(tab)

#fonction qui recherche dans l'api du
def locate(cp):
    r = requests.get("https://api-adresse.data.gouv.fr/search/?q="+str(cp)+"&type=municipality")
    test = r.json()
    if len(test['features']) > 0:
        name = test['features'][0]['properties']['name']
        return  name.lower() + "-"+ (str(cp))[:2] +"/"
    print("CP ERROR")
    return "errror"

#fonction qui contruit l'url 
def BuildUrl(type, cp):
    return "https://www.aladom.fr/" + type + "/" + locate(cp)

#fonction qui se lance lors de l'execution de la commande page  
def Cfind(cp, type, entityTable, limit):
    entityTable = ["DESC", "URL_INFO", "ID", "PLACE", "TITLE"] if entityTable == ["*"] else entityTable
    url = BuildUrl(type, cp)
    requestRes = request(url)
    if requestRes != 404:
        result = parse(requestRes)
        result = nav(result, list(requestRes.split('\n')))
        chooseData(result, entityTable, limit, cp)
        return result
    return 

def chooseData(result, entityTable, limit, cp):
    if len(result) == 0:
        return
    if limit == -1 or  limit > len(result):
        limit = len(result)
    f = open("users.xml", mode='w', encoding='utf-8')
    f.write("<?xml version=\"1.0\"?>\n")
    f.write("<Find>\n")
    f.write("\t<CP>"+str(cp)+"</CP>\n")
    f.write("\t<LIMIT>"+str(limit)+"</LIMIT>\n")
    for i in range(0, limit):
        f.write(f"\t<User id=\"{i}\">\n")
        for entity in entityTable:
             f.write(f"\t\t<{entity.capitalize() }>{result[i].get(entity)}</{entity.capitalize()}>\n")
        f.write(f"\t</User>\n")
    f.write("</Find>\n")
    f.close()

