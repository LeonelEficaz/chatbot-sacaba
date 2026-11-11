/* ============================================================
   PORTAL SACABA 2026 · Sami
   Portada, ficha dinámica, búsqueda, tema, idioma y mascota.
   ============================================================ */

(function () {
    'use strict';

    var DATA = Array.isArray(window.SACABA_TRAMITES) ? window.SACABA_TRAMITES : [];
    var CATS = window.SACABA_CATS || {};
    var BY_ID = {};
    var BY_SLUG = {};
    DATA.forEach(function (t) { BY_ID[t.id] = t; BY_SLUG[t.slug] = t; });

    var state = {
        lang: 'es',
        theme: 'light',
        cat: 'todos',
        query: '',
        current: null,
        welcomeDone: false
    };

    var TXT = {
        es: {
            inicio: 'Inicio', portal: 'Portal de trámites', buscador: 'Buscar',
            requisitos: 'Requisitos', pasos: 'Paso a paso', recomendaciones: 'Recomendaciones',
            intro: '¿De qué se trata?', costo: 'Costo', tiempo: 'Tiempo', modalidad: 'Modalidad',
            oficina: 'Dónde hacerlo', fuentes: 'Fuentes oficiales', relacionados: 'También te puede interesar',
            preguntar: 'Preguntar a Sami', imprimir: 'Imprimir', enlace: 'Copiar enlace',
            volver: 'Volver al inicio', actualizado: 'Información referencial · actualizada en 2026',
            antes: 'Antes de ir', verMapa: 'Cómo llegar', copiado: 'Enlace copiado',
            sinResultados: 'No encontramos ese trámite. Prueba con “carnet”, “multa” o “catastro”.',
            abrirFicha: 'Ver ficha y horarios', masBuscados: 'Los más buscados',
            horarios: 'Horarios de atención', abrirPagina: 'Abrir página del trámite',
            resumenQu: 'Resumen en quechua', fichaEs: 'El detalle completo está en español.',
            saludo: '¡Hola! Soy Sami, tu asistente municipal de Sacaba. Cuéntame qué necesitas, te escucho.',
            hablar: 'Hablar con Sami', buscarFicha: 'Buscar trámite'
        },
        qu: {
            inicio: 'Qallariy', portal: 'Tramitekuna', buscador: 'Maskay',
            requisitos: 'Requisitokuna', pasos: 'Imayna ruwana', recomendaciones: 'Yuyaychaykuna',
            intro: '¿Imamanta?', costo: 'Qullqi', tiempo: 'Pacha', modalidad: 'Ruway',
            oficina: 'Maypi ruwana', fuentes: 'Oficial pukyukuna', relacionados: 'Kaywan tinkisqa',
            preguntar: 'Samita tapuy', imprimir: 'Princhay', enlace: 'T’inkiyta copiay',
            volver: 'Qallariyman kutiy', actualizado: 'Qhawariy willay · 2026',
            antes: 'Manaraq riy', verMapa: 'Maypi kasqan', copiado: 'T’inkiy copiasqa',
            sinResultados: 'Chay trámite mana tarikunchu. “carnet”, “multa” utaq “catastro” tapuy.',
            abrirFicha: 'Ficha qhaway', masBuscados: 'Aswan maskasqakuna',
            horarios: 'Yanapay pachakuna', abrirPagina: 'Tramitep p’anqanta kichay',
            resumenQu: 'Runasimipi pisichay', fichaEs: 'Tukuy willakuy español simipi.',
            saludo: '¡Imaynallan! Noqaqa Sami, Sakaba Munisipyuq yanapayniyki. Imata munasqaykita niway, uyarishayki.',
            hablar: 'Samiwan rimay', buscarFicha: 'Trámite maskay'
        }
    };

    function t(key) { return (TXT[state.lang] && TXT[state.lang][key]) || TXT.es[key] || key; }

    function tituloPortal() {
        return state.lang === 'qu'
            ? 'Sami · Tramitekuna yanapaq | Sakaba Munisipyu'
            : 'Sami · Asistente de Trámites | G.A.M. Sacaba';
    }

    function esc(value) {
        return String(value == null ? '' : value)
            .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
    }

    function norm(text) {
        return String(text || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
    }

    function catName(cat) {
        var c = CATS[cat];
        if (!c) return cat;
        if (state.lang === 'qu') {
            var qu = { identidad: 'Identidad', vivienda: 'Wasi', negocio: 'Negosyo', servicios: 'Carrokuna', multas: 'Multakuna' };
            return qu[cat] || c.nombre;
        }
        return c.nombre;
    }

    /* Texto de una ficha en el idioma activo, con respaldo en espanol. */
    function campoQu(tr, campo) {
        if (state.lang === 'qu' && tr.qu && tr.qu[campo] != null) return tr.qu[campo];
        return tr[campo];
    }

    function listaQu(tr, campo) {
        var valor = campoQu(tr, campo);
        return Array.isArray(valor) ? valor : [];
    }

    /* ---------- BÚSQUEDA ---------- */
    // Mismas reglas que chatbot/tramites.py para que Sami abra la ficha aunque
    // el ciudadano no diga el nombre oficial ("mi cédula", "quiero vender mi carro").
    var DEBILES = { auto: 1, carro: 1, moto: 1, vehiculo: 1, placa: 1, casa: 1, terreno: 1,
        lote: 1, documento: 1, documentos: 1, identificacion: 1, ci: 1 };
    var GENERICAS = [
        ['multas_transito', ['multa', 'multas', 'infraccion', 'sancion']],
        ['carnet', ['documento', 'documentos', 'identificacion', 'ci']],
        ['licencia_funcionamiento', ['negocio', 'tienda', 'comercio', 'patente']],
        ['empadronamiento_predial', ['terreno', 'lote', 'inmueble', 'casa', 'propiedad']],
        ['impuesto_predial', ['impuesto', 'impuestos', 'tributo']]
    ];

    function puntajeClave(heno, clave) {
        var k = norm(clave).trim();
        if (!k) return 0;
        if (k.indexOf(' ') !== -1 || k.length <= 4) {
            return heno.indexOf(' ' + k + ' ') !== -1 ? k.length : 0;
        }
        return heno.indexOf(' ' + k) !== -1 ? k.length : 0;
    }

    function buscar(texto) {
        var q = norm(texto).trim();
        if (!q) return null;
        var heno = ' ' + q + ' ';
        var mejor = null, mejorP = 0;
        DATA.forEach(function (tr) {
            var claves = (tr.keywords || []).concat([tr.n]);
            claves.forEach(function (k) {
                if (DEBILES[norm(k).trim()]) return;
                var p = puntajeClave(heno, k);
                if (p > mejorP) { mejorP = p; mejor = tr; }
            });
        });
        if (mejor) return mejor;
        for (var i = 0; i < GENERICAS.length; i++) {
            var palabras = GENERICAS[i][1];
            for (var j = 0; j < palabras.length; j++) {
                if (puntajeClave(heno, palabras[j])) return BY_ID[GENERICAS[i][0]] || null;
            }
        }
        return null;
    }

    function filtrar() {
        var q = norm(state.query);
        return DATA.filter(function (tr) {
            if (state.cat !== 'todos' && tr.cat !== state.cat) return false;
            if (!q) return true;
            var heno = norm([tr.n, tr.resumen, tr.costo, tr.tag, (tr.keywords || []).join(' '), (tr.oficina || {}).nombre].join(' '));
            return heno.indexOf(q) !== -1;
        });
    }

    /* ---------- PORTADA ---------- */
    function renderGrid() {
        var grid = document.getElementById('tramitesGrid');
        var empty = document.getElementById('gridEmpty');
        if (!grid) return;
        var items = filtrar();
        grid.innerHTML = items.map(cardHtml).join('');
        if (empty) empty.hidden = items.length > 0;
    }

    function cardHtml(tr) {
        var nombre = campoQu(tr, 'n');
        var resumen = campoQu(tr, 'resumen');
        return '<a class="p-card" href="' + esc(tr.url) + '" data-open="' + esc(tr.id) + '" aria-label="' + esc(nombre) + '">' +
            '<div class="p-card-top"><span class="p-card-icon"><i class="fas fa-' + esc(tr.icon) + '"></i></span>' +
            '<span class="p-card-tag">' + esc(campoQu(tr, 'tag')) + '</span></div>' +
            '<h4>' + esc(nombre) + '</h4>' +
            '<p>' + esc(resumen) + '</p>' +
            '<div class="p-card-meta"><span class="cost"><i class="fas fa-coins"></i>' + esc(campoQu(tr, 'costo')) + '</span>' +
            '<span><i class="fas fa-clock"></i>' + esc(campoQu(tr, 'tiempo')) + '</span></div>' +
            '<span class="p-card-go" aria-hidden="true">' + t('abrirFicha') + ' <i class="fas fa-arrow-right"></i></span>' +
            '</a>';
    }

    /* ---------- FICHA ---------- */
    function show(idOrSlug, options) {
        var tr = BY_ID[idOrSlug] || BY_SLUG[idOrSlug];
        if (!tr) return false;
        state.current = tr;

        var home = document.getElementById('homeView');
        var art = document.getElementById('articleView');
        if (!art || !home) return false;
        home.hidden = true;
        art.hidden = false;
        art.innerHTML = articleHtml(tr);
        document.getElementById('crumbActual').textContent = campoQu(tr, 'n');
        document.title = campoQu(tr, 'n') + ' · Sami Sacaba';

        var url = tr.url;
        if (!options || !options.silent) {
            try { history.pushState({ tramite: tr.id }, '', url); } catch (e) {}
        }
        window.scrollTo({ top: 0, behavior: 'smooth' });
        return true;
    }

    function home(options) {
        state.current = null;
        var homeEl = document.getElementById('homeView');
        var art = document.getElementById('articleView');
        if (homeEl) homeEl.hidden = false;
        if (art) { art.hidden = true; art.innerHTML = ''; }
        var crumb = document.getElementById('crumbActual');
        if (crumb) crumb.textContent = t('portal');
        document.title = tituloPortal();
        if (!options || !options.silent) {
            try { history.pushState({ tramite: null }, '', '/#/inicio'); } catch (e) {}
        }
        if (options && options.scroll) {
            var target = document.getElementById(options.scroll);
            if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }

    function articleHtml(tr) {
        var nombre = campoQu(tr, 'n');
        var resumen = campoQu(tr, 'resumen');
        var cat = CATS[tr.cat] || {};

        var requisitos = listaQu(tr, 'requisitos').map(function (r) {
            return '<li>' + esc(r) + '</li>';
        }).join('');

        var pasos = listaQu(tr, 'pasos').map(function (p, i) {
            return '<div class="art-step"><span class="art-step-num">' + (i + 1) + '</span>' +
                '<div><h3>' + esc(p.t) + '</h3><p>' + esc(p.d) + '</p></div></div>';
        }).join('');

        var tips = listaQu(tr, 'recomendaciones').map(function (r) {
            return '<li><i class="fas fa-lightbulb"></i><span>' + esc(r) + '</span></li>';
        }).join('');

        var intro = listaQu(tr, 'intro').map(function (p) { return '<p>' + esc(p) + '</p>'; }).join('');

        var fuentes = (tr.fuente || []).map(function (f) {
            return '<a href="' + esc(f.url) + '" target="_blank" rel="noopener"><i class="fas fa-arrow-up-right-from-square"></i>' +
                esc(f.nombre) + '</a>';
        }).join('');

        var relacionados = (tr.relacionados || []).map(function (rid) {
            var r = BY_ID[rid];
            if (!r) return '';
            return '<button data-open="' + esc(r.id) + '"><i class="fas fa-' + esc(r.icon) + '"></i>' +
                esc(campoQu(r, 'n')) + '<span class="go"><i class="fas fa-chevron-right"></i></span></button>';
        }).join('');

        // En quechua la ficha completa ya esta traducida: el resumen aparte sobra.
        var quBox = (tr.qu && state.lang !== 'qu') ? '<div class="art-qu"><span>' + esc(t('resumenQu')) + '</span><p>' +
            esc(tr.qu.resumen) + '</p></div>' : '';

        var horariosDatos = listaQu(tr, 'horarios');
        var horarios = horariosDatos.map(function (h) {
            return '<div class="art-hours-row"><div><b>' + esc(h.dias) + '</b><span>' + esc(h.nota || '') + '</span></div>' +
                '<strong>' + esc(h.horas) + '</strong></div>';
        }).join('');
        var notaHorario = campoQu(tr, 'horario_nota');
        var horarioNota = notaHorario ? '<p class="art-hours-note"><i class="fas fa-circle-info"></i><span>' +
            esc(notaHorario) + '</span></p>' : '';

        var oficina = tr.oficina || {};
        if (state.lang === 'qu' && tr.qu && tr.qu.oficina) {
            oficina = Object.assign({}, oficina, tr.qu.oficina);
        }
        var mapa = oficina.mapa ? '<a class="art-map-btn" href="' + esc(oficina.mapa) + '" target="_blank" rel="noopener">' +
            '<i class="fas fa-map-location-dot"></i> ' + esc(t('verMapa')) + '</a>' : '';

        return '' +
            '<header class="art-hero">' +
                '<div class="art-icon-float"><i class="fas fa-' + esc(tr.icon) + '"></i></div>' +
                '<div class="art-top"><span class="art-cat"><i class="fas fa-' + esc(cat.icono || 'folder') + '"></i> ' +
                    esc(catName(tr.cat)) + '</span><span class="art-tag">' + esc(campoQu(tr, 'tag')) + '</span></div>' +
                '<h1>' + esc(nombre) + '</h1>' +
                '<p class="art-summary">' + esc(resumen) + '</p>' +
                '<div class="art-icons">' +
                    '<span><i class="fas fa-coins"></i>' + esc(campoQu(tr, 'costo')) + '</span>' +
                    '<span><i class="fas fa-clock"></i>' + esc(campoQu(tr, 'tiempo')) + '</span>' +
                    '<span><i class="fas fa-location-dot"></i>' + esc(oficina.nombre || '') + '</span>' +
                '</div>' +
            '</header>' +

            '<div class="art-layout">' +
                '<div class="art-body">' +
                    '<section class="art-block art-intro">' +
                        '<h2><i class="fas fa-circle-info"></i>' + esc(t('intro')) + '</h2>' +
                        intro + quBox +
                    '</section>' +
                    '<section class="art-block">' +
                        '<h2><i class="fas fa-clipboard-list"></i>' + esc(t('requisitos')) + '</h2>' +
                        '<ul class="art-req">' + requisitos + '</ul>' +
                    '</section>' +
                    '<section class="art-block">' +
                        '<h2><i class="fas fa-list-ol"></i>' + esc(t('pasos')) + '</h2>' +
                        '<div class="art-steps">' + pasos + '</div>' +
                    '</section>' +
                    '<section class="art-block">' +
                        '<h2><i class="fas fa-lightbulb"></i>' + esc(t('recomendaciones')) + '</h2>' +
                        '<ul class="art-tips">' + tips + '</ul>' +
                    '</section>' +
                '</div>' +

                '<aside class="art-side">' +
                    '<div class="art-side-card">' +
                        '<h3>' + esc(t('costo')) + '</h3>' +
                        '<div class="art-price">' + esc(campoQu(tr, 'costo')) + '</div>' +
                        '<p class="art-price-note">' + esc(campoQu(tr, 'costo_detalle')) + '</p>' +
                        '<div class="art-facts">' +
                            '<div><span>' + esc(t('tiempo')) + '</span><strong>' + esc(campoQu(tr, 'tiempo')) + '</strong></div>' +
                            '<div><span>' + esc(t('modalidad')) + '</span><strong>' + esc(campoQu(tr, 'modalidad')) + '</strong></div>' +
                        '</div>' +
                        '<button class="p-btn p-btn-primary" style="width:100%;margin-top:14px" data-ask="' +
                            esc(nombre) + '"><i class="fas fa-comments"></i> ' + esc(t('preguntar')) + '</button>' +
                        '<a class="art-map-btn" href="' + esc(tr.url) + '"><i class="fas fa-up-right-from-square"></i> ' +
                            esc(t('abrirPagina')) + '</a>' +
                    '</div>' +
                    '<div class="art-side-card art-office">' +
                        '<h3>' + esc(t('oficina')) + '</h3>' +
                        '<div class="art-office-name">' + esc(oficina.nombre || '') + '</div>' +
                        '<p><i class="fas fa-location-dot"></i><span>' + esc(oficina.direccion || '') + '</span></p>' +
                        '<p><i class="fas fa-clock"></i><span>' + esc(oficina.horario || '') + '</span></p>' +
                        '<p><i class="fas fa-phone"></i><span>' + esc(oficina.telefono || '') + '</span></p>' +
                        mapa +
                    '</div>' +
                    '<div class="art-side-card art-hours">' +
                        '<h3><i class="fas fa-clock" style="color:var(--g-600);margin-right:6px"></i>' + esc(t('horarios')) + '</h3>' +
                        '<div class="art-hours-list">' + horarios + '</div>' +
                        horarioNota +
                    '</div>' +
                    '<div class="art-side-card">' +
                        '<h3>' + esc(t('relacionados')) + '</h3>' +
                        '<div class="art-rel">' + relacionados + '</div>' +
                    '</div>' +
                    '<div class="art-side-card art-sources">' +
                        '<h3>' + esc(t('fuentes')) + '</h3>' + fuentes +
                    '</div>' +
                '</aside>' +
            '</div>' +

            '<div class="art-foot">' +
                '<span><i class="fas fa-shield-halved"></i>' + esc(t('actualizado')) + '</span>' +
                '<span><i class="fas fa-circle-check"></i>' + esc(campoQu(tr, 'modalidad')) + ' · ' + esc(campoQu(tr, 'tiempo')) + '</span>' +
                '<button class="p-tool" data-nav="inicio"><i class="fas fa-arrow-left"></i> ' + esc(t('volver')) + '</button>' +
            '</div>';
    }

    /* ---------- TOAST ---------- */
    function toast(msg) {
        var el = document.getElementById('pToast');
        if (!el) {
            el = document.createElement('div');
            el.id = 'pToast';
            el.style.cssText = 'position:fixed;left:50%;bottom:28px;transform:translate(-50%,20px);z-index:500;' +
                'background:#063b24;color:#fff;padding:11px 18px;border-radius:12px;font-size:12px;font-weight:600;' +
                'box-shadow:0 18px 40px -18px rgba(0,0,0,.6);opacity:0;transition:.25s;pointer-events:none;';
            document.body.appendChild(el);
        }
        el.textContent = msg;
        requestAnimationFrame(function () {
            el.style.opacity = '1';
            el.style.transform = 'translate(-50%,0)';
        });
        clearTimeout(el._timer);
        el._timer = setTimeout(function () {
            el.style.opacity = '0';
            el.style.transform = 'translate(-50%,20px)';
        }, 2200);
    }

    /* ---------- MASCOTA / VOZ ---------- */
    function mascots() {
        return [document.getElementById('mascotMini'), document.getElementById('mascotBig')];
    }
    function setMascotTalking(on) {
        mascots().forEach(function (m) {
            if (m) m.classList.toggle('is-talking', !!on);
        });
    }
    window.sacabaMascotTalking = setMascotTalking;

    window.SacabaSpeak = function (text) {
        if (typeof window.sacabaSpeak === 'function') {
            window.sacabaSpeak(text, state.lang);
        }
    };

    function initVoiceToggle() {
        var btn = document.getElementById('btnVoice');
        if (!btn) return;
        var saved = localStorage.getItem('sacaba_voz');
        var on = saved !== 'off';
        function apply() {
            btn.classList.toggle('is-off', !on);
            btn.setAttribute('aria-pressed', on ? 'true' : 'false');
            btn.innerHTML = '<i class="fas fa-' + (on ? 'volume-high' : 'volume-xmark') + '"></i>';
            localStorage.setItem('sacaba_voz', on ? 'on' : 'off');
            if (typeof window.sacabaSetVoice === 'function') window.sacabaSetVoice(on);
        }
        btn.addEventListener('click', function () {
            on = !on;
            apply();
            if (!on && typeof window.sacabaStopSpeaking === 'function') window.sacabaStopSpeaking();
            if (on) toast('Voz de Sami activada');
        });
        apply();
    }

    /* ---------- IDIOMA ---------- */
    /* ---------- TEXTOS ESTATICOS ES <-> QU ---------- */
    var QU_UI = {
        'Inicio': 'Qallariy',
        'Trámites': 'Tramitekuna',
        'Multas': 'Multakuna',
        'Institución': 'Munisipyu',
        'Funcionarios': 'Funcionariokuna',
        'En línea · 24/7': 'Kawsachkan · 24/7',
        'Asistente municipal de Sacaba': 'Sakaba munisipyuq yanapaq',
        'Prueba:': 'Yachaqay:',
        '“Quiero sacar mi carnet”': '“Carnetyta horqoyta munani”',
        'Portal de trámites': 'Tramitekuna',
        'Información oficial': 'Chiqa willay',
        'Voz y audio': 'Rimay nitaq audio',
        'Imprimir': 'Princhay',
        'Enlace': 'T’inkiy',
        'Copiar enlace': 'T’inkiyta copiay',
        'Nuevo asistente ciudadano': 'Musuq runa yanapaq',
        '¿Qué trámite': '¿Ima trámite',
        'necesitas hoy?': 'kunan munanki?',
        'Pregúntale a Sami en español o quechua. Mientras conversas, aquí verás la ficha completa con requisitos, costos, pasos y oficinas.':
            'Samita tapuy español utaq quechuapi. Rimashaspa, kaypi hunt’asqa fichata qhawanki: requisitokuna, qullqikuna, ruwanakuna nitaq oficinas.',
        'Buscar': 'Maskay',
        'Licencia': 'Licencia',
        'Catastro': 'Catastro',
        'Negocio': 'Negocio',
        'trámites explicados': 'tramitekuna willasqa',
        'idiomas: ES / QU': 'simikuna: ES / QU',
        'asistencia en línea': 'yanapay internetpi',
        'canales de pago': 'pagana ñankuna',
        'Los más buscados': 'Aswan maskasqakuna',
        '20 fichas': '20 fichas',
        'detalladas': 'willasqa',
        'Pago': 'Pago',
        'con QR': 'QRwan',
        'Atención': 'Yanapay',
        'Trámites que la gente consulta': 'Runakunaq tapukuynin tramitekuna',
        'Fichas completas, con lenguaje claro y datos oficiales.': 'Hunt’asqa fichakuna, sut’i simipi, chiqa willaywan.',
        'Todos': 'Tukuy',
        'Vivienda': 'Wasi',
        'Negocios': 'Negocio',
        'Vehículos': 'Carrokuna',
        'Pagos y multas': 'Pagokuna nitaq multakuna',
        'Paga tu multa sin filas': 'Multaykita mana filapi pagay',
        'Con la boleta o ficha del policía puedes pagar en bancos habilitados o escanear el QR desde tu banca móvil. También puedes pagar la ITV y las multas municipales.':
            'Policíaq boletanwan banco hunt’asqakunapi pagay utaq banca móvilmanta QRta escaneay. ITV nitaq munisipyu multakunatapas pagay atinki.',
        'Multas de tránsito': 'Tránsito multakuna',
        'Municipales': 'Munisipyu multakuna',
        'Horario de atención': 'Yanapay pacha',
        'Contacto': 'Tinkuy',
        'Portal oficial': 'Kamachiq portal',
        'Habla en español y quechua': 'Español nitaq quechuapi riman',
        'Soy': 'Noqa',
        'tu guía en Sacaba.': 'Sakabapi pusaqniyki.',
        'Cuéntame qué necesitas y te muestro la ficha completa: requisitos, costos, pasos, recomendaciones y la oficina exacta. También puedo leerte la respuesta en voz alta.':
            'Imata munasqaykita willaway; hunt’asqa fichata qhawachiyki: requisitokuna, qullqikuna, ruwanakuna, yuyaychaykuna nitaq chiqa oficina. Kutichiyta uyarinaykipaqpas atini.',
        'Empezar a conversar': 'Rimayta qallariy',
        'Escuchar saludo': 'Napaykuta uyariy',
        'Multas QR': 'Multakuna QR',
        'Saltar al contenido': 'Willayman riy',
        'Gobierno Autónomo Municipal': 'Munisipyu Kamachiq',
        'Nueva conversación': 'Musuq rimay',
        'o activa el audífono y di “Sami, …”': 'utaq uyarinata kichaspa “Sami, …” niy',
        'Ruta': 'Ñan',
        'No encontramos ese trámite. Prueba con “carnet”, “multa” o “catastro”, o pregúntale a Sami.':
            'Chay trámite mana tarikunchu. “carnet”, “multa” utaq “catastro” tapuy, utaq Samita tapuway.',
        'Banca móvil · QR': 'Móvil banca · QR',
        'Lun-Vie 8:00-12:00 / 14:00-18:00 · Sáb 8:00-12:00':
            'Killachaw-Chaskachaw 8:00-12:00 / 14:00-18:00 · Sábadu 8:00-12:00',
        'Palacio Consistorial': 'Munisipyu wasi',
        'Gobierno Autónomo Municipal de Sacaba': 'Sakaba Munisipyu',
        'Orientación ciudadana digital · Gestión 2026': 'Runakunapaq digital yanapay · 2026',
        'Información referencial elaborada a partir del portal oficial': 'Kay yachayqa oficial portalmanta hurqusqa',
        ', SEGIP, Policía Boliviana y RUAT. Confirma montos y requisitos en ventanilla antes de iniciar tu trámite.':
            ', SEGIP, Bolivia Policía nitaq RUATmanta. Manaraq qallarispa, ventanillapi qullqita nitaq requisitokunata chiqanchay.'
    };
    var QU_PH = {
        'Ej.: carnet, licencia, multas de tránsito, catastro…': 'Ahina: carnet, licencia, tránsito multakuna, catastro…',
        'Filtrar por nombre o palabra clave…': 'Sutinwan utaq simiwan suysuy…',
        'Escribe o habla tu consulta...': 'Tapukuyniykita qillqay utaq rimay…'
    };

    function translateStatic(lang) {
        var skip = { SCRIPT: 1, STYLE: 1, NOSCRIPT: 1, TEXTAREA: 1, OPTION: 1 };
        var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
            acceptNode: function (node) {
                var parent = node.parentNode;
                if (!parent || skip[parent.nodeName]) return NodeFilter.FILTER_REJECT;
                if (parent.closest && parent.closest('#articleView, #cw-msgs, #tramitesGrid, #cw-opts')) {
                    return NodeFilter.FILTER_REJECT;
                }
                return NodeFilter.FILTER_ACCEPT;
            }
        });
        var node;
        while ((node = walker.nextNode())) {
            if (node.__es === undefined) node.__es = node.nodeValue;
            var raw = node.__es;
            var key = raw.trim();
            if (!key) continue;
            var val = lang === 'qu' ? QU_UI[key] : null;
            node.nodeValue = val ? raw.replace(key, val) : raw;
        }
        document.querySelectorAll('input[placeholder]').forEach(function (el) {
            if (el.__ph === undefined) el.__ph = el.placeholder;
            var qu = QU_PH[el.__ph];
            el.placeholder = (lang === 'qu' && qu) ? qu : el.__ph;
        });
    }

    function applyLanguage(lang, opts) {
        opts = opts || {};
        state.lang = lang;
        document.documentElement.lang = lang === 'qu' ? 'qu' : 'es';
        var lbl = document.getElementById('pageLangLabel');
        if (lbl) lbl.textContent = lang === 'es' ? 'QU' : 'ES';
        localStorage.setItem('sacaba_lang', lang);
        translateStatic(lang);
        if (!state.current) document.title = tituloPortal();
        if (!opts.quiet && typeof window.sacabaSetLang === 'function') window.sacabaSetLang(lang);
        var crumb = document.getElementById('crumbActual');
        if (crumb && !state.current) crumb.textContent = t('portal');
        renderGrid();
        if (state.current) {
            var art = document.getElementById('articleView');
            if (art) art.innerHTML = articleHtml(state.current);
            if (crumb) crumb.textContent = campoQu(state.current, 'n');
        }
    }

    window.togglePageLang = function () {
        applyLanguage(state.lang === 'es' ? 'qu' : 'es');
    };

    /* API para que el chat cambie toda la pagina, incluso solo. */
    window.SacabaSetLang = function (lang) {
        if (lang !== 'es' && lang !== 'qu') return;
        if (state.lang === lang) return;
        applyLanguage(lang);
    };
    window.SacabaApplyPageLanguage = function (lang, opts) {
        if (lang !== 'es' && lang !== 'qu') return;
        applyLanguage(lang, opts || {});
    };

    /* ---------- TEMA ---------- */
    function initTheme() {
        var saved = localStorage.getItem('sacaba_theme');
        if (!saved) {
            saved = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
        }
        state.theme = saved;
        document.documentElement.setAttribute('data-theme', saved);
        var btn = document.getElementById('btnTheme');
        function icon() {
            if (btn) btn.innerHTML = '<i class="fas fa-' + (state.theme === 'dark' ? 'sun' : 'moon') + '"></i>';
        }
        icon();
        if (btn) btn.addEventListener('click', function () {
            state.theme = state.theme === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', state.theme);
            localStorage.setItem('sacaba_theme', state.theme);
            icon();
        });
    }

    /* ---------- NAVEGACIÓN ---------- */
    function initNav() {
        document.addEventListener('click', function (e) {
            var nav = e.target.closest('[data-nav]');
            if (nav) {
                var dest = nav.getAttribute('data-nav');
                if (dest === 'inicio') {
                    home({ scroll: null });
                    window.scrollTo({ top: 0, behavior: 'smooth' });
                } else if (dest === 'tramites') {
                    home({ scroll: 'seccionTramites' });
                } else if (dest === 'multas') {
                    show('multas_transito');
                } else if (dest === 'institucion') {
                    home({ scroll: 'seccionInstitucion' });
                }
                setActiveNav(dest);
                return;
            }

            var open = e.target.closest('[data-open]');
            if (open) {
                if (open.tagName === 'A' && open.getAttribute('href')) {
                    // Ctrl/Cmd/Shift conserva el enlace real: abrir en otra pestaña.
                    if (e.ctrlKey || e.metaKey || e.shiftKey) return;
                    e.preventDefault();
                }
                show(open.getAttribute('data-open'));
                setActiveNav('tramites');
                return;
            }

            var ask = e.target.closest('[data-ask]');
            if (ask) {
                var q = ask.getAttribute('data-ask');
                if (typeof window.openChatWithQuery === 'function') window.openChatWithQuery(q);
                return;
            }
        });

        document.querySelectorAll('.p-nav-link').forEach(function (btn) {
            btn.addEventListener('click', function () {
                setActiveNav(this.getAttribute('data-nav'));
            });
        });
    }

    function setActiveNav(dest) {
        document.querySelectorAll('.p-nav-link').forEach(function (b) {
            b.classList.toggle('active', b.getAttribute('data-nav') === dest);
        });
    }

    /* ---------- HERRAMIENTAS ---------- */
    function initTools() {
        var print = document.getElementById('btnPrint');
        if (print) print.addEventListener('click', function () { window.print(); });

        var share = document.getElementById('btnShare');
        if (share) share.addEventListener('click', function () {
            var url = state.current ? location.origin + state.current.url : location.href;
            if (navigator.clipboard && navigator.clipboard.writeText) {
                navigator.clipboard.writeText(url).then(function () { toast(t('copiado')); });
            } else {
                toast(url);
            }
        });
    }

    /* ---------- BIENVENIDA ---------- */
    function initWelcome() {
        var overlay = document.getElementById('welcomeOverlay');
        if (!overlay) return;
        function close() {
            overlay.classList.add('is-hidden');
            state.welcomeDone = true;
            document.body.style.overflow = '';
            var input = document.getElementById('cw-in');
            if (input) setTimeout(function () { input.focus(); }, 200);
        }
        var start = document.getElementById('welcomeStart');
        var listen = document.getElementById('welcomeListen');
        var closeBtn = document.getElementById('welcomeClose');
        function terminar() {
            if (!overlay.classList.contains('is-hidden')) close();
            // Este clic tambien vale para pedir el micro: Sami escucha sin que
            // el ciudadano tenga que buscar el boton del micromono.
            if (typeof window.SacabaPrepararMicro === 'function') window.SacabaPrepararMicro();
            if (typeof window.SacabaSkipPresentation === 'function') window.SacabaSkipPresentation();
        }
        function comenzar() {
            close();
            // El permiso del microfono necesita el gesto del clic; despues de la
            // presentacion Sami empieza a escuchar sola.
            if (typeof window.SacabaPrepararMicro === 'function') window.SacabaPrepararMicro();
            if (typeof window.SacabaStartPresentation === 'function') {
                window.SacabaStartPresentation();
            } else if (localStorage.getItem('sacaba_voz') !== 'off') {
                window.SacabaSpeak(t('saludo'));
            }
        }

        /* Al entrar se intenta encender el microfono sin esperar un clic. Si el
           navegador ya tiene el permiso concedido escucha de inmediato; si aun
           no lo tiene, se abre el aviso del navegador. Cuando el navegador exige
           un gesto o el ciudadano bloquea el microfono, la bienvenida se queda
           visible y el boton "Empezar a conversar" hace lo mismo. */
        var arrancado = false;
        function arrancarConMicro() {
            if (arrancado || overlay.classList.contains('is-hidden')) return;
            if (typeof window.SacabaPrepararMicro !== 'function') return;
            arrancado = true;
            window.SacabaPrepararMicro().then(function (ok) {
                if (!ok) { arrancado = false; return; }
                close();
                if (typeof window.SacabaSkipPresentation === 'function') {
                    window.SacabaSkipPresentation();
                }
            });
        }
        function intentarAuto() {
            if (!overlay || overlay.classList.contains('is-hidden')) return;
            if (navigator.permissions && navigator.permissions.query) {
                navigator.permissions.query({ name: 'microphone' }).then(function (permiso) {
                    if (permiso.state !== 'denied') arrancarConMicro();
                }).catch(function () { arrancarConMicro(); });
            } else {
                arrancarConMicro();
            }
        }
        setTimeout(intentarAuto, 500);
        if (start) start.addEventListener('click', comenzar);
        if (listen) listen.addEventListener('click', function (e) { e.stopPropagation(); comenzar(); });
        if (closeBtn) closeBtn.addEventListener('click', terminar);
        overlay.addEventListener('click', function (e) { if (e.target === overlay) terminar(); });
        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape' && !overlay.classList.contains('is-hidden')) terminar();
        });
        document.body.style.overflow = 'hidden';
    }

    /* ---------- BUSCADORES ---------- */
    function initSearch() {
        var form = document.getElementById('heroSearchForm');
        var heroInput = document.getElementById('heroSearch');
        if (form && heroInput) {
            form.addEventListener('submit', function (e) {
                e.preventDefault();
                var q = heroInput.value.trim();
                if (!q) return;
                var tr = buscar(q);
                if (tr) {
                    show(tr.id);
                    setActiveNav('tramites');
                } else {
                    state.query = q;
                    var g = document.getElementById('gridSearch');
                    if (g) g.value = q;
                    renderGrid();
                    home({ scroll: 'seccionTramites' });
                    toast(t('sinResultados'));
                }
            });
            heroInput.addEventListener('keydown', function (e) {
                if (e.key === 'Escape') { heroInput.value = ''; }
            });
        }

        var gridSearch = document.getElementById('gridSearch');
        if (gridSearch) gridSearch.addEventListener('input', function () {
            state.query = this.value;
            renderGrid();
        });

        document.querySelectorAll('#catTabs .p-tab').forEach(function (tab) {
            tab.addEventListener('click', function () {
                document.querySelectorAll('#catTabs .p-tab').forEach(function (x) { x.classList.remove('active'); });
                this.classList.add('active');
                state.cat = this.getAttribute('data-cat');
                renderGrid();
            });
        });
    }

    /* ---------- CHAT → PANEL ---------- */
    window.SacabaPanel = {
        show: function (id) { return show(id); },
        home: function () { home(); },
        search: function (text) {
            var tr = buscar(text);
            if (tr) { show(tr.id); setActiveNav('tramites'); return tr.id; }
            return null;
        },
        fromQuery: function (text, backendId) {
            if (backendId && BY_ID[backendId]) {
                show(backendId);
                setActiveNav('tramites');
                return backendId;
            }
            return this.search(text);
        }
    };

    /* ---------- RUTAS ---------- */
    function initRouter() {
        function fromHash() {
            var byPath = location.pathname.match(/^\/tramite\/([a-z0-9-]+)\/?$/i);
            if (byPath && BY_SLUG[byPath[1]]) { show(BY_SLUG[byPath[1]].id, { silent: true }); return; }
            var h = location.hash || '';
            var m = h.match(/#\/tramite\/([a-z0-9-]+)/i);
            if (m && BY_SLUG[m[1]]) { show(BY_SLUG[m[1]].id, { silent: true }); return; }
            home({ silent: true });
        }
        window.addEventListener('popstate', fromHash);
        if (location.hash) fromHash();
    }

    /* ---------- PROGRESO ---------- */
    function initProgress() {
        var bar = document.getElementById('scroll-progress');
        if (!bar) return;
        window.addEventListener('scroll', function () {
            var h = document.documentElement.scrollHeight - window.innerHeight;
            bar.style.width = (h > 0 ? (window.scrollY / h) * 100 : 0) + '%';
        }, { passive: true });
    }

    /* ---------- RESET CHAT ---------- */
    function initReset() {
        var btn = document.getElementById('btnResetChat');
        if (!btn) return;
        btn.addEventListener('click', function () {
            if (typeof window.sacabaResetChat === 'function') window.sacabaResetChat();
            home();
            toast('Conversación reiniciada');
        });
    }

    document.addEventListener('DOMContentLoaded', function () {
        initTheme();
        initNav();
        initTools();
        initSearch();
        initVoiceToggle();
        initWelcome();
        initRouter();
        initProgress();
        initReset();
        applyLanguage(localStorage.getItem('sacaba_lang') || 'es');
        renderGrid();
        if (!location.hash || location.hash === '#/inicio') home({ silent: true });

        var pregunta = new URLSearchParams(location.search).get('pregunta');
        if (pregunta) {
            var overlay = document.getElementById('welcomeOverlay');
            if (overlay) overlay.classList.add('is-hidden');
            document.body.style.overflow = '';
            if (typeof window.openChatWithQuery === 'function') window.openChatWithQuery(pregunta);
            history.replaceState(null, '', location.pathname + location.hash);
        }
    });
})();
