function comprobar(){

    DatosForm = {}
    mensaje = ""
    aux = true;

    DatosForm[0] = document.getElementById('nombre').value
    DatosForm[1] = document.getElementById('rfc').value
   
   

    if(!validarNombre(DatosForm[0])){
        mensaje = mensaje + "El nombre  no es correcto.  \n\n"
        aux =false;
    }

    if(!validarRFC(DatosForm[1])){
        mensaje = mensaje + "El rfc que ingreso no es valido.  \n\n"
        aux =false;
    }

    for (const key in DatosForm) {
        if(DatosForm[key] == ""){
            mensaje = mensaje + "Algunos de los campos estan vacios \n\n"
            aux=false
            break
        }
    }

    
    if(aux){
        document.getElementById("btn-registrar").style.display = 'block';
        document.getElementById("btn-comprobar").style.display = 'none';

    }
    else{
        var modal = $('#errorModal')
        modal.find('.modal-title').text("Error")
        modal.find('.modal-body').text(mensaje)
        modal.modal('show')

    }

}

function validarNombre(valor){                  
    var regex = /^\w[a-zA-Z]/                                                  
    var response = regex.test(valor)                                                           
    return response;                                                                        
}    

function validarRFC(valor){
    var regex = /^([A-Z,Ñ,&]{3,4}([0-9]{2})(0[1-9]|1[0-2])(0[1-9]|1[0-9]|2[0-9]|3[0-1])[A-Z|\d]{3})$/
    var response=regex.test(valor)
    return responses;
}