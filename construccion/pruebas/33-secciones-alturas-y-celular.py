# -*- coding: utf-8 -*-
"""Secciones, alturas y teléfono (DEC-212 y DEC-213).

   DEC-212: los títulos de sección nombran el tema y no tienen forma de
   pregunta; el aviso del artículo 331 ya no está en el paso 3; ámbito y
   «¿Cuál?» comparten renglón; listas y campos de texto miden lo mismo.
   DEC-213: en teléfono, un campo por renglón y la etiqueta pegada a su
   control; el asterisco no queda solo; cada campo de texto trae un ejemplo;
   el iPhone no toma colonias por fechas o direcciones; y una lista
   desplegable no se vuelve a abrir sola después de elegir."""
import os, pathlib, sys, re
AQUI = pathlib.Path(os.path.abspath(__file__)).parent
RAIZ = AQUI.parent
RUTA = pathlib.Path(os.environ.get('ARTEFACTO', RAIZ / 'artefacto.html'))
PROTO = RAIZ.parent / 'prototipo' / 'prototipo-denuncia-ambiental-sedema.html'
TMP  = AQUI / '_pagina33.html'
CHROMIUM = os.environ.get('CHROMIUM', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
from playwright.sync_api import sync_playwright

TMP.write_text('<!doctype html><html lang="es"><head><meta charset="utf-8">' +
               RUTA.read_text(encoding='utf-8') + '</body></html>', encoding='utf-8')
EXTERNO = ('ERR_TUNNEL_CONNECTION_FAILED','net::ERR_','Failed to load resource')
fallos, notas = [], []
def afirma(c, m): (notas if c else fallos).append(('OK  ' if c else 'FALLA ') + m)

# ---- La cabecera del prototipo: sin detección de fechas ni direcciones ----
cab = PROTO.read_text(encoding='utf-8')[:3000]
afirma(re.search(r'name="format-detection" content="[^"]*date=no[^"]*address=no', cab) is not None,
       'el prototipo pide al iPhone no tomar colonias por fechas o direcciones')
afirma('name="chrome" content="nointentdetection"' in cab, 'y lo mismo a Chrome en iPhone')

RAMA_GOB = "cargaEscenario('urbano'); guarda('tipo_denunciado','gobierno'); guarda('autoridad_nivel','cdmx'); guarda('es_estab','si');"

with sync_playwright() as pw:
    nav = pw.chromium.launch(executable_path=CHROMIUM)
    err = []
    for ancho in (1100, 390):
        pg = nav.new_context(viewport={'width':ancho,'height':900}).new_page()
        pg.on('console', lambda m: err.append(m.text) if m.type=='error' and not any(x in m.text for x in EXTERNO) else None)
        pg.on('pageerror', lambda e: err.append('pageerror: '+str(e)))
        pg.goto(TMP.as_uri()); pg.wait_for_timeout(600)
        tel = ancho < 700
        nom = 'teléfono' if tel else 'escritorio'

        # ---- Alturas parejas ----
        h = pg.evaluate("""() => { cargaEscenario('urbano'); irA(2);
          const a = id => { const e = document.getElementById(id); return e ? e.offsetHeight : 0; };
          return [a('f_alcaldia_dir'), a('f_colonia'), a('f_cp'), a('f_calle'), a('f_num_ext')]; }""")
        afirma(len(set(h)) == 1, '%s: alcaldía, colonia, CP, calle y número miden lo mismo %s' % (nom, h))

        # ---- Paso 3: secciones y autoridad ----
        p3 = pg.evaluate("""() => { %s irA(3);
          const t = [...document.querySelectorAll('#app h3.sub-seccion')].map(x => x.innerText.trim());
          const n = document.getElementById('f_autoridad_nivel'), c = document.getElementById('f_autoridad_denunciada');
          const txt = document.getElementById('app').innerText;
          return {titulos: t, pregunta: t.filter(x => x.indexOf('¿') >= 0),
                  temporalidadEtq: !!document.querySelector('#c_temporalidad > .etq'),
                  aviso331: txt.indexOf('procedimiento es distinto') >= 0 || txt.indexOf('artículo 331') >= 0,
                  dif: n && c ? Math.abs(n.getBoundingClientRect().top - c.getBoundingClientRect().top) : -1,
                  alturas: n && c ? [n.offsetHeight, c.offsetHeight] : []}; }""" % RAMA_GOB)
        afirma(p3['pregunta'] == [], '%s: ningún título de sección del paso 3 tiene forma de pregunta %s' % (nom, p3['titulos']))
        afirma('Responsable de los hechos' in p3['titulos'] and 'Cuándo ocurre' in p3['titulos'],
               '%s: las secciones son «Cuándo ocurre» y «Responsable de los hechos»' % nom)
        afirma(p3['temporalidadEtq'], '%s: «¿Desde cuándo ocurre?» es una pregunta, no un título' % nom)
        afirma(not p3['aviso331'], '%s: el paso 3 ya no muestra el aviso del artículo 331' % nom)
        if tel:
            afirma(p3['dif'] > 40, 'teléfono: ámbito y «¿Cuál?» van uno debajo del otro')
        else:
            afirma(0 <= p3['dif'] < 2, 'escritorio: ámbito y «¿Cuál?» comparten renglón')
        afirma(len(set(p3['alturas'])) == 1, '%s: y miden lo mismo %s' % (nom, p3['alturas']))

        # ---- Etiqueta pegada a su control, en renglón o suelto ----
        sep = pg.evaluate("""() => { cargaEscenario('urbano'); irA(2);
          const d = k => { const c = document.getElementById('c_'+k), l = c.querySelector('label'),
                                 f = document.getElementById('f_'+k), a = document.getElementById('a_'+k);
                           return Math.round(f.getBoundingClientRect().top - l.getBoundingClientRect().bottom
                                              - (a ? a.getBoundingClientRect().height : 0)); };
          return {calle: d('calle'), colonia: d('colonia'), entre: d('entre_calles')}; }""")
        afirma(max(sep.values()) <= 12, '%s: la etiqueta queda pegada a su campo, también en renglón %s' % (nom, sep))

        # ---- Marcadores ----
        sin = pg.evaluate("""() => { const out = [];
          const ramas = [{tiene_mz_lote:'si'}, {es_estab:'si', tipo_estab:'Otro', tipo_denunciado:'gobierno', autoridad_nivel:'cdmx', reporto_antes:'si'},
                         {identificacion:'nombre', dom_tiene_mz_lote:'si'}, {identificacion:'nombre', dom_fuera_cdmx:'si'},
                         {tipo_denunciado:'nose'}, {tiene_direccion:'no'}];
          for(const r of ramas){ cargaEscenario('urbano'); for(const k in r) guarda(k, r[k]);
            for(let n = 2; n <= 5; n++){ irA(n);
              document.querySelectorAll('#app input[type=text],#app input[type=tel],#app input[type=email],#app textarea').forEach(e => {
                if(e.offsetParent !== null && !e.placeholder) out.push(e.id); }); } }
          return [...new Set(out)]; }""")
        afirma(sin == [], '%s: todos los campos de texto traen un ejemplo %s' % (nom, sin))

        # ---- El asterisco no queda solo en un renglón ----
        ast = pg.evaluate("""() => { %s irA(3);
          const solos = [];
          document.querySelectorAll('#app label > .req, #app .etq > .req').forEach(r => {
            const t = r.previousSibling;
            if(!t || t.nodeType !== 3) return;
            const txt = t.textContent.replace(/[\\s\\u00a0]+$/, '');
            if(!txt) return;
            const rg = document.createRange(); rg.setStart(t, txt.length - 1); rg.setEnd(t, txt.length);
            const u = rg.getBoundingClientRect(), rr = r.getBoundingClientRect();
            if(Math.abs(u.top - rr.top) > 4) solos.push(r.parentElement.innerText.trim().slice(0, 40)); });
          return solos; }""" % RAMA_GOB)
        afirma(ast == [], '%s: ningún asterisco queda solo en su renglón %s' % (nom, ast))

        # ---- Un campo por renglón en teléfono ----
        if tel:
            col = pg.evaluate("""() => { cargaEscenario('urbano'); irA(2);
              const c = document.getElementById('f_calle').getBoundingClientRect(), n = document.getElementById('f_num_ext').getBoundingClientRect();
              const s = document.getElementById('f_alcaldia_dir');
              return {apilados: n.top > c.bottom, anchoNum: Math.round(n.width), anchoCalle: Math.round(c.width),
                      ws: getComputedStyle(s).whiteSpace}; }""")
            afirma(col['apilados'] and col['anchoNum'] == col['anchoCalle'],
                   'teléfono: calle y número exterior van uno debajo del otro, a todo lo ancho')
            afirma(col['ws'] == 'nowrap', 'teléfono: lo elegido en una lista ocupa un solo renglón')

        # ---- DEC-214: el espacio bajo un campo en renglón no depende del subgrid ----
        esp = pg.evaluate("""() => { cargaEscenario('urbano'); irA(2);
          const b = id => document.getElementById(id).getBoundingClientRect();
          const etq = k => document.querySelector('#c_'+k+' label').getBoundingClientRect();
          const cs = getComputedStyle(document.getElementById('c_calle'));
          return {calleNum: Math.round(etq('num_ext').top - b('f_calle').bottom),
                  numMz: Math.round(document.querySelector('#c_tiene_mz_lote .etq').getBoundingClientRect().top - b('f_num_ext').bottom),
                  cpRef: Math.round(etq('referencias').top - b('f_cp').bottom),
                  suelto: Math.round(etq('alcaldia_dir').top - b('f_entre_calles').bottom),
                  margenCampo: cs.marginBottom, display: cs.display}; }""")
        if tel:
            afirma(esp['display'] == 'block', 'teléfono: en un renglón, cada campo es un bloque, sin subgrid (%s)' % esp['display'])
            afirma(esp['calleNum'] >= 16, 'teléfono: entre calle y número exterior hay aire (%s px)' % esp['calleNum'])
        else:
            afirma(esp['margenCampo'] == '0px', 'escritorio: el espacio bajo el renglón lo pone el renglón, no el campo')
        afirma(esp['numMz'] >= 16 and esp['cpRef'] >= 16 and abs(esp['cpRef'] - esp['suelto']) <= 2,
               '%s: tras un renglón queda el mismo aire que tras un campo suelto %s' % (nom, esp))

        # ---- DEC-214: la colonia conserva su marcador al elegir alcaldía ----
        col2 = pg.evaluate("""() => { cargaEscenario('urbano'); guarda('alcaldia_dir',''); guarda('colonia',''); irA(2);
          const antes = document.getElementById('f_colonia').placeholder;
          const s = document.getElementById('f_alcaldia_dir'); s.value = 'Azcapotzalco'; s.dispatchEvent(new Event('change'));
          return [antes, document.getElementById('f_colonia').placeholder]; }""")
        afirma(col2[0] != '' and col2[1] != '' and col2[0] != col2[1],
               '%s: la colonia trae marcador antes y después de elegir alcaldía %s' % (nom, col2))

        # ---- DEC-214: sin «Denuncia sobre» en el paso 3 ----
        ds = pg.evaluate("() => { cargaEscenario('urbano'); irA(3); return document.getElementById('app').innerText.indexOf('Denuncia sobre') >= 0; }")
        afirma(not ds, '%s: el paso 3 ya no repite la materia bajo el título' % nom)
        pg.close()

    # ---- Con el dedo, la lista no se vuelve a enfocar (en iPhone se reabría) ----
    pg = nav.new_context(viewport={'width':390,'height':900}, has_touch=True).new_page()
    pg.goto(TMP.as_uri()); pg.wait_for_timeout(600)
    foco = pg.evaluate("""() => {
      const original = window.matchMedia;
      const res = {};
      for(const dedo of [true, false]){
        window.matchMedia = q => ({matches: q.indexOf('coarse') >= 0 ? dedo : original(q).matches});
        cargaEscenario('urbano'); guarda('es_estab','si'); guarda('tipo_estab',''); irA(3);
        const s = document.getElementById('f_tipo_estab'); s.focus();
        s.value = TIPOS_ESTAB[0]; s.dispatchEvent(new Event('change'));
        res[dedo ? 'dedo' : 'raton'] = document.activeElement ? document.activeElement.id : '';
        s.blur && document.getElementById('f_tipo_estab').blur();
        guarda('tipo_estab',''); irA(3);
        const s2 = document.getElementById('f_tipo_estab'); s2.value = 'Otro'; s2.dispatchEvent(new Event('change'));
        res[(dedo ? 'dedo' : 'raton') + 'Otro'] = document.activeElement ? document.activeElement.id : '';
      }
      window.matchMedia = original; return res; }""")
    afirma(foco['dedo'] != 'f_tipo_estab', 'con el dedo, elegir un tipo no vuelve a enfocar la lista (%s)' % foco['dedo'])
    afirma(foco['raton'] == 'f_tipo_estab', 'con teclado o ratón, el foco vuelve a la lista (%s)' % foco['raton'])
    afirma(foco['dedoOtro'] == 'f_tipo_estab_otro' and foco['ratonOtro'] == 'f_tipo_estab_otro',
           'con «Otro», el foco pasa al campo para especificarlo')
    pg.close()
    afirma(err == [], 'sin errores propios en consola: %s' % err[:2])
    nav.close()

print('\n'.join(notas)); print()
if fallos:
    print('\n'.join(fallos)); sys.exit(1)
print('TODAS LAS PRUEBAS PASAN (%d)' % len(notas))
