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

    # ---- 2. Paso 1 sin fundamento ----
    f = pg.evaluate("""() => { estado={}; irA(1); guarda('fundamento','si'); render();
      const t = document.getElementById('app').innerText;
      return {norma: document.querySelectorAll('.fo-norma').length, det: document.querySelectorAll('.fo-det').length,
              art: /\\bArts?\\.\\s*\\d|Ley Ambiental de la Ciudad|NADF-|\\[Art\\./.test(t),
              boton: [...document.querySelectorAll('.lin-detalle button')].map(b=>b.textContent).join('')}; }""")
    afirma(f['norma'] == 0 and not f['art'], 'con el detalle abierto, el paso 1 no muestra artículos ni leyes')
    afirma(f['det'] > 10, 'pero sí el detalle de cada supuesto (%d)' % f['det'])
    afirma('fundamento' not in f['boton'].lower(), 'y el botón ya no promete fundamento: %r' % f['boton'])
    busq = pg.evaluate("""() => { guarda('fundamento',''); guarda('filtro','NADF'); render();
      return document.querySelectorAll('#listaMaterias .fila-op').length; }""")
    afirma(busq == 0, 'el buscador ya no encuentra por texto legal que no se ve')
    pg.evaluate("() => { guarda('filtro',''); }")

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

    # ---- 4. Anónima con contacto opcional ----
    a = pg.evaluate("""() => { estado={}; cfg.validar=true; guarda('identificacion','anonima'); guarda('privacidad','si'); irA(5);
      const lab = k => { const l=document.querySelector('label[for="f_'+k+'"]'); return l?l.innerText:''; };
      return {correo: !!document.getElementById('f_correo'), tel: !!document.getElementById('f_telefono'),
              nombre: !!document.getElementById('f_nombre'), dom: !!document.getElementById('f_dom_calle'),
              notif: !!document.getElementById('c_notif_correo'),
              ast: (lab('correo')+lab('telefono')).indexOf('*')>=0, pasa: valida(5)}; }""")
    afirma(a['correo'] and a['tel'], 'la anónima ofrece correo y teléfono')
    afirma(not a['nombre'] and not a['dom'] and not a['notif'], 'sin nombre, sin domicilio y sin pregunta de notificación')
    afirma(not a['ast'] and a['pasa'] is True, 'los dos son opcionales: sin ellos, el paso se completa')
    m = pg.evaluate("""() => { guarda('correo','ana@correo'); render(); const ok = valida(5);
      return {ok, marcado: !!document.querySelector('#c_correo.invalido')}; }""")
    afirma(m['ok'] is False and m['marcado'], 'un correo mal escrito sí detiene el paso')
    t = pg.evaluate("""() => { guarda('telefono','55123'); guarda('correo','ana@correo.mx'); render(); return valida(5); }""")
    afirma(t is False, 'y un teléfono incompleto también')
    ok = pg.evaluate("""() => { guarda('telefono','5512345678'); render(); return {pasa: valida(5),
      aviso: document.getElementById('app').innerText.indexOf('sin un correo')>=0}; }""")
    afirma(ok['pasa'] is True and not ok['aviso'], 'con correo válido pasa, y ya no advierte que no habrá avisos')
    rv = pg.evaluate("""() => { irA(6); alternaDetalleRevision();
      const q = document.querySelector('#rb_quien .rb-res'); const dt=[...document.querySelectorAll('.resumen dt')].find(x=>x.textContent.indexOf('Contacto')===0);
      return {res: q?q.textContent:'', contacto: dt?dt.nextElementSibling.textContent:''}; }""")
    afirma('anónima' in rv['res'] and 'correo' in rv['res'], 'la revisión dice «anónima · con correo para avisos»: %r' % rv['res'])
    afirma('ana@correo.mx' in rv['contacto'], 'y muestra el contacto que dejó')
    ac = pg.evaluate("""() => { guarda('folio','SEDEMA-PRUEBA'); irA(7); return document.getElementById('app').innerText; }""")
    afirma('ana@correo.mx' in ac and 'No recibirás notificaciones' not in ac, 'el acuse usa el correo de la anónima')
    sin = pg.evaluate("""() => { guarda('correo',''); guarda('telefono',''); irA(7); return document.getElementById('app').innerText; }""")
    afirma('No recibirás notificaciones' in sin, 'y sin correo, el acuse dice que no habrá notificaciones')

    afirma(err == [], 'sin errores propios en consola: %s' % err[:2])
    pg.close(); nav.close()

print('\n'.join(notas)); print()
if fallos:
    print('\n'.join(fallos)); sys.exit(1)
print('TODAS LAS PRUEBAS PASAN (%d)' % len(notas))
