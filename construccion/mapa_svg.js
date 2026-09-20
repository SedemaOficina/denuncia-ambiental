
/* =========================================================
   MAPA VECTORIAL — versión para artefacto
   El entorno del artefacto bloquea imágenes y peticiones a
   servicios externos, de modo que no hay mosaicos de calles
   ni búsqueda por dirección. El mapa se dibuja con las capas
   del Sistema de Información Ambiental: contorno de la
   Ciudad, límites de alcaldía y los polígonos de zona.
   Estas definiciones sustituyen a las anteriores.
   ========================================================= */

var K_PROY = Math.cos(19.35 * Math.PI / 180);
function proyX(lon){ return lon * K_PROY; }
function proyY(lat){ return -lat; }
function invLat(y){ return -y; }
function invLon(x){ return x / K_PROY; }

var VISTA = null, VISTA_BASE = null, svgMapa = null, arrastrando = null;

function dDeGeom(g){
  var d = '', polis = g.type === 'Polygon' ? [g.coordinates] : g.coordinates;
  polis.forEach(function(poli){
    poli.forEach(function(anillo){
      anillo.forEach(function(pt,i){
        d += (i ? 'L' : 'M') + proyX(pt[0]).toFixed(5) + ' ' + proyY(pt[1]).toFixed(5) + ' ';
      });
      d += 'Z ';
    });
  });
  return d;
}

function centroideRing(g){
  var polis = g.type === 'Polygon' ? [g.coordinates] : g.coordinates, sx=0, sy=0, n=0;
  polis.forEach(function(p){ p[0].forEach(function(pt){ sx+=pt[0]; sy+=pt[1]; n++; }); });
  return [sy/n, sx/n];
}

function aplicaVista(){
  if(!svgMapa || !VISTA) return;
  svgMapa.setAttribute('viewBox', VISTA.x+' '+VISTA.y+' '+VISTA.w+' '+VISTA.h);
  var esc = VISTA.w / VISTA_BASE.w;
  svgMapa.querySelectorAll('.traza').forEach(function(p){
    p.setAttribute('stroke-width', (parseFloat(p.dataset.w) * esc).toFixed(5));
  });
  var tam = (VISTA.h * 0.020).toFixed(6);
  svgMapa.querySelectorAll('#etiquetas text').forEach(function(t){
    t.setAttribute('font-size', tam);
  });
  dibujaPunto();
}

function iniciaMapa(){
  var div = $('mapa'); if(!div) return;
  var b = CDMX_BBOX;
  var x0 = proyX(b[0]), x1 = proyX(b[2]), y0 = proyY(b[3]), y1 = proyY(b[1]);
  var mx = (x1-x0)*0.03, my = (y1-y0)*0.03;
  VISTA_BASE = {x:x0-mx, y:y0-my, w:(x1-x0)+2*mx, h:(y1-y0)+2*my};
  VISTA = {x:VISTA_BASE.x, y:VISTA_BASE.y, w:VISTA_BASE.w, h:VISTA_BASE.h};

  var alc = CAPAS_ALCALDIAS.map(function(f){
    return '<path class="traza alc" data-w="0.0012" d="'+dDeGeom(f.g)+'"><title>'+esc(f.p.nombre)+'</title></path>';
  }).join('');

  var etiquetas = CAPAS_ALCALDIAS.map(function(f){
    var c = centroideRing(f.g);
    return '<text x="'+proyX(c[1]).toFixed(5)+'" y="'+proyY(c[0]).toFixed(5)+'" text-anchor="middle">'+esc(f.p.nombre)+'</text>';
  }).join('');

  div.innerHTML =
    '<svg id="svgmapa" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid meet" role="img" aria-label="Mapa de la Ciudad de México">'+
      '<path id="contorno" class="traza" data-w="0.0022" d="'+dDeGeom(CDMX_BORDE)+'"/>'+
      '<g id="alcaldias">'+alc+'</g>'+
      '<g id="etiquetas">'+etiquetas+'</g>'+
      '<g id="zona"></g>'+
      '<g id="punto"></g>'+
    '</svg>'+
    '<div class="mapa-ctrl">'+
      '<button type="button" onclick="zoom(0.7)" aria-label="Acercar">+</button>'+
      '<button type="button" onclick="zoom(1.45)" aria-label="Alejar">&minus;</button>'+
      '<button type="button" onclick="resetVista()" aria-label="Ver toda la Ciudad">Toda la Ciudad</button>'+
    '</div>';

  svgMapa = $('svgmapa');
  aplicaVista();

  svgMapa.addEventListener('click', function(e){
    if(arrastrando) return;
    var p = aLatLon(e);
    if(p) ponMarcador(p[0], p[1]);
  });

  svgMapa.addEventListener('wheel', function(e){
    e.preventDefault();
    zoomEn(e.deltaY < 0 ? 0.85 : 1.18, e);
  }, {passive:false});

  var pan = null;
  svgMapa.addEventListener('pointerdown', function(e){
    if(e.target.closest('#punto')){
      arrastrando = 'punto';
      svgMapa.setPointerCapture(e.pointerId);
      return;
    }
    pan = {x:e.clientX, y:e.clientY, vx:VISTA.x, vy:VISTA.y};
    svgMapa.setPointerCapture(e.pointerId);
  });
  svgMapa.addEventListener('pointermove', function(e){
    if(arrastrando === 'punto'){
      var p = aLatLon(e);
      if(p){ guarda('lat', (+p[0]).toFixed(6)); guarda('lon', (+p[1]).toFixed(6)); dibujaPunto(); }
      return;
    }
    if(!pan) return;
    var r = svgMapa.getBoundingClientRect();
    VISTA.x = pan.vx - (e.clientX - pan.x) * (VISTA.w / r.width);
    VISTA.y = pan.vy - (e.clientY - pan.y) * (VISTA.h / r.height);
    aplicaVista();
  });
  function suelta(e){
    if(arrastrando === 'punto'){
      arrastrando = null;
      if(val('lat')) ponMarcador(val('lat'), val('lon'));
      return;
    }
    pan = null;
  }
  svgMapa.addEventListener('pointerup', suelta);
  svgMapa.addEventListener('pointercancel', suelta);

  if(val('lat')) ponMarcador(val('lat'), val('lon'));
}

function aLatLon(e){
  if(!svgMapa) return null;
  var r = svgMapa.getBoundingClientRect();
  var x = VISTA.x + (e.clientX - r.left) / r.width * VISTA.w;
  var y = VISTA.y + (e.clientY - r.top) / r.height * VISTA.h;
  return [invLat(y), invLon(x)];
}

function zoom(f){ zoomEn(f, null); }
function zoomEn(f, e){
  if(!VISTA) return;
  var cx, cy;
  if(e){
    var r = svgMapa.getBoundingClientRect();
    cx = VISTA.x + (e.clientX - r.left) / r.width * VISTA.w;
    cy = VISTA.y + (e.clientY - r.top) / r.height * VISTA.h;
  } else {
    cx = VISTA.x + VISTA.w/2; cy = VISTA.y + VISTA.h/2;
  }
  var nw = VISTA.w * f, nh = VISTA.h * f;
  if(nw > VISTA_BASE.w){ nw = VISTA_BASE.w; nh = VISTA_BASE.h; }
  if(nw < VISTA_BASE.w * 0.02) return;
  VISTA.x = cx - (cx - VISTA.x) * (nw / VISTA.w);
  VISTA.y = cy - (cy - VISTA.y) * (nh / VISTA.h);
  VISTA.w = nw; VISTA.h = nh;
  aplicaVista();
}
function resetVista(){
  VISTA = {x:VISTA_BASE.x, y:VISTA_BASE.y, w:VISTA_BASE.w, h:VISTA_BASE.h};
  aplicaVista();
}

function dibujaPunto(){
  var g = svgMapa && svgMapa.querySelector('#punto'); if(!g) return;
  if(!val('lat')){ g.innerHTML = ''; return; }
  var x = proyX(+val('lon')), y = proyY(+val('lat'));
  var s = VISTA.w * 0.035;
  g.innerHTML = '<g transform="translate('+x.toFixed(5)+' '+y.toFixed(5)+') scale('+(s/36).toFixed(6)+')" class="pin">'+
    '<ellipse cx="0" cy="0" rx="7" ry="2.6" fill="rgba(0,0,0,.28)"/>'+
    '<path d="M0 -44.5C-8 -44.5 -14.4 -38.1 -14.4 -30.1c0 10.2 12.4 24 13 24.6a1.9 1.9 0 0 0 2.8 0c.6-.6 13-14.4 13-24.6C14.4 -38.1 8 -44.5 0 -44.5z" fill="#9D2148" stroke="#fff" stroke-width="2.6"/>'+
    '<circle cx="0" cy="-30" r="5.4" fill="#fff"/></g>';
}

function resaltaPoligono(rasgo, grupo){
  limpiaResaltado();
  if(!rasgo || !svgMapa) return;
  var color = COLOR_ZONA[grupo] || '#9D2148';
  var g = svgMapa.querySelector('#zona');
  g.innerHTML = '<path class="traza" data-w="0.0022" d="'+dDeGeom(rasgo.g)+'" fill="'+color+'" fill-opacity=".30" stroke="'+color+'"/>';
  aplicaVista();
}
function limpiaResaltado(){
  var g = svgMapa && svgMapa.querySelector('#zona');
  if(g) g.innerHTML = '';
}
function quitaPunto(){
  ['lat','lon','capa_tipo','capa_nombre','dg','dg_nombre','dg_razon','fuera','concurrencia','coadmin','alcaldia_punto','punto_confirmado'].forEach(function(k){ guarda(k,''); });
  limpiaResaltado();
  render();
}
function ponMarcador(lat,lon){
  /* Igual que en el prototipo: cualquier colocacion o arrastre deja el punto
     sin confirmar. Esta funcion sobrescribe a la del prototipo, asi que la
     regla hay que repetirla aqui (ver LEEME, segunda regla). */
  guarda('punto_confirmado','');
  lat = (+lat).toFixed(6); lon = (+lon).toFixed(6);
  guarda('lat',lat); guarda('lon',lon);
  if($('coords')) $('coords').innerHTML = svgIcono('pin',15)+' '+lat+', '+lon;
  dibujaPunto();
  analizaCapas(lat,lon);
}
/* Sin servicio de geocodificación: la dirección no ubica el punto aquí. */
function ubicaPorDireccion(){
  var c = $('resBusqueda');
  if(c) c.innerHTML = '<div class="res-lista"><div class="vacio">Esta versión en línea no tiene el servicio que ubica la dirección. Da un clic sobre el mapa para colocar el punto.</div></div>';
}

/* El encuadre del mapa vectorial se centra en el punto, con el ancho de una colonia. */
function vaA(la,lo){
  if(VISTA_BASE){
    var w = VISTA_BASE.w * 0.035, h = VISTA_BASE.h * 0.035;
    VISTA = {x: proyX(lo) - w/2, y: proyY(la) - h/2, w: w, h: h};
    aplicaVista();
  }
  ponMarcador(la,lo);
  var c = $('resBusqueda'); if(c) c.innerHTML = '';
}
