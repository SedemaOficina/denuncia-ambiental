# -*- coding: utf-8 -*-
"""La pantalla de inicio (DEC-53, DEC-116).

   La portada es la eleccion del medio: en linea o en persona. Tenia 349
   palabras y casi cuatro pantallas de telefono, repetia el titulo del
   encabezado y dejaba los medios para presentar la denuncia en el pie.
   Estas comprobaciones fijan lo que no debe volver: el texto que crece, el
   boton que se aleja, la via presencial escondida, el domicilio escrito dos
   veces y el correo electronico ofrecido como via, que no lo es."""
import os, pathlib
AQUI = pathlib.Path(os.path.abspath(__file__)).parent
RAIZ = AQUI.parent
RUTA = pathlib.Path(os.environ.get('ARTEFACTO', RAIZ / 'artefacto.html'))
TMP  = AQUI / '_pagina.html'
CHROMIUM = os.environ.get('CHROMIUM', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
from playwright.sync_api import sync_playwright
import sys

TMP.write_text('<!doctype html><html lang="es"><head><meta charset="utf-8">' +
               RUTA.read_text(encoding='utf-8') + '</body></html>', encoding='utf-8')
EXTERNO = ('ERR_TUNNEL_CONNECTION_FAILED','net::ERR_','Failed to load resource')
fallos, notas = [], []
def afirma(c, m): (notas if c else fallos).append(('OK  ' if c else 'FALLA ') + m)

with sync_playwright() as pw:
    nav = pw.chromium.launch(executable_path=CHROMIUM)
    for ancho, alto, nom in [(390, 760, 'teléfono'), (1100, 800, 'escritorio')]:
        pg = nav.new_context(viewport={'width':ancho,'height':alto}).new_page()
        err = []
        pg.on('console', lambda m: err.append(m.text) if m.type=='error' and not any(x in m.text for x in EXTERNO) else None)
        pg.on('pageerror', lambda e: err.append('pageerror: '+str(e)))
        pg.goto(TMP.as_uri()); pg.wait_for_timeout(700)

        r = pg.evaluate("""() => {
          const a = document.getElementById('app');
          const t = a.innerText.replace(/\\s+/g,' ').trim();
          const b = [...a.querySelectorAll('.medio-principal button')].find(x => x.textContent.includes('Iniciar'));
          const medios = [...a.querySelectorAll('.medio')];
          const pie = document.getElementById('pieSede0'), pie1 = document.getElementById('pieSede1');
          return {
            palabras: t.split(' ').length,
            botonY: b ? Math.round(b.getBoundingClientRect().top + window.scrollY) : null,
            tarjetaY: b ? Math.round(b.closest('.medio-principal').getBoundingClientRect().top + window.scrollY) : null,
            botonEnLinea: !!(b && b.closest('.medio-principal')),
            medios: medios.length,
            persona: medios.length > 1 ? medios[1].innerText : '',
            enLineaPrimero: medios.length > 1 && medios[0].classList.contains('medio-principal'),
            ladoALado: medios.length > 1 && Math.abs(medios[0].getBoundingClientRect().top - medios[1].getBoundingClientRect().top) < 2,
            pend: medios.length > 1 ? !!medios[1].querySelector('.pendiente') : false,
            pieTxt: pie ? pie.innerText.replace(/\\s+/g,' ').trim() : '',
            dgs: SEDES.map(d => d.area),
            pendPersona: medios.length > 1 ? [...medios[1].querySelectorAll('.pendiente')].map(e => e.innerText.trim()) : [],
            ordenDG: medios.length > 1 ? [...medios[1].querySelectorAll('.sede')].every(s => { const g = s.querySelector('.sede-dg'), z = s.querySelector('.sede-zona'); return g && z && (g.compareDocumentPosition(z) & 4); }) : false,
            tituloPropio: !!a.querySelector('.portada-titulo'),
            faq: a.querySelectorAll('.faq details').length, faqAbiertas: a.querySelectorAll('.faq details[open]').length,
            temas: a.querySelectorAll('.temas .tema').length, grupos: GRUPOS_MATERIA.length,
            mismoAlto: medios.length > 1 && Math.abs(medios[0].getBoundingClientRect().height - medios[1].getBoundingClientRect().height) < 2,
            zonas: SEDES.map(d => d.zona),
            pie1Txt: pie1 ? pie1.innerText.replace(/\\s+/g,' ').trim() : '',
            mailto: document.querySelectorAll('a[href^="mailto:"]').length,
            cajas: a.querySelectorAll('.aviso').length,
            derechos: [...a.querySelectorAll('.derechos li')].map(li => li.innerText.trim()),
            derechosB: [...a.querySelectorAll('.derechos li b')].map(b => b.innerText.trim()),
            pasos: [...a.querySelectorAll('.despues b')].map(e => ({alto: e.getBoundingClientRect().height,
                     lh: parseFloat(getComputedStyle(e).lineHeight), top: Math.round(e.closest('li').getBoundingClientRect().top)})),
            tarjeta: t,
            desborde: document.documentElement.scrollWidth > window.innerWidth
          };
        }""")

        # Tope de texto. Era 350 y la portada lo llenaba; con DEC-116 baja a
        # 160. No es un numero arbitrario: es la portada actual (138) con
        # margen para ajustes de redaccion, no para una seccion nueva.
        # DEC-142 la deja en entrada, medios, qué necesitas y lo que la ley
        # reconoce: fuera el 911, los temas y qué pasa después.
        # DEC-147 vuelve a explicar el derecho y por qué importa denunciar, con
        # el texto que dio la Oficina de la Secretaría: el tope sube a 420.
        afirma(r['palabras'] <= 420, '%s: la portada cabe en %d palabras (tope 420)' % (nom, r['palabras']))
        afirma(r['faq'] >= 6 and r['faqAbiertas'] == 0, '%s: preguntas frecuentes, plegadas (%d)' % (nom, r['faq']))
        tam = pg.evaluate("() => getComputedStyle(document.querySelector('#app .faq summary')).fontSize")
        afirma(tam == '16px', '%s: las preguntas frecuentes van en 16 px, no en tamaño de título (DEC-182): %s' % (nom, tam))
        afirma(not r['tituloPropio'], '%s: la portada no repite un título junto al del encabezado' % nom)
        afirma(r['temas'] == 0 and '911' not in r['tarjeta'] and len(r['pasos']) == 0,
               '%s: sin temas, sin línea de emergencias y sin «qué pasa después» (DEC-142)' % nom)
        afirma('mismo dispositivo y navegador' in r['tarjeta'], '%s: pausar se aclara: desde el mismo dispositivo y navegador' % nom)
        afirma('BOSQUES URBANOS Y BARRANCAS' in r['persona'].upper(), '%s: la zona urbana nombra bosques urbanos y barrancas' % nom)
        afirma('Qué necesitas' in r['tarjeta'] or 'QUÉ NECESITAS' in r['tarjeta'], '%s: dice qué se necesita para denunciar' % nom)
        # Orden de la portada (DEC-183): los medios vuelven a ir justo después de la entrada.
        orden = pg.evaluate("""() => [...document.querySelectorAll('#app .rotulo-portada')].map(h => h.innerText.trim())""")
        afirma(orden == ['Denunciar el daño ambiental es tu derecho', 'Elige cómo presentarla', 'La visión de la Secretaría',
                         '¿Qué necesitas?', 'Preguntas frecuentes'],
               '%s: la portada va en el orden instruido (DEC-183, DEC-184): %s' % (nom, orden))
        un = pg.evaluate("() => [...document.querySelectorAll('#app button')].filter(b => b.textContent.includes('Iniciar')).length")
        afirma(un == 1 and r['botonEnLinea'], '%s: un solo botón «Iniciar mi denuncia», el de la tarjeta «En línea» (%d)' % (nom, un))
        if ancho >= 760:
            afirma(r['botonY'] is not None and r['botonY'] < alto,
                   '%s: el botón de iniciar se ve sin desplazar (a %s px de %d)' % (nom, r['botonY'], alto))
        else:
            afirma(r['tarjetaY'] is not None and r['tarjetaY'] + 60 < alto,
                   '%s: la tarjeta en línea asoma en la primera pantalla (a %s px de %d)' % (nom, r['tarjetaY'], alto))
        # Holgura en teléfono: la franja del borrador no toca la orilla y el panel no tapa el botón.
        hol = pg.evaluate("""() => { localStorage.setItem(CLAVE_BORRADOR, JSON.stringify({estado:{materia:'ava'}, paso:3, t:Date.now()})); irA(0);
          const p = document.querySelector('#franjaBorrador p'), b = document.querySelector('#franjaBorrador .btn'), e = document.querySelector('#franjaBorrador .enlace');
          const r = [p, b, e].map(x => x.getBoundingClientRect());
          const t = document.querySelector('#panel .toggle').getBoundingClientRect();
          const o = {izq: Math.min(...r.map(x => x.left)), der: innerWidth - Math.max(...r.map(x => x.right)), panelW: Math.round(t.width)};
          localStorage.removeItem(CLAVE_BORRADOR); irA(0); return o; }""")
        afirma(hol['izq'] >= 16 and hol['der'] >= 16, '%s: la franja del borrador deja margen a los lados (%s y %s px)' % (nom, round(hol['izq']), round(hol['der'])))
        if ancho < 560:
            afirma(hol['panelW'] <= 48, '%s: el panel de validación queda en un círculo con el engrane (%s px)' % (nom, hol['panelW']))

        # Los dos medios son el cuerpo de la pagina.
        afirma(r['medios'] == 2, '%s: la portada ofrece los dos medios para presentar la denuncia' % nom)
        afirma(r['botonEnLinea'], '%s: el botón de iniciar vive dentro del medio en línea' % nom)
        afirma(r['enLineaPrimero'], '%s: el medio en línea va primero' % nom)
        afirma('En persona' in r['persona'] and all(g in r['persona'] for g in r['dgs']) and r['ordenDG'],
               '%s: en persona va el nombre de cada dirección general, arriba de su zona (DEC-157)' % nom)
        afirma(r['pendPersona'].count('Domicilio y horario por confirmar') == 2 and r['pendPersona'].count('Teléfono por confirmar') == 2
               and 'Aragón' not in r['persona'] and '13:30' not in r['persona'],
               '%s: sin domicilios ni horarios: cada dirección general lleva «Domicilio y horario» y «Teléfono por confirmar» %s' % (nom, r['pendPersona']))
        esperado_lado = ancho >= 760
        afirma(r['ladoALado'] == esperado_lado,
               '%s: los dos medios van %s' % (nom, 'lado a lado' if esperado_lado else 'apilados'))

        # Mientras P-09 no se resuelva, el domicilio no puede presentarse como
        # confirmado: el PDF y el portal dicen dos cosas distintas.
        afirma(r['pend'], '%s: el domicilio lleva la marca de «por confirmar»' % nom)
        # En persona depende de la zona: DGIVA en suelo urbano y AVA; DGCORENADR
        # en suelo de conservacion y ANP (DEC-137).
        afirma(all(z.upper() in r['persona'].upper() for z in r['zonas']),
               '%s: en persona se dice a qué oficina acudir según la zona de los hechos' % nom)
        afirma('Inspección y Vigilancia Ambiental' in r['pieTxt'] and 'Recursos Naturales' in r['pie1Txt'],
               '%s: el pie nombra la dirección general de cada zona' % nom)
        if esperado_lado:
            afirma(r['mismoAlto'], '%s: las dos tarjetas tienen el mismo alto' % nom)
        # Una sola fuente: el pie marca lo mismo que la portada, sin las coordinaciones (DEC-158).
        afirma('Domicilio y horario por confirmar' in r['pieTxt'] and 'Teléfono por confirmar' in r['pie1Txt']
               and 'Atiende a través' not in r['pieTxt'] + r['pie1Txt'],
               '%s: el pie marca lo mismo que la portada y ya no nombra las coordinaciones' % nom)
        # El correo electronico no es una via de presentacion.
        afirma(r['mailto'] == 0, '%s: ningún enlace ofrece el correo electrónico como vía' % nom)
        afirma('correo electrónico' not in r['tarjeta'], '%s: la portada no menciona el correo como vía' % nom)

        # Lo que la ley reconoce ya no es un bloque: sus cuatro puntos son preguntas frecuentes (DEC-184).
        fq = pg.evaluate("""() => [...document.querySelectorAll('#app .faq details')].map(d => d.textContent.replace(/\\s+/g,' ').trim())""")
        todo = ' | '.join(fq)
        afirma(len(r['derechos']) == 0 and 'Lo que la ley te reconoce' not in r['tarjeta'],
               '%s: «Lo que la ley te reconoce» ya no es un bloque de la portada (DEC-184)' % nom)
        afirma(all(x in todo for x in ['Cualquier persona puede denunciar', 'la Secretaría valora los hechos igual',
                                        'Tus datos son confidenciales', 'Basta con describir lo que ocurre']),
               '%s: sus cuatro puntos siguen dichos, en las preguntas frecuentes' % nom)
        afirma(len(fq) == 9 and len(set(d.split('?')[0] for d in fq)) == 9, '%s: nueve preguntas, ninguna repetida (%d)' % (nom, len(fq)))
        afirma('pedir que sean confidenciales' not in todo and 'Tus datos son confidenciales' in todo,
               '%s: la confidencialidad se dice como regla, no como algo que se pide (DEC-119)' % nom)
        # Tres preguntas a la vista y un botón que despliega las nueve (DEC-185).
        fv = pg.evaluate("""() => { const vis = () => [...document.querySelectorAll('#app .faq details')].filter(d => d.offsetParent !== null).length;
          const b = document.querySelector('#app .faq-ver'); const a = vis(), t0 = b.innerText.trim(); b.click();
          const c = vis(), t1 = b.innerText.trim(), e1 = b.getAttribute('aria-expanded'); b.click();
          return {antes: a, despues: c, vuelve: vis(), t0: t0, t1: t1, e1: e1}; }""")
        afirma(fv['antes'] == 3 and fv['despues'] == 9 and fv['vuelve'] == 3 and fv['t0'] == 'Ver todas las preguntas (9)'
               and fv['t1'] == 'Ver menos preguntas' and fv['e1'] == 'true',
               '%s: se ven tres preguntas y «Ver todas las preguntas (9)» despliega las nueve: %s' % (nom, fv))
        # En la portada el pie no repite las oficinas; en el formulario sí las muestra.
        pie = pg.evaluate("""() => { const v = () => document.getElementById('pieEnPersona').offsetParent !== null;
          const a = v(); irA(1); const b = v(); irA(0); return [a, b]; }""")
        afirma(pie == [False, True], '%s: el pie no repite las dos oficinas en la portada y sí las muestra dentro del formulario: %s' % (nom, pie))
        afirma('sin dar tu nombre' in r['tarjeta'], '%s: la portada dice que se puede denunciar sin dar el nombre (DEC-77)' % nom)

        afirma(r['cajas'] == 0, '%s: no quedan cajas de aviso apiladas (%d)' % (nom, r['cajas']))
        afirma(not r['desborde'], '%s: sin desbordamiento horizontal' % nom)
        # El encabezado ya titula y describe: la portada no lo repite.
        afirma('Denuncia Ambiental' not in r['tarjeta'], '%s: la portada no repite el título del encabezado' % nom)
        afirma('Ten a la mano' not in r['tarjeta'], '%s: no vuelve «Ten a la mano»; lo dice «Qué necesitas»' % nom)
        afirma('Cultura de la denuncia.' in r['tarjeta'] and 'Justicia restaurativa.' in r['tarjeta'] and 'visión con la que la Secretaría' in r['tarjeta']
               and 'Denunciar no es pelearse con nadie' not in r['tarjeta'] and 'Por qué importa que denuncies' not in r['tarjeta'],
               '%s: cultura de la denuncia y justicia restaurativa, como visión de la Secretaría, sustituyen al párrafo de DEC-173 (DEC-178)' % nom)
        afirma(pg.evaluate("""() => { const b = [...document.querySelectorAll('#app .portada-bloque')].find(x => x.innerText.includes('Justicia restaurativa'));
          return !!b && b.querySelectorAll('.nec-ico svg').length === 2; }""") and 'antes que sólo actuar de manera punitiva' in r['tarjeta']
               and 'imponer una multa' not in r['tarjeta'],
               '%s: cada idea con su ícono, y la justicia restaurativa dice «antes que sólo actuar de manera punitiva» (DEC-179)' % nom)

        # El aviso de denuncia sin terminar puede acortarse, pero NUNCA puede
        # perder que aun no se ha presentado: sin esa frase alguien cierra el
        # navegador creyendo que ya denuncio (DEC-54).
        av = pg.evaluate("""() => {
          localStorage.setItem(CLAVE_BORRADOR, JSON.stringify(
            {estado:{materia:'ava', hechos:'x'.repeat(60)}, paso:3, t:Date.now()}));
          irA(0);
          const a = document.querySelector('.franja');
          const r = a ? {t: a.innerText.replace(/\\s+/g,' ').trim(),
                         botones: [...a.querySelectorAll('button')].length} : null;
          localStorage.removeItem(CLAVE_BORRADOR);
          return r;
        }""")
        afirma(av is not None, '%s: con un borrador guardado aparece el aviso' % nom)
        if av:
            afirma('no se ha presentado' in av['t'],
                   '%s: el aviso conserva que la denuncia aún no se ha presentado' % nom)
            afirma(av['botones'] == 2, '%s: el aviso ofrece continuar y descartar' % nom)
            fuera = pg.evaluate("""() => {
              localStorage.setItem(CLAVE_BORRADOR, JSON.stringify({estado:{materia:'ava'}, paso:3, t:Date.now()}));
              irA(0);
              const f = document.querySelector('.franja'), app = document.getElementById('app');
              const r = {dentro: !!(f && app.contains(f)),
                         antes: !!(f && f.getBoundingClientRect().top < app.getBoundingClientRect().top)};
              irA(1);
              r.enElPaso1 = !!document.querySelector('.franja');
              irA(0);
              localStorage.removeItem(CLAVE_BORRADOR);
              return r;
            }""")
            afirma(not fuera['dentro'], '%s: el aviso vive fuera del formulario' % nom)
            afirma(fuera['antes'], '%s: y encima de la tarjeta, como franja de sistema' % nom)
            afirma(not fuera['enElPaso1'], '%s: dentro del formulario ya no aparece' % nom)
            peso = pg.evaluate("""() => {
              localStorage.setItem(CLAVE_BORRADOR, JSON.stringify({estado:{materia:'ava'}, paso:3, t:Date.now()}));
              irA(0);
              const ini = [...document.querySelectorAll('#app button')].find(b => b.textContent.includes('Iniciar'));
              const con = [...document.querySelectorAll('button')].find(b => b.textContent.includes('Continuar donde'));
              if(!ini || !con) return null;
              const r = {iniRelleno: getComputedStyle(ini).backgroundColor,
                         conRelleno: getComputedStyle(con).backgroundColor};
              localStorage.removeItem(CLAVE_BORRADOR);
              return r;
            }""")
            afirma(peso is not None and peso['iniRelleno'] != peso['conRelleno'] and 'rgb(255, 255, 255)' in peso['conRelleno'],
                   '%s: continuar es secundario y no compite con iniciar (%s vs %s)'
                   % (nom, peso and peso['conRelleno'], peso and peso['iniRelleno']))
            afirma(len(av['t'].split(' ')) <= 26,
                   '%s: el aviso se mantiene breve (%d palabras, tope 26)' % (nom, len(av['t'].split(' '))))
        pg.evaluate("irA(0)"); pg.wait_for_timeout(200)

        afirma(err == [], '%s: sin errores propios en consola: %s' % (nom, err[:2]))
        pg.close()
    nav.close()

print('\n'.join(notas)); print()
if fallos:
    print('\n'.join(fallos)); sys.exit(1)
print('TODAS LAS PRUEBAS PASAN (%d)' % len(notas))
