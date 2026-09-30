/**
 * Revisión del formulario de Denuncia Ambiental · SEDEMA (DEC-153, DEC-155)
 *
 * Recibe las observaciones que deja quien revisa el formulario desde la liga
 * de revisión y las guarda en esta hoja. Hay UNA sola liga para todas las
 * personas; cada quien escribe su nombre en el formulario.
 * Instalación: revision/LEEME.md
 *
 * La liga lleva una palabra aleatoria (?revision=...) que genera esta hoja
 * con el menú Revisión → Generar liga de revisión. No está escrita en el
 * código —que es público— sino en las propiedades del script: sólo quien
 * tiene la liga puede escribir en la hoja. Generar una nueva invalida la
 * anterior.
 */

var CONFIG = {
  HOJA_OBS: 'Observaciones',
  LIGA_BASE: 'https://sedemaoficina.github.io/denuncia-ambiental/',
  ZONA: 'America/Mexico_City',
  MAX_TEXTO: 4000,
  MAX_NOMBRE: 80,
  MAX_POR_DIA: 1000,
  ESTADOS: ['Pendiente', 'En revisión', 'Para discusión', 'Atendida', 'Descartada'],
  ALFABETO: 'abcdefghjkmnpqrstuvwxyz23456789'
};

/* Columnas de Observaciones. El orden es el de la hoja; el nombre interno,
   el del JSON que manda el formulario. */
var COLS = [
  ['id', 'ID'], ['recibida', 'Recibida'], ['revisor', 'Revisor'], ['area', 'Área'],
  ['version', 'Versión'], ['paso', 'Paso'], ['pantalla', 'Pantalla'], ['seccion', 'Sección'],
  ['elemento', 'Elemento'], ['texto', 'Texto señalado'], ['tipo', 'Tipo'], ['observacion', 'Observación'],
  ['propuesta', 'Propuesta'], ['materia', 'Materia'], ['dispositivo', 'Dispositivo'],
  ['estado', 'Estado'], ['respuesta', 'Respuesta'], ['atendida_en', 'Atendida en'], ['uid', 'UID']
];

/* ================= Menú ================= */

function onOpen() {
  SpreadsheetApp.getUi().createMenu('Revisión')
    .addItem('Preparar la hoja', 'prepararHoja')
    .addItem('Generar liga de revisión', 'generarLiga')
    .addItem('Ver liga de revisión', 'verLiga')
    .addToUi();
}

/* Crea la hoja con sus encabezados, validaciones y colores. Se puede correr
   otra vez sin perder datos. */
function prepararHoja() {
  var ss = SpreadsheetApp.getActive();
  ss.setSpreadsheetTimeZone(CONFIG.ZONA);

  var obs = ss.getSheetByName(CONFIG.HOJA_OBS) || ss.insertSheet(CONFIG.HOJA_OBS);
  if (obs.getLastRow() <= 1) {            /* sin observaciones: se rehace el formato completo */
    obs.clear(); obs.clearConditionalFormatRules();
    obs.showColumns(1, obs.getMaxColumns());
    obs.getRange(1, 1, obs.getMaxRows(), obs.getMaxColumns()).clearDataValidations();
  }
  encabezado_(obs, COLS.map(function (c) { return c[1]; }));
  var anchos = [80, 130, 160, 140, 70, 45, 170, 200, 160, 260, 120, 320, 260, 110, 150, 110, 260, 90, 90];
  anchos.forEach(function (w, i) { obs.setColumnWidth(i + 1, w); });
  obs.getRange('B:B').setNumberFormat('dd/MM/yyyy HH:mm');
  obs.getRange(2, 1, obs.getMaxRows() - 1, COLS.length).setWrap(true).setVerticalAlignment('top');
  obs.hideColumns(col_('uid'));

  var cEdo = col_('estado');
  obs.getRange(2, cEdo, obs.getMaxRows() - 1, 1).setDataValidation(SpreadsheetApp.newDataValidation()
    .requireValueInList(CONFIG.ESTADOS, true).setAllowInvalid(false).build());
  var letra = columnaLetra_(cEdo);
  var colores = { 'Pendiente': '#FFF3CD', 'En revisión': '#EEF3FA', 'Para discusión': '#EEF3FA',
                  'Atendida': '#F1F8F4', 'Descartada': '#F4F5F6' };
  obs.setConditionalFormatRules(Object.keys(colores).map(function (e) {
    return SpreadsheetApp.newConditionalFormatRule()
      .whenFormulaSatisfied('=$' + letra + '2="' + e + '"')
      .setBackground(colores[e])
      .setRanges([obs.getRange(2, 1, obs.getMaxRows() - 1, COLS.length)]).build();
  }));

  var vieja = ss.getSheetByName('Revisores');
  if (vieja && vieja.getLastRow() <= 1) ss.deleteSheet(vieja);
  var sobra = ss.getSheetByName('Hoja 1') || ss.getSheetByName('Sheet1');
  if (sobra && ss.getSheets().length > 1 && sobra.getLastRow() === 0) ss.deleteSheet(sobra);

  if (!palabra_()) generarLiga();
  else aviso_('Hoja lista. La liga de revisión está en Revisión → Ver liga de revisión.');
}

/* Una sola liga para todas las personas que revisan. */
function generarLiga() {
  var ui = SpreadsheetApp.getUi();
  if (palabra_()) {
    var r = ui.alert('Generar liga nueva',
      'La liga actual dejará de funcionar y habrá que enviar la nueva a todas las personas que revisan. ¿Continuar?',
      ui.ButtonSet.YES_NO);
    if (r !== ui.Button.YES) return;
  }
  var p = '';
  for (var i = 0; i < 12; i++) p += CONFIG.ALFABETO.charAt(Math.floor(Math.random() * CONFIG.ALFABETO.length));
  PropertiesService.getScriptProperties().setProperty('PALABRA', p);
  verLiga();
}

function verLiga() {
  var p = palabra_();
  var ui = SpreadsheetApp.getUi();
  if (!p) { ui.alert('Todavía no hay liga: usa Revisión → Generar liga de revisión.'); return; }
  ui.alert('Liga de revisión', CONFIG.LIGA_BASE + '?revision=' + p +
    '\n\nEs la misma para todas las personas que revisan: cada quien escribe su nombre al abrirla.', ui.ButtonSet.OK);
}

/* ================= Web app ================= */

function doGet(e) {
  var p = (e && e.parameter) || {};
  try {
    if (p.accion === 'lista') return json_(lista_(p.palabra));
    return json_({ ok: false, error: 'accion' });
  } catch (err) {
    return json_({ ok: false, error: 'servidor' });
  }
}

function doPost(e) {
  try {
    var d = JSON.parse((e && e.postData && e.postData.contents) || '{}');
    if (d.accion === 'guardar') return json_(guardar_(d.palabra, d.obs || {}));
    return json_({ ok: false, error: 'accion' });
  } catch (err) {
    return json_({ ok: false, error: 'servidor' });
  }
}

/* ================= Lógica ================= */

function palabra_() { return PropertiesService.getScriptProperties().getProperty('PALABRA') || ''; }
function ligaValida_(p) { var v = palabra_(); return !!v && String(p || '') === v; }

function guardar_(palabra, o) {
  if (!ligaValida_(palabra)) return { ok: false, error: 'clave' };
  var nombre = String(o.revisor || '').replace(/\s+/g, ' ').trim().slice(0, CONFIG.MAX_NOMBRE);
  if (nombre.length < 3) return { ok: false, error: 'nombre' };
  if (!String(o.observacion || '').trim()) return { ok: false, error: 'vacia' };

  var lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try {
    var hoja = SpreadsheetApp.getActive().getSheetByName(CONFIG.HOJA_OBS);
    var ultima = hoja.getLastRow();
    var uid = String(o.uid || '').slice(0, 40);

    if (ultima > 1 && uid) {
      var ya = hoja.getRange(2, col_('uid'), ultima - 1, 1).createTextFinder(uid).matchEntireCell(true).findNext();
      if (ya) return { ok: true, id: hoja.getRange(ya.getRow(), col_('id')).getValue(), repetida: true };
    }
    if (ultima > 1) {
      var hoy = Utilities.formatDate(new Date(), CONFIG.ZONA, 'yyyyMMdd');
      var deHoy = hoja.getRange(2, col_('recibida'), ultima - 1, 1).getValues().filter(function (f) {
        return f[0] instanceof Date && Utilities.formatDate(f[0], CONFIG.ZONA, 'yyyyMMdd') === hoy;
      }).length;
      if (deHoy >= CONFIG.MAX_POR_DIA) return { ok: false, error: 'limite' };
    }

    var id = 'OBS-' + ('000' + ultima).slice(-4);
    var fila = {
      id: id, recibida: new Date(), revisor: nombre, area: String(o.area || '').slice(0, CONFIG.MAX_NOMBRE),
      version: o.version, paso: o.paso, pantalla: o.pantalla, seccion: o.seccion, elemento: o.elemento,
      texto: o.texto, tipo: o.tipo, observacion: o.observacion, propuesta: o.propuesta,
      materia: o.materia, dispositivo: o.dispositivo, estado: 'Pendiente', respuesta: '', atendida_en: '', uid: uid
    };
    hoja.appendRow(COLS.map(function (c) {
      var v = fila[c[0]];
      return v instanceof Date ? v : limpia_(v);
    }));
    return { ok: true, id: id };
  } finally {
    lock.releaseLock();
  }
}

/* Todas las observaciones: quienes revisan ven las de sus colegas, para no
   repetirlas. No viaja el identificador interno. */
function lista_(palabra) {
  if (!ligaValida_(palabra)) return { ok: false, error: 'clave' };
  var hoja = SpreadsheetApp.getActive().getSheetByName(CONFIG.HOJA_OBS);
  var out = [];
  if (hoja && hoja.getLastRow() > 1) {
    hoja.getRange(2, 1, hoja.getLastRow() - 1, COLS.length).getValues().forEach(function (f) {
      var o = {};
      COLS.forEach(function (c, i) { o[c[0]] = f[i] instanceof Date ? f[i].toISOString() : String(f[i]); });
      out.push({ id: o.id, creada: o.recibida, revisor: o.revisor, area: o.area, version: o.version,
                 pantalla: o.pantalla, seccion: o.seccion, texto: o.texto, tipo: o.tipo,
                 observacion: o.observacion, propuesta: o.propuesta, estado: o.estado || 'Pendiente',
                 respuesta: o.respuesta });
    });
  }
  return { ok: true, observaciones: out };
}

/* ================= Apoyo ================= */

function col_(nombre) {
  for (var i = 0; i < COLS.length; i++) if (COLS[i][0] === nombre) return i + 1;
  throw new Error('Columna desconocida: ' + nombre);
}

/* Recorta, y evita que un texto que empieza con = + - @ se lea como fórmula. */
function limpia_(v) {
  v = String(v == null ? '' : v).slice(0, CONFIG.MAX_TEXTO);
  return /^[=+\-@]/.test(v) ? "'" + v : v;
}

function encabezado_(hoja, titulos) {
  hoja.getRange(1, 1, 1, titulos.length).setValues([titulos])
    .setFontWeight('bold').setFontColor('#FFFFFF').setBackground('#9D2148').setVerticalAlignment('middle');
  hoja.setFrozenRows(1);
}

function columnaLetra_(n) {
  var s = '';
  while (n > 0) { var m = (n - 1) % 26; s = String.fromCharCode(65 + m) + s; n = Math.floor((n - 1) / 26); }
  return s;
}

function json_(o) {
  return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON);
}

function aviso_(t) {
  try { SpreadsheetApp.getActive().toast(t, 'Revisión', 8); } catch (e) { Logger.log(t); }
}
