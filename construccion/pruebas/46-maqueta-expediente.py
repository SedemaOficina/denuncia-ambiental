# -*- coding: utf-8 -*-
"""Maqueta del módulo de administración, bloque C: el expediente (DEC-244).

   Lo que se espera se calcula aquí, aparte de la maqueta, con las reglas del
   bosquejo (documento 22, §3.3 y §4) y de las decisiones que cita.

   1. Las seis secciones del bosquejo, en su orden, para cada denuncia.
   2. Encabezado: estado, área, remisión, persona asignada y plazo vigente
      —el del Manual (DEC-84), en días hábiles desde la recepción original—,
      con «vencido» cuando se pasa.
   3. Denuncia: todo lo capturado en el orden del acuse y el fundamento que
      citó el acuse, que es el de DEC-232.
   4. El género y la edad no aparecen por denuncia (documento 22, §7).
   5. Consulta no ve nombre, contacto, domicilio ni lugar de captura de las
      fotos, ni la sección de contacto; captura tampoco ve esa sección.
   6. Evidencia con la huella de cada foto; actuaciones en orden; vínculos de
      acumulación en los dos sentidos; denuncias cercanas en el radio.
   7. Acciones según el perfil; ninguna se ejecuta.
   8. Una denuncia de otra área no se abre aunque se escriba su folio.
   9. Se llega desde la bandeja y «Atrás» regresa; en teléfono el encabezado
      no se queda fijo y no hay desplazamiento horizontal.
  10. Los archivos sólo traen campos que el formulario define para las fotos."""
import datetime, json, math, os, pathlib, re, sys
AQUI = pathlib.Path(os.path.abspath(__file__)).parent
RAIZ = AQUI.parent.parent
MAQUETA = RAIZ / 'prototipo' / 'administracion' / 'maqueta-administracion.html'
DATOS = RAIZ / 'prototipo' / 'administracion' / 'denuncias-ficticias.json'
DOC22 = RAIZ / 'documentacion' / '22-bosquejo-modulo-de-administracion.md'
PROTO = RAIZ / 'prototipo' / 'prototipo-denuncia-ambiental-sedema.html'
CHROMIUM = os.environ.get('CHROMIUM')  # sin la variable, Playwright usa el Chromium que él mismo instala
from playwright.sync_api import sync_playwright
fallos, notas = [], []
def afirma(c, m): (notas if c else fallos).append(('OK  ' if c else 'FALLA ') + m)

datos = json.loads(DATOS.read_text(encoding='utf-8'))
doc = DOC22.read_text(encoding='utf-8')
exp = doc[doc.index('### 3.3 Expediente'):doc.index('### 3.4')]
SECCIONES = ['%s. %s' % m for m in re.findall(r'(?m)^(\d)\. \*\*([^*]+?)\.\*\*', exp)]
# Plazo que corre en cada estado (documento 22, §4; DEC-84). «suelo»: 93 días
# en suelo urbano (DGIVA) y 90 en suelo de conservación (DGCORENADR).
PLAZOS = {'recibida': (3, 'turnar'), 'por_ubicar': (3, 'turnar'), 'turnada': (10, 'analizar la competencia'),
          'en_analisis': (10, 'analizar la competencia'), 'returnada': (5, 'returnar'),
          'admitida': ('suelo', 'el procedimiento completo'), 'visita_programada': ('suelo', 'el procedimiento completo'),
          'visita_practicada': ('suelo', 'el procedimiento completo'), 'en_procedimiento': ('suelo', 'el procedimiento completo')}
CIERRAN = {'remitida', 'concluida', 'acumulada', 'sin_materia', 'recomendacion'}
# Acciones por rol: documento 22, §2 («Hace») y §3.3, con MA-10.
TODAS = ['Cambiar el estado', 'Asignar o reasignar', 'Returnar a la otra dirección general', 'Remitir a otra autoridad',
         'Acumular a otro expediente', 'Corregir el punto del mapa', 'Registrar la notificación', 'Agregar nota o documento',
         'Descargar la ficha en PDF']
ACCIONES = {'coordinacion': TODAS,
            'atencion': ['Cambiar el estado', 'Corregir el punto del mapa', 'Registrar la notificación', 'Agregar nota o documento', 'Descargar la ficha en PDF'],
            'captura': ['Agregar nota o documento', 'Descargar la ficha en PDF'],
            'consulta': ['Descargar la ficha en PDF']}

def recepcion(x): return x['captura']['fecha_recepcion_original'] if 'captura' in x else x['datos']['fecha_acuse']
def dia(iso): return datetime.date(int(iso[:4]), int(iso[5:7]), int(iso[8:10]))
def habiles(desde, hasta):
    d, n = dia(desde), 0
    while d < dia(hasta):
        d += datetime.timedelta(days=1)
        n += d.weekday() < 5
    return n
def metros(a, b):
    r = math.pi / 180
    la1, la2 = float(a['lat']) * r, float(b['lat']) * r
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((float(b['lon']) - float(a['lon'])) * r / 2) ** 2
    return 2 * 6371000 * math.asin(math.sqrt(h))
def plazo_esperado(x, hoy):
    e = x['tramite']['estado']
    if e in PLAZOS:
        dias, para = PLAZOS[e]
        total = {'DGIVA': 93, 'DGCORENADR': 90}[x['tramite']['area_actual']] if dias == 'suelo' else dias
        van = habiles(recepcion(x), hoy)
        return 'Para %s: %d días hábiles; van %d%s' % (para, total, van, ' · vencido' if van > total else '')
    return 'Ninguno: el trámite se cerró' if e in CIERRAN else 'P-07'
# El fundamento del acuse (DEC-232): el artículo del Reglamento Interior del
# área que recibe —los dos si no hay punto— y el 331 de la Ley Ambiental si se
# señaló a una autoridad y no va a la PROFEPA.
def fundamento(x):
    d = x['datos']
    dg = d.get('dg') if d.get('lat') else ''
    f = ('Reglamento Interior del Poder Ejecutivo y de la Administración Pública de la Ciudad de México, ' +
         {'DGIVA': 'artículo 191, fracción XXX', 'DGCORENADR': 'artículo 188, fracción XXXVIII'}.get(dg, 'artículos 188, fracción XXXVIII, y 191, fracción XXX'))
    if not (dg and d.get('remite_a')) and d.get('tipo_denunciado') == 'gobierno':
        f += '; Ley Ambiental de la Ciudad de México, artículo 331'
    return f + '.'

LEE = """() => {
  const sec = [...document.querySelectorAll('.seccion-exp')];
  const fichas = s => [...s.querySelectorAll('.ficha > div')].map(x => [x.querySelector('dt').textContent, x.querySelector('dd').textContent]);
  const h2 = document.querySelector('#pantalla h2');
  return {h2: h2 ? h2.textContent : '', texto: document.getElementById('pantalla').innerText,
    cab: Object.fromEntries([...document.querySelectorAll('.exp-datos > div')].map(x => [x.querySelector('dt').textContent, x.querySelector('dd').innerText])),
    secciones: sec.map(s => s.querySelector('h3').textContent).filter(t => /^\\d\\./.test(t)),
    fichas: Object.fromEntries(sec.map(s => [s.querySelector('h3').textContent, fichas(s)])),
    actuaciones: [...document.querySelectorAll('.linea-tiempo li strong')].map(s => s.textContent),
    cercanas: document.querySelectorAll('.lista-exp li').length,
    acciones: [...document.querySelectorAll('.accion summary')].map(s => s.textContent)};
}"""

with sync_playwright() as pw:
    nav = pw.chromium.launch(executable_path=CHROMIUM)
    pg = nav.new_context(viewport={'width':1280,'height':900}).new_page()
    err = []
    pg.on('console', lambda x: err.append(x.text) if x.type == 'error' and 'fonts.g' not in x.text else None)
    pg.on('pageerror', lambda e: err.append('pageerror: ' + str(e)))
    pg.goto(MAQUETA.as_uri() + '#/bandeja'); pg.wait_for_timeout(600)
    cat = pg.evaluate("() => ({hoy: HOY, radio: RADIO_CERCANAS, estados: Object.fromEntries(ESTADOS.map(e => [e.id, e.nom])), ids: DENUNCIAS.map(idDe)})")
    def abre(perfil, ident):
        pg.evaluate("([p, i]) => { cambiaPerfil(p); location.hash = '#/expediente/' + i; }", [perfil, ident]); pg.wait_for_timeout(60)
        return pg.evaluate(LEE)

    malos = {k: [] for k in ('secciones', 'cabecera', 'acuse', 'fundamento', 'genero', 'evidencia', 'actuaciones', 'vinculos', 'cercanas', 'acciones')}
    vistas = {}
    for x, ident in zip(datos, cat['ids']):
        t = x['tramite']; f = x['datos']['folio']
        perfil = 'coordinacion_' + (t['area_actual'] or 'DGIVA').lower()
        v = vistas[f] = abre(perfil, ident)
        if v['secciones'] != SECCIONES: malos['secciones'].append((f, v['secciones']))
        esperado = {'Estado': cat['estados'][t['estado']], 'Área que recibe': t['area_actual'] or 'Por determinar',
                    'Remisión': x['datos'].get('remite_a') or 'Ninguna', 'Persona asignada': t['asignado'] or 'Sin asignar'}
        pl = plazo_esperado(x, cat['hoy'])
        if f not in v['h2'] or any(v['cab'].get(k) != w for k, w in esperado.items()) or not (v['cab'].get('Plazo vigente', '') == pl or (pl == 'P-07' and 'P-07' in v['cab'].get('Plazo vigente', ''))):
            malos['cabecera'].append((f, v['cab'], pl))
        filas = [tuple(r) for b in x['acuse']['bloques'] for r in b['filas']]
        vistas_filas = [tuple(r) for r in v['fichas']['1. Denuncia']]
        if any(r not in vistas_filas for r in filas): malos['acuse'].append(f)
        if ('Fundamento que citó', fundamento(x)) not in vistas_filas or x['acuse']['fundamento'] != fundamento(x): malos['fundamento'].append(f)
        if 'Datos estadísticos' in v['texto'] or re.search(r'\b(Mujer|Hombre|No binaria)\b|\d+ a \d+ años|Menor de 18|60 años o más', v['texto']):
            malos['genero'].append(f)
        ev = v['texto'][v['texto'].index('3. Evidencia'):v['texto'].index('4. Actuaciones')]
        for a in x['archivos']:
            if a['name'] not in ev or a.get('sha256_original', a['name']) not in ev or ('lat_captura' in a and str(a['lat_captura']) not in ev):
                malos['evidencia'].append((f, a['name']))
        if 'captura' in x and x['captura']['soporte'] not in ev: malos['evidencia'].append((f, 'soporte'))
        if v['actuaciones'] != [cat['estados'][h['estado']] for h in t['historial']]: malos['actuaciones'].append(f)
        vin = dict(v['fichas']['6. Vínculos'])
        acumuladas = [o['datos']['folio'] for o in datos if o['tramite']['acumulada_en'] == f]
        if vin['Acumulada en'] != (t['acumulada_en'] or 'No') or not all(a in vin['Acumuladas a ésta'] for a in acumuladas):
            malos['vinculos'].append(f)
        cerca = 0 if not x['datos'].get('lat') else sum(1 for o in datos if o is not x and o['datos'].get('lat') and metros(x['datos'], o['datos']) <= cat['radio'])
        if v['cercanas'] != cerca: malos['cercanas'].append((f, v['cercanas'], cerca))
        if v['acciones'] != ACCIONES['coordinacion']: malos['acciones'].append(f)

    afirma(len(SECCIONES) == 6 and not malos['secciones'], 'cada expediente tiene las seis secciones del bosquejo, en su orden: %s' % [SECCIONES, malos['secciones'][:1]])
    afirma(not malos['cabecera'], 'el encabezado dice estado, área, remisión, persona y el plazo que corre, con «vencido» si se pasa: %s' % malos['cabecera'][:1])
    vencidos = sum('vencido' in v['cab'].get('Plazo vigente', '') for v in vistas.values())
    afirma(0 < vencidos < 40, 'hay expedientes con el plazo vencido y otros en tiempo: %d vencidos' % vencidos)
    afirma(not malos['acuse'], 'la sección «Denuncia» trae todo lo capturado, en el orden del acuse: %s' % malos['acuse'][:3])
    afirma(not malos['fundamento'], 'el fundamento que citó el acuse es el de DEC-232 en cada ruta: %s' % malos['fundamento'][:3])
    afirma(not malos['genero'], 'el género y la edad no aparecen por denuncia (documento 22, §7): %s' % malos['genero'][:3])
    afirma(not malos['evidencia'], 'la evidencia trae cada archivo con su huella y su lugar de captura, y el soporte de lo capturado: %s' % malos['evidencia'][:3])
    afirma(not malos['actuaciones'], 'las actuaciones son el historial completo, en orden: %s' % malos['actuaciones'][:3])
    afirma(not malos['vinculos'] and any(o['tramite']['acumulada_en'] for o in datos), 'la acumulación se ve en los dos expedientes: %s' % malos['vinculos'][:3])
    afirma(not malos['cercanas'], 'las denuncias cercanas son las que caen en el radio: %s' % malos['cercanas'][:3])
    afirma(not malos['acciones'], 'coordinación tiene las nueve acciones del bosquejo')

    # ---- 5. Datos personales por perfil ----
    personales = {x['datos']['folio']: [x['datos'][k] for k in ('nombre', 'apellido_paterno', 'correo', 'telefono', 'dom_calle') if x['datos'].get(k)] for x in datos}
    malos_c, malos_k = [], []
    for x, ident in zip(datos, cat['ids']):
        f = x['datos']['folio']
        v = abre('consulta', ident)
        lugares = [str(a['lat_captura']) for a in x['archivos'] if 'lat_captura' in a]
        if any(re.search(r'(?<!\w)' + re.escape(p) + r'(?!\w)', v['texto']) for p in personales[f] + lugares) \
           or 'Este perfil no ve nombre, contacto ni domicilio' not in v['texto'] or 'Sólo la ven atención y coordinación' not in v['texto'] \
           or v['acciones'] != ACCIONES['consulta']:
            malos_c.append(f)
        if 'captura' in x:
            v = abre('captura', ident)
            if 'Sólo la ven atención y coordinación' not in v['texto'] or v['acciones'] != ACCIONES['captura'] \
               or (x['datos']['identificacion'] == 'nombre' and x['datos']['nombre'] not in v['texto']):
                malos_k.append(f)
    afirma(not malos_c, 'consulta no ve nombre, contacto, domicilio ni lugar de captura, ni la sección de contacto; sólo descarga la ficha: %s' % malos_c[:3])
    afirma(not malos_k, 'captura ve los datos de lo que capturó, no la sección de contacto, y sólo agrega notas o descarga: %s' % malos_k[:3])
    x = next(o for o in datos if o['tramite']['area_actual'] == 'DGIVA')
    v = abre('atencion_dgiva', cat['ids'][datos.index(x)])
    afirma(v['acciones'] == ACCIONES['atencion'] and '5. Contacto y notificación' in v['fichas'] and v['fichas']['5. Contacto y notificación'],
           'atención ve el contacto y tiene sus cinco acciones: %s' % v['acciones'])
    pg.click('.accion summary >> nth=0')
    afirma(pg.evaluate("() => { const d = document.querySelector('.accion'); return d.open && /Pide/.test(d.innerText) && /Deja registrado/.test(d.innerText); }"),
           'cada acción, al abrirla, dice qué pediría y qué dejaría registrado')

    # ---- 8. Acceso por área ----
    otra = cat['ids'][next(i for i, o in enumerate(datos) if o['tramite']['area_actual'] == 'DGCORENADR')]
    a1 = abre('atencion_dgiva', otra)['texto']
    a2 = abre('atencion_dgiva', '2026-999999-0')['texto']
    afirma('Este perfil no ve la denuncia' in a1 and 'No hay ninguna denuncia con el folio' in a2 and 'Denuncia' not in a1.split('Expediente', 1)[1][:40],
           'una denuncia de otra área no se abre escribiendo su folio, y un folio que no existe lo dice')

    # ---- 9. Navegación ----
    pg.evaluate("() => { cambiaPerfil('coordinacion_dgiva'); location.hash = '#/bandeja/todas'; }"); pg.wait_for_timeout(150)
    pg.click('.tabla-bandeja a.folio >> nth=0'); pg.wait_for_timeout(150)
    n = pg.evaluate("() => ({hash: location.hash, foco: document.activeElement.tagName, h2: document.querySelector('#pantalla h2').textContent, fijo: getComputedStyle(document.querySelector('.exp-encabezado')).position})")
    pg.click('.lista-exp a >> nth=0'); pg.wait_for_timeout(150)
    otro = pg.evaluate("() => location.hash")
    pg.go_back(); pg.wait_for_timeout(100); pg.go_back(); pg.wait_for_timeout(150)
    afirma(n['hash'].startswith('#/expediente/') and n['foco'] == 'H2' and n['fijo'] == 'sticky' and otro != n['hash'] and pg.evaluate("() => location.hash") == '#/bandeja/todas',
           'de la bandeja al expediente, a una cercana y de vuelta con «Atrás»; el encabezado se queda fijo: %s' % n)
    afirma(err == [], 'sin errores en consola: %s' % err[:2])

    tel = nav.new_context(viewport={'width':360,'height':760}).new_page()
    tel.goto(MAQUETA.as_uri() + '#/bandeja'); tel.wait_for_timeout(400)
    anchos = []
    for x, ident in zip(datos, cat['ids']):
        tel.evaluate("([p, i]) => { cambiaPerfil(p); location.hash = '#/expediente/' + i; }", ['coordinacion_' + (x['tramite']['area_actual'] or 'DGIVA').lower(), ident]); tel.wait_for_timeout(40)
        anchos.append(tel.evaluate("() => document.documentElement.scrollWidth - innerWidth"))
    fijo = tel.evaluate("() => getComputedStyle(document.querySelector('.exp-encabezado')).position")
    afirma(max(anchos) <= 0 and fijo == 'static', 'a 360 px ningún expediente se desplaza a lo ancho y el encabezado no se queda fijo: %s' % max(anchos))
    nav.close()

# ---- 10. Campos de los archivos ----
p = PROTO.read_text(encoding='utf-8')
de_foto = set(re.findall(r"(?m)^\s*(\w+):\s*\{etq:.*por:'foto'", p)) | {'name', 'size'}
sobran = {k for x in datos for a in x['archivos'] for k in a} - de_foto
afirma(not sobran and 'sha256_original' in de_foto, 'los archivos sólo traen campos que el formulario define para las fotos: %s' % sorted(sobran))
afirma(all(x['datos'].get('ubicacion_origen') == ('punto' if x['datos'].get('lat') else 'direccion') for x in datos),
       'cada denuncia trae el origen de su ubicación, como lo guarda el formulario al enviar')

print('\n'.join(notas)); print()
if fallos:
    print('\n'.join(fallos)); sys.exit(1)
print('TODAS LAS PRUEBAS PASAN (%d)' % len(notas))
