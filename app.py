from flask import Flask, render_template, request
from flask_login import login_user, LoginManager
from modelo.models import Usuario, db

app = Flask(__name__)

#db=SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:admin@localhost/bolsa'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
#Configuración de la gestion Usuarios con Flask-Login
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view="inicio"
#rutas para el ingreso a la aplicacion

@login_manager.user_loader
def load_user(id):
    return Usuario.query.get(int(id))

@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/login',methods=['post'])
def login():
    u=Usuario()
    usuario=u.validar(request.form['email'], request.form['password'])
    if usuario!=None:
        login_user(u)
        return render_template('Principal.html')
    else:
        return 'Usuario invalido'

@app.route('/guardarUsuario',methods=['post'])
def guardarUsuario():
    usuario = Usuario()
    usuario.Nombre = request.form['nombre']
    usuario.IdUsuario = request.form['IdUsuario']
    usuario.Sexo = request.form['sexo']
    usuario.Telefono = request.form['telefono']
    usuario.Email = request.form['email']
    usuario.Contraseña = request.form['password']
    usuario.insertar()
    return render_template('index.html')

@app.route('/Principal')
def principal():
    return render_template('Principal.html')

@app.route('/Usuario')
def Usuario():
    return render_template('Usuarios/Usuarios.html')

@app.route('/RegistrarUsuario')
def registrarUsuario():
    return render_template('Usuarios/RegistrarUsuarios.html')

#############---CRUD  de ALUMNOS EGRESADOS###############################################

@app.route('/Alumnos')
def alumnos():
    return render_template('AlumnosEgresados/AlumnosEgresados.html')

@app.route('/altaAlumnos')
def alta_Alumnos():
    return render_template('AlumnosEgresados/altaAlumnos.html')

@app.route('/consultaAlumnos')
def consulta_Alumnos():
    return render_template('AlumnosEgresados/consultaAlumnos.html')

@app.route('/editarAlumnos')
def editar_Alumnos():
    return render_template('AlumnosEgresados/editarAlumnos.html')
@app.route('/eliminarAlumnos')
def eliminar_Alumnos():
    return render_template('AlumnosEgresados/eliminarAlumnos.html')
#############################################################################################################

#####################----CRUD de Reclutores--------##############
@app.route('/Reclutadores')
def reclutores():
    return render_template('Reclutadores/Reclutadores.html')

@app.route('/altaReclutores')
def alta_Reclutador():
    return render_template('Reclutadores/altaReclutores.html')
@app.route('/consultaReclutores')
def consulta_Reclutador():
    return render_template('Reclutadores/consultaReclutores.html')
@app.route('/editarReclutores')
def editar_Reclutador():
    return render_template('Reclutadores/editarReclutores.html')
@app.route('/eliminarReclutores')
def eliminar_Reclutador():
    return render_template('Reclutadores/eliminarReclutores.html')

####################################################################

@app.route('/Empresas')
def empresas():
    return render_template('Empresa/Empresa.html')

@app.route('/Contratos')
def contratos():
    return render_template('Contratos/Contrato.html')

@app.route('/Categorias')
def categorias():
    return render_template('Categoria/Categoria.html')

@app.route('/registrarCarrera')
def carreras():
    return render_template('Carreras/Carreras.html')

########################3------CRUD de Ofertas__________################################
@app.route('/Ofertas')
def ofertas():
    return render_template('Ofertas/Ofertas.html')

@app.route('/altaOferta')
def alta_Oferta():
    return render_template('Ofertas/altaOferta.html')
@app.route('/ConsultaOfertas')
def consulta_Ofertas():
    return render_template('Ofertas/ConsultaOfertas.html')
@app.route('/editarOferta')
def editar_Oferta():
    return render_template('Ofertas/editarOferta.html')
@app.route('/eliminarOferta')
def eliminar_Oferta():
    return render_template('Ofertas/eliminarOferta.html')

##############################################################################

@app.route('/Postulaciones')
def postulaciones():
    return render_template('Postulacion/Postulacion.html')

#######################-------CRUD DE PersonalVinculacion--------###################
@app.route('/PersonalVinculacion')
def personal():
    return render_template('PersonalVinculacion/PersonalVinculacion.html')

@app.route('/altaPersonalVinculacion')
def alta_Reclutores():
    return render_template('PersonalVinculacion/altaPersonalVinculacion.html')
@app.route('/consultaPersonalVinculacion')
def consulta_PersonalVinculacion():
    return render_template('PersonalVinculacion/consultaPersonalVinculacion.html')
@app.route('/editarPersonalVinculacion')
def editar_PersonalVinculacion():
    return render_template('PersonalVinculacion/editarPersonalVinculacion.html')
@app.route('/eliminarPersonalVinculacion')
def eliminar_PersonalVinculacion():
    return render_template('PersonalVinculacion/eliminarPersonalVinculacion.html')
##############################################################################

@app.route('/Entrevista')
def entrevista():
    return render_template('Entrevista/Entrevista.html')

#@app.route('/registrarProducto')
#def registrarProducto():
 #   return '<h1>Registrando un producto</h1>'

#@app.route('/eliminarDocente/<int:idDocente>')
#def eliminarDocente(idDocente):
 #   return 'Eliminando al docente' + str(idDocente)

#@app.route('/consultarDocente/<id>')
#def eliminarDocente(id):
 #   return 'Consultando al docente' + id

#inicio del CRUD de alumnos

#@app.route('/alumnos/new')
#def nuevoAlumno():
 #   return render_template('Alumnos/altaAlumno.html')

#@app.route('/alumnos/edit')
#def editarAlumno():
 #   return render_template('Alumnos/editarAlumno.html')

if  __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)