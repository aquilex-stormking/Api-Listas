import pandas as pd
import requests
import json
from bs4 import BeautifulSoup, NavigableString
import warnings
import re

data =None
# libreria para ignorar las advertencias
def trae_datos(page=1):

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
        print(datos)
        while dato < datos:
            
            data=trae_datos(page)
            if data is None:
                return guarda
            if data is not None and 'items' in data:
                for o in data['items']:
                    if o['title'] is not None and o['uid'] is not None:
                        guarda.append((o['uid'],o['title']))
                    dato+=1
                
            else:
                dato+=1
            
            page+=1
            
        dffbi = pd.DataFrame(guarda, columns=['uid', 'title'])
        dffbi.to_pickle("dummy3.pkl")
        if data is not None and 'items' in data:    
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

def terroristas():
     #carga lista de terroristas
    url = "http://historico.presidencia.gov.co/prensa_new/sne/2004/abril/05/04052004.htm"
    response = requests.get(url)

    if response.status_code == 200:
        html_content = response.text
    else:
        print("Error al acceder a la página:", response.status_code)
        exit()

    # Analiza el contenido de la página con Beautiful Soup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Busca el elemento <p> con la clase 'parrafos' que contiene '1. PERSONAS'
    start = soup.find('p', class_='parrafos', string=lambda text: '1. PERSONAS' in text)

    # Busca el elemento <p> con la clase 'parrafos' que contiene '2. GRUPOS Y ENTIDADES'
    end = soup.find('p', class_='parrafos', string=lambda text: '2. GRUPOS Y ENTIDADES' in text)

    # Busca los elementos que representan a las personas entre esas dos etiquetas
    # Por ejemplo, supongamos que las personas están en elementos 'div' con la clase 'person'
    persons = []
    for sibling in start.next_siblings:
        if sibling == end:
            break
        if isinstance(sibling, NavigableString):
            continue  # ignora las cadenas de texto entre los elementos
        if sibling.get('class') == ['parrafos']:
            persons.append(sibling)

    # Extrae el texto de los elementos
    persons_text = [person.get_text() for person in persons]
    clean_persons_text = [person.replace('\r\n       ', '') for person in persons_text]
    clean_persons_text = [person.replace('\r\n  ', '') for person in clean_persons_text]
    
    # Inicializa una lista vacía para guardar los datos agrupados
    grouped_data = []

    # Inicializa una cadena vacía para guardar la información de la persona actual
    current_person = ''

    for line in clean_persons_text:
        # Si la línea comienza con un número seguido de un punto, es el inicio de una nueva persona
        if re.match(r'\d+\.', line):
            # Si current_person no está vacío, entonces tenemos información de una persona que debemos guardar
            if current_person:
                grouped_data.append(current_person)
            # Inicia una nueva persona
            current_person = line
        else:
            # Si la línea no comienza con un número seguido de un punto, es información adicional de la persona actual
            current_person += ' ' + line

    # Asegúrate de guardar la información de la última persona
    if current_person:
        grouped_data.append(current_person)
    
    extracted_data = []
    # Recorrer cada cadena en la lista de datos
    for string in grouped_data:
        # Buscar patrones de texto que correspondan a la información que necesitas
        index = re.search(r'\d+\.', string)
        name = re.search(r'\. ([A-Za-zÁÉÍÓÚáéíóú ,*]*)', string)
        birth = re.search(r'nacido el ([\d\.]+)', string)
        identification = re.search(r'DNI no ([\d\.]+)|DNI n\.o ([\d\.]+)|pasaporte n\.o ([\d\.]+)', string)
    
        # Añadir la información extraída a la lista (si existe, si no, añadir None)
        extracted_data.append({
            'Index': index.group(0)[:-1] if index else None,
            'Name': name.group(1) if name else None,
            'Birth': birth.group(1) if birth else None,
            'Identification': identification.group(1) if identification else None
        })

    # Convertir la lista de datos extraídos en un DataFrame
    df = pd.DataFrame(extracted_data)

    # Ver el DataFrame
    print(df)

    paragraph = soup.find('p', class_='parrafos', string=lambda text: '2. GRUPOS Y ENTIDADES' in text)

    # Busca los elementos que representan a las personas después de ese párrafo
    # Por ejemplo, supongamos que las personas están en elementos 'div' con la clase 'person'
    # Nota: esto dependerá de cómo esté estructurada la página web
    persons = paragraph.find_next_siblings('p', class_='parrafos')

    # Extrae el texto de los elementos
    groups_text = [person.get_text() for person in persons]

    