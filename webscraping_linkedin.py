
from urllib.request import urlopen
from urllib.error import HTTPError
import bs4
from bs4 import BeautifulSoup
import unicodedata
import requests
from controller import Controller
import re


def contain_br(contents):
    for element in contents:
        if type(element) is bs4.element.Tag:
            if element.name == "br":
                return True
    return False


def get_content(contents):
    lista = []
    for element in contents:
        if type(element) is bs4.element.NavigableString:
            if str(element) is not None and str(element).strip() != "":
                lista.append(str(element))
    return lista


def scraping_ofertas(con, url_principal, url_busqueda, sufix_url, pagina_inicial, cant_paginas, cant_ofertas, id_carga):
    controller = Controller()
    lista_oferta = []       
    i=1
    for i in range(pagina_inicial, cant_paginas):
        url_pagina = url_busqueda + str(i*25)
        req = requests.get(url_pagina)
        soup = BeautifulSoup(req.text, "lxml")
        avisos=soup.find('ul', class_='jobs-search__results-list')
        if avisos !=None:
            avisos=soup.find('ul', class_='jobs-search__results-list').find_all("li")
            for li in avisos:
                    oferta = {}
                    oferta["id_carga"] = id_carga
                    # Almacena la url de la pagina
                    oferta["url_pagina"] = url_pagina
                    # Almacena la url de la oferta
                    oferta["url"]       =   li.find("a")['href']
                    #print(oferta["url"])
                    oferta["puesto"]    =   li.find("h3", {"class": "result-card__title"}).get_text()
                    oferta["empresa"]   =   li.find("h4", {"class": "result-card__subtitle"}).get_text()
                    oferta["lugar"]     =   li.find("span", {"class": "job-result-card__location"}).get_text()
                    salario = li.find("span", {"class": "salaryText"})            
                    if salario!=None:                                            
                        oferta["salario"]=salario.get_text()
                    else:
                        oferta["salario"]=''
                    oferta["fecha_publicacion"]=li.find("time").get('datetime')
                    oferta["id_anuncioempleo"]=li.get('data-id')
                    # Accede al contenido HTML del detalle de la oferta en especifico
                    reqDeta = requests.get(oferta["url"])            
                    soup_deta = BeautifulSoup(reqDeta.text, "lxml")
                    aviso_deta = soup_deta.find("div", {"class": "show-more-less-html__markup"}).text+'.'
                    texto= aviso_deta.replace("'","")
                    texto = texto.replace("..",".")
                    texto = unicodedata.normalize("NFKD",re.sub('[-(),*@¿?/¡!+<>;%#|°=:]','',texto.upper())).encode("ascii","ignore").decode("utf-8",'ignore')
                    if texto!=None:    
                        oferta["detalle"]=texto[0:7998]
                    # #--> descomentar esta linea para que se realice la insercion
                    oferta["id_oferta"]=controller.registrar_oferta(con, oferta)
                    lista_oferta.append(oferta)
        else:
            print("\nNo se encuentran ofertas\n")
      
    return lista_oferta

#Existe una lógica oferta detalles que nos puede ayudar a evaluar el contenido



def scraping_ofertadetalle(con,listaOferta):
    controller = Controller()
    i=0
    for i in range(0,len(listaOferta)):
        oferta = {}
        oferta["id_oferta"] =  listaOferta[i]["id_oferta"]
        lista = listaOferta[i]["detalle"].split(sep='.')
        #print(lista)
        oferta["descripcion_tupla"]=""
        j=0
        for j in range(0,len(lista)):
            oferta["descripcion_tupla"]=lista[j][0:1998]
            if (len(oferta["descripcion_tupla"])>=3):
            # print(".................................OFERTA..........................................")
            # print(oferta)
                controller.registrar_oferta_detalle(con,oferta)


def replace_quote(list):
    new_list = []
    for el in list:
        el = el.replace("'", "''")
        new_list.append(el)
    return new_list
