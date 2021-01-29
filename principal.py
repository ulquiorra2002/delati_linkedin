# -*- coding: utf-8 -*-
import psycopg2
from configuration_linkedin import *
import webscraping_linkedin
from controller import Controller
from dbconnection import Connection


def set_url_busqueda(carga,urlkeywords):
        carga["url_principal"] = WS_PORTAL_LABORAL_URL
        urlbusqueda = "/jobs/search/?geoId=102927786&keywords="
        urladiconal = "&location=Per%C3%BA"
        paginado = "&start="

        carga["url_prefix"] = carga["url_principal"] + urlbusqueda + urlkeywords  
        carga["url_sufix"] = ""

        carga["url_busqueda"] = carga["url_principal"] + urlbusqueda + urlkeywords 


def connect_bd():
    con = Connection(DB_HOST, DB_SERVICE, DB_USER, DB_PASSWORD)
    con.connect()
    return con
   

if __name__ == "__main__":
    controller = Controller()
    con = connect_bd()

    carga = {}
    carga["pagina"] = WS_PORTAL_LABORAL
    carga["cant_paginas"] = WS_PAGINAS
    carga["pagina_inicial"] = WS_PAGINA_INICIAL
    carga["cant_ofertas"] = WS_OFERTAS
    carga["busqueda_area"] = WS_AREA
    carga["busqueda"] = ""
    urlkeywords = controller.dbkeywords.consultar_keywords(con)
    
    for index in range(0,1):
            listaOferta={}
            set_url_busqueda(carga,urlkeywords[index])
            index_keywords = index + 1
            print(urlkeywords[index])
            carga["id_carga"] = controller.registrar_webscraping(con, carga, index_keywords)

            listaOferta = webscraping_linkedin.scraping_ofertas(con, carga["url_principal"],carga["url_prefix"], carga["url_sufix"],
                                                    carga["pagina_inicial"], carga["cant_paginas"], carga["cant_ofertas"],
                                                    carga["id_carga"])
            webscraping_linkedin.scraping_ofertadetalle(con,listaOferta)