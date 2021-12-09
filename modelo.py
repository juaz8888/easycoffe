
import sqlite3


class db():
    def __init__(self):
        self.conn = sqlite3.connect("easycoffee.db") 
        self.cur=self.conn.cursor()

    def nuevo_usuario(self,nombre,apellido,email,contraseña):
        data=(nombre,apellido,email,contraseña)
        query="INSERT INTO USUARIO (NOMBRE,APELLIDO,EMAIL,CONTRASEÑA) VALUES (?,?,?,?) "
        self.cur.execute(query,data)
        self.conn.commit()


    def consulta_usuario(self,correo,pwd):
        query=(f"SELECT * FROM USUARIO WHERE EMAIL='{correo}' AND CONTRASEÑA='{pwd}'")
        self.cur.execute(query)
        dato=self.cur.fetchone()
        if dato:
            #retorna el nombre y el codigo correspondiente
            return([dato[1],dato[0]])
        else:
            return(False)

    def valida_usuario(self,cod):
        query=(f"SELECT * FROM USUARIO WHERE COD='{cod}'")
        self.cur.execute(query)
        dato=self.cur.fetchone()
        if dato:
            #retorna el nombre y el codigo correspondiente
            return([dato[1],dato[0]])
        else:
            return(False)
    # cur.execute("SELECT * FROM ESTADO_PLANTA")
    # print(cur.fetchall())

    def nuevo_lote(self,descripcion,area,cod_usuario,topografia,imagen,estado_l,plantas,fechaf_estdao):
        data=(descripcion,area,cod_usuario,topografia,imagen,estado_l,plantas,fechaf_estdao)
        query="INSERT INTO LOTE (DESCRIPCION,AREA,COD_USUARIO,TOPOGRAFIA,IMAGEN,ESTADO_LOTE,PLANTAS,FECHAF_ESTADO) VALUES (?,?,?,?,?,?,?,?)"
        self.cur.execute(query,data)
        self.conn.commit()
        return("Datos guardados")

    def buscar_lote(self,cod):
        query=(f"SELECT * FROM LOTE WHERE COD_USUARIO='{cod}'")
        self.cur.execute(query)
        dato=self.cur.fetchall()
        return (dato)

    def info_lote(self,cod,cod_lote):
        query=(f"SELECT * FROM LOTE WHERE COD='{cod_lote}' AND COD_USUARIO='{cod}'")
        self.cur.execute(query)
        dato=self.cur.fetchall()
        return dato


    def contar_plantas_lote(self, cod, cod_lote):
        query=(f"SELECT count (*) FROM CULTIVO WHERE COD_USUARIO='{cod}' AND COD_LOTE='{cod_lote}'")
        self.cur.execute(query)
        dato=self.cur.fetchall()
        return dato

    def actualiza_planta_lote(self, cod, cod_lote, act_planta):
        query=(f"UPDATE LOTE SET PLANTAS = {act_planta} WHERE COD={cod_lote} AND COD_USUARIO={cod}")   
        self.cur.execute(query)
        self.conn.commit()


    def pruebas_crecimiento(self, arreglo):
        data=(arreglo['cod_usuario'],arreglo['cod_lote'],arreglo['dato1'],arreglo['dato2'],arreglo['dato3'],arreglo['dato4'],arreglo['dato5'],arreglo['cod_prueba_est'])
        query=(f"INSERT INTO PRUEBAS_CRECIMIENTO (COD_USUARIO, COD_LOTE, HUMEDAD, ALTURA, ANCHO, ARCILLA, NITROGENO, COD_PRUEBA_EST) VALUES (?,?,?,?,?,?,?,?)")  
        self.cur.execute(query,data)
        self.conn.commit()

    def buscar_resultados(self,cod):
        query=(f"SELECT * FROM PRUEBAS_CRECIMIENTO WHERE COD_USUARIO='{cod}' ")
        self.cur.execute(query)
        dato=self.cur.fetchall()
        busq_datos_ref=[]
        busq_descripcion_lote=[]
        for item in dato:
            query=(f"SELECT * FROM PRUEBA_ESTANDAR WHERE COD='{item[8]}' ")
            self.cur.execute(query)
            busq_datos_ref.append(self.cur.fetchall())
            query=(f"SELECT DESCRIPCION FROM LOTE WHERE COD='{item[2]}' AND COD_USUARIO='{item[1]}' ")
            self.cur.execute(query)
            busq_descripcion_lote.append(self.cur.fetchall())
        resultado={}
        resultado['datos']=dato
        resultado['datos_ref']=busq_datos_ref
        resultado['descripcion']=busq_descripcion_lote

        return resultado
        

if __name__ == "__main__":
    
    # dato=base.buscar_lote(1)
    # print(type(dato[0][5]))
    # dato=base.actualiza_planta_lote(6,1,120)
    # print(dato)
    pass
    
    
    