import pandas as pd
import requests
import json
from bs4 import BeautifulSoup
import warnings



# libreria para ignorar las advertencias
def trae_datos(page=1):

    try:    
        response = requests.get('https://api.fbi.gov/wanted/v1/list', params = {
            'page': page
        })
        data = json.loads(response.content)
    except:
        data = None
        raise Exception

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
        f_name = i.find('firstname')
        s_name = i.find('lastname')
        u_id = i.find('uid')
        t_id = i.find('idtype')
        n_id = i.find('idnumber')
        address = i.find('address')
        country = i.find('country')
        city = i.find('city')

        f_name = validar(f_name)
        s_name = validar(s_name)
        u_id = validar(u_id)
        t_id = validar(t_id)
        n_id = validar(n_id)
        address = validar(address)
        address = address.replace('\n', ' ')
        country = validar(country)
        city = validar(city)

        pasa1.append((u_id,(f_name+" "+s_name).upper(),t_id,n_id,address,country,city))

    dfofac = pd.DataFrame(pasa1, columns = ['uid', 'first_name','tipoId','identificacion','direccion','pais','ciudad'])
    dfofac.to_pickle("dummy.pkl")

    # Se obtiene la informacion de la onu
    url = "https://scsanctions.un.org/resources/xml/sp/consolidated.xml"
    xml = requests.get(url)
    soup = BeautifulSoup(xml.content, 'lxml', from_encoding='utf-8')
    persona = soup.findAll('individual')
    pasa1 = []

    for i in persona:
        
        data_id = i.find('dataid')
        f_name = i.find('first_name')
        s_name = i.find('second_name')
        t_name = i.find('third_name')
        a_name = i.find('alias_name')
        t_id = i.find('type_of_document')
        n_id = i.find('number')
        description = i.find('note')
        country = i.find('issuing_country') 
        date_birth = i.find('date')
        data_id = validar(data_id)
        f_name = validar(f_name)
        s_name = validar(s_name)
        t_name = validar(t_name)
        a_name = validar(a_name)
        t_id = validar(t_id)
        n_id = validar(n_id)
        description = validar(description)
        country = validar(country)
        date_birth = validar(date_birth)
        
        nombre = f_name+' '+s_name+' '+t_name+' '+a_name
        pasa1.append((data_id,nombre.upper(),t_id,n_id,description,country,date_birth)) 
            
    dfonu = pd.DataFrame(pasa1, columns = ['dataid', 'first_name','tipo_documento','numero_documento','description','pais','fecha_nacimiento'])
    #almacenar datos en la base de datos sql
    dfonu.to_pickle("dummy2.pkl")

    # Se obtiene la informacion del fbi
    data=trae_datos()
    guarda = []
    
    if data is None:
        return guarda

    else:
        datos = data['total']
        dato = 0
        page=0
        while dato < datos:
            
            data=trae_datos(page)
            for o in data['items']:
                
                if o['title'] is not None and o['uid'] is not None:
                    guarda.append((o['uid'],o['title']))
                dato+=1
            page+=1
        dffbi = pd.DataFrame(guarda, columns=['uid', 'title'])
        dffbi.to_pickle("dummy3.pkl")
            
        for o in data['items']:
            detallelink = ''
            if o['details'] is not None :
                o['details'] = o['details'] = o['details'].replace('<p>', ' ')
                o['details'] = o['details'] = o['details'].replace('</p>', ' ')
                o['details'] = o['details'] = o['details'].replace('\r\n', ' ')
                
                if "<a" in o['details']:
                    detallelink= o['details'][o['details'].index("<a")+3 : o['details'].index("</a>")-1]
                    
            o['url']
            o['nationality']
            o['images']   
            guarda.append((o['uid'], o['title'], o['details'], o['url'], o['nationality'], o['images'],detallelink))
            dato += 1
        page += 1
        dffbi = pd.DataFrame(guarda, columns = ['uid', 'title','detalle','link_info','nacionalidad','link_picture','detallelink'])
        dffbi.to_pickle("dummy3.pkl")

    #carga lista de terroristas
    url = "https://eur-lex.europa.eu/legal-content/ES/TXT/HTML/?uri=OJ:L:2022:025:FULL"
    response = requests.get(url)

    if response.status_code == 200:
        html_content = response.text
    else:
        print("Error al acceder a la página:", response.status_code)
        exit()

    soup = BeautifulSoup(html_content, "html.parser")
    personas = []
    grupos = []
    cont = 0
    lista_terro = []
    # Encuentra el div con el id "L_2022025ES.01000301"
    target_div = soup.find("div", id="L_2022025ES.01000301")

    if target_div:
        # Encuentra todas las tablas dentro del div
        tables = target_div.find_all("table")

        # Itera sobre las tablas y busca los elementos <span> en cada una de ellas
        for table in tables:
            span_elements = table.find_all("span")
            for span in span_elements:
                if cont <=12:
                    personas.append(span.text)
                    cont+= 1
                else :
                    grupos.append(span.text)
    
    else:           
        print("No se encontró el div con el id 'L_2022025ES.01000301'")
    persona = []
    grupo = []
    for o in personas:
        indice_primera_coma = o.find(',')
        indice_segunda_coma = o.find(',', indice_primera_coma + 1)
        indice_punto = o.rfind('.')
        indice_segundo_punto =o.rfind(':')
        
        nombre = o[:indice_primera_coma].strip()
        apellido = o[indice_primera_coma + 1:indice_segunda_coma].strip()
        nacimiento = o[indice_segunda_coma+1:indice_punto].strip()
        pasaporte = o[indice_segundo_punto + 1:].strip()
        datos = {
            'nombre': nombre,
            'apellido': apellido,
            'nacimiento': nacimiento,
            'pasaporte': pasaporte
        }
        print(datos)
        persona.append(datos)
    for o in grupos:
        datos= {
            'nombre':o,
            'apellido': '',
            'nacimiento': '',
            'pasaporte': ''
        }
        persona.append(datos) 
    
    dfterro = pd.DataFrame(persona, columns = ['nombre', 'apellido','nacimiento','pasaporte'])
    dfterro.to_pickle("dummy4.pkl")

cargardatos()

