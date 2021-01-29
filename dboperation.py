import psycopg2


class DBWebscraping_linkedin:
    def __init__(self):
        pass

    def insert_webscraping(self, con, carga, index_keywords):
        try:
          index_KEY =str(index_keywords)
          mydb = con.connect()         
          cur = mydb.cursor() 
          # insertando un registro
          sql = "insert into webscraping (busqueda, busqueda_area, pagina_web, url_pagina, url_busqueda,fecha_creacion,fecha_modificacion,id_keyword) values (%s,%s,%s,%s,%s,current_date,current_date,'"+index_KEY+"')"
          params = (carga["busqueda"], carga["busqueda_area"], carga["pagina"], carga["url_principal"],carga["url_busqueda"])
                    
          cur.execute(sql, params)                 

          mydb.commit()

          sql = "SELECT last_value FROM webscraping_id_webscraping_seq"
          cur.execute(sql)  
          row_id = int(cur.fetchone()[0])
          
          # close the communication with the PostgreSQL
          cur.close()
          mydb.close()      
        except (Exception, psycopg2.DatabaseError) as error:                
                print (error)
                mydb.close()
        return row_id


class DBOferta:
    def __init__(self):
        pass

    def insert_oferta(self, connection, oferta):
        # try:
        #     mydb = connection.connect()
        #     cur = mydb.cursor()                                    
        #     sql = "insert into Oferta (id_webscraping, titulo,empresa,lugar,salario,oferta_detalle,url_oferta,url_pagina,fecha_creacion,fecha_modificacion,fecha_publicacion,id_anuncioempleo) values (%s,%s,%s,%s,%s,%s,%s,%s,current_date,current_date,%s,%s)"            
        #     params = (oferta["id_carga"], oferta["puesto"].strip(), oferta["empresa"].strip(), oferta["lugar"].strip(),oferta["salario"].strip(),oferta["detalle"].strip(), oferta["url"], oferta["url_pagina"],oferta["fecha_publicacion"],oferta["id_anuncioempleo"])
        #     cur.execute(sql, params)        
        #     mydb.commit()  
        #     sql = "SELECT last_value FROM Oferta_id_oferta_seq"
        #     cur.execute(sql)  
        #     row_id = int(cur.fetchone()[0])
        #     print(row_id)
        #     close the communication with the PostgreSQL
        #     cur.close()
        #     mydb.close()                           

        # except (Exception, psycopg2.DatabaseError) as error:                
        #         print ("-------------Exception, psycopg2.DatabaseError-------------------")
        #         print (error)
        #         mydb.close()        
        # return row_id        
        mydb = connection.connect()
        cur = mydb.cursor()
        sql0= "SELECT COUNT(id_anuncioempleo) FROM oferta WHERE id_anuncioempleo='"+str(oferta["id_anuncioempleo"])+"'"
        cur.execute(sql0)
        conteo = int(cur.fetchone()[0])
        cur.close()
        mydb.close() 
        if (conteo==0):       
            try:
                mydb = connection.connect()
                cur = mydb.cursor()                                    
                sql = "insert into Oferta (id_webscraping, titulo,empresa,lugar,salario,oferta_detalle,url_oferta,url_pagina,fecha_creacion,fecha_modificacion,fecha_publicacion,id_anuncioempleo) values (%s,%s,%s,%s,%s,%s,%s,%s,current_date,current_date,%s,%s)"            
                params = (oferta["id_carga"], oferta["puesto"].strip(), oferta["empresa"].strip(), oferta["lugar"].strip(),oferta["salario"].strip(),oferta["detalle"].strip(), oferta["url"], oferta["url_pagina"],oferta["fecha_publicacion"],oferta["id_anuncioempleo"])
                cur.execute(sql, params)        
                mydb.commit()
                print("Oferta nueva: ")
                print(oferta["url"])
                sql = "SELECT last_value FROM Oferta_id_oferta_seq"
                cur.execute(sql)  
                row_id = int(cur.fetchone()[0])
                print(row_id)
                # close the communication with the PostgreSQL
                cur.close()
                mydb.close()                           

            except (Exception, psycopg2.DatabaseError) as error:                
                    print ("-------------Exception, psycopg2.DatabaseError-------------------")
                    print (error)
                    mydb.close()        
        else :
                mydb = connection.connect()
                cur = mydb.cursor()
                sql = "SELECT last_value FROM Oferta_id_oferta_seq"
                cur.execute(sql)  
                row_id = int(cur.fetchone()[0])
                print("Oferta antigua: ")
                print(row_id)
                # close the communication with the PostgreSQL
                cur.close()
                mydb.close()
        return row_id                           

      



class DBOfertadetalle:
    def __init__(self):
        pass
    #strip() devuelve una cadena eliminando los caracteres iniciales como los finlaes 
    def insert_ofertadetalle(self, connection, oferta_detalle):        
        try:
            mydb = connection.connect()
            cur = mydb.cursor()                                    
            sql = "INSERT INTO OFERTA_DETALLE (id_oferta,descripcion,fecha_creacion,fecha_modificacion) VALUES (%s,%s,current_date,current_date)"            
            params = (oferta_detalle["id_oferta"],oferta_detalle["descripcion_tupla"])
            cur.execute(sql, params)        
            mydb.commit()  
            cur.close()
            mydb.close()                           

        except (Exception, psycopg2.DatabaseError) as error:                
                print ("-------------Exception, psycopg2.DatabaseError-------------------")
                print (error)
                mydb.close()                  
        return 1
       



class DBKeywords_linkedin:
    def __init__(self):
        pass

    def consultar_keywords(self,connection):
        mydb = connection.connect()
        cur = mydb.cursor()
        sql = "SELECT descripcion from KEYWORD_SEARCH"
        cur.execute(sql)
        rows = [item[0] for item in cur.fetchall()]
        keywords = []
        for index in range(0, len(rows)):
            keywords.append(rows[index].replace(" ", "%20"))
        cur.close()
        mydb.close() 
        return keywords
        
