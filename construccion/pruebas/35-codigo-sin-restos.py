# -*- coding: utf-8 -*-
"""Código y hojas de estilo sin restos (criterio 4 de la fase 1, DEC-227).

   Lo que antes se revisaba a mano en cada auditoría de cierre queda como
   batería: funciones duplicadas o sin uso, clases de estilo que nadie usa
   —también dentro de @media y @supports—, selectores declarados dos veces,
   «!important» fuera del bloque de movimiento reducido, colores fuera de
   :root, identificadores como selector de estilo (Regla 3), restos de
   depuración y código comentado. Se lee el código del documento, no una
   pantalla: así no hace falta recorrer todos los estados."""
import os, pathlib, re, io, sys, collections
AQUI = pathlib.Path(os.path.abspath(__file__)).parent
RAIZ = AQUI.parent
RUTA = pathlib.Path(os.environ.get('ARTEFACTO', RAIZ / 'artefacto.html'))
fallos, notas = [], []
def afirma(c, m): (notas if c else fallos).append(('OK  ' if c else 'FALLA ') + m)
PROTO = RAIZ.parent / 'prototipo' / 'prototipo-denuncia-ambiental-sedema.html'
MAQUETA = RAIZ.parent / 'prototipo' / 'administracion' / 'maqueta-administracion.html'
# Variables globales que la pagina no usa porque las lee un generador: INTERNOS
# lo lee generar_doc09.py; ESTADOS y CANALES de la maqueta, generar_admin.py.
LEIDAS_FUERA = {'prototipo': {'INTERNOS'}, 'artefacto': {'INTERNOS'}, 'maqueta': {'ESTADOS', 'CANALES'}}
# El artefacto agrega el mapa vectorial: sus funciones sustituyen a propósito
# las del mapa de calles (construir.py), así que el código se audita en el
# prototipo, que es la fuente; los estilos, en los dos.
for etiqueta, origen in (('prototipo', PROTO), ('artefacto', RUTA), ('maqueta', MAQUETA)):
  s = origen.read_text(encoding='utf-8')
  estilos = '\n'.join(re.findall(r'<style[^>]*>(.*?)</style>', s, re.S))
  scripts = '\n'.join(re.findall(r'<script[^>]*>(.*?)</script>', s, re.S))
  cuerpo = re.sub(r'<style[^>]*>.*?</style>', ' ', s, flags=re.S)
  sin_coment_js = re.sub(r'/\*.*?\*/', ' ', scripts, flags=re.S)
  sin_coment_js = re.sub(r'(?m)^\s*//.*$', ' ', sin_coment_js)
  codigo = re.sub(r'<script[^>]*>.*?</script>', ' ', cuerpo, flags=re.S) + '\n' + sin_coment_js
  # 1. funciones sin uso
  funcs = re.findall(r'\bfunction\s+([A-Za-z_$][\w$]*)\s*\(', sin_coment_js)
  dup_f = [f for f, n in collections.Counter(funcs).items() if n > 1]
  sin_uso_f = [f for f in sorted(set(funcs)) if len(re.findall(r'(?<![\w$.])' + re.escape(f) + r'(?![\w$])', codigo)) < 2]
  # 2. variables de nivel superior sin uso
  vars_ = re.findall(r'(?m)^(?:var|let|const)\s+([A-Za-z_$][\w$]*)', sin_coment_js)
  sin_uso_v = [v for v in sorted(set(vars_)) if len(re.findall(r'(?<![\w$])' + re.escape(v) + r'(?![\w$])', codigo)) < 2]
  # 3. CSS
  css = re.sub(r'/\*.*?\*/', ' ', estilos, flags=re.S)
  importantes = len(re.findall(r'!important', css))
  # reglas top-level y dentro de @media/@supports
  def reglas(txt, ctx=''):
      out = []; i = 0
      while i < len(txt):
          j = txt.find('{', i)
          if j < 0: break
          sel = txt[i:j].strip()
          # buscar llave de cierre equilibrada
          d = 1; k = j + 1
          while d and k < len(txt):
              if txt[k] == '{': d += 1
              elif txt[k] == '}': d -= 1
              k += 1
          cuerpo_r = txt[j+1:k-1]
          if sel.startswith('@media') or sel.startswith('@supports'):
              out += reglas(cuerpo_r, sel)
          elif not sel.startswith('@'):
              out.append((ctx, sel, cuerpo_r))
          i = k
      return out
  R = reglas(css)
  clases_css = set()
  for ctx, sel, _ in R:
      clases_css |= set(re.findall(r'\.([A-Za-z][\w-]*)', re.sub(r'url\([^)]*\)', '', sel)))
  texto_no_css = codigo
  sin_uso_c = sorted(c for c in clases_css if not re.search(r'(?<![\w-])' + re.escape(c) + r'(?![\w-])', texto_no_css))
  # selectores repetidos en el mismo contexto
  cuenta = collections.Counter()
  for ctx, sel, _ in R:
      for parte in [x.strip() for x in sel.split(',')]:
          cuenta[(ctx, re.sub(r'\s+', ' ', parte))] += 1
  repetidos = sorted([(c, s_) for (c, s_), n in cuenta.items() if n > 1])
  # colores fuera de :root
  fuera_root = []
  for ctx, sel, cu in R:
      if sel.strip() in (':root',) or ':root' in sel: continue
      for m in re.findall(r'#[0-9a-fA-F]{3,8}\b|rgba?\([^)]*\)', cu):
          if m.startswith('rgba(0, 0, 0') or m.startswith('rgba(0,0,0'): continue
          fuera_root.append((sel[:50], m))
  # 4. ids referenciados que nunca se crean
  ids_ref = set(re.findall(r"\$\('([A-Za-z][\w-]*)'\)", sin_coment_js)) | set(re.findall(r"getElementById\('([A-Za-z][\w-]*)'\)", sin_coment_js))
  ids_def = set(re.findall(r'id=\\?["\']([A-Za-z][\w-]*)', s)) | set(re.findall(r"id=\"'\+?'?([A-Za-z][\w-]*)", s))
  ids_huerf = sorted(i for i in ids_ref if i not in ids_def and not re.search(r"id=[\"']" + re.escape(i), s) and ("'" + i) not in s.replace("$('"+i,'').replace("getElementById('"+i,''))
  # 5. código comentado (zombi): líneas comentadas que parecen código
  zombi = [l.strip()[:90] for l in re.findall(r'(?m)^\s*//\s*(.*[;{}]\s*)$', scripts)]
  bloques = [b.strip()[:90] for b in re.findall(r'/\*(.*?)\*/', scripts, re.S) if re.search(r'(function\s*\(|\bvar\s+\w+\s*=|\)\s*;\s*$|^\s*if\s*\()', b, re.M) and len(re.findall(r'[;{}]', b)) >= 3]
  # 6. console.log / debugger
  dbg = re.findall(r'console\.log\(|debugger;', scripts)

  # Excepciones anotadas: la regla común de los campos de captura más la propia
  # de cada control que la necesita (alto del texto largo, flecha de la lista,
  # ancho de la fecha en iPhone).
  EXCEPCION = {('', 'textarea'), ('', 'select'), ('', 'input[type=date]')}
  if etiqueta == 'prototipo': afirma(not dup_f, etiqueta + ': ninguna función se declara dos veces: %s' % dup_f)
  if etiqueta == 'prototipo': afirma(not sin_uso_f, etiqueta + ': ninguna función queda sin uso: %s' % sin_uso_f)
  afirma([v for v in sin_uso_v if v not in LEIDAS_FUERA[etiqueta]] == [], etiqueta + ': ninguna variable global queda sin uso: %s' % sin_uso_v)
  afirma(not sin_uso_c, etiqueta + ': ninguna clase de estilo queda huérfana, tampoco en @media o @supports: %s' % sin_uso_c)
  afirma([x for x in repetidos if x not in EXCEPCION] == [], etiqueta + ': ningún selector se declara dos veces, salvo las tres excepciones anotadas: %s' % repetidos)
  reducido = re.search(r'@media\s*\(prefers-reduced-motion:\s*reduce\)\s*\{(.*?)\}\s*\}', css, re.S)
  dentro = len(re.findall(r'!important', reducido.group(1))) if reducido else 0
  afirma(importantes == dentro, etiqueta + ': «!important» sólo en el bloque de movimiento reducido (%d de %d)' % (dentro, importantes))
  afirma(not fuera_root, etiqueta + ': ningún color fuera de :root: %s' % fuera_root[:3])
  ids_css = [sel for ctx, sel, _ in R if re.search(r'#[A-Za-z]', sel)]
  afirma(not ids_css, etiqueta + ': ningún identificador se usa como selector de estilo (Regla 3): %s' % ids_css[:3])
  afirma(not dbg, etiqueta + ': sin restos de depuración (console.log, debugger)')
  # Una propiedad, una vez por regla; el respaldo de max-height para
  # navegadores sin dvh es deliberado y va comentado.
  dprop = []
  for ctx_, sel_, cu_ in R:
      props = [x.split(':')[0].strip() for x in re.sub(r'/\*.*?\*/', '', cu_).split(';') if ':' in x]
      dprop += [(sel_.strip()[:50], q) for q, n in collections.Counter(props).items() if n > 1 and q != 'max-height']
  afirma(not dprop, etiqueta + ': ninguna propiedad se declara dos veces en la misma regla: %s' % dprop)
  # Regla 9: un estilo en línea repetido se vuelve clase; los anchos de
  # columna de una tabla son la excepción.
  enlinea = collections.Counter(x.strip() for x in re.findall(r'style=\\?"([^"\\]+)', s))
  repe = [k for k, n in enlinea.items() if n > 1 and not re.fullmatch(r'width:\d+%', k)]
  afirma(not repe, etiqueta + ': ningún estilo en línea se repite (Regla 9): %s' % repe)
  afirma(not zombi and not bloques, etiqueta + ': sin código comentado: %s' % (zombi + bloques)[:2])
  # 7. Un catch vacío calla un error sin decir por qué es seguro callarlo (A4-01).
  vacios = re.findall(r'catch\s*\(\s*\w*\s*\)\s*\{\s*\}', scripts)
  afirma(not vacios, etiqueta + ': ningún catch vacío sin un comentario que diga por qué: %d' % len(vacios))

# ---- Ampliación del bloque 6 de la auditoría (DEC-239) ----
s = PROTO.read_text(encoding='utf-8')
scripts = '\n'.join(re.findall(r'<script[^>]*>(.*?)</script>', s, re.S))
sin_coment = re.sub(r'(?m)^\s*//.*$', ' ', re.sub(r'/\*.*?\*/', ' ', scripts, flags=re.S))

# 8. Variables locales sin uso (A4-01): en cada función de nivel superior, todo
#    nombre que se declara con var, let o const se vuelve a usar.
def funciones(txt):
    lineas, out, i = txt.split('\n'), [], 0
    while i < len(lineas):
        m = re.match(r'function\s+([A-Za-z_$][\w$]*)\s*\(', lineas[i])
        if not m: i += 1; continue
        j = i
        if not (lineas[i].rstrip().endswith('}') and lineas[i].count('{') == lineas[i].count('}')):
            j = i + 1
            while j < len(lineas) and not lineas[j].startswith('}'): j += 1
        out.append((m.group(1), '\n'.join(lineas[i:j + 1]))); i = j + 1
    return out
def declarados(cuerpo):
    """Los nombres de cada declaración, también los que siguen a una coma."""
    nombres = []
    for m in re.finditer(r'\b(?:var|let|const)\s+', cuerpo):
        k, prof, partes, ini = m.end(), 0, [], m.end()
        while k < len(cuerpo):
            ch = cuerpo[k]
            if ch in '\'"`':
                k = cuerpo.find(ch, k + 1)
                if k < 0: break
            elif ch in '([{': prof += 1
            elif ch in ')]}':
                if prof == 0: break
                prof -= 1
            elif ch == ',' and prof == 0: partes.append(cuerpo[ini:k]); ini = k + 1
            elif ch in ';\n' and prof == 0: break
            k += 1
        partes.append(cuerpo[ini:k])
        nombres += [mm.group(1) for mm in (re.match(r'\s*([A-Za-z_$][\w$]*)', x) for x in partes) if mm]
    return nombres
locales = []
for nombre, cuerpo in funciones(sin_coment):
    # Sin el contenido de las cadenas: en «dg = val('dg')» la cadena contaba
    # como un uso, y la variable que encontró la auditoría pasaba inadvertida.
    codigo_f = re.sub(r"'(?:[^'\\\n]|\\.)*'|\"(?:[^\"\\\n]|\\.)*\"", "''", cuerpo)
    for v in set(declarados(codigo_f)):
        if len(re.findall(r'(?<![\w$.])' + re.escape(v) + r'(?![\w$])', codigo_f)) < 2:
            locales.append('%s en %s()' % (v, nombre))
afirma(not locales, 'prototipo: ninguna variable local queda sin uso: %s' % sorted(locales)[:6])

# 9. Comentarios que citan preguntas cerradas (F1-02): una pregunta retirada o
#    consolidada ya no es referencia, y una resuelta no puede seguir «sin resolver».
d05 = (RAIZ.parent / 'documentacion' / '05-decisiones-y-pendientes.md').read_text(encoding='utf-8').split('\n')
reg = {}
for l in d05[d05.index('### Registro de respuestas'):]:
    if re.match(r'\| P-\d+ \|', l):
        c_ = [x.strip() for x in l.strip().strip('|').split('|')]
        reg[c_[0]] = c_[1]
cerradas = [p for p, e in reg.items() if re.match(r'\*\*(Retirada|Consolidada)', e)]
resueltas = [p for p, e in reg.items() if e.strip() and not re.match(r'\*\*(Retirada|Consolidada|En parte)', e)]
comentarios = re.findall(r'/\*.*?\*/', scripts, re.S) + re.findall(r'(?m)//.*$', scripts) + re.findall(r'<!--.*?-->', s, re.S)
viejos = [p for p in cerradas for c_ in comentarios if re.search(re.escape(p) + r'(?!\d)', c_)]
ABIERTA = r'no está resuelta|no esta resuelta|no resuelta|sin resolver|por resolver|cuando se resuelva|mientras no se resuelva'
abiertos = [p for p in resueltas for c_ in comentarios if re.search(re.escape(p) + r'(?!\d)', c_) and re.search(ABIERTA, c_, re.I)]
afirma(not viejos, 'prototipo: ningún comentario cita una pregunta retirada o consolidada: %s' % sorted(set(viejos)))
afirma(not abiertos, 'prototipo: ningún comentario presenta como abierta una pregunta resuelta: %s' % sorted(set(abiertos)))

# 10. El artefacto conserva las metaetiquetas del teléfono y el idioma (A3-01).
a = RUTA.read_text(encoding='utf-8')
antes = a[:a.find('<title>')]
afirma(all(x in antes for x in ('name="viewport"', 'name="format-detection" content="telephone=no, date=no, address=no, email=no"',
                                'name="chrome" content="nointentdetection"', "document.documentElement.lang = 'es-MX'")),
       'artefacto: conserva viewport, format-detection y nointentdetection antes de <title>, y fija el idioma es-MX')

print('\n'.join(notas)); print()
if fallos:
    print('\n'.join(fallos)); sys.exit(1)
print('TODAS LAS PRUEBAS PASAN (%d)' % len(notas))
