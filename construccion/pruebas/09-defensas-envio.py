# -*- coding: utf-8 -*-
"""Las dos defensas del envío: prueba de humanidad y límite por origen (DEC-86).

   Un formulario público de denuncia es un blanco: basta un guion para abrir
   mil expedientes en una hora. La prueba de humanidad es lo único que detiene
   el envío automatizado, y por eso va pegada al botón de enviar y se exige
   incluso con la validación de campos apagada. El límite lo cuenta el
   servidor; aquí se comprueba lo que la persona ve cuando lo alcanza, que es
   la parte que el servidor no puede inventar."""
import os, pathlib, sys
AQUI = pathlib.Path(os.path.abspath(__file__)).parent
RAIZ = AQUI.parent
RUTA = pathlib.Path(os.environ.get('ARTEFACTO', RAIZ / 'artefacto.html'))
TMP  = AQUI / '_pagina09.html'
CHROMIUM = os.environ.get('CHROMIUM', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
from playwright.sync_api import sync_playwright

TMP.write_text('<!doctype html><html lang="es"><head><meta charset="utf-8">' +
               RUTA.read_text(encoding='utf-8') + '</body></html>', encoding='utf-8')
EXTERNO = ('ERR_TUNNEL_CONNECTION_FAILED','net::ERR_','Failed to load resource')
fallos, notas = [], []
def afirma(c, m): (notas if c else fallos).append(('OK  ' if c else 'FALLA ') + m)

with sync_playwright() as pw:
    nav = pw.chromium.launch(executable_path=CHROMIUM)
    pg = nav.new_context(viewport={'width':1100,'height':900}).new_page()
    err = []
    pg.on('console', lambda m: err.append(m.text) if m.type=='error' and not any(x in m.text for x in EXTERNO) else None)
    pg.on('pageerror', lambda e: err.append('pageerror: '+str(e)))
    pg.goto(TMP.as_uri()); pg.wait_for_timeout(700)

    # ---- 1. La prueba va donde se envía, no en un paso anterior ----
    r = pg.evaluate("""() => {
      cfg.validar = false; cfg.limite = false;
      guarda('verificacion',''); irA(6);
      const h = document.querySelector('.humano');
      const b = [...document.querySelectorAll('#app button')].find(x => x.textContent.indexOf('Enviar') >= 0);
      // Se mide antes de recorrer los pasos: irA() rehace la pantalla y los
      // elementos capturados dejan de estar en el documento.
      const antes = !!h && !!b && h.getBoundingClientRect().top < b.getBoundingClientRect().top;
      const pasos = [];
      for(let n = 1; n <= 5; n++){ irA(n); if(document.querySelector('.humano')) pasos.push(n); }
      irA(6);
      return {existe: !!h, antesDelBoton: antes,
              enOtrosPasos: pasos,
              asterisco: !!h && h.innerText.indexOf('*') >= 0,
              acertijo: !!h && h.innerText.toLowerCase().indexOf('acertijo') >= 0};
    }""")
    afirma(r['existe'], 'la prueba de humanidad está en la pantalla de envío')
    afirma(r['antesDelBoton'], 'y justo antes del botón de enviar')
    afirma(r['enOtrosPasos'] == [], 'no aparece en ningún paso anterior: %s' % r['enOtrosPasos'])
    afirma(not r['asterisco'], 'no se disfraza de campo obligatorio: no lleva asterisco')
    afirma(r['acertijo'], 'y dice que no hay acertijos, que es lo que la gente teme')

    # ---- 2. Sin la prueba no se envía, ni con la validación apagada ----
    r = pg.evaluate("""() => {
      cfg.validar = false; cfg.limite = false;
      guarda('verificacion',''); guarda('folio',''); irA(6);
      const salida = enviar();
      return {envio: salida, paso: paso, folio: val('folio'),
              marcado: !!document.querySelector('#c_verificacion.invalido'),
              mensaje: (document.querySelector('#c_verificacion .err')||{}).textContent || ''};
    }""")
    afirma(r['envio'] is False and r['paso'] == 6,
           'sin la prueba no se envía, aunque la validación de campos esté apagada')
    afirma(r['folio'] == '', 'y no se emite folio')
    afirma(r['marcado'], 'el control queda marcado como inválido')
    afirma('eres una persona' in r['mensaje'],
           'con un mensaje que dice qué falta: %r' % r['mensaje'].strip()[:48])

    # ---- 3. Con la prueba, el envío procede ----
    r = pg.evaluate("""() => {
      cfg.validar = false; cfg.limite = false;
      guarda('verificacion','si'); guarda('folio',''); irA(6);
      enviar();
      return {paso: paso, folio: val('folio')};
    }""")
    afirma(r['paso'] == 7 and r['folio'] != '', 'con la prueba marcada, el envío procede y hay folio')

    # ---- 4. El límite: lo que ve quien lo alcanza ----
    r = pg.evaluate("""() => {
      cfg.validar = false; cfg.limite = true;
      guarda('verificacion','si'); guarda('folio',''); irA(6);
      enviar();
      const t = document.getElementById('app').innerText;
      return {paso: paso, folio: val('folio'), texto: t.replace(/\\s+/g,' '),
              salidas: document.querySelectorAll('.derechos li').length,
              volver: [...document.querySelectorAll('#app button')].some(b => b.textContent.indexOf('Volver a mi denuncia') >= 0)};
    }""")
    afirma(r['paso'] == 8, 'al alcanzar el límite se muestra su propia pantalla')
    afirma(r['folio'] == '', 'y no se emite folio: la denuncia no se dio por presentada')
    afirma('no se perdió' in r['texto'], 'lo primero que dice es que la denuncia no se perdió')
    # Dos salidas, y sólo las dos que la Secretaría puede sostener: volver a
    # intentarlo por esta misma plataforma, o presentarla en la Oficialía de
    # Partes. El correo electrónico se retiró: ofrecerlo abría una tercera vía
    # de recepción que nadie había diseñado ni tiene quien la turne (DEC-99).
    afirma(r['salidas'] == 2, 'ofrece dos salidas, no un muro (%d)' % r['salidas'])
    afirma('en persona' in r['texto'] and 'Oficialía de Partes' in r['texto'],
           'la vía presencial, con su domicilio al pie')
    afirma('correo electrónico' not in r['texto'],
           'y no se ofrece el correo como canal de denuncia')
    afirma('compartes la conexión' not in r['texto'],
           'ni se explica el límite por la conexión compartida')
    afirma(r['volver'], 'se puede volver a la denuncia sin recapturarla')

    # ---- 5. El límite no se anuncia con cifras ----
    afirma(not any(x in r['texto'] for x in [' 5 denuncias', ' 20 denuncias', 'por hora', 'por día']),
           'la pantalla no publica el umbral: quien lo conoce lo bordea')

    afirma(err == [], 'sin errores propios en consola: %s' % err[:2])
    pg.close(); nav.close()

print('\n'.join(notas)); print()
if fallos:
    print('\n'.join(fallos)); sys.exit(1)
print('TODAS LAS PRUEBAS PASAN (%d)' % len(notas))
