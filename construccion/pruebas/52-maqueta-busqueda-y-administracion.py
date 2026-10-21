# -*- coding: utf-8 -*-
"""Maqueta del módulo de administración, bloque F: búsqueda, exportación y
   administración (DEC-249).

   1. Ya no queda ninguna pantalla «por construir» en ningún perfil.
   2. La descarga de la bandeja sale con sus columnas y sólo con lo que la
      bandeja tiene; sin datos de quien denuncia, salvo la de coordinación,
      que pide motivo y queda en la bitácora. Género y edad, nunca.
   3. Un valor que empieza como fórmula no se vuelve fórmula en la hoja.
   4. La descarga de indicadores trae las cifras del tablero, con género y
      edad ocultos bajo el mínimo.
   5. Un folio, su consecutivo o el folio de origen abren el expediente.
   6. Administración: perfiles, catálogos, plazos y umbrales tal como los usa
      la maqueta, lo que falta configurar y la bitácora de la sesión.
   7. En teléfono no hay desplazamiento horizontal."""
import csv, io, json, os, pathlib, sys
AQUI = pathlib.Path(os.path.abspath(__file__)).parent
RAIZ = AQUI.parent.parent
MAQUETA = RAIZ / 'prototipo' / 'administracion' / 'maqueta-administracion.html'
DATOS = RAIZ / 'prototipo' / 'administracion' / 'denuncias-ficticias.json'
CHROMIUM = os.environ.get('CHROMIUM')  # sin la variable, Playwright usa el Chromium que él mismo instala
from playwright.sync_api import sync_playwright
fallos, notas = [], []
def afirma(c, m): (notas if c else fallos).append(('OK  ' if c else 'FALLA ') + m)
# Lo único que la maqueta pide a internet son las tipografías; si no cargan, no
# es un error de la maqueta. Chrome no pone la dirección en el texto del aviso:
# se lee de su ubicación.
TIPOGRAFIAS = ('https://fonts.googleapis.com/', 'https://fonts.gstatic.com/')
COLUMNAS = ['Folio', 'Recepción', 'Canal', 'Materia', 'Alcaldía', 'Colonia', 'Tipo de zona', 'Área que recibe', 'Remisión',
            'Estado', 'Persona asignada', 'Días hábiles']
PERSONALES = ['Denunciante', 'Contacto', 'Domicilio para notificaciones']

datos = json.loads(DATOS.read_text(encoding='utf-8'))
folio_de = {x['datos']['folio']: x for x in datos}

with sync_playwright() as pw:
    nav = pw.chromium.launch(executable_path=CHROMIUM)
    pg = nav.new_context(viewport={'width':1280,'height':900}, accept_downloads=True).new_page()
    err = []
    pg.on('console', lambda x: err.append(x.text) if x.type == 'error' and not (x.location or {}).get('url', '').startswith(TIPOGRAFIAS) else None)
    pg.on('pageerror', lambda e: err.append('pageerror: ' + str(e)))
    pg.goto(MAQUETA.as_uri() + '#/bandeja'); pg.wait_for_timeout(500)
    def ve(perfil, hash_):
        pg.evaluate("([p, h]) => { document.getElementById('perfil').value = p; cambiaPerfil(p); location.hash = h; }", [perfil, hash_]); pg.wait_for_timeout(150)
    def baja(texto):
        with pg.expect_download() as d: pg.click('text=' + texto)
        return list(csv.reader(io.StringIO(pathlib.Path(d.value.path()).read_bytes().decode('utf-8-sig'))))

    # ---- 1. Nada por construir ----
    pend = pg.evaluate("""() => { const malos = [];
      PERFILES.forEach(p => { cambiaPerfil(p.id); p.pantallas.filter(s => s !== 'expediente').forEach(s => { location.hash = '#/' + s; muestra(false);
        if(/se construye en el bloque|llega con el bloque/.test(document.getElementById('pantalla').innerText)) malos.push(p.id + ':' + s); }); });
      return malos; }""")
    afirma(pend == [], 'ninguna pantalla de ningún perfil queda «por construir»: %s' % pend)

    # ---- 2. Descarga de la bandeja ----
    ve('consulta', '#/bandeja/por_turnar'); ve('consulta', '#/busqueda')
    filas = baja('Descargar sin datos personales (CSV)')
    esperado = [x['datos']['folio'] for x in datos if x['tramite']['estado'] == 'recibida']
    nombres = [x['datos'][k] for x in datos for k in ('nombre', 'correo', 'telefono', 'dom_calle') if x['datos'].get(k)]
    texto = '\n'.join(','.join(f) for f in filas)
    afirma(filas[0] == COLUMNAS and sorted(f[0] for f in filas[1:]) == sorted(esperado),
           'la descarga sale con las columnas de la bandeja y sólo con lo que la bandeja tiene: %d denuncias' % (len(filas) - 1))
    afirma(not any(n in texto for n in nombres) and 'Género' not in filas[0] and not any(o in texto for o in ('Mujer', 'Hombre', 'años')),
           'sin nombre, correo, teléfono ni domicilio de quien denuncia, y sin género ni edad')
    afirma('sólo de coordinación' in pg.inner_text('#pantalla') and not pg.locator('#f-motivo').count(), 'consulta no puede descargar datos personales')
    ve('atencion_dgiva', '#/busqueda')
    afirma(not pg.locator('#f-motivo').count() and not pg.locator('text=Descargar los indicadores (CSV)').count(),
           'atención tampoco, y no descarga indicadores porque no tiene tablero')

    ve('coordinacion_dgiva', '#/bandeja/todas'); ve('coordinacion_dgiva', '#/busqueda')
    antes = pg.evaluate("() => bitacora.length")
    pg.click('text=Descargar con datos personales (CSV)'); pg.wait_for_timeout(150)
    afirma('Escribe el motivo' in pg.inner_text('#aviso-descarga') and pg.evaluate("() => bitacora.length") == antes,
           'sin motivo no hay descarga con datos personales ni registro')
    pg.fill('#f-motivo', 'Revisión de prueba')
    filas = baja('Descargar con datos personales (CSV)')
    suyas = [x for x in datos if x['tramite']['area_actual'] in ('DGIVA', '')]
    quien = {x['datos']['folio']: {f[0]: f[1] for b in x['acuse']['bloques'] if b['id'] == 'quien' for f in b['filas']} for x in suyas}
    bien = all([f[12], f[13], f[14]] == [quien[f[0]].get(k, '') for k in PERSONALES] for f in filas[1:])
    afirma(filas[0] == COLUMNAS + PERSONALES and len(filas) - 1 == len(suyas) and bien,
           'coordinación descarga su área con nombre, contacto y domicilio, tal como los dice el acuse')
    b = pg.evaluate("() => bitacora[0]")
    afirma(b['perfil'] == 'Coordinación · DGIVA' and 'con datos personales' in b['que'] and 'Revisión de prueba' in b['que'] and str(len(suyas)) in b['que'],
           'la descarga con datos personales queda en la bitácora con su motivo: %s' % b['que'])

    # ---- 3. Fórmulas ----
    afirma(pg.evaluate("() => [valorCsv('=1+1'), valorCsv('@SUMA'), valorCsv('Normal')]") == ['"\'=1+1"', '"\'@SUMA"', '"Normal"'],
           'un valor que empieza como fórmula sale como texto')

    # ---- 4. Indicadores ----
    ve('consulta', '#/busqueda')
    filas = baja('Descargar los indicadores (CSV)')
    resumen = {f[2]: f[3] for f in filas if f[0] == 'Resumen'}
    cifras = pg.evaluate("() => Object.fromEntries(cifrasTablero(conjuntoTablero()).map(x => [x[0], String(x[1])]))")
    edad = {f[2]: f[3] for f in filas if f[1] == 'Rango de edad'}
    afirma(filas[0] == ['Grupo', 'Indicador', 'Concepto', 'Valor'] and resumen == cifras and resumen['Recibidas'] == '40',
           'los indicadores traen las cifras del tablero: %s' % resumen)
    afirma(edad.get('18 a 29 años') == 'menos de 3' and len({f[0] for f in filas[1:]}) == 6,
           'con los cinco grupos y la edad oculta bajo el mínimo: %s' % edad)

    # ---- 5. Abrir por folio ----
    def abre(q):
        pg.fill('#f-folio', q); pg.click('text=Abrir el expediente'); pg.wait_for_timeout(150)
        h = pg.evaluate("() => location.hash"); ve('consulta', '#/busqueda'); return h
    origen = next(x for x in datos if x['datos'].get('folio_origen'))
    r = [abre('000105'), abre('SEDEMA/DEN/2026/000101-9'), abre(origen['datos']['folio_origen'])]
    pg.fill('#f-folio', '999999'); pg.click('text=Abrir el expediente'); pg.wait_for_timeout(150)
    afirma(r[0].endswith('2026-000105-0') and r[1].endswith('2026-000101-9') and r[2] == '#/expediente/' + origen['datos']['folio'].replace('SEDEMA/DEN/', '').replace('/', '-')
           and 'ninguna denuncia con ese folio' in pg.inner_text('#aviso-folio'),
           'el consecutivo, el folio completo y el folio de origen abren el expediente; uno que no existe lo dice: %s' % r)

    # ---- 6. Administración ----
    ve('coordinacion_dgiva', '#/expediente/2026-000101-9')
    ve('administracion', '#/administracion')
    adm = pg.evaluate("""() => ({texto: document.getElementById('pantalla').innerText,
      perfiles: [...document.querySelectorAll('table')][0].querySelectorAll('tbody tr').length,
      acciones: [...[...document.querySelectorAll('table')][0].querySelectorAll('tbody tr')].map(tr => +tr.querySelector('.num').textContent),
      esperadas: PERFILES.map(p => ACCIONES.filter(a => a.roles.indexOf(p.rol) >= 0).length),
      params: [...[...document.querySelectorAll('table')][1].querySelectorAll('tbody tr')].map(tr => tr.innerText.split('\\t')[1])})""")
    afirma(adm['perfiles'] == 7 and adm['acciones'] == adm['esperadas'], 'administración lista los siete perfiles con sus acciones')
    cat = pg.evaluate("() => Object.fromEntries([...document.querySelectorAll('.ficha > div')].map(x => [x.querySelector('dt').textContent, x.querySelector('dd').textContent]))")
    afirma(cat['Materias'].startswith('19,') and cat['Estados del trámite'].startswith('16:') and cat['Canales'].startswith('5:')
           and cat['Marcas de revisión'].startswith('3:') and 'OBS-0024' in cat['Giros y supuestos de otra autoridad'],
           'y los catálogos con sus cuentas')
    afirma(adm['params'][:3] == ['3 días hábiles', '10 días hábiles', '5 días hábiles']
           and '93 días hábiles en la DGIVA; 90 días hábiles en la DGCORENADR' in adm['params']
           and '50 metros y 15 días' in adm['params'] and '500 metros' in adm['params'],
           'los plazos y umbrales son los que usa la maqueta: %s' % adm['params'][:5])
    afirma(all(s in adm['texto'] for s in ('MA-11', 'MA-12', 'SIA-26', 'Consulta el expediente SEDEMA/DEN/2026/000101-9', 'Descarga la bandeja con datos personales')),
           'dice qué falta configurar y la bitácora trae las consultas y descargas de la sesión')
    ve('administracion', '#/inicio')
    afirma('Pendientes de configuración' in pg.inner_text('#pantalla') and pg.locator('#pantalla tbody tr').count() == 5,
           'el inicio de administración trae lo pendiente y las últimas cinco entradas de la bitácora')
    afirma(err == [], 'sin errores en consola: %s' % err[:2])

    tel = nav.new_context(viewport={'width':360,'height':760}).new_page()
    tel.goto(MAQUETA.as_uri() + '#/bandeja'); tel.wait_for_timeout(400)
    anchos = []
    for perfil, h in (('coordinacion_dgiva', '#/busqueda'), ('administracion', '#/administracion'), ('administracion', '#/inicio')):
        tel.evaluate("([p, h]) => { cambiaPerfil(p); location.hash = h; }", [perfil, h]); tel.wait_for_timeout(150)
        anchos.append(tel.evaluate("() => document.documentElement.scrollWidth - innerWidth"))
    afirma(max(anchos) <= 0, 'a 360 px no hay desplazamiento horizontal: %s' % anchos)
    nav.close()

print('\n'.join(notas)); print()
if fallos:
    print('\n'.join(fallos)); sys.exit(1)
print('TODAS LAS PRUEBAS PASAN (%d)' % len(notas))
