# Importaciones necesarias
import base64
import os
from pathlib import Path
import threading
import webbrowser

from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify

# Importar funciones del motor del chatbot
from chatbot.engine import (
    LANGUAGES, detect_language, get_ai_resp, is_ai_available,
    translate_page, transcribe_audio, search_tramites, get_search_suggestions,
    get_office_location, search_offices, get_all_offices, get_directions,
    get_nearby_places, generate_map_embed, geocode_address, reverse_geocode,
    search_nearby_osm, NOMINATIM_URL,
    translate_word, search_quechua_dictionary, get_quechua_phrases, learn_quechua_word,
    QUECHUA_LOCAL_DB,
    gemini_chat, gemini_translate, gemini_quechua_tutor, gemini_analyze_tramite,
    is_gemini_available, get_gemini_status, GEMINI_MODEL
)

# Configuración de la aplicación
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')

# Crear aplicación Flask
app = Flask(
    __name__,
    template_folder=str(BASE_DIR / 'templates'),
    static_folder=str(BASE_DIR / 'static'),
)
app.secret_key = 'chatbot-sacaba-2026'

# Configuración del servidor
DEFAULT_LANGUAGE = 'es'  # Idioma por defecto: español
HOST = '127.0.0.1'       # Dirección del servidor
PORT = 5000              # Puerto del servidor


def _open_browser() -> None:
    webbrowser.open(f'http://{HOST}:{PORT}')


def run_app(open_browser: bool = True) -> None:
    if open_browser:
        threading.Timer(1.0, _open_browser).start()

    app.run(debug=False, host=HOST, port=PORT, use_reloader=False)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({'error': 'Cuerpo de la solicitud invalido: se esperaba JSON.'}), 400

    message = data.get('message')
    if message is None:
        return jsonify({'error': 'Falta el campo obligatorio "message".'}), 400
    if not isinstance(message, str):
        return jsonify({'error': 'El campo "message" debe ser texto.'}), 400

    language = data.get('language', DEFAULT_LANGUAGE)
    if not isinstance(language, str) or language not in LANGUAGES:
        language = detect_language(message)

    response = get_ai_resp(message.strip(), language)

    return jsonify({'response': response, 'options': [], 'language': language})


@app.route('/audio-to-text', methods=['POST'])
def audio_to_text():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({'error': 'Cuerpo invalido.'}), 400

    audio_b64 = data.get('audio')
    if not audio_b64:
        return jsonify({'error': 'Falta el campo "audio".'}), 400

    language = data.get('language', 'es')

    try:
        audio_bytes = base64.b64decode(audio_b64)
        text = transcribe_audio(audio_bytes, language)
        return jsonify({'text': text})
    except Exception as e:
        return jsonify({'error': f'Error al procesar audio: {str(e)}'}), 500


@app.route('/language', methods=['POST'])
def language():
    data = request.get_json(silent=True)
    if not isinstance(data, dict) or 'language' not in data:
        return jsonify({'error': 'Falta el campo obligatorio "language".'}), 400

    lang = data.get('language')
    if lang not in LANGUAGES:
        return jsonify({'error': 'Idioma no soportado. Idiomas disponibles: es, qu.'}), 400

    return jsonify({'language': lang})


@app.route('/api/ai-status')
def ai_status():
    return jsonify({'ai': is_ai_available()})


@app.route('/api/translate', methods=['POST'])
def translate():
    data = request.get_json(silent=True)
    if not isinstance(data, dict) or not isinstance(data.get('items'), list) or not data['items']:
        return jsonify({'error': 'Se esperaba {"items": [{"text": "..."}]}.'}), 400

    items = []
    for it in data['items']:
        if isinstance(it, dict) and isinstance(it.get('text'), str) and it['text'].strip():
            items.append((str(it.get('id', 'el-' + str(len(items)))), it['text']))

    if not items:
        return jsonify({'error': 'No se recibieron textos para traducir.'}), 400
    if len(items) > 500:
        return jsonify({'error': 'Demasiados textos para traducir (maximo 500).'}), 400

    translations = translate_page(items)
    if translations is None:
        return jsonify({'error': 'La API de IA no esta disponible en este momento.'}), 503

    return jsonify({'translations': translations})


@app.route('/api/search', methods=['GET', 'POST'])
def search():
    """Busqueda avanzada de tramites con filtros opcionales.

    GET params:
        q: texto libre
        min_price: precio minimo
        max_price: precio maximo
        max_days: tiempo maximo en dias
        department: departamento
        category: categoria
        lang: idioma (es/qu)

    POST JSON:
        {"q": "...", "min_price": 0, "max_price": 100, ...}
    """
    if request.method == 'POST':
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return jsonify({'error': 'Cuerpo JSON invalido.'}), 400
        query = data.get('q', data.get('query'))
        min_price = data.get('min_price')
        max_price = data.get('max_price')
        max_days = data.get('max_days')
        department = data.get('department')
        category = data.get('category')
        lang = data.get('language', data.get('lang', 'es'))
    else:
        query = request.args.get('q', request.args.get('query'))
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        max_days = request.args.get('max_days', type=int)
        department = request.args.get('department')
        category = request.args.get('category')
        lang = request.args.get('language', request.args.get('lang', 'es'))

    if lang not in LANGUAGES:
        lang = 'es'

    if min_price is not None and min_price < 0:
        min_price = 0
    if max_price is not None and max_price < 0:
        max_price = None
    if max_days is not None and max_days < 0:
        max_days = None

    results = search_tramites(
        query=query,
        min_price=min_price,
        max_price=max_price,
        max_days=max_days,
        department=department,
        category=category,
        lang=lang
    )

    return jsonify(results)


@app.route('/api/search/suggestions')
def search_suggestions():
    """Retorna sugerencias de busqueda para el usuario."""
    return jsonify(get_search_suggestions())


# =====================================================================
# OPENSTREETMAP / NOMINATIM API (100% GRATUITA)
# =====================================================================

@app.route('/api/maps/info')
def maps_info():
    """Retorna información sobre la API de mapas utilizada."""
    return jsonify({
        'provider': 'OpenStreetMap + Nominatim',
        'status': '100% gratuito',
        'api_key_required': False,
        'tiles_url': 'https://tile.openstreetmap.org',
        'nominatim_url': NOMINATIM_URL,
        'usage_policy': 'https://operations.osmfoundation.org/policies/nominatim/',
    })


@app.route('/api/maps/offices')
def maps_offices():
    """Retorna todas las oficinas municipales con sus coordenadas."""
    offices = get_all_offices()
    result = []
    for key, office in offices.items():
        result.append({
            'key': key,
            'name': office['name'],
            'address': office['address'],
            'lat': office['lat'],
            'lng': office['lng'],
            'phone': office.get('phone', ''),
            'hours': office.get('hours', ''),
            'map_url': f"https://www.openstreetmap.org/?mlat={office['lat']}&mlon={office['lng']}&zoom=17",
            'description': office.get('description', ''),
        })
    return jsonify({'offices': result, 'total': len(result)})


@app.route('/api/maps/office/<office_key>')
def maps_office(office_key):
    """Retorna información de una oficina específica."""
    office = get_office_location(office_key)
    if not office:
        return jsonify({'error': f'Oficina "{office_key}" no encontrada.'}), 404
    return jsonify({
        'key': office_key,
        'name': office['name'],
        'address': office['address'],
        'lat': office['lat'],
        'lng': office['lng'],
        'phone': office.get('phone', ''),
        'hours': office.get('hours', ''),
        'map_url': f"https://www.openstreetmap.org/?mlat={office['lat']}&mlon={office['lng']}&zoom=17",
        'description': office.get('description', ''),
    })


@app.route('/api/maps/search')
def maps_search():
    """Busca oficinas por nombre o descripción."""
    query = request.args.get('q', request.args.get('query'))
    results = search_offices(query)
    return jsonify({
        'results': results,
        'total': len(results),
        'query': query,
    })


@app.route('/api/maps/directions/<office_key>')
def maps_directions(office_key):
    """Genera URL de direcciones hacia una oficina usando OpenStreetMap.

    Params opcionales:
        from_lat: latitud de origen
        from_lng: longitud de origen
    """
    from_lat = request.args.get('from_lat', type=float)
    from_lng = request.args.get('from_lng', type=float)

    if from_lat is None or from_lng is None:
        office = get_office_location(office_key)
        if not office:
            return jsonify({'error': f'Oficina "{office_key}" no encontrada.'}), 404
        return jsonify({
            'office': office['name'],
            'address': office['address'],
            'map_url': f"https://www.openstreetmap.org/?mlat={office['lat']}&mlon={office['lng']}&zoom=17",
            'lat': office['lat'],
            'lng': office['lng'],
            'message': 'Proporcione from_lat y from_lng para direcciones desde su ubicación.',
        })

    result = get_directions(from_lat, from_lng, office_key)
    if not result:
        return jsonify({'error': f'Oficina "{office_key}" no encontrada.'}), 404
    return jsonify(result)


@app.route('/api/maps/nearby')
def maps_nearby():
    """Busca oficinas cercanas a una ubicación."""
    lat = request.args.get('lat', type=float)
    lng = request.args.get('lng', type=float)
    radius = request.args.get('radius', 2000, type=float)

    if lat is None or lng is None:
        return jsonify({'error': 'Se requieren parámetros lat y lng.'}), 400

    results = get_nearby_places(lat, lng, radius)
    return jsonify({
        'results': results,
        'total': len(results),
        'search_center': {'lat': lat, 'lng': lng},
        'radius': radius,
    })


@app.route('/api/maps/embed/<office_key>')
def maps_embed(office_key):
    """Retorna código HTML para embeber un mapa de OpenStreetMap."""
    zoom = request.args.get('zoom', 17, type=int)
    result = generate_map_embed(office_key, zoom)
    if not result:
        return jsonify({'error': f'Oficina "{office_key}" no encontrada.'}), 404
    return jsonify(result)


@app.route('/api/maps/geocode')
def maps_geocode():
    """Convierte una dirección a coordenadas usando Nominatim."""
    address = request.args.get('q', request.args.get('address'))
    if not address:
        return jsonify({'error': 'Se requiere parámetro q (dirección).'}), 400

    result = geocode_address(address)
    if not result:
        return jsonify({'error': 'No se encontraron coordenadas para esa dirección.'}), 404
    return jsonify(result)


@app.route('/api/maps/reverse')
def maps_reverse():
    """Convierte coordenadas a dirección usando Nominatim."""
    lat = request.args.get('lat', type=float)
    lng = request.args.get('lng', type=float)

    if lat is None or lng is None:
        return jsonify({'error': 'Se requieren parámetros lat y lng.'}), 400

    result = reverse_geocode(lat, lng)
    if not result:
        return jsonify({'error': 'No se pudo obtener la dirección.'}), 404
    return jsonify(result)


@app.route('/api/maps/overpass')
def maps_overpass():
    """Busca lugares cercanos usando Overpass API de OpenStreetMap."""
    lat = request.args.get('lat', type=float)
    lng = request.args.get('lng', type=float)
    radius = request.args.get('radius', 1000, type=int)
    query = request.args.get('q', '')

    if lat is None or lng is None:
        return jsonify({'error': 'Se requieren parámetros lat y lng.'}), 400

    results = search_nearby_osm(lat, lng, query, radius)
    return jsonify({
        'results': results,
        'total': len(results),
        'search_center': {'lat': lat, 'lng': lng},
        'radius': radius,
    })


# =====================================================================
# GLOSBLE DICTIONARY API - DICCIONARIO GRATUITO ES <-> QU
# =====================================================================

@app.route('/api/dictionary/translate', methods=['GET', 'POST'])
def dictionary_translate():
    """Traduce una palabra usando Glosbe Dictionary API.

    GET params:
        q: palabra a traducir
        from: idioma fuente (es/qu)
        to: idioma destino (qu/es)

    POST JSON:
        {"word": "...", "from": "es", "to": "qu"}
    """
    if request.method == 'POST':
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return jsonify({'error': 'Cuerpo JSON inválido.'}), 400
        word = data.get('word', data.get('q'))
        from_lang = data.get('from', 'es')
        to_lang = data.get('to', 'qu')
    else:
        word = request.args.get('q', request.args.get('word'))
        from_lang = request.args.get('from', 'es')
        to_lang = request.args.get('to', 'qu')

    if not word:
        return jsonify({'error': 'Se requiere parámetro q (palabra).'}), 400

    if from_lang not in LANGUAGES or to_lang not in LANGUAGES:
        return jsonify({'error': 'Idiomas no soportados. Use es o qu.'}), 400

    result = translate_word(word, from_lang, to_lang)
    if not result:
        return jsonify({
            'word': word,
            'translation': None,
            'message': f'No se encontró traducción para "{word}" de {from_lang} a {to_lang}.',
        })

    return jsonify(result)


@app.route('/api/dictionary/search')
def dictionary_search():
    """Busca palabras en el diccionario local de quechua.

    GET params:
        q: término de búsqueda
    """
    query = request.args.get('q', request.args.get('query'))
    if not query:
        return jsonify({'error': 'Se requiere parámetro q (búsqueda).'}), 400

    results = search_quechua_dictionary(query)
    return jsonify({
        'query': query,
        'results': results,
        'total': len(results),
    })


@app.route('/api/dictionary/phrases')
def dictionary_phrases():
    """Retorna frases comunes en quechua por categoría.

    GET params:
        category: common, greetings, numbers, tramites, locations, time
    """
    category = request.args.get('category', 'common')
    phrases = get_quechua_phrases(category)

    return jsonify({
        'category': category,
        'phrases': phrases,
        'total': len(phrases),
    })


@app.route('/api/dictionary/categories')
def dictionary_categories():
    """Retorna las categorías disponibles del diccionario."""
    return jsonify({
        'categories': [
            {'id': 'common', 'name': 'Frases Comunes', 'icon': '💬'},
            {'id': 'greetings', 'name': 'Saludos', 'icon': '👋'},
            {'id': 'numbers', 'name': 'Números', 'icon': '🔢'},
            {'id': 'tramites', 'name': 'Trámites', 'icon': '📋'},
            {'id': 'locations', 'name': 'Ubicaciones', 'icon': '📍'},
            {'id': 'time', 'name': 'Tiempo', 'icon': '⏰'},
        ],
    })


@app.route('/api/dictionary/learn', methods=['POST'])
def dictionary_learn():
    """Añade una nueva palabra al diccionario local.

    POST JSON:
        {"spanish": "palabra", "quechua": "traducción", "example": "ejemplo"}
    """
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({'error': 'Cuerpo JSON inválido.'}), 400

    es_word = data.get('spanish', data.get('es'))
    qu_word = data.get('quechua', data.get('qu'))
    example = data.get('example', '')

    if not es_word or not qu_word:
        return jsonify({'error': 'Se requieren campos "spanish" y "quechua".'}), 400

    result = learn_quechua_word(es_word, qu_word, example)
    return jsonify({
        'status': 'success',
        'word': result,
        'message': f'Palabra "{es_word}" aprendida como "{qu_word}".',
    })


@app.route('/api/dictionary/stats')
def dictionary_stats():
    """Retorna estadísticas del diccionario local."""
    return jsonify({
        'total_words': len(QUECHUA_LOCAL_DB),
        'languages': ['es', 'qu'],
        'source': 'Base de datos local + Glosbe API',
        'categories': {
            'greetings': len([k for k in QUECHUA_LOCAL_DB if k in ['hola', 'buenos días', 'buenas tardes', 'gracias', 'por favor', 'adiós']]),
            'numbers': len([k for k in QUECHUA_LOCAL_DB if k in ['uno', 'dos', 'tres', 'cuatro', 'cinco', 'seis', 'siete', 'ocho', 'nueve', 'diez']]),
            'family': len([k for k in QUECHUA_LOCAL_DB if k in ['madre', 'padre', 'hermano', 'hermana', 'hijo', 'hija', 'esposo', 'esposa']]),
            'tramites': len([k for k in QUECHUA_LOCAL_DB if k in ['carnet', 'trámite', 'documento', 'certificado', 'constancia', 'licencia', 'permiso', 'pago', 'costo', 'precio']]),
            'locations': len([k for k in QUECHUA_LOCAL_DB if k in ['municipalidad', 'oficina', 'dirección', 'ubicación']]),
            'time': len([k for k in QUECHUA_LOCAL_DB if k in ['hoy', 'mañana', 'ayer', 'tarde', 'temprano', 'siempre', 'nunca']]),
            'questions': len([k for k in QUECHUA_LOCAL_DB if k.startswith('¿')]),
            'actions': len([k for k in QUECHUA_LOCAL_DB if k in ['ir', 'venir', 'hacer', 'buscar', 'pagar', 'esperar', 'hablar', 'entender']]),
        },
    })


# =====================================================================
# GOOGLE GEMINI API - IA GRATUITA
# =====================================================================

@app.route('/api/gemini/status')
def gemini_status():
    """Retorna el estado de Google Gemini API."""
    return jsonify(get_gemini_status())


@app.route('/api/gemini/chat', methods=['POST'])
def gemini_chat_endpoint():
    """Envía un mensaje a ChatGPT (primario) o Gemini (fallback) y retorna la respuesta.

    POST JSON:
        {"message": "¿Qué trámites hay?", "language": "es"}
    """
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({'error': 'Cuerpo JSON inválido.'}), 400

    message = data.get('message', data.get('q'))
    if not message:
        return jsonify({'error': 'Se requiere campo "message".'}), 400

    language = data.get('language', data.get('lang', 'es'))
    if language not in LANGUAGES:
        language = 'es'

    context = data.get('context')

    # 1) PRIMERO: Intentar con ChatGPT (asistente primordial)
    chatgpt_response = get_ai_resp(message, language)
    if chatgpt_response and chatgpt_response != get_resp(message, language):
        return jsonify({
            'success': True,
            'response': chatgpt_response,
            'source': 'chatgpt',
            'model': CHAT_MODEL,
            'language': language,
        })

    # 2) SEGUNDO: Si ChatGPT falla, usar Gemini (fallback gratuito)
    result = gemini_chat(message, language, context)

    if result.get('success'):
        return jsonify(result)
    elif result.get('fallback'):
        # 3) TERCERO: Si ambos fallan, usar chatbot local
        local_response = get_resp(message, language)
        return jsonify({
            'success': True,
            'response': local_response,
            'source': 'local_fallback',
            'language': language,
        })
    else:
        return jsonify({'error': result.get('error', 'Error desconocido.')}), 500


@app.route('/api/gemini/translate', methods=['POST'])
def gemini_translate_endpoint():
    """Traduce texto usando Google Gemini.

    POST JSON:
        {"text": "Hola", "from": "es", "to": "qu"}
    """
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({'error': 'Cuerpo JSON inválido.'}), 400

    text = data.get('text', data.get('q'))
    if not text:
        return jsonify({'error': 'Se requiere campo "text".'}), 400

    source_lang = data.get('from', 'es')
    target_lang = data.get('to', 'qu')

    if source_lang not in LANGUAGES or target_lang not in LANGUAGES:
        return jsonify({'error': 'Idiomas no soportados. Use es o qu.'}), 400

    result = gemini_translate(text, source_lang, target_lang)

    if result.get('success'):
        return jsonify(result)
    else:
        return jsonify({'error': result.get('error', 'Error de traducción.')}), 500


@app.route('/api/gemini/tutor', methods=['POST'])
def gemini_tutor_endpoint():
    """Tutor de quechua usando Google Gemini.

    POST JSON:
        {"word": "hola", "language": "es"}
    """
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({'error': 'Cuerpo JSON inválido.'}), 400

    word = data.get('word', data.get('q'))
    if not word:
        return jsonify({'error': 'Se requiere campo "word".'}), 400

    language = data.get('language', 'es')
    if language not in LANGUAGES:
        language = 'es'

    result = gemini_quechua_tutor(word, language)

    if result.get('success'):
        return jsonify(result)
    else:
        return jsonify({'error': result.get('error', 'Error del tutor.')}), 500


@app.route('/api/gemini/tramite', methods=['POST'])
def gemini_tramite_endpoint():
    """Analiza un trámite usando Google Gemini.

    POST JSON:
        {"tramite": "carnet de identidad"}
    """
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({'error': 'Cuerpo JSON inválido.'}), 400

    tramite = data.get('tramite', data.get('q'))
    if not tramite:
        return jsonify({'error': 'Se requiere campo "tramite".'}), 400

    result = gemini_analyze_tramite(tramite)

    if result.get('success'):
        return jsonify(result)
    else:
        return jsonify({'error': result.get('error', 'Error al analizar trámite.')}), 500


@app.route('/api/gemini/quechua', methods=['POST'])
def gemini_quechua_endpoint():
    """Traduce y explica en quechua usando Gemini.

    POST JSON:
        {"text": "Buenos días, ¿cómo estás?", "to": "qu"}
    """
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({'error': 'Cuerpo JSON inválido.'}), 400

    text = data.get('text', data.get('q'))
    if not text:
        return jsonify({'error': 'Se requiere campo "text".'}), 400

    target = data.get('to', 'qu')

    prompt = f"""Traduce y explica en quechua boliviano (runasimi de Sacaba, Bolivia):

Texto: "{text}"

Proporciona:
1. Traducción al quechua
2. Pronunciación fonética
3. Ejemplo de uso
4. Notas culturales si aplica

Responde de forma breve y didáctico."""

    result = gemini_chat(prompt, target)

    if result.get('success'):
        return jsonify({
            'success': True,
            'text': text,
            'quechua': result['response'],
            'source': 'gemini',
        })
    else:
        return jsonify({'error': result.get('error', 'Error en traducción.')}), 500


if __name__ == '__main__':
    run_app(open_browser=True)
