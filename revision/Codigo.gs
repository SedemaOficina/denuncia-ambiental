/**
 * Revisión del formulario de Denuncia Ambiental · SEDEMA (DEC-153)
 *
 * Recibe las observaciones que deja quien revisa el formulario con una liga
 * ?revision=CLAVE y las guarda en esta hoja. Instalación: revision/LEEME.md
 *
 * Hojas:
 *   Observaciones  una fila por observación; Estado, Respuesta y Atendida en
 *                  los llena la Oficina de la Secretaría.
 *   Revisores      una fila por persona: su clave, nombre, área y liga.
 */

var CONFIG = {
  HOJA_OBS: 'Observaciones',
  HOJA_REV: 'Revisores',
  LIGA_BASE: 'https://sedemaoficina.github.io/denuncia-ambiental/',
  ZONA: 'America/Mexico_City',
  MAX_TEXTO: 4000,
  MAX_POR_DIA: 300,
  ESTADOS: ['Pendiente', 'En revisión', 'Para discusión', 'Atendida', 'Descartada'],
  ALFABETO: 'ABCDEFGHJKMNPQRSTUVWXYZ23456789'
};

/* Columnas de Observaciones. El orden es el de la hoja; el nombre interno,
   el del JSON que manda el formulario. */
var COLS = [
  ['id', 'ID'], ['recibida', 'Recibida'], ['clave', 'Clave'], ['revisor', 'Revisor'], ['area', 'Área'],
  ['version', 'Versión'], ['paso', 'Paso'], ['pantalla', 'Pantalla'], ['seccion', 'Sección'],
  ['elemento', 'Elemento'], ['texto', 'Texto señalado'], ['tipo', 'Tipo'], ['observacion', 'Observación'],
  ['propuesta', 'Propuesta'], ['materia', 'Materia'], ['dispositivo', 'Dispositivo'],
  ['estado', 'Estado'], ['respuesta', 'Respuesta'], ['atendida_en', 'Atendida en'], ['uid', 'UID']
];
var COLS_REV = ['Clave', 'Nombre', 'Área', 'Activa', 'Ve todas', 'Liga'];

/* ================= Menú ================= */

function onOpen() {
  SpreadsheetApp.getUi().createMenu('Revisión')
    .addItem('Preparar la hoja', 'prepararHoja')
    .addItem('Agregar revisor', 'agregarRevisor')
    .addToUi();
}

/* Crea las dos hojas con sus encabezados, validaciones y colores. Se puede
   correr otra vez sin perder datos. */
function prepararHoja() {
  var ss = SpreadsheetApp.getActive();
  ss.setSpreadsheetTimeZone(CONFIG.ZONA);

  var obs = ss.getSheetByName(CONFIG.HOJA_OBS) || ss.insertSheet(CONFIG.HOJA_OBS);
  encabezado_(obs, COLS.map(function (c) { return c[1]; }));
  var anchos = [80, 130, 90, 150, 110, 70, 45, 170, 200, 160, 260, 120, 320, 260, 110, 150, 110, 260, 90, 90];
  anchos.forEach(function (w, i) { obs.setColumnWidth(i + 1, w); });
  obs.getRange('B:B').setNumberFormat('dd/MM/yyyy HH:mm');
  obs.getRange(2, 1, obs.getMaxRows() - 1, COLS.length).setWrap(true).setVerticalAlignment('top');
  obs.hideColumns(col_('uid'));

  var cEdo = col_('estado');
  var rEdo = obs.getRange(2, cEdo, obs.getMaxRows() - 1, 1);
  rEdo.setDataValidation(SpreadsheetApp.newDataValidation()
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

  var rev = ss.getSheetByName(CONFIG.HOJA_REV) || ss.insertSheet(CONFIG.HOJA_REV);
  encabezado_(rev, COLS_REV);
  [110, 220, 160, 70, 80, 420].forEach(function (w, i) { rev.setColumnWidth(i + 1, w); });
  var siNo = SpreadsheetApp.newDataValidation().requireValueInList(['Sí', 'No'], true).build();
  rev.getRange(2, 4, rev.getMaxRows() - 1, 2).setDataValidation(siNo);

  var sobra = ss.getSheetByName('Hoja 1') || ss.getSheetByName('Sheet1');
  if (sobra && ss.getSheets().length > 2 && sobra.getLastRow() === 0) ss.deleteSheet(sobra);
  aviso_('Hoja lista. Agrega a cada persona con Revisión → Agregar revisor.');
}

/* Pide nombre y área, genera la clave y deja la liga lista para enviar. */
function agregarRevisor() {
  var ui = SpreadsheetApp.getUi();
  var n = ui.prompt('Agregar revisor', 'Nombre de la persona:', ui.ButtonSet.OK_CANCEL);
  if (n.getSelectedButton() !== ui.Button.OK || !n.getResponseText().trim()) return;
  var a = ui.prompt('Agregar revisor', 'Área (por ejemplo, DGIVA · Dirección de Inspección):', ui.ButtonSet.OK_CANCEL);
  if (a.getSelectedButton() !== ui.Button.OK) return;
  var t = ui.alert('Agregar revisor', '¿Puede ver las observaciones de todas las personas?', ui.ButtonSet.YES_NO);

  var hoja = SpreadsheetApp.getActive().getSheetByName(CONFIG.HOJA_REV);
  if (!hoja) { prepararHoja(); hoja = SpreadsheetApp.getActive().getSheetByName(CONFIG.HOJA_REV); }
  var existentes = hoja.getLastRow() > 1 ? hoja.getRange(2, 1, hoja.getLastRow() - 1, 1).getValues().map(function (r) { return String(r[0]); }) : [];
  var clave;
  do { clave = generarClave_(); } while (existentes.indexOf(clave) >= 0);
  var liga = CONFIG.LIGA_BASE + '?revision=' + clave;
  hoja.appendRow([clave, limpia_(n.getResponseText().trim()), limpia_(a.getResponseText().trim()), 'Sí',
                  t === ui.Button.YES ? 'Sí' : 'No', liga]);
  ui.alert('Liga de revisión', n.getResponseText().trim() + ':\n\n' + liga +
    '\n\nEnvíala sólo a esa persona. Para retirarle el acceso, cambia «Activa» a «No».', ui.ButtonSet.OK);
}

/* ================= Web app ================= */

function doGet(e) {
  var p = (e && e.parameter) || {};
  try {
    if (p.accion === 'lista') return json_(lista_(p.clave));
    return json_({ ok: false, error: 'accion' });
  } catch (err) {
    return json_({ ok: false, error: 'servidor' });
  }
}

function doPost(e) {
  try {
    var d = JSON.parse((e && e.postData && e.postData.contents) || '{}');
    if (d.accion === 'guardar') return json_(guardar_(d.clave, d.obs || {}));
    return json_({ ok: false, error: 'accion' });
  } catch (err) {
    return json_({ ok: false, error: 'servidor' });
  }
}

/* ================= Lógica ================= */

function revisor_(clave) {
  clave = String(clave || '').trim().toUpperCase();
  if (!/^[A-Z0-9-]{4,40}$/.test(clave)) return null;
  var hoja = SpreadsheetApp.getActive().getSheetByName(CONFIG.HOJA_REV);
  if (!hoja || hoja.getLastRow() < 2) return null;
  var filas = hoja.getRange(2, 1, hoja.getLastRow() - 1, 5).getValues();
  for (var i = 0; i < filas.length; i++) {
    var f = filas[i];
    if (String(f[0]).trim().toUpperCase() === clave && String(f[3]) === 'Sí') {
      return { clave: clave, nombre: String(f[1]), area: String(f[2]), veTodas: String(f[4]) === 'Sí' };
    }
  }
  return null;
}

function guardar_(clave, o) {
  var r = revisor_(clave);
  if (!r) return { ok: false, error: 'clave' };
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
      var datos = hoja.getRange(2, 1, ultima - 1, col_('clave')).getValues();
      var deHoy = datos.filter(function (f) {
        return f[col_('clave') - 1] === r.clave && f[1] instanceof Date &&
          Utilities.formatDate(f[1], CONFIG.ZONA, 'yyyyMMdd') === hoy;
      }).length;
      if (deHoy >= CONFIG.MAX_POR_DIA) return { ok: false, error: 'limite' };
    }

    var id = 'OBS-' + ('000' + ultima).slice(-4);
    var fila = {
      id: id, recibida: new Date(), clave: r.clave, revisor: r.nombre, area: r.area,
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

function lista_(clave) {
  var r = revisor_(clave);
  if (!r) return { ok: false, error: 'clave' };
  var hoja = SpreadsheetApp.getActive().getSheetByName(CONFIG.HOJA_OBS);
  var out = [];
  if (hoja && hoja.getLastRow() > 1) {
    var filas = hoja.getRange(2, 1, hoja.getLastRow() - 1, COLS.length).getValues();
    filas.forEach(function (f) {
      var o = {};
      COLS.forEach(function (c, i) { o[c[0]] = f[i] instanceof Date ? f[i].toISOString() : String(f[i]); });
      if (r.veTodas || o.clave === r.clave) {
        out.push({ id: o.id, creada: o.recibida, revisor: o.revisor, version: o.version, pantalla: o.pantalla,
                   seccion: o.seccion, texto: o.texto, tipo: o.tipo, observacion: o.observacion,
                   propuesta: o.propuesta, estado: o.estado || 'Pendiente', respuesta: o.respuesta });
      }
    });
  }
  return { ok: true, revisor: { nombre: r.nombre, area: r.area, veTodas: r.veTodas }, observaciones: out };
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

function generarClave_() {
  var c = '';
  for (var i = 0; i < 8; i++) {
    c += CONFIG.ALFABETO.charAt(Math.floor(Math.random() * CONFIG.ALFABETO.length));
    if (i === 3) c += '-';
  }
  return c;
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
