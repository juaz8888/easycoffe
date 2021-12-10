from re import match
from typing import Match
from flask import Flask, render_template, abort, request, redirect, url_for, session
from flask.wrappers import Request
import modelo

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login.html")
def inicio_sesion():

    return render_template("login.html")


@app.route("/form_ini.html",methods=["POST","GET"])
def form_ini():
    if request.method=="POST":
        correo=request.form["correo"]
        pwd=request.form["contraseña"]

        #validacion de los datos
        db=modelo.db()
        dato=db.consulta_usuario(correo,pwd)

        if dato==False:
            return render_template("login.html",r_usuario=1)
        else:
            return render_template("form_ini.html",nombre=dato[0],cod=dato[1]) 

    if request.method=="GET":
        cod=request.args.get("cod")       
        db=modelo.db()  
        dato=db.valida_usuario(cod)
        if dato==False:
            return render_template("login.html",r_usuario=1)
        else:
            return render_template("form_ini.html",nombre=dato[0],cod=dato[1]) 

@app.route('/form_usuario.html')
def form_usuario():
    return render_template("form_usuario.html")

@app.route('/usuario_registro.html', methods=['POST','GET'] )
def usuario_registro():
   if request.method=='POST':
       nombre=request.form['Nombre']
       apellido=request.form['Apellido']
       contraseña=request.form['Contraseña1']
       vcontraseña=request.form['Contraseña2']
       email=request.form['email']
       db=modelo.db()
       db.nuevo_usuario(nombre,apellido,email,contraseña)

       return redirect(url_for("index"))

@app.route('/form_cultivo.html', methods=['POST','GET'] )
def form_cultivo():
    if request.method=='GET':
        cod=request.args.get("cod")
        db=modelo.db()
        lote=db.buscar_lote(cod)
        return render_template("form_cultivo.html",cod=cod,lote=lote)


@app.route('/form_nuevo_lote.html', methods=['POST','GET'])
def nuevo_lote():
    db=modelo.db()  
    if request.method=="GET":
        cod=request.args.get("cod")       
        
        dato=db.valida_usuario(cod)
        if dato==False:
            return ("Algo ha salido mal, inicia nuevamente sesion")
        else:
            return render_template("form_nuevo_lote.html",cod=dato[1]) 

    if request.method=="POST":
        #obtiene la informacion del metodo post
        descripcion=request.form['descripcion']
        area=request.form['area']
        topografia=request.form['topografia']
        imagen=request.form['imagen']
        cod=request.form['cod']
        #guarda la informacion en base de datos
        mensaje=db.nuevo_lote(descripcion,area,cod,topografia,imagen,"SIEMBRA",0,"31-12-2021")
        lote=db.buscar_lote(cod)

        return render_template("form_cultivo.html",cod=cod,lote=lote)
        
@app.route('/form_planta_lote.html',methods=['POST','GET'])
def agrega_planta():
    db=modelo.db() 
   
    if request.method=="GET":
       
        cod=request.args.get("cod") 
        lote=request.args.get("lote")
        #busca informqacion del lote
        info_lote=db.info_lote(cod,lote)
        #cuenta la cantidad de plantas en el lote
        #n_plantas=db.contar_plantas_lote(cod,lote)
        
        #limite de plantas sugerido
        area_lote=info_lote[0][2]
        limite=area_lote*0.4


        #info para el template
        info={'descripcion': info_lote[0][1],'n_plantas':info_lote[0][7],'estado_lote':info_lote[0][6],'estado_fecha':info_lote[0][8],'area':area_lote,'limite':int(limite)}

    return render_template("form_planta_lote.html",cod=cod,lote=lote, info=info)

@app.route('/actualizar_planta', methods=['POST'])
def act_planta():
    db=modelo.db() 
    if request.method=='POST':

        cod=request.form['cod']
        lote=request.form['lote']
        act_planta=int(request.form['n_plantas'])
        print(act_planta)

        if act_planta>=0:
            db.actualiza_planta_lote(cod,lote,act_planta)
            info_lote=db.info_lote(cod,lote)
            area_lote=info_lote[0][2]
            limite=area_lote*0.4

            info={'descripcion': info_lote[0][1],'n_plantas':info_lote[0][7],'estado_lote':info_lote[0][6],'estado_fecha':info_lote[0][8],'area':area_lote,'limite':int(limite)}
        else:
            info_lote=db.info_lote(cod,lote) 
            area_lote=info_lote[0][2]
            limite=area_lote*0.4
            info={'descripcion': info_lote[0][1],'n_plantas':info_lote[0][7],'estado_lote':info_lote[0][6],'estado_fecha':info_lote[0][8],'area':area_lote,'limite':int(limite)} 
    
    
    return render_template("form_planta_lote.html",cod=cod,lote=lote, info=info)

@app.route('/diagnostico',methods=['POST','GET'])
def diagnostico():
    db=modelo.db()
    if request.method=='POST':
        datos=[]
        datos=request.form['datos[]']
        cod=request.form['cod']
        lote=request.form['lote']
        cod_prueba_est=request.form['cod_prueba_est']
        dcc=[]
       
        tx=""
        for i in datos:
            
            
            if i==",":
                dcc.append(tx)
                tx=""
                continue
            tx=tx+ i
        dcc.append(tx)

        print(dcc)
        
        dec=controles()
        arreglo=dec.decodificador(dcc)
        arreglo['cod_usuario']=cod
        arreglo['cod_lote']=lote
        arreglo['cod_prueba_est']=cod_prueba_est
        db.pruebas_crecimiento(arreglo)
        
        dato=db.valida_usuario(cod)
        return render_template("form_ini.html",nombre=dato[0],cod=dato[1])


@app.route("/resultados.html",methods=['POST','GET'])
def resultados(): 
    db=modelo.db()
    if request.method=='GET':
        cod=request.args.get("cod") 
        datos=db.buscar_resultados(cod)

    datos_prueba=datos['datos']  
    datos_r=datos['datos_ref']
    datos_result=[]
    texto=""
    
    for item in datos_prueba:
        
        
        #humedad
        dr=item[3]
        dt=datos_r[0][0][2]
        if (dt/1.1)<dr<(dt*1.1):
            texto=texto + "Hm normal "
            
        else:
            texto=texto + " Hm* "
              

        #ALTURA
        dr=item[4]
        dt=datos_r[0][0][3]
        if (dt/1.1)<dr<(dt*1.1):
            texto=texto + "At normal "
            
        else:
            texto=texto + " At* "
             

        #ANCHO
        dr=item[5]
        dt=datos_r[0][0][4]
        if (dt/1.1)<dr<(dt*1.1):
            texto=texto + "Ac normal "
            
        else:
            texto=texto + " Ac* "
               

        #Arcilla
        dr=item[6]
        dt=datos_r[0][0][5]
        if (dt/1.1)<dr<(dt*1.1):
            texto=texto + "Al normal "
            
        else:
            texto=texto + " Al* "
               

        #Nitrogeno
        dr=item[7]
        dt=datos_r[0][0][6]
        if (dt/1.1)<dr<(dt*1.1):
            texto=texto + "Ng normal "
            
        else:
            texto=texto + " Ng* "
                
        
        datos_result.append(texto)

    return render_template("resultados.html",cod=cod,datos=datos['datos'],datos_ref=datos['datos_ref'],descripcion=datos['descripcion'],datos_result=datos_result)



class controles():

    def decodificador(self,dicc):
        n_muestras=len(dicc)/5
        x=1
        
        datos={}
        datos['dato1']=0
        datos['dato2']=0
        datos['dato3']=0
        datos['dato4']=0
        datos['dato5']=0
        cd=0
        while x <= n_muestras:
            
            contador=0
            while contador<=(5-1):
                
                datos['dato1']=(float(dicc[cd])+datos['dato1'])
                contador=contador+1
                cd+=1
                datos['dato2']=(float(dicc[cd])+datos['dato2'])
                contador=contador+1
                cd+=1
                datos['dato3']=(float(dicc[cd])+datos['dato3'])
                contador=contador+1
                cd+=1
                datos['dato4']=(float(dicc[cd])+datos['dato4'])
                contador=contador+1
                cd+=1
                datos['dato5']=(float(dicc[cd])+datos['dato5'])
                contador=contador+1
                cd+=1
                print(datos)
                

            x=x+1    


        datos['dato1']=round(datos['dato1']/n_muestras,2)
        datos['dato2']=round(datos['dato2']/n_muestras,2)
        datos['dato3']=round(datos['dato3']/n_muestras,2)
        datos['dato4']=round(datos['dato4']/n_muestras,2)
        datos['dato5']=round(datos['dato5']/n_muestras,2)
        print(datos)


        return(datos)



app.run(port=5000, debug=True)
