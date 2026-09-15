/* ============================================
   MAIN.JS - PORTAL MODERNO SACABA 2026
   ============================================ */

var PAGE_ES = {};
var PAGE_QU = {};
var PAGE_QU_AI = null;
var pageLang = 'es';
var aiTranslating = false;
var aiFailed = false;

/* ========== TRADUCCIÓN (ES/QU) para elementos estáticos ========== */
function aiKeyFor(el, i) {
    return el.getAttribute('data-id') || ('el-' + i);
}

function applyAIPage() {
    if (!PAGE_QU_AI) return;
    document.querySelectorAll('[data-qu]').forEach(function(el, i) {
        var t = PAGE_QU_AI[aiKeyFor(el, i)];
        if (t) el.innerHTML = t;
    });
}

function translateWithAI() {
    if (aiTranslating || aiFailed) return;
    aiTranslating = true;
    var items = [];
    document.querySelectorAll('[data-qu]').forEach(function(el, i) {
        var es = el.getAttribute('data-es') || el.innerHTML;
        if (es && es.trim()) items.push({ id: aiKeyFor(el, i), text: es });
    });
    if (!items.length) { aiTranslating = false; return; }
    fetch('/api/translate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ items: items })
    }).then(function(r) {
        return r.json();
    }).then(function(data) {
        if (data && data.translations) {
            PAGE_QU_AI = data.translations;
            if (pageLang === 'qu') applyAIPage();
        } else {
            aiFailed = true;
        }
    }).catch(function() {
        aiFailed = true;
    }).then(function() {
        aiTranslating = false;
    });
}

function translatePage(lang) {
    pageLang = lang;
    document.querySelectorAll('[data-qu]').forEach(function(el) {
        if (lang === 'qu') {
            el.innerHTML = el.getAttribute('data-qu');
        } else {
            el.innerHTML = el.getAttribute('data-es') || el.innerHTML;
        }
    });
    if (lang === 'qu') {
        if (PAGE_QU_AI) {
            applyAIPage();
        } else {
            translateWithAI();
        }
    }
    var lbl = document.getElementById('pageLangLabel');
    if (lbl) lbl.textContent = lang === 'es' ? 'QU' : 'ES';
    if (typeof renderTramites === 'function') {
        renderTramites();
    }
}

function togglePageLang() {
    translatePage(pageLang === 'es' ? 'qu' : 'es');
}

/* ========== TARJETAS DE TRÁMITES (dinámicas) ========== */
var L = {
    es: { req: "Requisitos", donde: "Dónde / Ubicación", pasos: "Pasos a Seguir", ver: "Ver requisitos, pasos y ubicación", consultar: "Consultar con el Chat", sinTitulo: "Sin resultados", sinDesc: "No encontramos un trámite con ese término. Pregúntale al chatbot o intenta con: carnet, catastro, vehículo, licencia." },
    qu: { req: "Requisitokuna", donde: "Maypi / Ubicación", pasos: "Ruwanapaq Pasokuna", ver: "Requisitos, pasos nitaq ubicación qhaway", consultar: "Chatwan Tapukuy", sinTitulo: "Mana rastrariy atikunchu", sinDesc: "Chay simipi trámite mana tarikunchu. Chatbotman tapuy uta qhaway: carnet, catastro, vehículo, licencia." }
};

function tq(k) {
    return L[pageLang] ? (L[pageLang][k] || L.es[k]) : L.es[k];
}

function tramiteCardHtml(t) {
    var li = document.createElement('div');
    li.className = 'tramite-item';
    li.dataset.category = t.cat;
    li.id = t.id;
    li.style.animationDelay = '0s';

    var qu = pageLang === 'qu' && TRAMITES_QU && TRAMITES_QU[t.id];
    var n = qu ? qu.qn : t.n;
    var d = qu ? qu.qd : t.d;

    var reqs = t.req.map(function(r) { return '<li>' + escHtml(r) + '</li>'; }).join('');
    var steps = t.pasos.map(function(s) { return '<li>' + escHtml(s) + '</li>'; }).join('');
    var map = t.map ? '<div class="tramite-location"><i class="fas fa-map-marker-alt"></i><a href="' + t.map + '" target="_blank">' + (pageLang==='qu'?'Google Mapspi qhaway':'Ver ubicación en Google Maps') + '</a></div>' : '<div class="tramite-location"><i class="fas fa-map-marker-alt"></i><span>' + escHtml(t.where) + '</span></div>';

    li.innerHTML =
        '<div class="tramite-num">' + t.num + '</div>' +
        '<div class="tramite-info">' +
            '<h3><i class="' + t.icon + '"></i> ' + escHtml(n) + '</h3>' +
            '<p>' + escHtml(d) + '</p>' +
            '<div class="tramite-details">' +
                '<span><i class="fas fa-dollar-sign"></i> ' + escHtml(t.c) + '</span>' +
                '<span><i class="fas fa-clock"></i> ' + escHtml(t.t) + '</span>' +
                '<span><i class="fas fa-building"></i> ' + escHtml(t.dep) + '</span>' +
            '</div>' +
            map +
            '<div class="tramite-accordion">' +
                '<button class="accordion-btn" onclick="toggleAccordion(this)"><i class="fas fa-chevron-down"></i> ' + tq('ver') + '</button>' +
                '<div class="accordion-content"><div class="detail-grid">' +
                    '<div class="detail-col"><h4><i class="fas fa-clipboard-list"></i> ' + tq('req') + '</h4><ul>' + reqs + '</ul>' +
                        '<h4 class="d-mt"><i class="fas fa-map-marked-alt"></i> ' + tq('donde') + '</h4><p class="where-text">' + escHtml(t.where) + '</p></div>' +
                    '<div class="detail-col"><h4><i class="fas fa-list-ol"></i> ' + tq('pasos') + '</h4><ol>' + steps + '</ol>' +
                        '<div class="cost-tip"><p><i class="fas fa-info-circle"></i> ' + escHtml(t.costDetail) + '</p>' +
                        '<p><i class="fas fa-lightbulb"></i> ' + escHtml(t.consejo) + '</p></div></div>' +
                '</div></div>' +
            '</div>' +
        '</div>' +
        '<div class="tramite-action"><button class="chat-query-btn" onclick="openChatWithQuery(\'' + escAttr(t.n) + '\')"><i class="fas fa-comments"></i> ' + tq('consultar') + '</button></div>';

    return li;
}

function escHtml(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function escAttr(s) {
    return String(s).replace(/'/g, "\\'").replace(/"/g, '&quot;');
}

function currentFilter() {
    var active = document.querySelector('.filter-btn.active');
    return active ? active.dataset.filter : 'todos';
}

function renderTramites() {
    var grid = document.getElementById('tramites-grid');
    if (!grid || !window.TRAMITES_DATA) return;
    var q = (document.getElementById('tramiteSearch').value || '').toLowerCase().trim();
    var filter = currentFilter();
    grid.innerHTML = '';
    var shown = 0;
    TRAMITES_DATA.forEach(function(t) {
        var hay = (t.n + ' ' + t.d + ' ' + t.dep + ' ' + t.where + ' ' + (t.req || []).join(' ')).toLowerCase();
        if (filter !== 'todos' && t.cat !== filter) return;
        if (q && hay.indexOf(q) === -1) return;
        grid.appendChild(tramiteCardHtml(t));
        shown++;
    });
    if (!shown) {
        grid.innerHTML = '<div class="tramite-empty"><i class="fas fa-search"></i><h4>' + tq('sinTitulo') + '</h4><p>' + tq('sinDesc') + '</p></div>';
    }
}

function scrollToSection(id) {
    var target = document.getElementById(id);
    if (target) {
        var top = target.getBoundingClientRect().top + window.pageYOffset - 80;
        window.scrollTo({ top: top, behavior: 'smooth' });
    }
}

/* ========== SMOOTH SCROLL + HEADER ========== */
function initHeaderScroll() {
    var header = document.querySelector('.main-header');
    if (!header) return;
    window.addEventListener('scroll', function() {
        header.classList.toggle('scrolled', window.scrollY > 50);
    });
}

/* ========== REVEAL ========== */
function initScrollReveal() {
    var reveals = document.querySelectorAll('.reveal');
    var observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });
    reveals.forEach(function(el) { observer.observe(el); });
}

/* ========== ACCORDION ========== */
function toggleAccordion(btn) {
    var content = btn.nextElementSibling;
    var isOpen = content.classList.contains('open');
    document.querySelectorAll('.accordion-content').forEach(function(c) { c.classList.remove('open'); });
    document.querySelectorAll('.accordion-btn').forEach(function(b) { b.classList.remove('active'); });
    if (!isOpen) {
        content.classList.add('open');
        btn.classList.add('active');
    }
}

document.addEventListener('DOMContentLoaded', function() {
    /* Guardar textos originales */
    document.querySelectorAll('[data-qu]').forEach(function(el) {
        el.setAttribute('data-es', el.innerHTML);
    });

    renderTramites();

    /* Buscador */
    var search = document.getElementById('tramiteSearch');
    if (search) {
        search.addEventListener('input', renderTramites);
        search.addEventListener('keydown', function(e) { if (e.key === 'Enter') e.preventDefault(); });
    }

    /* Filtros por categoría */
    document.querySelectorAll('.filter-btn').forEach(function(btn) {
        btn.addEventListener('click', function() {
            document.querySelectorAll('.filter-btn').forEach(function(b) { b.classList.remove('active'); });
            this.classList.add('active');
            renderTramites();
        });
    });

    /* Accesos rápidos con búsqueda precargada */
    document.querySelectorAll('.quick-item[data-search]').forEach(function(item) {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            var term = this.dataset.search;
            var s = document.getElementById('tramiteSearch');
            if (s) {
                s.value = term;
                document.querySelectorAll('.filter-btn').forEach(function(b) { b.classList.remove('active'); });
                var all = document.querySelector('.filter-btn[data-filter="todos"]');
                if (all) all.classList.add('active');
                renderTramites();
            }
            scrollToSection('tramites');
        });
    });

    /* Mobile menu */
    var mobileMenuBtn = document.getElementById('mobileMenuBtn');
    var mainNav = document.querySelector('.main-nav');
    if (mobileMenuBtn && mainNav) {
        mobileMenuBtn.addEventListener('click', function() {
            var isOpen = mainNav.style.display === 'flex';
            mainNav.style.display = isOpen ? 'none' : 'flex';
            if (!isOpen) {
                mainNav.style.position = 'absolute';
                mainNav.style.top = '100%';
                mainNav.style.left = '0';
                mainNav.style.right = '0';
                mainNav.style.background = 'rgba(5,46,22,0.98)';
                mainNav.style.backdropFilter = 'blur(20px)';
                mainNav.style.flexDirection = 'column';
                mainNav.style.padding = '16px';
                mainNav.style.boxShadow = '0 8px 32px rgba(0,0,0,0.3)';
                mainNav.style.zIndex = '1000';
                mainNav.style.borderRadius = '0 0 16px 16px';
            }
        });
    }

    /* Smooth scroll nav */
    document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            scrollToSection(this.getAttribute('href').substring(1));
        });
    });

    /* Active nav on scroll */
    window.addEventListener('scroll', function() {
        var sections = document.querySelectorAll('.section, .hero-banner');
        sections.forEach(function(section) {
            var rect = section.getBoundingClientRect();
            if (rect.top <= 160 && rect.bottom >= 160) {
                var id = section.getAttribute('id');
                if (id) {
                    document.querySelectorAll('.nav-link').forEach(function(l) { l.classList.remove('active'); });
                    var link = document.querySelector('.nav-link[href="#' + id + '"]');
                    if (link) link.classList.add('active');
                }
            }
        });
    });

    initScrollReveal();
    initHeaderScroll();
});