var apiUrl="/submit_venta";
const inputBuscador = document.getElementById('input-buscador');
const inputCliente = document.getElementById('input-cliente');
const inputBuscadorCliente = document.getElementById('input-buscador-clientes');
const listaCarrito = document.querySelector('#lista-carrito');
const venta = document.getElementById('venta');
var js;
var jsClientes;
var listaRefacciones;
var listaClientes;
var imgRefacciones;
var cart = [];
var refacciones = [];

monstrasJSON();
async function monstrasJSON() {
    var respuesta = await fetch("/json-refacciones");
    const respuestaClientes = await fetch("/json-clientes");
    var json = await respuesta.text();
    var jsonClientes = await respuestaClientes.text();
    js = JSON.parse(json);
    jsClientes = JSON.parse(jsonClientes);
    llenarTablaRefacciones(js);
    llenarTablaClientes(jsClientes);
}

function llenarTablaRefacciones (js){
    const contenedorTablaRefacciones = document.getElementById('contenido-lista-ventas');
    for (x in js){
        const refaccion = 
                        `
                    <div class="contenedor-ventas mt-3 mb-3" id="contenedor-ventas">
                        <div class="refaccion-marco">
                            <div class="row ml-2">
                                <div class="col">
                                    <label for="">ID REFACCIÓN</label>
                                    <br>
                                    <div id="barcode" class="parametro">
                                        ${js[x].barcode}
                                    </div>
                                </div>
                                <div class="col">
                                    <label for="">NOMBRE</label>
                                    <br>
                                    <div id="nombre" class="parametro">
                                        ${js[x].nombre}
                                    </div>
                                </div>
                                <div class="col">
                                    <button class="boton-mostrar" id="mostrar" onclick="mostrar(${x})"><i class="fa-solid fa-image"></i></button>
                                </div>
                            </div>
                            <div class="row mt-4">
                                <div class="col">
                                    <label for="">PRECIO</label>
                                    <br>
                                    <div id="precio" class="parametro">
                                        $${js[x].precio}
                                    </div>
                                </div>
                                <div class="col">
                                    <label for="">CANTIDAD DISPONIBLE</label>
                                    <br>
                                    <div id="cantidad" class="parametro">
                                        ${js[x].cantidad}
                                    </div>
                                </div>
                                <div class="col">
                                    <button class="boton-mostrar" id="agregarCarrito" onclick="agregarCarrito(${x})"><i class="fa-solid fa-cart-shopping"></i></button> 
                                </div>
                            </div>        
                        </div>
                    </div>
                    `;
                    contenedorTablaRefacciones.innerHTML += refaccion;
    }
    listaRefacciones = document.querySelectorAll('#contenedor-ventas');
}

function llenarTablaClientes(js){
    const contenidoTablaClientes = document.getElementById('lista-clientes');
    
    for (x in js){
        const elemento = 
        `
            <div class="elemento-cliente" id="elemento-cliente">
                <div class="row">
                    <div class="col-6">
                        <label for="nombre">${js[x].id_cliente}: ${js[x].nombres}</label>
                        <label for="celular">CELULAR - ${js[x].celular}</label>
                    </div>
                    <div class="col-6">
                        <button onclick="seleccionarCliente(${x})" class="seleccionar-cliente">SELECCIONAR</button>
                    </div>
                </div>
            </div>
        `;
        contenidoTablaClientes.innerHTML += elemento;
    }
    listaClientes = document.querySelectorAll('#elemento-cliente');
}

function mostrar(x){
    const image =  document.querySelector('#imagen-venta');
    const elemento = `<img src="/pi/${js[x].barcode}" width="350px" height="250px">`;
    image.innerHTML = "";
    image.innerHTML += elemento;
}

function confirmarVenta(){
    document.getElementById('mensaje-confirmacion').style.display="block";
}

function regresarVenta(){
    document.getElementById('mensaje-confirmacion').style.display="none";
}

function finalizarCarrito(){ 
    let idClientei = document.getElementById('id-input-seleccion').value;
    let nombrei = document.querySelectorAll('.nombre-cart');
    let cantidadi = document.querySelectorAll('.cantidad-cart');
    let barcodei = document.querySelectorAll('.barcode-cart');
    let precioi = document.querySelectorAll('.precio-cart');
    for (i=0;i<nombrei.length;i++){
        refacciones.push({barcode: barcodei[i].value,nombre: nombrei[i].value,cantidad: cantidadi[i].value, precio: precioi[i].value});
    }
    cart.push({Cliente: idClientei, Refaccion: refacciones});
    let stringArray = JSON.stringify(cart);
    sendJSON(stringArray, cart);
    console.log(cart);
}

function sendJSON(JSON, cart){
    let xhr = new XMLHttpRequest();
    let url = "/submit_venta";
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON);
    window.location = "/ultimaVenta";  
}


function agregarCarrito(x){
    const seleccion = document.querySelectorAll('#agregarCarrito');
    const item = seleccion[x].closest('#contenedor-ventas');
    const nombreItem = item.querySelector('#nombre').textContent;
    const cantidadItem = item.querySelector('#cantidad').textContent;
    const percioItem = item.querySelector('#precio').textContent
    const barcodeItem = item.querySelector('#barcode').textContent
    let cantidad = cantidadItem.replace(/\s+/g, ''); 
    if (cantidad > 0){
        venta.disabled = false;
        venta.style.opacity = 1;
        agregarItemCarrito(nombreItem, cantidadItem, percioItem, barcodeItem);
    }
}

function agregarItemCarrito(nombreItem, cantidadItem, percioItem, barcodeItem){
    let nombre = nombreItem.replace(/\s+/g, ''); 
    let precio = percioItem.replace(/\s+/g, ''); 
    let cantidad = cantidadItem.replace(/\s+/g, ''); 
    let barcode = barcodeItem.replace(/\s+/g, ''); 
    const nombreRefaccion = listaCarrito.getElementsByClassName('nombre-cart');
    for (i=0;i<nombreRefaccion.length;i++){
        if(nombreRefaccion[i].value === nombre){
            let row = nombreRefaccion[i].parentElement.parentElement
            .parentElement.querySelector('.cantidad-cart').value;
            console.log(row);
            console.log(cantidad);
            if (row == cantidad){
                return;
            }else{
                nombreRefaccion[i].parentElement.parentElement.parentElement.querySelector('.cantidad-cart').value++;
                actualizarCarritoTotal();
                return;
            }
        }
    }
    const rowItem = document.createElement('div');
    const element = 
    `
        <div class="row-item" id="row-item">
            <div class="row">
                <div class="col">
                    <input type="text" id="nombre-cart" class="nombre-cart" value="${nombre}" disabled>
                </div>
                <div class="col-3">
                    <div class="row">
                        <div class="col">
                            <input type="number" id="cantidad-cart" class="cantidad-cart" value="1" disabled>
                        </div>
                        <div class="col">
                            <div class="row">
                                <button id="aumentar" class="boton-cantidad">+</button>  
                            </div>
                             <div class="row">
                                <button id="reducir" class="boton-cantidad">-</button>                  
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col">
                    <input type="text" id="precio-cart" class="precio-cart" value="${precio}" disabled>
                </div>
                <div class="col">
                    <input type="text" id="barcode-cart" class="barcode-cart" value="${barcode}" style="display: none;" disabled>
                    <button class="eliminar-cart">X</button>
                </div>
            </div>
        </div>
    `;
    rowItem.innerHTML = element;
    listaCarrito.append(rowItem);
    rowItem.querySelector('.eliminar-cart').addEventListener('click', eliminarCarrito);
    rowItem.querySelector('#reducir').addEventListener('click',reducir);
    rowItem.querySelector('#aumentar').addEventListener('click',aumentar);
    actualizarCarritoTotal();
}



function actualizarCarritoTotal(){
    let total = 0;
    const carritoTotal = document.querySelector('#total');
    const itemCarrito = document.querySelectorAll('#row-item');
    itemCarrito.forEach((item)=>{
        const itemElement = item.querySelector('#precio-cart');
        const elementPrecio = Number (itemElement.value.replace('$',''));
        const contadorElemento = item.querySelector('.cantidad-cart');
        const valorContadorElemento = Number (contadorElemento.value);
        total = total + elementPrecio * valorContadorElemento;
    });
    carritoTotal.innerHTML = `${total.toFixed(2)}$`
}



function aumentar(e){
    const input = e.target.parentElement.parentElement.parentElement;
    const inputCantidad = input.querySelector('#cantidad-cart');
    const row = inputCantidad.parentElement.parentElement.parentElement.parentElement.parentElement;
    const barcodeCart = row.querySelector('#barcode-cart').value.replace(/\s+/g, '');
    const listRefa = document.querySelectorAll('#contenedor-ventas');
    listRefa.forEach((item)=>{
        const idListaRefa = item.querySelector('#barcode');
        const idRefa = idListaRefa.innerHTML.replace(/\s+/g, '');
        const cantidadRefa = item.querySelector('#cantidad');
        const cantRefaccion = cantidadRefa.innerHTML.replace(/\s+/g, '');
        if (barcodeCart == idRefa){
            if (input.querySelector('#cantidad-cart').value < cantRefaccion){
                input.querySelector('#cantidad-cart').value++;
                actualizarCarritoTotal();
            }
        }
    });
}

function reducir(e){
    const input = e.target.parentElement.parentElement.parentElement;
    const inputCantidad = input.querySelector('#cantidad-cart');
    const row = inputCantidad.parentElement.parentElement.parentElement.parentElement.parentElement;
    const barcodeCart = row.querySelector('#barcode-cart').value.replace(/\s+/g, '');
    const listRefa = document.querySelectorAll('#contenedor-ventas');
    listRefa.forEach((item)=>{
        const idListaRefa = item.querySelector('#barcode');
        const idRefa = idListaRefa.innerHTML.replace(/\s+/g, '');
        
        if (barcodeCart == idRefa){
            if (input.querySelector('#cantidad-cart').value > 1){
                input.querySelector('#cantidad-cart').value--;
                actualizarCarritoTotal();
            }
        }
    });
}

function eliminarCarrito(event){
    const botonClick = event.target;
    botonClick.closest('#row-item').remove();
    actualizarCarritoTotal();
    const listaRefa = document.querySelectorAll('#row-item');
    if (listaRefa.length<1){
        venta.disabled = true;
        venta.style.opacity = 0.5;
    }
}

inputBuscador.addEventListener('keyup', ()=>{
    buscadorRefacciones(listaRefacciones, js)
});

inputCliente.addEventListener("click", ()=>{
    document.querySelector('#buscador-cliente').classList.toggle('active');
});

inputBuscadorCliente.addEventListener('keyup', ()=>{
    buscadorClientes(listaClientes, jsClientes);
});

function buscadorRefacciones(listaRefacciones, js){
    var filtro = inputBuscador.value.toUpperCase();
    for( i = 0 ; i < listaRefacciones.length ; i++){
        if (js[i].barcode.toUpperCase().indexOf(filtro)>-1 || js[i].nombre.toUpperCase().indexOf(filtro) > -1) {
            listaRefacciones[i].style.display="";
        }else{
            listaRefacciones[i].style.display="none";
        }
    }
}

function buscadorClientes(listaClientes, js){
    var filtro = inputBuscadorCliente.value.toUpperCase();
    for (i=0; i<listaClientes.length;i++){
        if(js[i].nombres.toUpperCase().indexOf(filtro)>-1 || js[i].celular.indexOf(filtro)>-1){
            listaClientes[i].style.display="";
        }else{
            listaClientes[i].style.display="none";
        }
    }
}

function seleccionarCliente(x){
    document.querySelector('#id-input-seleccion').value = jsClientes[x].id_cliente;
    document.querySelector('#input-cliente-seleccion').value = jsClientes[x].nombres;
    document.querySelector('#buscador-cliente').classList.toggle('active');
    const lista = document.querySelectorAll('#row-item');
    for (i = 0; i<lista.length;i++){
        lista[i].remove();
    }
    refacciones.length = 0;
    cart.length = 0;
}