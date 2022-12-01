var http = new XMLHttpRequest();
var url = '/finalizar_rep/finalizar';
/*
var importe = document.getElementById('importe').value;
var id = document.getElementById('id-rep').value;
var form = document.getElementById('contenido-prinicipal-reparaciones');
var formulario = new FormData(form);
http.open('POST', url);
http.send(formulario);
http.onload = () => console.log(http.responseText);
function alerta(e, http){

    const resp = JSON.parse(http.responseText);
    alert(resp.msg+" ***** "+resp.status);
    e.preventDefault();
}
*/

var form = document.getElementById('contenido-prinicipal-reparaciones');
var msg = document.querySelector(".mensaje");

form.addEventListener('submit', function(e){
});

form.addEventListener("click", function(e){
    //alerta(e, http)
    msg.style.opacity = "1";
    e.preventDefault();
});