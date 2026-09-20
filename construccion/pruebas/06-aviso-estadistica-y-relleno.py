# -*- coding: utf-8 -*-
"""El cierre del formulario: estadistica, aviso de privacidad y relleno.

   Tres cosas distintas que viven en el mismo tramo final. Las preguntas de
   genero y edad tienen que poder dejarse en blanco, en las dos rutas. El
   aviso de privacidad tiene que leerse en pantalla antes de enviar, no detras
   de un enlace. Y el relato tiene que parecer un texto: el formulario de la
   PAOT admite una denuncia con los campos llenos de letras al azar."""
import os, pathlib, sys
AQUI = pathlib.Path(os.path.abspath(__file__)).parent
RAIZ = AQUI.parent
RUTA = pathlib.Path(os.environ.get('ARTEFACTO', RAIZ / 'artefacto.html'))
TMP  = AQUI / '_pagina06.html'
CHROMIUM = os.environ.get('CHROMIUM', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
from playwright.sync_api import sync_playwright

TMP.write_text('<!doctype html><html lang="es"><head><meta charset="utf-8">' +
               RUTA.read_text(encoding='utf-8') + '</body></html>', encoding='utf-8')
EXTERNO = ('ERR_TUNNEL_CONNECTION_FAILED','net::ERR_','Failed to load resource')
fallos, notas = [], []
def afirma(c, m): (notas if c else fallos).append(('OK  ' if c else 'FALLA ') + m)

RELLENO = 'sdfgh sdfgh qwrtp zxcvb sdfgh qwrtp zxcvb sdfgh qwrtp zxcvb mnbvc'
RELATO  = ('Todos los dias desde hace dos semanas, a partir de las seis de la manana, el taller '
           'de la esquina saca humo negro por un tubo y huele a solvente quemado. No se puede '
           'abrir la ventana y hay ninos en la casa de al lado.')

with sync_playwright() as pw:
    nav = pw.chromium.launch(executable_path=CHROMIUM)
    pg = nav.new_context(viewport={'width':1100,'height':900}).new_page()
    err = []
    pg.on('console', lambda m: err.append(m.text) if m.type=='error' and not any(x in m.text for x in EXTERNO) else None)
    pg.on('pageerror', lambda e: err.append('pageerror: '+str(e)))
    pg.goto(TMP.as_uri()); pg.wait_for_timeout(700)

    # ---- 1. Las dos preguntas estadisticas, en las dos rutas ----
    for ruta, nom in [('anonima','anónima'), ('nombre','con datos')]:
        r = pg.evaluate("""(ruta) => {
          cfg.validar = true;
          guarda('identificacion', ruta); irA(5);
          const g = document.getElementById('f_sexo_genero'), e = document.getElementById('f_edad_rango');
          const et = k => { const l = document.querySelector('label[for="f_'+k+'"]');
                            return l ? l.innerText.trim() : ''; };
          return {hay: !!g && !!e,
                  opcionesG: g ? g.options.length : 0,
                  opcionesE: e ? e.options.length : 0,
                  asterisco: (et('sexo_genero')+et('edad_rango')).indexOf('*') >= 0,
                  noResponde: g ? [...g.options].some(o => o.text.indexOf('no decirlo') >= 0) : false};
        }""", ruta)
        afirma(r['hay'], 'ruta %s: se preguntan género y edad' % nom)
        afirma(not r['asterisco'], 'ruta %s: ninguna de las dos lleva asterisco' % nom)
        afirma(r['noResponde'], 'ruta %s: el género admite no responder' % nom)
        afirma(r['opcionesG'] >= 6 and r['opcionesE'] >= 7,
               'ruta %s: las dos listas tienen todas sus opciones (%d y %d)' % (nom, r['opcionesG'], r['opcionesE']))

    # Sin responderlas, el paso 5 se completa.
    pasa = pg.evaluate("""() => {
      cfg.validar = true; guarda('identificacion','anonima');
      guarda('sexo_genero',''); guarda('edad_rango',''); guarda('privacidad','si');
      irA(5); return valida(5);
    }""")
    afirma(pasa is True, 'sin responder género ni edad, el paso 5 se completa')

    # ---- 2. El aviso de privacidad se lee en pantalla ----
    av = pg.evaluate("""() => {
      irA(5);
      const p = document.querySelector('.priv');
      if(!p) return null;
      const chk = document.getElementById('chkPriv');
      const t = p.innerText;
      return {visible: p.getBoundingClientRect().height > 60,
              antesDelCheck: !!chk && p.getBoundingClientRect().top < chk.getBoundingClientRect().top,
              rotulos: ['Qui\\u00e9n trata tus datos','Para qu\\u00e9 se usan','Con qu\\u00e9 fundamento',
                        'Cu\\u00e1nto tiempo','A qui\\u00e9n pueden transferirse','C\\u00f3mo ejerces tus derechos']
                       .filter(x => t.indexOf(x) >= 0).length,
              huecos: p.querySelectorAll('.pendiente').length,
              alertas: [...document.querySelectorAll('#app [onclick]')]
                        .filter(b => (b.getAttribute('onclick')||'').indexOf('Aviso de privacidad integral') >= 0).length};
    }""")
    afirma(av is not None and av['visible'], 'el aviso de privacidad ocupa lugar en la pantalla')
    afirma(av and av['antesDelCheck'], 'y va antes de la casilla con la que se consiente')
    afirma(av and av['rotulos'] == 6, 'trae los seis rótulos del aviso simplificado (%s)' % (av and av['rotulos']))
    afirma(av and av['huecos'] >= 5, 'los datos que faltan quedan a la vista como huecos (%s)' % (av and av['huecos']))
    afirma(av and av['alertas'] == 0, 'ya no se esconde detrás de una ventana del navegador')

    # ---- 3. El relato tiene que parecer un texto ----
    h = pg.evaluate("""([relleno, relato]) => ({
        relleno: pareceTexto(relleno),
        relato: pareceTexto(relato),
        corto: pareceTexto('humo'),
        tecla: pareceTexto('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'),
        conFaltas: pareceTexto('tiran escombro en la baranca de tarango otravez y nadie ase nada')
    })""", [RELLENO, RELATO])
    afirma(h['relleno'] is False, 'un relato de letras al azar no pasa por texto')
    afirma(h['tecla'] is False, 'una tecla repetida tampoco')
    afirma(h['corto'] is False, 'una sola palabra tampoco')
    afirma(h['relato'] is True, 'un relato real sí pasa')
    afirma(h['conFaltas'] is True, 'y también uno con faltas de ortografía: no se castiga a quien escribe mal')

    v = pg.evaluate("""(relleno) => {
      cfg.validar = true;
      guarda('materia','rsu'); guarda('tiene_direccion','si');
      guarda('hechos', relleno); irA(3);
      const ok = valida(3);
      const e = document.getElementById('e_hechos');
      const res = document.getElementById('resumenErrores');
      return {ok: ok, mensaje: e ? e.textContent : '', resumen: res ? res.innerText : ''};
    }""", RELLENO)
    afirma(v['ok'] is False, 'con el relato de relleno, el paso 3 no avanza')
    afirma('no se entiende' in v['mensaje'],
           'y el mensaje dice cuál es el problema, no «este dato es necesario»: %r' % v['mensaje'][:60])
    afirma('Revisa' in v['resumen'] or 'Faltan' in v['resumen'], 'el resumen de errores lo recoge')

    # ---- 4. El acuse: ratificacion y correo ----
    ac = pg.evaluate("""() => {
      guarda('folio','SEDEMA-2026-000001'); guarda('identificacion','nombre');
      guarda('correo','persona@ejemplo.mx'); guarda('fecha_acuse','20 de septiembre de 2026');
      irA(7);
      const t = document.getElementById('app').innerText;
      return {ratifica: t.indexOf('ratificar') >= 0,
              tresDias: t.indexOf('tres d\\u00edas h\\u00e1biles') >= 0,
              spam: t.indexOf('correo no deseado') >= 0};
    }""")
    afirma(ac['ratifica'] and ac['tresDias'],
           'el acuse explica la ratificación de la Procuraduría y que aquí no hace falta')
    afirma(ac['spam'], 'y avisa que el acuse puede caer en correo no deseado')

    afirma(err == [], 'sin errores propios en consola: %s' % err[:2])
    pg.close(); nav.close()

print('\n'.join(notas)); print()
if fallos:
    print('\n'.join(fallos)); sys.exit(1)
print('TODAS LAS PRUEBAS PASAN (%d)' % len(notas))
