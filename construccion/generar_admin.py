# -*- coding: utf-8 -*-
"""Arma lo que la maqueta del modulo de administracion toma del formulario
(DEC-242), para que no haya dos copias que se separen:

1. Las variables de color y medida (:root) y el logotipo, leidos del texto del
   prototipo del formulario; los nombres de las materias, de su catalogo
   MATERIAS; las opciones de genero y edad, del paso 5; las capas del mapa
   vectorial; y el «hoy» fijo con que se cuentan los dias habiles.
2. Cuarenta denuncias ficticias, armadas con la logica del propio formulario:
   se carga un escenario del panel de validacion, se cambia lo que haga falta
   y el formulario calcula lo demas —area que recibe, remision, tipo de zona,
   alcaldia del punto, celda UGA, folio con su caracter verificador y fecha de
   recepcion en hora de la Ciudad—. Cada una pasa la validacion de los cinco
   pasos; si alguna no, el guion se detiene. Se guardan en
   prototipo/administracion/denuncias-ficticias.json, con la forma que tendra
   la base, y se inyectan en la maqueta.
3. Lo que el modulo agrega al tramite —estado, area actual, persona asignada,
   historial, notificacion, marcas de revision— segun la propuesta del
   bosquejo (documento 22). Los estados, las marcas y las personas de
   atención se leen de la maqueta, que es donde viven; los canales de la
   captura, del formulario, y lo capturado por personal pasa por su modo
   captura (AD-03).

Todo es determinista: sin azar ni reloj, de modo que correrlo dos veces da el
mismo resultado. Necesita el artefacto (construir.py) y Playwright.

Uso:  python construccion/generar_admin.py
"""
import datetime, hashlib, json, os, pathlib, re, sys
from playwright.sync_api import sync_playwright

RAIZ    = pathlib.Path(os.path.abspath(__file__)).parent.parent
PROTO   = RAIZ / 'prototipo' / 'prototipo-denuncia-ambiental-sedema.html'
ARTE    = RAIZ / 'construccion' / 'artefacto.html'
MAQUETA = RAIZ / 'prototipo' / 'administracion' / 'maqueta-administracion.html'
DATOS   = RAIZ / 'prototipo' / 'administracion' / 'denuncias-ficticias.json'
TMP     = RAIZ / 'construccion' / '_generar_admin.html'
CHROMIUM = os.environ.get('CHROMIUM')
INICIO, FIN = 'DESDE EL FORMULARIO', 'FIN DE LO QUE VIENE DEL FORMULARIO'

# El «hoy» de la maqueta es fijo: con el reloj real, los plazos y los
# vencimientos cambiarian cada dia y las pruebas no podrian fijarlos.
HOY = datetime.datetime(2026, 10, 21, 10, 0, tzinfo=datetime.timezone(datetime.timedelta(hours=-6)))

# ---------------------------------------------------------------------------
# Personas ficticias: legibles e inequivocamente falsas (norma de datos
# ficticios). Nada que parezca una persona real.
NOMBRES = [('Fulana', 'de Tal', 'Ejemplo'), ('Mengano', 'Pérez', 'Prueba'), ('Zutana', 'López', 'Ficticia'),
           ('Perengano', 'Ruiz', 'Ejemplo'), ('Fulano', 'Gómez', 'Prueba'), ('Mengana', 'Díaz', 'Ficticia'),
           ('Zutano', 'Herrera', 'Ejemplo'), ('Perengana', 'Soto', 'Prueba')]
NOMBRE_LARGO = ('Fulana de las Mercedes Guadalupe', 'de Tal y Ejemplo', 'Prueba Ficticia')
# Las personas de atención viven en la maqueta (PERSONAL), que simula a una de
# ellas en el perfil de atención; se leen de ahí más abajo.
COORDINACION = {'DGIVA': 'Coordinación de prueba (DGIVA)', 'DGCORENADR': 'Coordinación de prueba (DGCORENADR)', '': 'Coordinación de prueba'}

# Un relato por materia, para que lo que se lee concuerde con lo que se elige.
HECHOS = {
  'impacto':      'Construyen un edificio de cinco pisos en un predio que era jardín y no hay letrero de autorización ambiental a la vista.',
  'emisiones':    'De la chimenea del negocio sale humo gris todas las tardes y el olor llega a las casas de la cuadra.',
  'ruido':        'La maquinaria de la fábrica trabaja de noche y el ruido no deja dormir a los vecinos de la calle.',
  'quema':        'Queman llantas y basura en un terreno baldío los fines de semana; el humo es negro y muy espeso.',
  'vehiculo':     'Un camión de carga sale todos los días del patio echando humo negro por el escape.',
  'verificacion': 'En el verificentro aprueban autos sin revisarlos si se paga una cantidad extra en la caja.',
  'plasticos':    'El comercio sigue entregando bolsas de plástico y popotes de un solo uso a todos los clientes.',
  'rsu':          'El restaurante saca su basura sin separar a la banqueta desde la noche anterior a la recolección.',
  'descargas':    'Del local sale agua jabonosa con olor a químico directo a la coladera de la calle cada mañana.',
  'construccion': 'La obra deja escombro y costales de cemento roto en la banqueta y nadie los recoge.',
  'cascajo':      'Camiones de volteo tiran cascajo en la orilla de la barranca por las noches.',
  'arbolado':     'Cortaron tres árboles grandes del camellón sin poner aviso ni explicar el motivo.',
  'areas_verdes': 'Están pavimentando el jardín del parque para hacer un estacionamiento de autos.',
  'tala':         'Derriban encinos con motosierra dentro del bosque y sacan la madera en camionetas.',
  'agua_zona':    'Rellenaron con tierra el canal que corría junto a las parcelas y el agua ya no pasa.',
  'asentamiento': 'Levantan casas de block en una zona que antes era bosque; cada semana aparece una nueva.',
  'terraceos':    'Una máquina retroexcavadora está quitando la tierra del cerro y la cargan en camiones.',
  'agroquimicos': 'En las parcelas rocían un plaguicida de olor muy fuerte que mata a los peces del canal.',
  'ava':          'Cercaron con malla una parte del área verde protegida y cobran por entrar.'
}
# Dónde se apoya cada grupo de materias: escenarios del panel, por zona.
BASES = {'zonas': ['sin_calle', 'conservacion', 'anp_coadmin', 'ava', 'anp_federal'],
         'otras': ['urbano', 'gobierno', 'otro_giro']}
CON_ESTABLECIMIENTO = {'emisiones', 'ruido', 'rsu', 'descargas', 'plasticos', 'verificacion', 'construccion'}
CANAL = {2: 'oficialia', 9: 'oficialia', 16: 'oficialia', 23: 'oficialia', 30: 'oficialia',
         1: 'telefono', 5: 'telefono', 19: 'telefono', 33: 'telefono', 12: 'correo', 26: 'correo', 37: 'comparecencia', 39: 'comparecencia'}
SOPORTE = {'oficialia': 'escrito-con-sello.pdf', 'telefono': 'nota-de-llamada.pdf', 'correo': 'correo-recibido.pdf',
           'comparecencia': 'acta-de-comparecencia.pdf'}
# Casos incómodos, cada uno una vez: la norma pide que algo se rompa.
SIN_PUNTO, ALCALDIA_DISTINTA, LARGO, SIN_ARCHIVOS_CADA = 3, 7, 13, 6
# El mismo hecho por dos vías (P-21, control 4): la 1 llega por teléfono con la
# materia de la 0, a unos treinta metros y dos días antes, para que la vista
# «Posible duplicado» de la bandeja tenga qué mostrar.
DUPLICA = {1: 0}
HECHOS_DUPLICADO = 'En el predio de junto levantan varios pisos sin ningún permiso a la vista; ya lo habían reportado otros vecinos.'
# Marcas que el servidor pondría al recibir (documento 15; SIA-15, SIA-26).
MARCA = {6: 'humanidad', 7: 'rafaga', 11: 'completitud'}
# Cinco de las más antiguas, todas cerradas, llegaron el año anterior: el
# tablero y el mapa tienen así dos años que comparar (DEC-251). Se recorren
# 52 semanas, que caen en el mismo día de la semana, para que los días
# hábiles se cuenten igual que si fueran de este año.
ANIO_ANTERIOR = {32, 34, 36, 38, 39}
UN_ANIO = datetime.timedelta(weeks=52)

def plan():
    """Una especificacion por denuncia, en el orden de los folios."""
    p = []
    materias = MATERIAS_IDS * 3
    for i in range(40):
        m = materias[i]
        grupo = 'zonas' if GRUPO[m] == 'zonas' else 'otras'
        bases = BASES[grupo]
        base = bases[i % len(bases)]
        # En las ANP federales y en el bosque urbano el punto no se mueve: El
        # Historico Coyoacan mide un kilometro y el AVA del escenario es
        # angosta; desplazado, el punto se sale del poligono.
        k = 0 if base in ('anp_coadmin', 'anp_federal', 'ava') else 1
        d = (((i * 7) % 9 - 4) * 0.0012 * k, ((i * 5) % 9 - 4) * 0.0012 * k)
        if i in DUPLICA:
            otra = p[DUPLICA[i]]
            m, base, d = otra['materia'], otra['base'], (otra['desplaza'][0] + 0.0002, otra['desplaza'][1] + 0.0002)
        anonima = i % 5 == 4
        corre = UN_ANIO if i in ANIO_ANTERIOR else datetime.timedelta(0)
        resp = 'gobierno' if base == 'gobierno' else ('empresa' if m in CON_ESTABLECIMIENTO else ('nose' if i % 3 == 0 else 'particular'))
        p.append({'i': i, 'base': base, 'materia': m, 'hechos': HECHOS_DUPLICADO if i in DUPLICA else HECHOS[m], 'desplaza': d,
                  'sin_punto': i == SIN_PUNTO, 'punto_otra_alcaldia': i == ALCALDIA_DISTINTA,
                  'anonima': anonima, 'nombre': NOMBRE_LARGO if i == LARGO else NOMBRES[i % len(NOMBRES)],
                  'establecimiento': m in CON_ESTABLECIMIENTO, 'otro_giro': i == 26, 'responsable': resp,
                  'fecha_ms': int((HOY - corre - datetime.timedelta(days=round(i * 1.3, 2), hours=i % 7)).timestamp() * 1000),
                  'consecutivo': 101 + i, 'archivos': i % SIN_ARCHIVOS_CADA != 5})
    return p

ARMA = r"""(plan) => {
  const fuera = [], salida = [];
  for (const r of plan) {
    cargaEscenario(r.base); cfg.validar = true;
    const g = (k, v) => guarda(k, v);
    g('materia', r.materia); g('hechos', r.hechos);
    if (r.materia !== 'vehiculo') g('veh_servicio', ''); else g('veh_servicio', 'carga');
    /* Establecimiento y responsable, coherentes con la materia. */
    if (r.establecimiento) {
      const giros = TIPOS_ESTAB.filter(t => t !== 'Otro');
      g('es_estab', 'si'); g('tipo_estab', r.otro_giro ? 'Otro' : giros[r.i % giros.length]);
      g('tipo_estab_otro', r.otro_giro ? 'Taller de pruebas' : ''); g('nombre_estab', 'Negocio Ficticio ' + r.i);
    } else { g('es_estab', 'no'); g('tipo_estab', ''); g('tipo_estab_otro', ''); g('nombre_estab', ''); }
    g('tipo_denunciado', r.responsable);
    if (r.responsable === 'nose') g('resp_senas', 'Dos personas en una camioneta blanca, entre semana por la mañana.');
    if (r.responsable === 'gobierno') { g('autoridad_nivel', 'alcaldia'); g('resp_area', 'Dirección de Obras de prueba'); }
    limpiaResponsable();
    /* Quien denuncia: con nombre ficticio o anónima con correo de ejemplo. */
    if (r.anonima) {
      g('identificacion', 'anonima');
      ['nombre','apellido_paterno','apellido_materno','dom_calle','dom_num_ext','dom_num_int','dom_entre_calles','dom_colonia','dom_cp',
       'dom_alcaldia','dom_municipio','dom_entidad','dom_fuera_cdmx','dom_tiene_mz_lote','dom_manzana','dom_lote','ruido_medicion'].forEach(k => g(k, ''));
      g('correo', 'anonima.' + String(r.i).padStart(2, '0') + '@ejemplo.local'); g('telefono', '');
    } else {
      g('identificacion', 'nombre');
      g('nombre', r.nombre[0]); g('apellido_paterno', r.nombre[1]); g('apellido_materno', r.nombre[2]);
      g('correo', r.nombre[0].split(' ')[0].toLowerCase() + '.' + String(r.i).padStart(2, '0') + '@ejemplo.local');
      g('telefono', '55000000' + String(r.i).padStart(2, '0'));
      /* Un escenario anónimo no trae domicilio: se le da uno de prueba. */
      if (!val('dom_calle') && !val('dom_fuera_cdmx')) {
        g('dom_tiene_mz_lote', 'no'); g('dom_num_ext', '10'); g('dom_colonia', 'La Joya'); g('dom_cp', '14090'); g('dom_alcaldia', 'Tlalpan');
      }
      g('dom_calle', 'Calle de Prueba ' + r.i);
      g('ruido_medicion', r.materia === 'ruido' ? 'si' : '');
    }
    /* El punto: el del escenario, un poco desplazado; o ninguno; o en otra
       alcaldía que la de la dirección. El formulario calcula lo demás. */
    if (r.sin_punto) {
      ['lat','lon','coord_pegar','alcaldia','capa_tipo','capa_clase','capa_categoria','capa_nombre','dg','remite_a','dg_nombre','dg_razon',
       'fuera','concurrencia','coadmin','uga','uga_version'].forEach(k => g(k, ''));
    } else {
      let la = +val('lat') + r.desplaza[0], lo = +val('lon') + r.desplaza[1];
      if (r.punto_otra_alcaldia) { la = 19.3720; lo = -99.1580; }
      analizaCapas(la.toFixed(6), lo.toFixed(6));
      if (val('fuera') === 'si') { fuera.push(r.i); continue; }
      g('lat', la.toFixed(6)); g('lon', lo.toFixed(6)); g('coord_pegar', la.toFixed(6) + ', ' + lo.toFixed(6));
    }
    actualizaAvisoAlcaldia();
    g('ubicacion_origen', val('lat') ? 'punto' : 'direccion');   /* como al enviar */
    const recibida = horaDeLaCiudad(new Date(r.fecha_ms));
    const cons = String(r.consecutivo).padStart(6, '0');
    g('fecha_acuse', recibida);
    g('folio', 'SEDEMA/DEN/' + recibida.slice(0, 4) + '/' + cons + '-' + digitoLuhn(recibida.slice(0, 4) + cons));
    g('fecha_hecho', recibida.slice(0, 8) + String(Math.max(1, +recibida.slice(8, 10) - 9)).padStart(2, '0'));
    /* Lo que llega por otro canal pasa por el modo captura del formulario
       (AD-03): su paso 0, su soporte y la recepción original, como al guardar. */
    if (r.captura) {
      cfg.captura = true;
      g('canal', r.canal); g('recepcion_fecha', r.captura.fecha); g('recepcion_hora', r.captura.hora);
      g('folio_origen', r.captura.folio_origen); g('recibio', r.captura.recibio); g('soporte', r.captura.soporte);
      g('fecha_recepcion_original', r.captura.fecha + 'T' + r.captura.hora + ':00' + recibida.slice(-6));
      g('verificacion', '');
    } else g('verificacion', 'si');
    /* Cada una pasa la validación de sus pasos, como si se hubiera enviado. */
    const malos = [];
    for (let n = r.captura ? 0 : 1; n <= 5; n++) { irA(n); if (!valida(n)) malos.push(n + ':' + Object.keys(MOTIVO).join(',')); }
    if (malos.length) { fuera.push(r.i + ' no valida ' + malos.join(' ')); continue; }
    const datos = {}; Object.keys(estado).sort().forEach(k => { if (estado[k] !== '' && estado[k] != null) datos[k] = estado[k]; });
    /* Lo capturado, en el orden del acuse y con el id de cada bloque, y el
       fundamento que citó el acuse (documento 22, §3.3). Sin género ni edad:
       en el módulo sólo aparecen en agregado (documento 22, §7). */
    const sg = val('sexo_genero'), er = val('edad_rango'), suyos = archivos;
    g('sexo_genero', ''); g('edad_rango', '');
    if (!r.archivos) archivos = [];
    const caja = document.createElement('div'); caja.innerHTML = pRevision();
    const idDe = Object.fromEntries([...caja.querySelectorAll('details.rev-bloque')].map(b => [b.querySelector('.rb-tit').textContent.trim(), b.id.slice(3)]));
    const acuse = {fundamento: fundamentoAcuse(), bloques: datosDelAcuse().map(b => ({id: idDe[b.titulo], titulo: b.titulo, filas: b.filas}))};
    g('sexo_genero', sg); g('edad_rango', er); archivos = suyos;
    salida.push({i: r.i, datos: datos, acuse: acuse, archivos: r.archivos ? archivos.map(a => ({name: a.name, size: a.size})) : []});
  }
  return {salida, fuera};
}"""

def foto(i, datos, j, a):
    """Lo que el formulario guarda de cada foto (DEC-121), con valores de
    prueba: la huella es de un texto, no de una imagen, y el lugar de captura
    cae junto al punto. Un PNG no trae EXIF, y la segunda foto de cada
    denuncia viene sin GPS, como pasa a menudo."""
    a = dict(a)
    ext = a['name'].rsplit('.', 1)[-1].lower()
    if ext not in ('jpg', 'jpeg', 'png'):
        return a
    a.update({'size_original': a['size'] * 4 + 81920 * (j + 1),
              'sha256_original': hashlib.sha256(('ficticio:%s:%s' % (datos['folio'], a['name'])).encode()).hexdigest(),
              'dimensiones': '2048x1536', 'optimizada': True, 'tipo': 'image/jpeg'})
    if ext != 'png' and datos.get('fecha_hecho'):
        a['fecha_captura'] = '%sT%02d:%02d:00' % (datos['fecha_hecho'], 8 + (i + j) % 10, (i * 7 + j * 13) % 60)
        if j == 0 and datos.get('lat'):
            a['lat_captura'] = round(float(datos['lat']) + 0.0001, 6)
            a['lon_captura'] = round(float(datos['lon']) - 0.0001, 6)
    return a

def entre_marcas(texto, inicio, fin, nuevo):
    """Reemplaza lo que hay entre la marca de inicio y la primera de fin que la
    sigue (las marcas se conservan). Se detiene si la de inicio no esta
    exactamente una vez o si no la sigue una de fin."""
    a = [m.end() for m in re.finditer(re.escape(inicio), texto)]
    b = texto.find(fin, a[0]) if len(a) == 1 else -1
    if b < 0:
        sys.exit('ERROR: no se encontraron, una sola vez y en orden, las marcas «%s» … «%s» en la maqueta.' % (inicio[:50], fin[:50]))
    return texto[:a[0]] + nuevo + texto[b:]

def tramite(r, datos, estados_ids):
    """Lo que el modulo agrega: estado, area actual, asignacion, historial,
    notificacion y marcas de revision. Ciclo principal del bosquejo, con los
    casos laterales."""
    i, dg = r['i'], datos.get('dg', '')
    camino = ['recibida', 'turnada', 'en_analisis', 'admitida', 'visita_programada', 'visita_practicada',
              'en_procedimiento', 'resuelta', 'notificada', 'concluida']
    especial = {SIN_PUNTO: 'por_ubicar', 8: 'returnada', 15: 'sin_materia', 22: 'acumulada'}
    if i in especial: final = especial[i]
    elif datos.get('remite_a'): final = 'remitida' if i % 2 == 0 else 'turnada'
    elif datos.get('tipo_denunciado') == 'gobierno' and i % 2 == 0: final = 'recomendacion'
    else: final = camino[min(len(camino) - 1, i // 4)]
    if final not in estados_ids:
        sys.exit('ERROR: el estado «%s» no existe en ESTADOS de la maqueta.' % final)
    if i in ANIO_ANTERIOR and final not in CIERRAN:
        sys.exit('ERROR: la denuncia %d llega el año anterior y no está cerrada («%s»).' % (i, final))
    if final == 'por_ubicar': pasos = ['recibida', 'por_ubicar']
    elif final in camino: pasos = camino[:camino.index(final) + 1]
    else: pasos = ['recibida', 'turnada', 'en_analisis', final]   # salidas laterales del ciclo
    area = dg
    if final == 'returnada': area = 'DGCORENADR' if dg == 'DGIVA' else 'DGIVA'
    recibida = datetime.datetime.fromisoformat(datos['fecha_acuse'])
    hueco = (HOY - (UN_ANIO if i in ANIO_ANTERIOR else datetime.timedelta(0)) - recibida) / max(1, len(pasos))
    historial = []
    for n, e in enumerate(pasos):
        quien = 'Sistema' if e in ('recibida', 'por_ubicar') else COORDINACION[dg] if e in ('turnada', 'returnada', 'remitida', 'acumulada') \
                else PERSONAL.get(area or 'DGIVA')[i % 2]
        historial.append({'estado': e, 'fecha': (recibida + hueco * n).isoformat(timespec='seconds'), 'persona': quien,
                          'nota': 'Movimiento de prueba.' if n else 'Ingresó por ' + ('el formulario en línea' if r['canal'] == 'en_linea' else 'captura por personal') + '.'})
    asignado = PERSONAL.get(area, [''])[i % 2] if final not in ('recibida', 'por_ubicar', 'turnada') else ''
    notif = None
    if final in ('notificada', 'concluida'):
        anon = datos.get('identificacion') == 'anonima'
        notif = {'medio': 'correo' if anon else 'domicilio', 'fecha': historial[-1]['fecha'],
                 'resultado': 'rebotado' if anon and i % 2 else 'entregado'}
    return {'estado': final, 'area_actual': area, 'asignado': asignado, 'historial': historial,
            'materia_confirmada': MATERIAS_IDS[(MATERIAS_IDS.index(datos['materia']) + 1) % len(MATERIAS_IDS)] if i in (10, 21) else datos['materia'],
            'notificacion': notif, 'acumulada_en': None, 'marcas': [MARCA[i]] if i in MARCA else []}

# ---------------------------------------------------------------------------
proto = PROTO.read_text(encoding='utf-8')
raiz = re.search(r'(?ms)^:root\{.*?^\}', proto)
logo = re.search(r'<img class="logo-inst"[^>]*>', proto)
if not raiz or not logo:
    sys.exit('ERROR: no se encontraron :root o el logotipo en el prototipo.')

def capa(nombre):
    """Una capa del SIA tal como la trae el prototipo: var NOMBRE=<JSON>;"""
    m = re.search(r'(?m)^var %s=(.*);$' % nombre, proto)
    if not m:
        sys.exit('ERROR: no se encontró la capa %s en el prototipo.' % nombre)
    return json.loads(m.group(1))
if not ARTE.exists():
    sys.exit('ERROR: no existe %s; corre antes construccion/construir.py.' % ARTE)

TMP.write_text('<!doctype html><html lang="es"><head><meta charset="utf-8">' + ARTE.read_text(encoding='utf-8') + '</body></html>', encoding='utf-8')
with sync_playwright() as pw:
    nav = pw.chromium.launch(executable_path=CHROMIUM)
    pg = nav.new_page()
    pg.goto(MAQUETA.as_uri()); pg.wait_for_timeout(300)
    estados_ids = pg.evaluate("() => ESTADOS.map(e => e.id)")
    CIERRAN = pg.evaluate("() => ESTADOS.filter(e => e.cierra).map(e => e.id)")
    marcas_ids = pg.evaluate("() => MARCAS.map(m => m.id)")
    PERSONAL = pg.evaluate("() => PERSONAL")
    pg.goto(TMP.as_uri()); pg.wait_for_timeout(600)
    MATERIAS_IDS = pg.evaluate("() => MATERIAS.map(m => m.id)")
    materias = pg.evaluate("() => MATERIAS.map(m => ({id: m.id, nom: m.nom}))")
    GRUPO = pg.evaluate("() => Object.fromEntries(MATERIAS.map(m => [m.id, m.g]))")
    canales = pg.evaluate("() => CANALES_CAPTURA.map(c => ({id: c.id, nom: c.nom}))")
    canales_ids = ['en_linea'] + [c['id'] for c in canales]
    P = plan()
    for r in P:
        r['canal'] = CANAL.get(r['i'], 'en_linea')
        if r['canal'] != 'en_linea':
            # Lo que llega por ventanilla o teléfono llega en horario de
            # oficina, un día antes de capturarse.
            recibida = datetime.datetime.fromtimestamp(r['fecha_ms'] / 1000, HOY.tzinfo)
            original = (recibida - datetime.timedelta(days=1)).replace(hour=9 + r['i'] % 8, minute=(r['i'] * 7) % 60)
            r['captura'] = {'fecha': original.strftime('%Y-%m-%d'), 'hora': original.strftime('%H:%M'),
                            'folio_origen': 'OP-%d-%04d' % (original.year, 500 + r['i']), 'recibio': 'Persona de Oficialía de prueba',
                            'soporte': SOPORTE[r['canal']]}
    hecho = pg.evaluate(ARMA, P)
    # Las opciones de género y edad, como las ofrece el paso 5 del formulario,
    # para que el tablero las cuente con los mismos nombres.
    estadistica = pg.evaluate("""() => { cargaEscenario('urbano'); irA(5);
      const o = k => [...document.querySelectorAll('#f_' + k + ' option')].filter(x => x.value).map(x => ({v: x.value, t: x.textContent}));
      return {sexo_genero: o('sexo_genero'), edad_rango: o('edad_rango')}; }""")
    nav.close()
TMP.unlink(missing_ok=True)
if not (estadistica['sexo_genero'] and estadistica['edad_rango']):
    sys.exit('ERROR: no se encontraron en el paso 5 del formulario las opciones de género y edad.')
if hecho['fuera']:
    sys.exit('ERROR: denuncias de prueba que no se pudieron armar: %s' % hecho['fuera'])
if any(c not in canales_ids for c in set(CANAL.values()) | {'en_linea'}):
    sys.exit('ERROR: un canal del generador no existe en CANALES_CAPTURA del formulario.')
if any(x not in marcas_ids for x in MARCA.values()):
    sys.exit('ERROR: una marca del generador no existe en MARCAS de la maqueta.')

denuncias = []
por_i = {r['i']: r for r in P}
for s in hecho['salida']:
    r = por_i[s['i']]
    d = {'es_ficticio': True, 'canal': r['canal'], 'datos': s['datos'],
         'archivos': [foto(r['i'], s['datos'], j, a) for j, a in enumerate(s['archivos'])]}
    if r['canal'] != 'en_linea':
        # Canal, recepción original, folio de origen, quién recibió y soporte
        # vienen en los datos, como los guarda el formulario; quién capturó lo
        # da la cuenta del módulo (AD-03).
        d['captura'] = {'capturo': 'Persona de captura de prueba'}
    d['acuse'] = s['acuse']
    d['tramite'] = tramite(r, s['datos'], estados_ids)
    denuncias.append(d)
# Una acumulada apunta a otra de su misma materia: la principal.
for d in denuncias:
    if d['tramite']['estado'] == 'acumulada':
        principal = next(x for x in denuncias if x is not d and x['datos']['materia'] == d['datos']['materia'])
        d['tramite']['acumulada_en'] = principal['datos']['folio']

DATOS.write_text(json.dumps(denuncias, ensure_ascii=False, indent=1) + '\n', encoding='utf-8', newline='\n')

# Las capas del mapa, las mismas del mapa vectorial del formulario: contorno,
# alcaldías y suelo de conservación completos; de las Áreas Naturales
# Protegidas y de Valor Ambiental, sólo las que tocan las denuncias de prueba,
# porque se dibuja lo que resulta del cruce y poco más.
zonas = {d['datos'].get('capa_nombre') for d in denuncias}
capas = {'bbox': capa('CDMX_BBOX'), 'borde': capa('CDMX_BORDE'),
         'alcaldias': [{'nombre': f['p']['nombre'], 'g': f['g']} for f in capa('CAPAS_ALCALDIAS')],
         'suelo': [f['g'] for f in capa('CAPAS_SUELO')],
         'zonas': [{'nombre': f['p']['nombre'], 'g': f['g']} for f in capa('CAPAS_GEOM') if f['p']['nombre'] in zonas]}

m = MAQUETA.read_text(encoding='utf-8')
m = entre_marcas(m, '/* ==== %s: variables de :root (construccion/generar_admin.py; no se edita aquí) ==== */' % INICIO,
                 '/* ==== %s ==== */' % FIN, '\n' + raiz.group(0) + '\n')
m = entre_marcas(m, '<!-- ==== %s: logotipo (construccion/generar_admin.py; no se edita aquí) ==== -->' % INICIO,
                 '<!-- ==== %s ==== -->' % FIN, '\n    ' + logo.group(0) + '\n')
m = entre_marcas(m, '/* ==== %s: catálogos y denuncias ficticias (construccion/generar_admin.py; no se edita aquí) ==== */' % INICIO,
                 '/* ==== %s ==== */' % FIN,
                 '\nvar HOY = ' + json.dumps(HOY.isoformat(timespec='seconds')) + ';\n'
                 'var MATERIAS = ' + json.dumps(materias, ensure_ascii=False) + ';\n'
                 'var OPCIONES_ESTADISTICA = ' + json.dumps(estadistica, ensure_ascii=False) + ';\n'
                 'var CANALES_CAPTURA = ' + json.dumps(canales, ensure_ascii=False) + ';\n'
                 'var CAPAS = ' + json.dumps(capas, ensure_ascii=False, separators=(',', ':')) + ';\n'
                 'var DENUNCIAS = ' + json.dumps(denuncias, ensure_ascii=False) + ';\n')
MAQUETA.write_text(m, encoding='utf-8', newline='\n')
print('maqueta de administración: %d denuncias ficticias; %.1f KB' % (len(denuncias), len(m.encode('utf-8')) / 1024))
