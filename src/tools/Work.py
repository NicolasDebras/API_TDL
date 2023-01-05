def verifIfIsWord(word):
    f = open("work.txt", mode='r', encoding='utf-8')
    result = f.read().find(word)
    f.close()
    return result

#fonction qui transforme le xml en JSON
def XmlToJson():
    import xmltodict
    import pprint
    import json

    with open('users.xml') as fd:
        doc = xmltodict.parse(fd.read())

    pp = pprint.PrettyPrinter(indent=4)
    return json.dumps(doc)

#fonction qui permet d'ecrire different test pour la fonction find
def WriteTest():
    w = open("work.txt", mode='r', encoding='utf-8')
    read = w.read()
    tab = list(read.split('\n'))
    f = open("test_find.py", mode='w', encoding='utf-8')
    f.write("from Findscrapper import Cfind\n\n")
    for element in tab:
        f.write("def test" + element.replace("-", '') + "():\n")
        f.write('   test = Cfind(78300, "'+element+'" , ["*"], -1)\n')
        f.write('   assert test == 0\n\n')

#fonction qui permet d'ecrire des tests pour la focntion de select 
def writeTestSelect():
    w = open("work.txt", mode='r', encoding='utf-8')
    read = w.read()
    tab = list(read.split('\n'))
    f = open("test_select.py", mode='w', encoding='utf-8')
    f.write('from Selectscrapper import Cselect\n')
    f.write("from Findscrapper import Cfind, BuildUrl, parse, request\n\n")
    for element in tab:
        f.write("def test_select_" + element.replace("-", '') + "():\n")
        f.write('   url = BuildUrl("'+element+'", 78300)\n')
        f.write('   res = request(url)\n')
        f.write('   r = parse(res)\n')
        f.write('   test = Cselect(r[0]["ID"][2:-1], ["*"])\n')
        f.write('   assert test == 0\n\n')
    return
