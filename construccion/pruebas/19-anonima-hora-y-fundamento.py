# -*- coding: utf-8 -*-
"""Cuatro retiros y una apertura (DEC-119).

   1. La hora aproximada ya no se pregunta: ni campo ni renglón en la revisión.
   2. El paso 1 no enseña fundamento legal: el detalle de cada supuesto sí.
   3. La confidencialidad deja de ser pregunta: es la regla, y lo dice el
      aviso de privacidad.
   4. La denuncia anónima ofrece correo y teléfono, opcionales: sin ellos se
      envía; con un correo mal escrito, no; con correo, el acuse lo usa."""
import os, pathlib, sys
AQUI = pathlib.Path(os.path.abspath(__file__)).parent
RAIZ = AQUI.parent
RUTA = pathlib.Path(os.environ.get('ARTEFACTO', RAIZ / 'artefacto.html'))
TMP  = AQUI / '_pagina19.html'
CHROMIUM = os.environ.get('CHROMIUM', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
from playwright.sync_api import sync_playwright
TMP.write_text('<!doctype html><html lang="es"><head><meta charset="utf-8">' +
               RUTA.read_text(encoding='utf-8') + '</body></html>', encoding='utf-8')
EXTERNO = ('ERR_TUNNEL_CONNECTION_FAILED','net::ERR_','Failed to load resource')
fallos, notas = [], []
def afirma(c, m): (notas if c else fallos).append(('OK  ' if c else 'FALLA ') + m)

with sync_playwright() as pw:
    nav = pw.chromium.launch(executable_path=CHROMIUM)
    pg = nav.new_context(viewport={'width':390,'height':800}).new_page()
    err = []
    pg.on('console', lambda m: err.append(m.text) if m.type=='error' and not any(x in m.text for x in EXTERNO) else None)
    pg.on('pageerror', lambda e: err.append('pageerror: '+str(e)))
    pg.goto(TMP.as_uri()); pg.wait_for_timeout(700)

    # ---- 1. Sin hora ----
    h = pg.evaluate("""() => { estado={}; archivos=[]; guarda('materia','rsu'); irA(3);
      const t = document.getElementById('app').innerText;
      return {campo: !!document.getElementById('f_hora_h'), texto: /Hora aproximada|m\\u00e1s frecuente/.test(t),
              oblig: 'hora_h' in OBLIG, fecha: !!document.getElementById('f_fecha_hecho')}; }""")
    afirma(not h['campo'] and not h['texto'], 'el paso 3 ya no pregunta la hora')
    afirma(not h['oblig'], 'ni el catálogo de campos la declara')
    afirma(h['fecha'], 'la fecha se conserva')
    rv = pg.evaluate("""() => { irA(6); alternaDetalleRevision();
      const dt=[...document.querySelectorAll('.resumen dt')].find(x=>x.textContent.indexOf('Temporalidad')===0);
      return dt ? dt.nextElementSibling.textContent : ''; }""")
    afirma('horas' not in rv, 'y la revisión no la menciona (%r)' % rv)

    # ---- 2. Paso 1: título y subtítulo, sin detalle ni fundamento (DEC-119, DEC-122) ----
    f = pg.evaluate("""() => { estado={}; irA(1);
      const t = document.getElementById('app').innerText;
      const filas = [...document.querySelectorAll('#listaMaterias .fila-op:not(.otra)')].map(b => ({
        nom: (b.querySelector('.fo-nom')||{}).textContent || '', sub: (b.querySelector('.fo-desc')||{}).textContent || ''}));
      return {det: document.querySelectorAll('.fo-det, .fo-norma, .lin-detalle').length,
              art: /\\bArts?\\.\\s*\\d|Ley Ambiental de la Ciudad|NADF-|\\[Art\\./.test(t),
              boton: /Ver el detalle|Ocultar el detalle/.test(t), filas}; }""")
    afirma(f['det'] == 0 and not f['boton'], 'el paso 1 ya no tiene detalle desplegable')
    afirma(not f['art'], 'ni muestra artículos o leyes')
    afirma(len(f['filas']) == 19 and all(x['nom'] and x['sub'] for x in f['filas']),
           'los %d supuestos llevan título y subtítulo' % len(f['filas']))
    norm = lambda x: x.lower().strip()
    rep = [x['nom'] for x in f['filas'] if norm(x['nom']) in norm(x['sub']) or norm(x['sub']) in norm(x['nom'])]
    afirma(rep == [], 'ningún subtítulo repite su título: %s' % rep)
    largos = [x['sub'] for x in f['filas'] if len(x['sub']) > 60]
    afirma(largos == [], 'los subtítulos caben en una línea corta (≤ 60 caracteres): %s' % largos)
    busq = pg.evaluate("""() => { const n = q => { guarda('filtro', q); render(); return [...document.querySelectorAll('#listaMaterias .fila-op .fo-nom')].map(x=>x.textContent); };
      const r = {nadf: n('NADF').length, vib: n('vibraciones')}; guarda('filtro',''); render(); return r; }""")
    afirma(busq['nadf'] == 0, 'el buscador no encuentra por texto legal')
    afirma(any('Ruido' in x for x in busq['vib']), 'pero sí por lo que decía el detalle: «vibraciones» lleva a %s' % busq['vib'])

    # ---- 3. Sin pregunta de confidencialidad ----
    c = pg.evaluate("""() => { estado={}; guarda('identificacion','nombre'); irA(5);
      const t = document.getElementById('app').innerText, p = document.querySelector('.priv');
      return {pregunta: !!document.getElementById('c_reserva') || /mantengan confidenciales/.test(t),
              aviso: p ? /Confidencialidad\\./.test(p.innerText) && /no se hacen del conocimiento/.test(p.innerText) : false,
              condicional: p ? /Si solicitaste/.test(p.innerText) : true}; }""")
    afirma(not c['pregunta'], 'el paso 5 ya no pregunta por la confidencialidad')
    afirma(c['aviso'] and not c['condicional'], 'el aviso de privacidad la declara como regla, sin «si solicitaste»')
    rv = pg.evaluate("""() => { irA(6); alternaDetalleRevision();
      return [...document.querySelectorAll('.resumen dt')].some(x=>x.textContent.indexOf('Confidencialidad')===0); }""")
    afirma(not rv, 'ni aparece en la revisión')
    port = pg.evaluate("() => { irA(0); return document.getElementById('app').innerText; }")
    afirma('pedir que sean confidenciales' not in port and 'no se dan a conocer' in port, 'la portada lo dice como regla')

    # ---- 4. Anónima: correo obligatorio, teléfono opcional (DEC-119, DEC-120) ----
    a = pg.evaluate("""() => { estado={}; cfg.validar=true; guarda('identificacion','anonima'); guarda('privacidad','si'); irA(5);
      const lab = k => { const l=document.querySelector('label[for="f_'+k+'"]'); return l?l.innerText:''; };
      return {correo: !!document.getElementById('f_correo'), tel: !!document.getElementById('f_telefono'),
              nombre: !!document.getElementById('f_nombre'), dom: !!document.getElementById('f_dom_calle'),
              notif: !!document.getElementById('c_notif_correo'),
              astC: lab('correo').indexOf('*')>=0, astT: lab('telefono').indexOf('*')>=0,
              pasa: valida(5), marcado: !!document.querySelector('#c_correo.invalido')}; }""")
    afirma(a['correo'] and a['tel'], 'la anónima pide correo y ofrece teléfono')
    afirma(not a['nombre'] and not a['dom'] and not a['notif'], 'sin nombre, sin domicilio y sin pregunta de notificación')
    afirma(a['astC'] and not a['astT'], 'el correo lleva marca de obligatorio; el teléfono no')
    afirma(a['pasa'] is False and a['marcado'], 'sin correo, el paso no avanza y el correo se marca')
    m = pg.evaluate("""() => { guarda('correo','ana@correo'); render(); return valida(5); }""")
    afirma(m is False, 'un correo mal escrito tampoco')
    t = pg.evaluate("""() => { guarda('telefono','55123'); guarda('correo','ana@correo.mx'); render(); return valida(5); }""")
    afirma(t is False, 'un teléfono incompleto sí detiene el paso')
    ok = pg.evaluate("""() => { guarda('telefono',''); render(); return valida(5); }""")
    afirma(ok is True, 'con correo válido y sin teléfono, pasa')
    rv = pg.evaluate("""() => { irA(6); alternaDetalleRevision();
      const q = document.querySelector('#rb_quien .rb-res'); const dt=[...document.querySelectorAll('.resumen dt')].find(x=>x.textContent.indexOf('Contacto')===0);
      return {res: q?q.textContent:'', contacto: dt?dt.nextElementSibling.textContent:''}; }""")
    afirma('anónima' in rv['res'] and 'correo' in rv['res'], 'la revisión dice «anónima · con correo para avisos»: %r' % rv['res'])
    afirma('ana@correo.mx' in rv['contacto'], 'y muestra el correo')
    ac = pg.evaluate("""() => { guarda('folio','SEDEMA-PRUEBA'); irA(7); return document.getElementById('app').innerText; }""")
    afirma('ana@correo.mx' in ac and 'No recibirás notificaciones' not in ac, 'el acuse se envía al correo de la anónima')

    # ---- 4 bis. Formatos admitidos (DEC-120) ----
    f = pg.evaluate("""() => { archivos.length=0; irA(4);
      const inp=document.getElementById('inputArch');
      agregaArchivos([{name:'a.jpg',size:1},{name:'b.JPEG',size:1},{name:'c.png',size:1},{name:'d.mp4',size:1},{name:'e.mov',size:1},
                      {name:'f.doc',size:1},{name:'g.docx',size:1},{name:'h.pdf',size:1},{name:'i.xls',size:1},{name:'j.xlsx',size:1}]);
      const ok = archivos.length;
      archivos.length=0; agregaArchivos([{name:'k.heic',size:1},{name:'l.webp',size:1},{name:'m.gif',size:1}]);
      const t=document.getElementById('app').innerText;
      return {ok, rech: archivos.length, accept: inp?inp.getAttribute('accept'):'',
              texto: /JPG, JPEG o PNG/.test(t) && /MP4 o MOV/.test(t) && /Word, PDF o Excel/.test(t)}; }""")
    afirma(f['ok'] == 10, 'se admiten JPG, JPEG, PNG, MP4, MOV, Word, PDF y Excel (%d de 10)' % f['ok'])
    afirma(f['rech'] == 0, 'HEIC, WEBP y GIF se rechazan')
    afirma('.xlsx' in f['accept'] and '.heic' not in f['accept'], 'el selector de archivos ofrece los mismos formatos')
    afirma(f['texto'], 'y la pantalla los anuncia con esas palabras')
    pg.evaluate("() => { archivos.length=0; }")

    # ---- 5. Número exterior obligatorio con dirección (DEC-120) ----
    n = pg.evaluate("""() => { estado={}; cfg.validar=true; guarda('materia','rsu'); guarda('tiene_direccion','si'); irA(2);
      const l = document.querySelector('label[for="f_num_ext"]');
      guarda('calle','Calle 5'); guarda('alcaldia_dir','Iztacalco'); guarda('colonia','Pantitlán I'); guarda('cp','08100');
      guarda('lat','19.410000'); guarda('lon','-99.070000'); guarda('alcaldia','Iztacalco');
      valida(2);
      const sinNum = !!document.querySelector('#c_num_ext.invalido');
      guarda('num_ext','S/N'); render(); valida(2);
      const conSN = !document.querySelector('#c_num_ext.invalido');
      return {ast: l ? l.innerText.indexOf('*')>=0 : false, oblig: esObligatorio('num_ext'), sinNum, conSN}; }""")
    afirma(n['oblig'] and n['ast'], 'con dirección, el número exterior es obligatorio y lleva su marca')
    afirma(n['sinNum'], 'vacío, detiene el paso')
    afirma(n['conSN'], '«S/N» es respuesta válida')
    sd = pg.evaluate("() => { guarda('tiene_direccion','no'); return esObligatorio('num_ext'); }")
    afirma(sd is False, 'sin dirección no se exige')

    # ---- 6. Establecimiento: «Especifica» al lado del tipo, el nombre después (DEC-120) ----
    pg.set_viewport_size({'width':1100,'height':900})
    e = pg.evaluate("""() => { estado={}; guarda('materia','rsu'); guarda('es_estab','si'); guarda('tipo_estab','Otro'); irA(3);
      const r = id => { const x=document.getElementById(id); return x ? x.getBoundingClientRect() : null; };
      const t=r('f_tipo_estab'), o=r('f_tipo_estab_otro'), n=r('f_nombre_estab');
      return t&&o&&n ? {mismaFila: Math.abs(t.top-o.top)<2, alLado: o.left>t.right, debajo: n.top>Math.max(t.bottom,o.bottom)} : null; }""")
    afirma(e and e['mismaFila'] and e['alLado'], 'en escritorio, «Especifica el tipo» va al lado del tipo de establecimiento')
    afirma(e and e['debajo'], 'y el nombre del establecimiento va después de los dos')
    pg.set_viewport_size({'width':390,'height':800})
    e2 = pg.evaluate("""() => { const r=id=>document.getElementById(id).getBoundingClientRect();
      return r('f_tipo_estab').bottom < r('f_tipo_estab_otro').top && r('f_tipo_estab_otro').bottom < r('f_nombre_estab').top; }""")
    afirma(e2, 'en teléfono quedan en ese orden: tipo, especifica, nombre')
    e3 = pg.evaluate("""() => { const s=document.getElementById('f_tipo_estab'); s.value=TIPOS_ESTAB[0].v||TIPOS_ESTAB[0]; s.dispatchEvent(new Event('change'));
      return !document.getElementById('f_tipo_estab_otro') && !!document.getElementById('f_nombre_estab'); }""")
    afirma(e3, 'con otro tipo, «Especifica» se retira y el nombre se queda')

    afirma(err == [], 'sin errores propios en consola: %s' % err[:2])
    pg.close(); nav.close()

print('\n'.join(notas)); print()
if fallos:
    print('\n'.join(fallos)); sys.exit(1)
print('TODAS LAS PRUEBAS PASAN (%d)' % len(notas))
