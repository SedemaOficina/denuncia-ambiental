# -*- coding: utf-8 -*-
"""Los defectos que la auditoría del 20 de septiembre encontró (DEC-100).

   Las trece baterías anteriores estaban en verde y ninguna de ellas habría
   detectado ninguno de estos. Tienen una familia común: **se comprobaba el
   estado y no la pantalla**. La ficha del cruce turnaba bien a la PROFEPA
   —eso sí se medía— y debajo imprimía, en verde, que la Secretaría atendía
   en el ámbito local; el resumen de errores listaba el punto del mapa y su
   enlace no llevaba a ninguna parte; el botón de descartar el borrador no
   hacía nada. Todo eso convivía con 343 comprobaciones en verde.

   Esta batería mira lo que la persona ve y lo que la persona pulsa."""
import os, pathlib, sys
AQUI = pathlib.Path(os.path.abspath(__file__)).parent
RAIZ = AQUI.parent
RUTA = pathlib.Path(os.environ.get('ARTEFACTO', RAIZ / 'artefacto.html'))
TMP  = AQUI / '_pagina14.html'
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

    # ---- 1. La ficha del cruce no puede decir dos cosas a la vez ----
    #    Se lee el PANEL, no el estado. Se recorre cada parque federal, con
    #    convenio y sin él, más el único punto con concurrencia federal-local.
    def ficha(la, lo):
        return pg.evaluate("""([a,b]) => {
          cfg.validar = false; guarda('materia','tala'); guarda('tiene_direccion','no');
          irA(2); ponMarcador(a, b);
          const c = document.getElementById('panelCapas');
          return {txt: c ? c.innerText : '', dg: val('dg_nombre'), coadmin: val('coadmin'),
                  concurrencia: val('concurrencia')};
        }""", [la, lo])

    federales = pg.evaluate("""() => CAPAS_GEOM.filter(f => f.p.grupo === 'ANP · Federal').map(f => f.p.nombre)""")
    DENTRO = """(nombre) => {
      const f = CAPAS_GEOM.find(x => x.p.nombre === nombre); if(!f) return null;
      const pts = []; (function rec(x){
        if(Array.isArray(x) && x.length===2 && typeof x[0]==='number') pts.push(x);
        else if(Array.isArray(x)) x.forEach(rec); })(f.g.coordinates);
      const lons = pts.map(p=>p[0]), lats = pts.map(p=>p[1]);
      const x0=Math.min(...lons), x1=Math.max(...lons), y0=Math.min(...lats), y1=Math.max(...lats);
      for(let i=1;i<12;i++) for(let j=1;j<12;j++){
        const lo=x0+(x1-x0)*i/12, la=y0+(y1-y0)*j/12;
        if(buscaEn(CAPAS_GEOM, la, lo, p => p.nombre===nombre)) return {lat:la, lon:lo};
      } return null; }"""

    contradice, dobles = [], []
    for nom in federales:
        pt = pg.evaluate(DENTRO, nom)
        if not pt: continue
        f = ficha(pt['lat'], pt['lon'])
        if 'PROFEPA' in (f['dg'] or '') and 'ámbito local' in f['txt']:
            contradice.append(nom)
        if f['txt'].count('a consulta de las áreas') > 1:
            dobles.append((nom, 'P-22 repetido'))
        if f['txt'].count('El punto también se encuentra dentro') > 1:
            dobles.append((nom, 'concurrencia repetida'))
    afirma(contradice == [],
           'ningún parque federal dice a la vez PROFEPA y «se atiende en el ámbito local»: %s' % contradice)
    afirma(dobles == [], 'y ninguna advertencia aparece dos veces en la misma ficha: %s' % dobles)

    # El Cerro de la Estrella es el único con decreto federal y local a la vez.
    f = ficha(19.34596, -99.09696)
    afirma('PROFEPA' in (f['dg'] or ''), 'Cerro de la Estrella: se turna a la PROFEPA (%s)' % f['dg'])
    afirma(f['txt'].count('a consulta de las áreas') == 1,
           'y la advertencia del criterio provisional aparece una sola vez')

    # ---- 2. El botón de descartar el borrador hace algo ----
    b = pg.evaluate("""() => {
      estado = {}; archivos = [];
      guarda('materia','tala'); guarda('hechos','Están tirando cascajo en la barranca.');
      guardaBorrador(); irA(0);
      const franja = document.getElementById('franjaBorrador');
      const bot = [...franja.querySelectorAll('button')].find(x => x.textContent.indexOf('Descartar') >= 0);
      if(!bot) return {franja: !!franja.innerText.trim(), bot: false};
      bot.click();
      const conf = document.getElementById('confirmaBorrar');
      return {franja: true, bot: true, confirma: !!conf,
              dentro: conf ? franja.contains(conf) : false};
    }"""); pg.wait_for_timeout(250)
    afirma(b['franja'], 'con un borrador guardado, la portada lo ofrece')
    afirma(b.get('bot'), 'y tiene botón de descartar')
    afirma(b.get('confirma'), 'que abre la confirmación en vez de no hacer nada')
    afirma(b.get('dentro'), 'y la abre junto al botón, no en otra pantalla')
    borrado = pg.evaluate("""() => {
      const s = [...document.querySelectorAll('#confirmaBorrar button')].find(x => x.textContent.indexOf('Sí, descartar') >= 0);
      if(s) s.click();
      return {queda: !!leeBorrador()};
    }"""); pg.wait_for_timeout(250)
    afirma(not borrado['queda'], 'al confirmar, el borrador se borra de verdad')

    # ---- 3. Los límites de archivos se aplican, y lo que se rechaza se dice ----
    a = pg.evaluate("""() => {
      estado = {}; archivos = []; irA(4);
      const f = (n, mb) => ({name: n, size: mb * 1048576});
      agregaArchivos([f('a.jpg',2), f('enorme.jpg',300), f('hoja.xlsx',1)]);
      const lista = document.getElementById('listaArch');
      return {n: archivos.length, txt: lista ? lista.innerText : '',
              nombres: archivos.map(x => x.name)};
    }"""); pg.wait_for_timeout(200)
    afirma(a['nombres'] == ['a.jpg'], 'se acepta sólo el archivo admisible: %s' % a['nombres'])
    afirma('enorme.jpg' in a['txt'] and 'MB' in a['txt'],
           'se dice qué archivo se rechazó por tamaño y por qué')
    afirma('hoja.xlsx' in a['txt'], 'y cuál por tipo no admitido')
    corte = pg.evaluate("""() => {
      archivos = [];
      const muchos = []; for(let i=0;i<14;i++) muchos.push({name:'f'+i+'.jpg', size:1048576});
      agregaArchivos(muchos);
      return {n: archivos.length, txt: document.getElementById('listaArch').innerText};
    }"""); pg.wait_for_timeout(200)
    afirma(corte['n'] == 10, 'el corte por número se aplica (%d)' % corte['n'])
    afirma('sólo se admiten 10' in corte['txt'], 'y no se callan los sobrantes')

    # ---- 4. El foco acompaña a la persona al cambiar de paso ----
    fo = pg.evaluate("""() => {
      estado = {}; archivos = []; cfg.validar = false;
      guarda('materia','tala'); irA(2);
      const antes = document.activeElement ? document.activeElement.tagName : '';
      irA(3);
      const a = document.activeElement;
      return {antes, etiqueta: a ? a.tagName : '', esEncabezado: !!(a && a.closest && a.closest('#app .tarjeta') && a.tagName === 'H2')};
    }"""); pg.wait_for_timeout(250)
    afirma(fo['esEncabezado'],
           'al cambiar de paso el foco va al encabezado, no al principio del documento (%s)' % fo['etiqueta'])
    quieto = pg.evaluate("""() => {
      const a = document.activeElement;
      guarda('es_estab','no'); render();
      return document.activeElement === a || document.activeElement.tagName !== 'H2';
    }"""); pg.wait_for_timeout(200)
    afirma(quieto, 'y no se lo quita a quien está contestando dentro del mismo paso')

    # ---- 5. «Editar», en la revisión, aterriza en el campo ----
    ed = pg.evaluate("""() => {
      cargaEscenario('urbano'); return null;
    }"""); pg.wait_for_timeout(400)
    perdidos = pg.evaluate("""() => {
      irA(6);
      const bots = [...document.querySelectorAll('#app button.editar')];
      const malos = [];
      bots.forEach((b, i) => {
        const m = /vaACampo\\((\\d+),'([a-z_0-9]+)'\\)/.exec(b.getAttribute('onclick') || '');
        if(!m) return;
        const destino = +m[1], clave = m[2];
        irA(destino);
        if(!document.getElementById('c_' + clave) && !document.getElementById('f_' + clave))
          malos.push(clave);
        irA(6);
      });
      return {n: bots.length, malos};
    }"""); pg.wait_for_timeout(400)
    afirma(perdidos['malos'] == [],
           'los %d botones «Editar» llevan a un campo que existe: %s' % (perdidos['n'], perdidos['malos']))

    # ---- 6. Cada clave del catálogo se rinde en alguna pantalla ----
    #    Esto es lo que habría cazado el campo fantasma «responsables» y el
    #    punto del mapa sin ancla: un campo que el documento 09 declara y que
    #    en ninguna ruta se puede llenar.
    fantasmas = pg.evaluate("""() => {
      const vistos = new Set();
      const rutas = [
        {tiene_direccion:'si', materia:'tala', tipo_denunciado:'empresa', es_estab:'si', tipo_estab:'Otro',
         identificacion:'nombre', notif_correo:'no', sabe_permisos:'si', reporto_antes:'si', temporalidad:'unico'},
        {tiene_direccion:'no', materia:'tala', tipo_denunciado:'gobierno', autoridad_nivel:'cdmx',
         identificacion:'llave', sesion_llave:'si', notif_correo:'si'},
        {tiene_direccion:'si', materia:'tala', tipo_denunciado:'particular', identificacion:'anonima'}
      ];
      rutas.forEach(r => {
        estado = {}; archivos = [];
        Object.keys(r).forEach(k => guarda(k, r[k]));
        for(let p = 1; p <= 6; p++){
          irA(p);
          Object.keys(OBLIG).forEach(k => {
            if(document.getElementById('c_'+k) || document.getElementById('f_'+k)) vistos.add(k);
          });
        }
      });
      /* Los campos derivados no se rinden por definicion: la alcaldia la
         determina el punto del mapa y por eso no tiene control (DEC-72). */
      return Object.keys(OBLIG).filter(k => !vistos.has(k) &&
        !(OBLIG[k].cond_txt && OBLIG[k].cond_txt.indexOf('No se pregunta') === 0));
    }"""); pg.wait_for_timeout(600)
    afirma(fantasmas == [],
           'ningún campo del catálogo es un fantasma: todos se rinden en alguna ruta (%s)' % fantasmas)

    # ---- 7. Las ramas declaran el paso donde de verdad viven ----
    ramas = pg.evaluate("""() => {
      const porEtq = {};
      Object.keys(OBLIG).forEach(k => { porEtq[OBLIG[k].etq] = OBLIG[k].p; });
      return BIFURCACIONES.filter(b => porEtq[b.pregunta] !== undefined
                                    && String(porEtq[b.pregunta]) !== String(b.paso))
                          .map(b => b.pregunta + ': dice ' + b.paso + ', vive en ' + porEtq[b.pregunta]);
    }""")
    afirma(ramas == [], 'cada rama declara el paso donde vive el campo que nombra: %s' % ramas)

    # ---- 8. El escenario abre donde se ve lo que anuncia ----
    giro = pg.evaluate("""() => { cargaEscenario('otro_giro');
      return {paso: paso, campo: !!document.getElementById('f_tipo_estab_otro')}; }""")
    pg.wait_for_timeout(300)
    afirma(giro['campo'], 'el escenario del giro no listado abre donde el campo de texto se ve (paso %s)' % giro['paso'])

    # ---- 9. Lo capturado en una rama de responsable no sobrevive a la otra ----
    sobra = pg.evaluate("""() => {
      cargaEscenario('urbano'); irA(3);
      const antes = val('establecimiento');
      guarda('tipo_denunciado','particular'); limpiaResponsable(); render();
      irA(6);
      const resumen = document.getElementById('app').innerText;
      return {antes, despues: val('establecimiento'),
              enResumen: antes ? resumen.split(antes).length - 1 : 0};
    }"""); pg.wait_for_timeout(400)
    afirma(sobra['antes'] != '', 'el escenario captura una razón social')
    afirma(sobra['despues'] == '',
           'que no sobrevive al cambio de rama de responsable: %r' % sobra['despues'])
    afirma(sobra['enResumen'] == 0, 'ni reaparece en la revisión (%d veces)' % sobra['enResumen'])

    # ---- 10. El folio nombra al área que atiende ----
    fol = {}
    for esc_id, esperado in [('urbano','DGIVA'), ('conservacion','DGCORENADR'), ('anp_federal','REM')]:
        r = pg.evaluate("""(id) => { cargaEscenario(id); guarda('verificacion','si');
          cfg.limite = false; irA(6); enviar();
          return {folio: val('folio'), dg: val('dg')}; }""", esc_id)
        pg.wait_for_timeout(300)
        fol[esc_id] = r
        afirma(('/'+esperado+'/') in (r['folio'] or ''),
               '%s: el folio nombra al área que atiende (%s)' % (esc_id, r['folio']))

    # ---- 11. El acuse federal no promete plazos de la Secretaría ----
    ac = pg.evaluate("""() => { cargaEscenario('anp_federal'); guarda('verificacion','si');
      irA(6);
      const envio = document.getElementById('app').innerText;
      enviar();
      const acuse = document.getElementById('app').innerText;
      return {envio, acuse}; }"""); pg.wait_for_timeout(400)
    afirma('tres días hábiles y analiza el caso en diez' not in ac['envio'],
           'el aviso de envío no compromete a la PROFEPA con los plazos de la Secretaría')
    afirma('los plazos de atención los fija esa autoridad' in ac['envio'],
           'y dice de quién son los plazos')
    afirma('de esa dirección general' not in ac['acuse'],
           'el acuse no llama dirección general de la Secretaría a la PROFEPA')

    # ---- 12. Ninguna regla de estilo apunta a una clase que no existe ----
    #    Es el barrido de la misma familia que el de --error-txt: una regla
    #    cuyo selector ya no aparece en ninguna parte es una regla que nadie
    #    volverá a mirar, y ahí es donde se pudren las cosas. Se busca la
    #    clase en el CÓDIGO del documento, no en una pantalla concreta: así no
    #    hace falta recorrer todos los estados para saber si se usa.
    muertos = pg.evaluate("""() => {
      const todo = document.documentElement.outerHTML;
      const soloEstilos = [...document.querySelectorAll('style')].map(s => s.textContent).join('\\n');
      const fuera = todo.split(soloEstilos).join(' ');   /* el documento sin sus hojas */
      const usada = c => fuera.indexOf(c) >= 0;
      const malas = new Set();
      for(const hoja of document.styleSheets){
        let reglas; try { reglas = hoja.cssRules; } catch(e){ continue; }
        for(const r of reglas){
          if(!r.selectorText) continue;
          (r.selectorText.match(/\\.[A-Za-z][\\w-]*/g) || []).forEach(c => {
            if(!usada(c.slice(1))) malas.add(c.slice(1));
          });
        }
      }
      return [...malas].sort();
    }"""); pg.wait_for_timeout(300)
    afirma(muertos == [],
           'ninguna regla de estilo apunta a una clase que el documento no usa: %s' % muertos)

    afirma(err == [], 'sin errores propios en consola: %s' % err[:3])
    pg.close(); nav.close()

print('\n'.join(notas)); print()
if fallos:
    print('\n'.join(fallos)); sys.exit(1)
print('TODAS LAS PRUEBAS PASAN (%d)' % len(notas))
