#archivo principal archivo ejecutor ---   request-redirect enviar la ifo atravez del formulario y guardarla en la base de datos



from flask import Flask, render_template, request,redirect, session
from flaskext.mysql import MySQL

app=Flask(__name__) #todo el entorno con python, para poder trabajar con flask
#creamos llave secreata para la contraseña en el login
app.secret_key="hola"
#Establecemos conexion a la base de datos
mysql=MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='libreria'
mysql.init_app(app)



#donde con controla y la ruta
@app.route('/') #ruta para la primera pagina--aca esta en la raiz de la pagina '/'
def inicio():
    return render_template('Sitio/Index.html') #renderizado de las plantillas

@app.route('/Libros')
def libros():
    return render_template('Sitio/Libros.html')

@app.route('/Nosotros')
def nosotros():
    return render_template('Sitio/Nosotros.html')   


@app.route('/Admin')
def admin_Libros():
    #si no hay un login en la session
    if not'login' in session:
        return redirect('Admin/Login')#no l o dejamos pasar
        #minimizamos el riesgo que un usuario ajeno no entre

    conexion=mysql.connect()
    #traer la informacion de la base de datos
    #para que salga en la pagina web
    cursor=conexion.cursor()
    cursor.execute("SELECT * FROM libros")#consulta a la base de datos
    libros=cursor.fetchall()
    conexion.commit()

    return render_template('Admin/Libros.html', libros=libros)   

#ruta que reciba la informacion, ruta admin libros , poner el metodo como lo va a recibir
@app.route('/Admin/Libros/Guardar' , methods=['POST']) 
def admin_libros_guardar():
    __nombre=request.form['nombre_Libro']#a nombre asignele =voy a traer la informacion del formulario en el espacion input nombre_Libro
    __imagen=request.files['imagen_Libro']#files=traigame los archivos
    __url=request.form['url_Libro']
    #print(__nombre)
    #print(__imagen)
    #print(__url)
    #Ejecutar la sentencia de insercion de datos a la tabla
    sql="INSERT INTO libros (nombre, imagen, url) VALUES(%s, %s, %s )"
    datos=(__nombre, __imagen.filename, __url) #.filename=para que solo me salga el nombre del archivo
    conexion= mysql.connect()
    cursor=conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()
    return redirect('/Admin')

@app.route('/Admin/Libros/Editar', methods=['POST'])  
def editar():
    #recibir el dato con el metodo request y especificamos el name que nos lo envia
    __id__=request.form['id']
    #llamamos la conexion
    conexion=mysql.connect()
    cursor=conexion.cursor()
    #extraer la informacion, TRAIGAME LOS DATOS DE LA TABLA LIBROS
    consulta="SELECT * FROM libros WHERE id=%s"
    #cursor.execute("SELECT * FROM libros WHERE id=%s,"(__id__))
    cursor.execute(consulta, __id__)
    #para poder trabajar y poder editar por que aun estamos es consultado
    dato=cursor.fetchall()
    conexion.commit()
    #retornar valo y enviar dato llave primaria render que me lleve a otro sitio llamado editar
    return render_template('Admin/Editar.html',d= dato[0]) #enviamos el dato fetchall que me traiga todos los datos


@app.route('/Admin/Libros/Modificar', methods=['POST'])
def modificar():
    #recibimos todos los datos

    __id__ = request.form['filtro']
    __nombre__ = request.form['nombre_Libro']
    __url__ = request.form['url_Libro']

    conexion = mysql.connect()
    cursor =conexion.cursor()
    cursor.execute("UPDATE libros SET nombre=%s, url=%s WHERE id=%s",(__nombre__, __url__, __id__))#ingresar los datos debo de concatenar
    conexion.commit()
    return redirect('/Admin')# para redireccionarme a la pagina libros


@app.route('/Admin/Libros/Eliminar', methods=['POST'])
def eliminar():
    __id__ = request.form['id']
    conexion = mysql.connect()
    cursor =conexion.cursor()#nos lleva a donde necesitamos
    cursor.execute("DELETE FROM libros  WHERE id=%s",( __id__))#ingresar los datos debo de concatenar
    conexion.commit()
    return redirect('/Admin')# para redireccionarme a la pagina libros

@app.route('/Admin/Login')
def admin_login():
    return render_template('Admin/Login.html')

@app.route('/Admin/Login', methods=['POST']) #metodo post como enviamos la informacion atravez de el login
def admin_login_post():
    #recibimos datos que el usuario digita en el formulario
    __usuario__=request.form["txtUsuario"]
    __password__=request.form["txtPassword"]
    #variables de sesion
    if __usuario__=="Admin" and __password__=="123":
        session["login"]=True #declaramos variable tipo session
        session["usuario"]="administrador"
        #debo de cerrar las variabbles de session cerrar sesion para limpiar variables
        return redirect('/Admin')    
    return render_template('Admin/Login.html')


@app.route('/Cerrar')
def admin_cerrar():
    session.clear()#para limpiar las variables de sesion
    return redirect('Admin/Login')

    



     

    












if __name__=='__main__':
    app.run(debug=True)#ejecutame la app app.run en modo depuracion

