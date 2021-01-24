import preprocessing
from nltk import word_tokenize
from dboperation import DBWebscraping_linkedin
from dboperation import DBOferta
from dboperation import DBOfertadetalle
from dboperation import DBKeywords_linkedin


class Controller:
    def __init__(self):
        self.dbwebscraping = DBWebscraping_linkedin()
        self.dboferta = DBOferta()
        self.dbofertadetalle = DBOfertadetalle()
        self.dbkeywords = DBKeywords_linkedin()


    def registrar_webscraping(self, con, webscraping,index_keywords):
        id = self.dbwebscraping.insert_webscraping(con, webscraping,index_keywords)
        return id
    
    def obtener_keywords(self,con):
        respuesta = self.dbkeywords.consultar_keywords(con)
        return respuesta



    #Inserción directa
    def registrar_oferta(self, con, oferta):
        idResult = self.dboferta.insert_oferta(con, oferta)
        return idResult 

    #Insercion ofertas_detalle
    def registrar_oferta_detalle(self, con, oferta):
        idofertadetalle = self.dbofertadetalle.insert_ofertadetalle(con, oferta) 
        return idofertadetalle           





    #Inserción por lista
    def registrar_ofertas(self, con, lista_oferta):
        print(len(lista_oferta))
        for oferta in lista_oferta:
            print("----------------analizando que hay en lista oferta---------------------")
            print(oferta)
            idPuesto = self.dboferta.insert_oferta(con, oferta)     



    def generar_insert_ofertadetalle(self, oferta):
        sql_insert = "INSERT INTO OFERTA_DETALLE (id_oferta,descripcion,fecha_creacion,fecha_modificacion) VALUES (%s,'%s',sysdate,sysdate);"
        sql_result = ""
        for ed in oferta["listaDescripcion"]:
            sql = sql_insert % (oferta["idPuesto"], ed)
            sql_result = sql_result + sql
        return sql_result


    def registrar_normalizado(self, con, lista):
        for element in lista:
            new_words = preprocessing.normalize_words(word_tokenize(element["descripcion"]))
            descripcion_normalizada = " ".join(new_words)
            element["descripcion_normalizada"] = descripcion_normalizada
            DBOfertadetalle.update_requisito(con, element)
