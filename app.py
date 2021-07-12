from flask import Flask, render_template, request
from flask_login import login_user, LoginManager
from modelo.models import Usuario, db

app = Flask(__name__)

# db=SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:admin@localhost/bolsa'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Configuración de la gestion Usuarios con Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "inicio"
# rutas para el ingreso a la aplicacion


@login_manager.user_loader
def load_user(id):
    return Usuario.query.get(int(id))


@app.route('/')
def inicio():
    return render_template('index.html')


@app.route('/login', methods=['post'])
def login():
    u = Usuario()
    usuario = u.validar(request.form['email'], request.form['password'])
    if usuario != None:
        login_user(u)
        return render_template('Principal.html')
    else:
        return 'Usuario invalido'


@app.route('/guardarUsuario', methods=['post'])
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


@app.route('/registrarAlumno')
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


@app.route('/opcionesAlumno')
def opciones_Alumnos():
    return render_template('AlumnosEgresados/opcionesAlumnos.html')
#############################################################################################################

#######################-------CRUD DE PersonalVinculacion--------###################


@app.route('/registrarPersonal')
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


@app.route('/opcionesPersonal')
def opciones_Personal():
    return render_template('PersonalVinculacion/opcionesPersonal.html')
#####################----CRUD de Reclutores--------##############


@app.route('/registrarReclutador')
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


@app.route('/opcionesReclutador')
def opciones_Reclutador():
    return render_template('Reclutadores/opcionesReclutadores.html')

###############################----Tablas de Ale-----#####################################

#-------CRUD-CARRERAS----------#


@app.route('/registrarCarrera')
def registrarCarreras():
    return render_template('Carreras/registrarCarreras.html')


@app.route('/opcionesCarreras')
def opcionesCarreras():
    return render_template('Carreras/opcionesCarreras.html')

#------CRUD EMPRESAS----------#


@app.route('/registrarEmpresa')
def registrarEmpresas():
    return render_template('Empresas/registrarEmpresas.html')


@app.route('/opcionesEmpresa')
def opcionesEmpresas():
    return render_template('Empresas/opcionesEmpresas.html')


#------CRUD de Ofertas---------#
@app.route('/registrarOferta')
def registrarOfertas():
    return render_template('Ofertas/registrarOfertas.html')


@app.route('/opcionesOfertas')
def opcionesOfertas():
    return render_template('Ofertas/opcionesOfertas.html')

#-----CRUD ENTREVISTAS-------#


@app.route('/registrarEntrevista')
def registrarEntrevista():
    return render_template('Entrevistas/registrarEntrevista.html')


@app.route('/opcionesEntrevista')
def opcionesEntrevista():
    return render_template('Entrevistas/opcionesEntrevista.html')

#######################--------Tablas de meny-----------#############################
#####-----CRUD Contrato-----#####


@app.route('/registrarContrato')
def registrarContrato():
    return render_template('Contratos/registrarContrato.html')


@app.route('/opcionesContratos')
def opcionesContratos():
    return render_template('Contratos/opcionesContratos.html')
#####-----CRUD Categoria-----#####


@app.route('/registrarCategoria')
def registrarCategoria():
    return render_template('Categoria/registrarCategoria.html')


@app.route('/opcionesCategoria')
def oopcionesCategoria():
    return render_template('Categoria/opcionesCategoria.html')
#####-----CRUD Postulacion-----#####


@app.route('/registrarOAlu')
def registrarOAlu():
    return render_template('Postulacion/registrarOAlu.html')


@app.route('/opcionesOAlu')
def opcionesOAlus():
    return render_template('Postulacion/opcionesOAlu.html')

##############################################################################


@app.route('/Entrevista')
def entrevista():
    return render_template('Entrevista/Entrevista.html')


# @app.route('/registrarProducto')
# def registrarProducto():
 #   return '<h1>Registrando un producto</h1>'

# @app.route('/eliminarDocente/<int:idDocente>')
# def eliminarDocente(idDocente):
 #   return 'Eliminando al docente' + str(idDocente)

# @app.route('/consultarDocente/<id>')
# def eliminarDocente(id):
 #   return 'Consultando al docente' + id

# inicio del CRUD de alumnos

# @app.route('/alumnos/new')
# def nuevoAlumno():
 #   return render_template('Alumnos/altaAlumno.html')

# @app.route('/alumnos/edit')
# def editarAlumno():
 #   return render_template('Alumnos/editarAlumno.html')


@app.errorhandler(404)
def error_404(e):
    return render_template('Comunes/error404.html'), 404


@app.errorhandler(500)
def error_500(e):
    return render_template('Comunes/error500.html'), 500


if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)
