# -*- coding: utf-8 -*-
"""Observaciones de la revisión de la DGIVA atendidas (DEC-188 a DEC-191).
   Cada cambio que pidió la Dirección General se comprueba en pantalla, no en
   el estado: que se lea lo que se acordó y que no reaparezca lo que se quitó."""
import os, pathlib, sys
AQUI = pathlib.Path(os.path.abspath(__file__)).parent
RAIZ = AQUI.parent
RUTA = pathlib.Path(os.environ.get('ARTEFACTO', RAIZ / 'artefacto.html'))
TMP  = AQUI / '_pagina29.html'
CHROMIUM = os.environ.get('CHROMIUM', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
from playwright.sync_api import sync_playwright
TMP.write_text('<!doctype html><html lang="es"><head><meta charset="utf-8">' +
               RUTA.read_text(encoding='utf-8') + '</body></html>', encoding='utf-8')
EXTERNO = ('ERR_TUNNEL_CONNECTION_FAILED','net::ERR_','Failed to load resource')
fallos, notas = [], []
def afirma(c, m): (notas if c else fallos).append(('OK  ' if c else 'FALLA ') + m)
with sync_playwright() as pw:
    nav = pw.chromium.launch(executable_path=CHROMIUM)
    pg = nav.new_context(viewport={'width':1200,'height':900}).new_page()
    err = []
    pg.on('pageerror', lambda e: err.append('pageerror: '+str(e)))
    pg.goto(TMP.as_uri()); pg.wait_for_timeout(700)

    # ---- Portada (DEC-188, DEC-189) ----
    p = pg.evaluate("() => document.getElementById('app').innerText")
    afirma('Presencial' in p and 'En persona' not in p, 'la tarjeta dice «Presencial» (OBS-0001)')
    afirma('Disponible las 24 horas, todos los días' in p and 'diez minutos' not in p, 'sin promesa de tiempo (OBS-0006, OBS-0017)')
    afirma('unidad administrativa competente' in p and 'qué oficina' not in p, '«unidad administrativa competente», no «oficina» (OBS-0007, OBS-0018)')
    afirma('San Juan de Aragón' in p and '9689 5009' in p, 'domicilio y teléfono de la DGIVA (OBS-0008)')
    afirma(' tala ' not in p, 'la entrada ya no dice «tala» (OBS-0002)')
    fq = pg.evaluate("() => [...document.querySelectorAll('#app .faq details')].map(d => d.textContent).join(' ')")
    afirma('Tus datos son confidenciales' in fq and 'Ley de Protección de Datos Personales en Posesión de Sujetos Obligados de la Ciudad de México' in fq
           and 'Ley General' not in fq, 'la confidencialidad se conserva y cita la ley local, no la General (OBS-0012)')

    # ---- Paso 1: tarjetas y derivaciones (DEC-188 a DEC-190) ----
    m = pg.evaluate("""() => { estado = {}; irA(1);
      const t = document.getElementById('app').innerText;
      const ids = DERIVA.map(d => d.id);
      const ruido = MATERIAS.filter(x => x.id === 'ruido')[0];
      return {t, ids, ruido: ruido.nom + ' · ' + ruido.c,
              inv: (DERIVA.filter(d => d.id === 'd_ruido_comercio')[0] || {inst: []}).inst.map(i => i.n).join()}; }""")
    for palabra in ['olores', 'globos', 'escombro', 'cascajo', 'ruido excesivo', 'luz excesiva']:
        afirma(palabra not in m['t'].lower(), 'el paso 1 ya no dice «%s»' % palabra)
    afirma(m['ruido'] == 'Ruido o vibraciones · De una industria o fábrica', 'la tarjeta de ruido es la de la industria (OBS-0004): %s' % m['ruido'])
    afirma('INVEA' in m['inv'], 'el ruido de comercios se deriva al INVEA (DEC-190)')
    afirma(all(x in m['ids'] for x in ['d_olores', 'd_visual', 'd_ruido_comercio']), 'olores, anuncios y ruido de comercios están en «Mi caso no está en la lista»')

    # ---- Paso 2 y 3 ----
    t2 = pg.evaluate("() => { cargaEscenario('urbano'); irA(2); return document.getElementById('app').innerText; }")
    afirma('Calle o avenida' in t2 and 'vialidad' not in t2.lower(), '«Calle o avenida» (OBS-0014)')
    t3 = pg.evaluate("() => { irA(3); return document.getElementById('app').innerText; }")
    afirma('permisos' not in t3.lower(), 'el paso 3 ya no pregunta por permisos (OBS-0027)')
    afirma('Razón social' not in t3, 'ni por la razón social (OBS-0026)')
    afirma('derribo, poda, tiro de residuos' in pg.evaluate("() => document.getElementById('f_hechos').placeholder"), 'los ejemplos de hechos son los de la DGIVA (OBS-0015)')
    op = pg.evaluate("""() => ['fecha_hecho','reporto_antes','temporalidad'].map(k => {
      const c = document.getElementById('c_'+k); return c ? c.innerText.includes('(opcional)') : null; })""")
    afirma(op == [True, True, True], 'la fecha, las gestiones previas y la temporalidad dicen «(opcional)» (OBS-0016, OBS-0030): %s' % op)
    apag = pg.evaluate("() => { cfg.validar = false; render(); const r = document.getElementById('app').innerText.includes('(opcional)'); cfg.validar = true; render(); return r; }")
    afirma(not apag, 'con la obligatoriedad apagada no se marca nada como opcional')

    # ---- Fecha aproximada (OBS-0016) ----
    f = pg.evaluate("""() => { irA(3); const antes = val('fecha_hecho');
      cambiaFechaNoSabe(true);
      const sel = !!document.getElementById('f_fecha_mes') && !!document.getElementById('f_fecha_anio'), cal = !!document.getElementById('f_fecha_hecho');
      guarda('fecha_mes','Agosto'); guarda('fecha_anio','2026');
      const pasa = valida(3); irA(6); const rev = document.getElementById('app').textContent;
      irA(3); cambiaFechaNoSabe(false);
      return {antes, sel, cal, pasa, rev: rev.includes('Aproximada: agosto de 2026'), suelta: !val('fecha_mes') && !val('fecha_anio'),
              anios: document.getElementById('f_fecha_hecho') ? aniosAtras().length : 0}; }""")
    afirma(f['antes'] != '', 'el escenario trae una fecha exacta')
    afirma(f['sel'] and not f['cal'], '«No sé la fecha exacta» cambia el calendario por mes y año')
    afirma(f['pasa'], 'y sin fecha exacta se puede continuar')
    afirma(f['rev'], 'la revisión dice «Aproximada: agosto de 2026»')
    afirma(f['suelta'] and f['anios'] == 10, 'al volver a la fecha exacta se suelta lo aproximado; el año ofrece diez opciones')

    # ---- Paso 5 y acuse (OBS-0031, OBS-0023) ----
    t5 = pg.evaluate("() => { guarda('identificacion','anonima'); irA(5); return document.getElementById('app').innerText; }")
    afirma('ponerse en contacto contigo' in t5 and 'pueda escribirte' not in t5, 'la anónima dice «ponerse en contacto contigo» (OBS-0031)')
    pg.evaluate("() => { cargaEscenario('urbano'); guarda('verificacion','si'); irA(6); enviar(); }")
    pg.wait_for_timeout(400)
    ac = pg.evaluate("() => document.getElementById('app').innerText")
    afirma('Número de registro' in ac or 'NÚMERO DE REGISTRO' in ac, 'el acuse rotula «Número de registro» (OBS-0023)')
    afirma('folio' not in ac.lower(), 'y la palabra «folio» ya no aparece en el acuse')
    afirma(not err, 'sin errores de página: %s' % err[:2])
    nav.close()
TMP.unlink()
for n in notas + fallos: print(n)
sys.exit(1 if fallos else 0)
