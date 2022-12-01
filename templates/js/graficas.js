var js;
async function mostrarJSON(){
    var respuesta = await fetch("/json-stats");
    var json = await respuesta.text();
    js = JSON.parse(json);
    llenarTabla(js);
    tablaSemanales(js);
    tablaTotalesMensuales(js);
    tablaTotalesSemanales(js);
    
}
mostrarJSON();
function llenarTabla(js){
  let date = new Date();
  var xArray = ["Enero","Febrero","Marzo","Abril","Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"];
  var yArray = [js.monto.mensuales.enero, js.monto.mensuales.febrero, js.monto.mensuales.marzo, js.monto.mensuales.abril, js.monto.mensuales.mayo,js.monto.mensuales.junio,js.monto.mensuales.julio,js.monto.mensuales.agosto,js.monto.mensuales.septiembre,js.monto.mensuales.octubre,js.monto.mensuales.noviembre,js.monto.mensuales.diciembre];
  var data = [{
      x: xArray,
      y: yArray,
      type:"bar"
  }];

  var layout = {title: "Ingresos de ventas por mes REPORTE - "+date.toISOString().split('T')[0]+" Digic LiFE Solutions"};
  Plotly.newPlot("monto-mensualuales", data, layout);
}

function tablaSemanales(js){
  let date = new Date();
  var xArray = ["Actual","Anterior"];
  var yArray = [js.monto.semanales.actual, js.monto.semanales.anterior];
  var data = [{
      x: xArray,
      y: yArray,
      type:"bar"
  }];
  var layout = {title: "Ingresos de ventas en la semana actual y semana pasada - "+date.toISOString().split('T')[0]+" Digic LiFE Solutions"};
  Plotly.newPlot("monto-semanales", data, layout);
}

function tablaTotalesMensuales(js){
  let date = new Date();
  var xArray = ["Enero","Febrero","Marzo","Abril","Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"];
  var yArray = [js.totales.mensuales.enero, js.totales.mensuales.febrero, js.totales.mensuales.marzo, js.totales.mensuales.abril, js.totales.mensuales.mayo,js.totales.mensuales.junio,js.totales.mensuales.julio,js.totales.mensuales.agosto,js.totales.mensuales.septiembre,js.totales.mensuales.octubre,js.totales.mensuales.noviembre,js.totales.mensuales.diciembre];
  var data = [{
      x: xArray,
      y: yArray,
      type:"bar"
  }];

  var layout = {title: "Ventas por mes REPORTE - "+date.toISOString().split('T')[0]+" Digic LiFE Solutions"};
  Plotly.newPlot("totales-mensuales", data, layout);
}

function tablaTotalesSemanales(js){
  let date = new Date();
  var xArray = ["Actual","Anterior"];
  var yArray = [js.totales.semanales.actual, js.totales.semanales.anterior];
  var data = [{
      x: xArray,
      y: yArray,
      type:"bar"
  }];
  var layout = {title: "Ventas en la semana actual y semana pasada - "+date.toISOString().split('T')[0]+" Digic LiFE Solutions"};
  Plotly.newPlot("totales-semanales", data, layout);
}