import pandas as pd
import requests
import json
from bs4 import BeautifulSoup
import warnings



# libreria para ignorar las advertencias
def traeDatos(page=1):

    try:    
        response = requests.get('https://api.fbi.gov/wanted/v1/list', params = {
            'page': page
        })
        data = json.loads(response.content)
    except:
        data = None

    return data

def validar(a):
        if a is not None:
            return a.text
        else:
            a=" "
            return a
        
def cargardatos():

    warnings.filterwarnings("ignore")

    #Obtener Datos de XML   
    # Se obtiene la informacion de la ofac
    urlofac = "https://www.treasury.gov/ofac/downloads/consolidated/consolidated.xml"
    xmlofac = requests.get(urlofac)
    soupofac = BeautifulSoup(xmlofac.content, 'lxml', from_encoding='utf-8')
    persona = soupofac.findAll('sdnentry')
    pasa1 = [] 

    for i in persona:
        fName = i.find('firstname')
        sName = i.find('lastname')
        uID = i.find('uid')
        tId = i.find('idtype')
        nId = i.find('idnumber')
        aDdress = i.find('address')
        cCountry = i.find('country')
        cCity = i.find('city')

        fName = validar(fName)
        sName = validar(sName)
        uID = validar(uID)
        tId = validar(tId)
        nId = validar(nId)
        aDdress = validar(aDdress)
        cCountry = validar(cCountry)
        cCity = validar(cCity)

        pasa1.append((uID,(fName+" "+sName).upper(),tId,nId,aDdress,cCountry,cCity))

    dfofac = pd.DataFrame(pasa1, columns = ['uid', 'first_name','tipoId','identificacion','direccion','pais','ciudad'])
    dfofac.to_pickle("dummy.pkl")

    # Se obtiene la informacion de la onu
    url = "https://scsanctions.un.org/resources/xml/sp/consolidated.xml"
    xml = requests.get(url)
    soup = BeautifulSoup(xml.content, 'lxml', from_encoding='utf-8')
    persona = soup.findAll('individual')
    pasa1 = []

    for i in persona:
        
        dataId = i.find('dataid')
        fName = i.find('first_name')
        sName = i.find('second_name')
        tName = i.find('third_name')
        aName = i.find('alias_name')
        tId = i.find('type_of_document')
        nId = i.find('number')
        description = i.find('note')
        cCountry = i.find('issuing_country') 
        dateBirth = i.find('date')
        dataId = validar(dataId)
        fName = validar(fName)
        sName = validar(sName)
        tName = validar(tName)
        aName = validar(aName)
        tId = validar(tId)
        nId = validar(nId)
        description = validar(description)
        cCountry = validar(cCountry)
        dateBirth = validar(dateBirth)
        
        nombre = fName+' '+sName+' '+tName+' '+aName
        pasa1.append((dataId,nombre.upper(),tId,nId,description,cCountry,dateBirth)) 
            
    dfonu = pd.DataFrame(pasa1, columns = ['dataid', 'first_name','tipo_documento','numero_documento','description','pais','fecha_nacimiento'])
    #almacenar datos en la base de datos sql
    dfonu.to_pickle("dummy2.pkl")

    # Se obtiene la informacion del fbi
    data=traeDatos()
    guarda = []
    print(data)
    if data is None:
        return guarda

    else:
        datos = data['total']
        dato = 0
        page=0
        while dato < datos:
            
            data=traeDatos(page)
            for o in data['items']:
                
                if o['title'] is not None and o['uid'] is not None:
                    guarda.append((o['uid'],o['title']))
                dato+=1
            page+=1
        dffbi = pd.DataFrame(guarda, columns=['uid', 'title'])
        dffbi.to_pickle("dummy3.pkl")
        #     data = traeDatos(page)
            
        for o in data['items']:
            
            o['details']
            o['url']
            o['nationality']
            o['images']   
            guarda.append((o['uid'], o['title'], o['details'], o['url'], o['nationality'], o['images']))
            dato += 1
        page += 1
        dffbi = pd.DataFrame(guarda, columns = ['uid', 'title','detalle','link_info','nacionalidad','link_picture'])
        dffbi.to_pickle("dummy3.pkl")

cargardatos()