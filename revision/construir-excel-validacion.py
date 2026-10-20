# -*- coding: utf-8 -*-
"""Excel de validación de observaciones para la DGIVA (formulario de denuncia ambiental)."""
import io
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule

GUINDA, DORADO, GRIS = '9D2148', 'B28E5C', '55585A'
ROSA, CREMA, BLANCO = 'F7F1F3', 'FBF6EC', 'FFFFFF'
TIT, CUE = 'Cabin', 'Roboto'
fino = Side(style='thin', color='D9D9D9')
borde = Border(left=fino, right=fino, top=fino, bottom=fino)

# ---------- Datos ----------
ctrl = [l.split('\t') for l in io.open(__import__('os').path.join(__import__('os').path.dirname(__file__), 'control-observaciones-2026-10-19.tsv'), encoding='utf-8').read().rstrip('\n').split('\n')]
assert len(ctrl) == 32

DG, CJ = ('Dirección General', 'DGIVA'), ('Juan Camilo Escobar Londoño', 'COJUMIVA')
obs = [  # (revisor, área, pantalla, lo que se pidió, decisión)
 (('Benjamín', 'DGIVA'), 'Portada', 'Cambiar «En persona» por «Presencial».', 'Aceptada'),
 (DG, 'Portada', 'Usar «derribo», término de la norma, en lugar de «tala».', 'Aceptada'),
 (DG, 'Paso 1', 'Quitar «olores» de la tarjeta de emisiones: no hay marco jurídico para atenderlos.', 'Aceptada'),
 (DG, 'Paso 1', 'Quitar «olores», «anuncios», «de un negocio» y «luz excesiva» de la tarjeta de ruido; limitarla a fuentes fijas en materia de industria.', 'En discusión'),
 (DG, 'Paso 1', 'Quitar «ruido excesivo» de la tarjeta de vehículo contaminante.', 'Aceptada'),
 (DG, 'Portada', 'Cambiar «en unos diez minutos» por «solo te lleva 10 minutos».', 'Aceptada con ajuste'),
 (DG, 'Portada', 'No hablar de «oficinas» sino de unidades administrativas.', 'Aceptada con ajuste'),
 (DG, 'Portada', 'Publicar domicilio, horario y teléfono de la DGIVA.', 'Aceptada'),
 (DG, 'Paso 1', 'Quitar los globos metálicos (algunos tienen autorización de la DGEIRA) y listar bolsas, popotes, vasos, charolas, platos, hisopos y bastoncillos.', 'Aceptada con ajuste'),
 (DG, 'Paso 1', 'Usar los términos de la norma: «residuos de la construcción» en lugar de «cascajo» o «escombro».', 'Aceptada con ajuste'),
 (DG, 'Portada', 'Quitar «ni vivir en el lugar»: en ruido la medición se hace en el punto de denuncia.', 'Aceptada con ajuste'),
 (DG, 'Portada', 'Señalar que los datos están protegidos por la Ley General de Protección de Datos Personales.', 'Aceptada con ajuste'),
 (DG, 'Paso 1', 'Redactar «Una obra realiza un mal manejo de sus residuos de la construcción o demolición».', 'Aceptada con ajuste'),
 (DG, 'Paso 2', 'Cambiar «Calle o vialidad» por «Calle o avenida».', 'Aceptada'),
 (DG, 'Paso 3', 'Ejemplos de hechos: humo, ruido, descarga, derrame, derribo, poda, tiro de residuos.', 'Aceptada'),
 (DG, 'Paso 3', 'Permitir dar la fecha sin precisar el día exacto.', 'En discusión'),
 (CJ, 'Portada', 'No prometer un tiempo de llenado («diez minutos»).', 'Aceptada'),
 (CJ, 'Portada', 'Sustituir «oficina» por «Dirección General» o «unidad competente».', 'Aceptada con ajuste'),
 (CJ, 'Portada', 'Reescribir la pregunta de la denuncia anónima en «usted» e incluir el envío del informe de acciones por correo.', 'Aceptada con ajuste'),
 (CJ, 'Portada', 'Ampliar los ejemplos de casos de otra autoridad: arbolado en vía pública, interior de vivienda, condominios y unidades habitacionales.', 'En discusión'),
 (CJ, 'Portada', 'Revisar la pregunta «¿Puedo dejarla a medias?» (sin propuesta).', 'Aceptada'),
 (CJ, 'Portada', 'Reescribir «¿Puedo dejarla a medias?» en «usted» y advertir que el avance se pierde al borrar el historial.', 'Aceptada con ajuste'),
 (CJ, 'Portada', 'No generar un folio nuevo (ya existen SAD, SUAC, SAC y AP) y mantener la denuncia ciudadana por correo.', 'Aceptada con ajuste'),
 (CJ, 'Paso 3', 'Revisar la lista de tipos de establecimiento: algunos giros no son competencia de la CIVASU (por ejemplo, «antro»).', 'En discusión'),
 (CJ, 'Paso 3', 'Cuestiona la utilidad de la pregunta sobre el responsable: más del 70 % no la contesta.', 'Aceptada con ajuste'),
 (CJ, 'Paso 3', 'Eliminar la razón social: es redundante y obliga a consultar documentos de un tercero.', 'Aceptada'),
 (CJ, 'Paso 3', 'Eliminar la pregunta sobre permisos; plantea el caso de un restaurante en Los Dinamos.', 'En discusión'),
 (('Anónimo', 'Zona protección'), 'Paso 1', 'Registro de prueba sin contenido («Mo» / «No»).', 'Descartada'),
 (DG, 'Paso 3', 'Responsable: dejar un campo abierto después de elegir persona, empresa o autoridad.', 'Aceptada con ajuste'),
 (DG, 'Paso 3', 'Marcar como opcional, o eliminar, «Gestiones previas».', 'Aceptada'),
 (DG, 'Paso 5', 'Cambiar «pueda escribirte» por «pueda ponerse en contacto contigo».', 'Aceptada'),
 (DG, 'Paso 5', 'En ruido, preguntar si acepta que la medición se haga en su domicilio.', 'Aceptada'),
]
assert len(obs) == 32

preguntas = [
 ('OBS-0004', 'Instancia para olores, anuncios y luz', '¿La PAOT es la instancia correcta para orientar las denuncias de malos olores y de anuncios o luz excesiva?',
  'Esos supuestos salieron de la tarjeta de ruido y ahora aparecen en «Mi caso no está en la lista» remitiendo a la PAOT.'),
 ('OBS-0027', 'Caso de Los Dinamos', '¿Coinciden en turnar a la DGCORENADR el caso del restaurante en Los Dinamos? ¿Quién atiende el uso de leña sin legal procedencia?',
  'Con el cruce espacial del formulario, el punto cae en suelo de conservación (La Magdalena Contreras).'),
 ('OBS-0024', 'Giros fuera de competencia', '¿Qué giros de la lista «Tipo de establecimiento» quedan fuera de la competencia de la CIVASU?',
  'Lista actual: obra en construcción o demolición; taller mecánico, hojalatería o pintura; industria o fábrica; bodega o almacén; restaurante, fonda o cocina económica; bar, cantina, salón de fiestas o antro; tienda, abarrotes u otro comercio; panadería o tortillería; carnicería, pollería o pescadería; lavandería o tintorería; gasolinera o estación de servicio; estacionamiento o pensión; hospital, clínica, consultorio o laboratorio; escuela, oficina o edificio público; banco de materiales, mina o tiro de tierra; centro de acopio o reciclaje; vivero, granja, establo o rastro; espectáculo público, feria o evento; otro.'),
 ('OBS-0016', 'Fecha aproximada', '¿Basta con registrar que la persona no conoce la fecha, o se necesita una fecha aproximada (mes y año)?',
  'Desde DEC-206 el formulario pregunta «¿Conoces la fecha en que ocurrió o inició?»; con «No» no se pide fecha y ya no se registra una aproximada, que era lo que pedía la observación.'),
 ('OBS-0020', 'Casos de otra autoridad', '¿Qué autoridad atiende el arbolado en vía pública y los hechos dentro de viviendas, condominios o unidades habitacionales? ¿Qué casos de arbolado sí atiende la Secretaría?',
  'El formulario tiene la tarjeta «Daño a arbolado urbano» como competencia de la Secretaría; en 2026, el 40.7 % de las denuncias de arbolado se declararon incompetencia.'),
 ('P-09', 'Datos de la DGCORENADR', 'Domicilio, horario de atención y teléfono de la Coordinación de Inspección Ambiental en Suelo de Conservación y Áreas Naturales Protegidas (DGCORENADR).',
  'La tarjeta «Presencial» los muestra todavía como «por confirmar».'),
 ('P-07', 'Plazo para informar', '¿En cuántos días hábiles se responde a quien consulta el estado de su denuncia?',
  'El Manual Administrativo fija los plazos del procedimiento, pero no el de informar a la persona denunciante.'),
]

# ---------- Utilidades ----------
def f(size=10, bold=False, color='000000', italic=False, titulo=False):
    return Font(name=TIT if titulo else CUE, size=size, bold=bold, color=color, italic=italic)
def relleno(c): return PatternFill('solid', start_color=c, end_color=c)
def ajusta(ws, carta=True, horizontal=True):
    ws.page_setup.paperSize = ws.PAPERSIZE_LETTER
    ws.page_setup.orientation = 'landscape' if horizontal else 'portrait'
    ws.page_setup.fitToWidth, ws.page_setup.fitToHeight = 1, 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_margins.left = ws.page_margins.right = 0.6
    ws.page_margins.top = ws.page_margins.bottom = 0.7
    ws.oddFooter.center.text = 'Página &P de &N'
    ws.oddFooter.center.size, ws.oddFooter.center.color = 8, GRIS
    ws.oddHeader.right.text = 'SEDEMA · Oficina de la Secretaría'
    ws.oddHeader.right.size, ws.oddHeader.right.color = 8, GRIS
def encabezado(ws, fila, titulos, anchos):
    for i, (t, a) in enumerate(zip(titulos, anchos), 1):
        c = ws.cell(row=fila, column=i, value=t)
        c.font = f(10, True, BLANCO, titulo=True); c.fill = relleno(GUINDA)
        c.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True); c.border = borde
        ws.column_dimensions[c.column_letter].width = a
    ws.row_dimensions[fila].height = 32
def banda(ws, titulo, sub, ncols):
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=ncols)
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=ncols)
    a = ws.cell(row=1, column=1, value=titulo); a.font = f(15, True, GUINDA, titulo=True)
    b = ws.cell(row=2, column=1, value=sub); b.font = f(10, False, GRIS, italic=True)
    ws.row_dimensions[1].height = 26
    for col in range(1, ncols + 1):
        ws.cell(row=3, column=col).border = Border(top=Side(style='medium', color=GUINDA))

wb = Workbook()

# ---------- Hoja 1: Resumen ----------
r = wb.active; r.title = 'Resumen'
r.sheet_view.showGridLines = False
banda(r, 'Validación de observaciones · Formulario de Denuncia Ambiental',
      'Secretaría del Medio Ambiente · Oficina de la Secretaría · 19 de octubre de 2026', 4)
r.column_dimensions['A'].width = 34; r.column_dimensions['B'].width = 16
r.column_dimensions['C'].width = 34; r.column_dimensions['D'].width = 16
datos = [
 ('Versión del formulario', 'Versión 19 · Validación DGIVA'),
 ('Liga de la versión publicada', 'https://sedemaoficina.github.io/denuncia-ambiental/'),
 ('Observaciones registradas', '32 (19 de la Dirección General, 11 de la COJUMIVA, 1 nominal y 1 de prueba)'),
 ('Periodo de revisión', 'Del 2 al 19 de octubre de 2026'),
]
fila = 5
for k, v in datos:
    r.cell(row=fila, column=1, value=k).font = f(10, True, GRIS)
    r.merge_cells(start_row=fila, start_column=2, end_row=fila, end_column=4)
    c = r.cell(row=fila, column=2, value=v); c.font = f(10)
    if v.startswith('http'): c.hyperlink = v; c.font = f(10, color=GUINDA)
    fila += 1

fila += 1
r.cell(row=fila, column=1, value='Decisión de la Secretaría').font = f(11, True, GUINDA, titulo=True)
r.cell(row=fila, column=3, value='Estado en la hoja de revisión').font = f(11, True, GUINDA, titulo=True)
fila += 1
for col, t in ((1, 'Decisión'), (2, 'Observaciones'), (3, 'Estado'), (4, 'Observaciones')):
    c = r.cell(row=fila, column=col, value=t); c.font = f(10, True, BLANCO, titulo=True); c.fill = relleno(GUINDA)
    c.alignment = Alignment(horizontal='center'); c.border = borde
ini = fila + 1
decisiones = ['Aceptada', 'Aceptada con ajuste', 'En discusión', 'Descartada']
estados = ['Atendida', 'Para discusión', 'En revisión', 'Descartada']
for i in range(4):
    fl = ini + i
    for col, t, rango in ((1, decisiones[i], "Observaciones!$F$6:$F$37"), (3, estados[i], "Observaciones!$I$6:$I$37")):
        a = r.cell(row=fl, column=col, value=t); a.font = f(10); a.border = borde
        b = r.cell(row=fl, column=col + 1, value='=COUNTIF(%s,%s)' % (rango, a.coordinate))
        b.font = f(10); b.alignment = Alignment(horizontal='center'); b.border = borde
        if i % 2: a.fill = b.fill = relleno(ROSA)
tot = ini + 4
for col in (1, 3):
    a = r.cell(row=tot, column=col, value='Total'); a.font = f(10, True); a.border = borde
    b = r.cell(row=tot, column=col + 1, value='=SUM(%s%d:%s%d)' % (chr(64 + col + 1), ini, chr(64 + col + 1), ini + 3))
    b.font = f(10, True); b.alignment = Alignment(horizontal='center'); b.border = borde

fila = tot + 2
r.cell(row=fila, column=1, value='Qué se pide a la DGIVA').font = f(11, True, GUINDA, titulo=True)
pasos = [
 '1. En la hoja «Observaciones», revisar en cada renglón la decisión y cómo quedó el formulario.',
 '2. Llenar las dos columnas en color crema: «Validación DGIVA» (lista: Conforme / No conforme / Con comentarios) y «Comentario DGIVA».',
 '3. En la hoja «Preguntas DGIVA», escribir la respuesta de cada pregunta en la columna en color crema.',
 '4. Devolver el archivo a la Oficina de la Secretaría. Con las respuestas se emite la siguiente versión y se prepara el acta de validación.',
]
for p in pasos:
    fila += 1
    r.merge_cells(start_row=fila, start_column=1, end_row=fila, end_column=4)
    c = r.cell(row=fila, column=1, value=p); c.font = f(10); c.alignment = Alignment(wrap_text=True, vertical='top')
    r.row_dimensions[fila].height = 28
fila += 2
r.merge_cells(start_row=fila, start_column=1, end_row=fila, end_column=4)
n = r.cell(row=fila, column=1, value='Nota: el formulario conserva el trato de «tú» en todas sus pantallas; de las propuestas redactadas en «usted» se incorporó el contenido. '
       'El identificador de la denuncia se presenta como «número de registro» para no confundirlo con las numeraciones internas de la DGIVA.')
n.font = f(8, color=GRIS, italic=True); n.alignment = Alignment(wrap_text=True, vertical='top'); r.row_dimensions[fila].height = 36
ajusta(r, horizontal=False)

# ---------- Hoja 2: Observaciones ----------
o = wb.create_sheet('Observaciones')
o.sheet_view.showGridLines = False
cols = ['ID', 'Revisor', 'Área', 'Pantalla', 'Lo que se pidió', 'Decisión', 'Cómo quedó en el formulario', 'Versión', 'Estado en la hoja', 'Validación DGIVA', 'Comentario DGIVA']
anchos = [10, 20, 12, 10, 42, 15, 62, 14, 14, 16, 34]
banda(o, 'Observaciones de la revisión y su atención', 'Tabla 1. Observaciones registradas en la hoja de revisión, decisión de la Secretaría y texto vigente en la versión 15.', len(cols))
encabezado(o, 5, cols, anchos)
for i, ((rev, area), pant, pidio, dec) in enumerate(obs):
    fl = 6 + i
    est, resp, dec_n = ctrl[i]
    vals = ['OBS-%04d' % (i + 1), rev, area, pant, pidio, dec, resp, dec_n or '—', est, None, None]
    for j, v in enumerate(vals, 1):
        c = o.cell(row=fl, column=j, value=v); c.font = f(9); c.border = borde
        c.alignment = Alignment(wrap_text=True, vertical='top', horizontal='center' if j in (1, 3, 4, 6, 8, 9) else 'left')
        if j >= 10: c.fill = relleno(CREMA)
        elif i % 2: c.fill = relleno(ROSA)
    o.cell(row=fl, column=1).font = f(9, True, GUINDA)
    o.row_dimensions[fl].height = max(30, 13 * (len(resp) // 78 + 1))
dv = DataValidation(type='list', formula1='"Conforme,No conforme,Con comentarios"', allow_blank=True)
dv.error, dv.errorTitle = 'Elige una opción de la lista.', 'Validación DGIVA'
o.add_data_validation(dv); dv.add('J6:J37')
for txt, col in (('"En discusión"', 'FFF3CD'), ('"Descartada"', 'EEEEEE')):
    o.conditional_formatting.add('F6:F37', FormulaRule(formula=['$F6=%s' % txt], fill=relleno(col)))
fn = o.cell(row=39, column=1, value='Fuente: hoja «Revisión · Formulario de Denuncia Ambiental» (modo revisión del formulario) y documento 05 «Decisiones y pendientes», DEC-188 a DEC-210. '
            'Nota: las columnas en color crema son para llenado de la DGIVA.')
o.merge_cells('A39:K39'); fn.font = f(8, color=GRIS, italic=True); fn.alignment = Alignment(wrap_text=True); o.row_dimensions[39].height = 24
o.freeze_panes = 'B6'
o.auto_filter.ref = 'A5:K37'
o.print_title_rows = '5:5'
ajusta(o)

# ---------- Hoja 3: Preguntas DGIVA ----------
p = wb.create_sheet('Preguntas DGIVA')
p.sheet_view.showGridLines = False
cols = ['No.', 'Referencia', 'Tema', 'Pregunta', 'Contexto', 'Respuesta DGIVA']
anchos = [6, 12, 22, 52, 58, 46]
banda(p, 'Preguntas para la DGIVA', 'Tabla 2. Información que la Dirección General debe confirmar para cerrar la validación.', len(cols))
encabezado(p, 5, cols, anchos)
for i, (ref, tema, preg, ctx) in enumerate(preguntas):
    fl = 6 + i
    for j, v in enumerate([i + 1, ref, tema, preg, ctx, None], 1):
        c = p.cell(row=fl, column=j, value=v); c.font = f(9, j == 4); c.border = borde
        c.alignment = Alignment(wrap_text=True, vertical='top', horizontal='center' if j <= 2 else 'left')
        if j == 6: c.fill = relleno(CREMA)
        elif i % 2: c.fill = relleno(ROSA)
    p.row_dimensions[fl].height = max(48, 13 * (len(ctx) // 70 + 1))
fn = p.cell(row=6 + len(preguntas) + 1, column=1, value='Nota: P-07 y P-09 son preguntas abiertas del documento 05 del proyecto; las demás derivan de observaciones de la revisión. La columna en color crema es para llenado de la DGIVA.')
p.merge_cells(start_row=fn.row, start_column=1, end_row=fn.row, end_column=6)
fn.font = f(8, color=GRIS, italic=True); fn.alignment = Alignment(wrap_text=True); p.row_dimensions[fn.row].height = 24
p.freeze_panes = 'A6'
p.print_title_rows = '5:5'
ajusta(p)

wb.save(__import__('os').path.join(__import__('os').path.dirname(__file__), 'Validacion-observaciones-DGIVA-v5.xlsx'))
print('ok')
