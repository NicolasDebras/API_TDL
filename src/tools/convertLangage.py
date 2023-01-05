from scrapper.Findscrapper import Cfind
from scrapper.Selectscrapper import Cselect


def convertLanguage(p):
    entityTable = entityExtract(p[1], [])
    if p[0] == "FIND":
        limit = -1
        if len(p) <= 1:
            print("error")
            return
        cp = p[2][1]
        Type = p[2][2]
        if Type is None:
            print("Vous avez mis une catégorie qui n'existe pas")
            return
        if len(p) == 4 and p[3] >= 0:
            limit = p[3]
        Cfind(cp, Type, entityTable, limit)
    elif p[0] == 'SELECT':
        print(p[2])
        if  p[2] == None:
            return
        Cselect(p[2], entityTable)


def entityExtract(entity, entityTable):
    if type(entity) != str:
        if len(entity) > 2 and type(entity) == tuple:
            entityExtract(entity[2], entityTable)
        if len(entity) > 1 and type(entity) == tuple:
            entityExtract(entity[1], entityTable)
    if 'ENTITY' != entity and 'EMPTY' != entity and type(entity) == str:
        entityTable.append(entity)
    return entityTable