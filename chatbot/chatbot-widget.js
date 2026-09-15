/* ============================================
   CHATBOT WIDGET MODERNO - IA + AUDIO
   ============================================ */
(function() {
'use strict';

/* ===== BASE DE CONOCIMIENTO COMPLETA ===== */
var KB = {
    carnet_conducta: {
        es: {
            n: "Certificado de Conducta (Antecedentes)", icon: "\u2705",
            d: "Documento que certifica que no tienes antecedentes penales ni policiales en Bolivia.",
            donde: "Oficinas de la Policia (FELCC) o en linea a traves del portal policial.",
            cuanto: "Bs. 20 (valor de ley del certificado).",
            que_necesito: ["Cedula de identidad vigente","Formulario de solicitud","Pago de la tasa correspondiente"],
            como: ["Reune tu cedula de identidad","Llena el formulario de solicitud","Cancela el valor del certificado","Te lo entregan impreso y firmado"],
            cuanto_tarda: "Inmediato o hasta 1 dia habil segun el sistema.",
            horario: "Lunes a viernes en horario habil.",
            consejo: "Se pide para empleo, estudios y tramites en el exterior.",
            r: ["Cedula","Formulario","Pago"],
            c: "Bs. 20", t: "1 dia", dep: "Policia (FELCC)",
            p: ["Cedula","Formulario","Pago","Entrega"],
            u: ""
        },
        qu: {
            n: "Conducta Certificado (Antecedente)", icon: "\u2705",
            d: "Boliviapi mana penaltapas ni policial yachaycachay kasqaykita riqsichiq documento.",
            donde: "Policia (FELCC) oficinaspi.",
            cuanto: "Bs. 20 (certificadoq chanin).",
            que_necesito: ["Cedula vigente","Solicitud formulario","Chantinta pagay"],
            como: ["Cedulaykita apamuy","Formulariota qillqay","Certificadoq chantinta pagay","Firmado nitaq impreso chaskikuy"],
            cuanto_tarda: "Chay p'unchay utaq 1 p'unchay llamkaq.",
            horario: "Lun-Vie horario habilpi.",
            consejo: "Llamkay, yachay nitaq huk paisespi tramitospaq mañakun.",
            r: ["Cedula","Formulario","Pago"],
            c: "Bs. 20", t: "1 p'unchay", dep: "Policia (FELCC)",
            p: ["Cedula","Formulario","Pago","Chaskiy"],
            u: ""
        }
    },
    licencia_conducir: {
        es: {
            n: "Licencia de Conducir", icon: "\uD83D\uDE97",
            d: "Obtencion o renovacion de la licencia de conducir vehiculos livianos, pesados o motocicletas (SEGIP).",
            donde: "Centro de Licencias SEGIP en Sacaba o Cochabamba.",
            cuanto: "Varia segun la categoria (liviana, pesada, moto) y el curso.",
            que_necesito: ["Cedula de identidad vigente","Certificado de conducta (antecedentes)","Certificado medico de salud","Comprobante de pago","Fotografias (para el expediente)"],
            como: ["Reune tus documentos (CI, antecedentes, certificado medico)","Cancela el valor de la categoria","Aprueba el examen (teorico y practico)","Entregan tu licencia"],
            cuanto_tarda: "De 1 a 2 semanas segun la agenda del SEGIP.",
            horario: "Lunes a viernes en horario habil.",
            consejo: "Renueva tu licencia antes del vencimiento para evitar sanciones.",
            r: ["CI","Conducta","Medico","Pago"],
            c: "Segun categoria", t: "1-2 semanas", dep: "SEGIP - Transito",
            p: ["Documentos","Pago","Examen","Entrega"],
            u: ""
        },
        qu: {
            n: "Manejo Licencia", icon: "\uD83D\uDE97",
            d: "Liviano, pesado utaq moto vehiculokunata manenaypaq licencia hurqoy utaq renovay (SEGIP).",
            donde: "SEGIP Centro de Licencias Sacabapi utaq Cochabambapi.",
            cuanto: "Categoriaqmanhina (liviana, pesada, moto) utaq cursomanhina.",
            que_necesito: ["Cedula vigente","Conducta certificado","Salud medico certificado","Pago comprobante","Fotokuna (expedientepaq)"],
            como: ["Documentosta apamuy (CI, antecedente, medico)","Categoriaq chantinta pagay","Examen aprobay (teorico y practico)","Licenciaykita qun"],
            cuanto_tarda: "1-2 semana SEGIP agendaqmanhina.",
            horario: "Lun-Vie horario habilpi.",
            consejo: "Licenciaykita vencenantataq renovay, sancion ama kananpaq.",
            r: ["CI","Conducta","Medico","Pago"],
            c: "Segun categoria", t: "1-2 semana", dep: "SEGIP - Transito",
            p: ["Documentos","Pago","Examen","Chaskiy"],
            u: ""
        }
    },
    registro_civil: {
        es: {
            n: "Registro Civil (Certificado de Nacimiento)", icon: "\uD83D\uDD82",
            d: "Certificado de nacimiento, matrimonio o defuncion expedido por el Registro Civil de Sacaba.",
            donde: "Oficina del Registro Civil - Municipalidad de Sacaba.",
            cuanto: "Bs. 10 por certificado (el valor puede variar).",
            que_necesito: ["Cedula de identidad del solicitante","Datos del inscrito (nombres, fecha y lugar)","En caso de aclaracion, partida original"],
            como: ["Acude al Registro Civil de Sacaba","Solicita el certificado con los datos","Cancela el valor","Retira tu certificado"],
            cuanto_tarda: "Inmediato si los datos existen en el registro.",
            horario: "Lunes a viernes en horario habil.",
            consejo: "Lleva los datos exactos del inscrito para una busqueda rapida.",
            r: ["CI","Datos inscrito","Partida original (si aplica)"],
            c: "Bs. 10", t: "Inmediato", dep: "Registro Civil",
            p: ["Registro Civil","Solicitud","Pago","Retiro"],
            u: ""
        },
        qu: {
            n: "Registro Civil (Nacimiento Certificado)", icon: "\uD83D\uDD82",
            d: "Nacimiento, matrimonio utaq defuncion certificado, Sacaba Registro Civil qusqa.",
            donde: "Registro Civil Oficina - Municipalidad de Sacaba.",
            cuanto: "Bs. 10 certificado (chaninmi tiyan).",
            que_necesito: ["Solicitanteq cedula","Inscritop datos (suti, p'unchay, lugar)","Aclaracion kaspaqa, partida original"],
            como: ["Sacaba Registro Civilman riy","Datoswan certificadota mañay","Chaninta pagay","Certificadoykita chaskiy"],
            cuanto_tarda: "Datos registropi kaptinqa, chay p'unchaylla.",
            horario: "Lun-Vie horario habilpi.",
            consejo: "Inscritop exacto datosta apamuy, usqay maskanaykipaq.",
            r: ["CI","Datos","Partida original"],
            c: "Bs. 10", t: "Chaylla", dep: "Registro Civil",
            p: ["Registro Civil","Mañay","Pago","Chaskiy"],
            u: ""
        }
    },
    carnet: {
        es: {
            n: "Carnet de Identidad (Cedula)", icon: "\uD83E\UDAAA",
            d: "Documento de identificacion personal obligatorio para todos los ciudadanos bolivianos.",
            donde: "Las oficinas del SEGIP se encuentran en Sacaba.",
            donde_link: "https://maps.app.goo.gl/f27gLh5Accp2UmKW9",
            cuanto: "Bs. 17 (diecisiete bolivianos).",
            cuanto_detail: "Se puede pagar en Banco Union u otras entidades financieras autorizadas.",
            que_necesito: ["Comprobante de pago de Bs. 17","Cedula anterior (si es renovacion)","Denuncia policial (en caso de perdida)"],
            como: ["Realiza el pago de Bs. 17 en Banco Union","Acude a las oficinas del SEGIP","Presenta tu comprobante y cedula anterior","Registraran tus huellas dactilares","Te tomaran una foto digital","Listo! Retiras tu carnet"],
            cuanto_tarda: "Inmediato, lo haces el mismo dia.",
            horario: "Lunes a viernes en horario habil de oficina.",
            consejo: "Ve temprano para evitar filas. Lleva todos tus documentos.",
            r: ["Comprobante Bs. 17","Cedula anterior","Denuncia (si perdiste)"],
            c: "Bs. 17", t: "Inmediato", dep: "SEGIP",
            p: ["Pago Bs. 17","SEGIP","Comprobante","Huellas","Foto","Retiro"],
            u: "https://maps.app.goo.gl/f27gLh5Accp2UmKW9"
        },
        qu: {
            n: "Carnet de Identidad (Cedula)", icon: "\uD83E\UDAAA",
            d: "Identidad documento, obligatorio tukuy runapaq. SEGIP oficinaspi qillchachikuy (mushuqta utaq renovacion).",
            donde: "SEGIP oficinas Sacabapi tiyanku.",
            donde_link: "https://maps.app.goo.gl/f27gLh5Accp2UmKW9",
            cuanto: "Bs. 17 (chunka qanchisniyuq bolivianos).",
            cuanto_detail: "Banco Unionpi utaq huk bankokunapi pagay tiyan.",
            que_necesito: ["Bs. 17 pagasqayki comprobante (Banco Union)","Nawpaq cedula (renovacion kaspa)","Denuncia policial (chinkachiptiykiqa)"],
            como: ["Bs. 17ta pagay Banco Unionpi","SEGIP oficinasman riy","Comprobante nitaq cedulata rikuchiy","Maki huellakunata registray","Fotota horqoy","Listo! Carnetta chaskikuy"],
            cuanto_tarda: "Chay p'unchaylla rurasqa kan.",
            horario: "Lun-Vie horario habilpi.",
            consejo: "Tempranuta riy, filakuna ama kananpaq. Tukuy documentoykita apamuy.",
            r: ["Bs. 17 comprobante","Cedula","Denuncia"],
            c: "Bs. 17", t: "Chaylla", dep: "SEGIP",
            p: ["Bs. 17ta pagay","SEGIPman riy","Comprobante","Huellakuna","Foto","Carnetta chaskikuy"],
            u: "https://maps.app.goo.gl/f27gLh5Accp2UmKW9"
        }
    },
    residencia: {
        es: {
            n: "Constancia de Residencia", icon: "\uD83C\uDFE0",
            d: "Documento que certifica tu residencia en el municipio de Sacaba.",
            donde: "Direccion de Registro Social, en la municipalidad.",
            cuanto: "Bs. 15.",
            que_necesito: ["Fotocopia de cedula de identidad","Fotocopia de libreta de servicio militar","Recibo de pago de servicios basicos","Declaracion jurada de residencia","Dos fotos tamano carnet"],
            como: ["Recoge el formulario en Ventanilla Unica","Llena el formulario con tus datos","Presenta los requisitos","Realiza el pago en caja","Retira la constancia en 2-3 dias"],
            cuanto_tarda: "2 a 3 dias habiles.",
            horario: "Lunes a viernes, 8:00 a 12:00 / 14:30 a 18:30.",
            consejo: "Lleva todos los requisitos para un solo viaje.",
            r: ["Cedula","Libreta militar","Recibo de servicios","Declaracion jurada","2 fotos"],
            c: "Bs. 15", t: "2-3 dias", dep: "Registro Social",
            p: ["Formulario","Requisitos","Pago","Verificacion","Retiro"],
            u: ""
        },
        qu: {
            n: "Tiyay Constancia (Residencia)", icon: "\uD83C\uDFE0",
            d: "Huk runaq Sakaba munisipyupi tiyasqanta riqsichiq documento.",
            donde: "Registro Social oficinaqpi, municipalidadpi.",
            cuanto: "Bs. 15.",
            que_necesito: ["Cedula fotocopia","Libreta militar fotocopia","Servicios recibo (yaku, lliphi, telefono)","Declaracion jurada","Iskay carnet fotokuna"],
            como: ["Formulariota apakamuy (Ventanilla Unica)","Formulariota qillqay qan datosniykita","Requisitokunata rikuchiy","Cajapi pagay","Constanciata chaskikuy (2-3 p'unchay)"],
            cuanto_tarda: "2-3 p'unchay llamkaq.",
            horario: "Lun-Vie, 8:00-12:00 / 14:30-18:30.",
            consejo: "Tukuy requisitokunata apakuy, huk kutilla kananpaq.",
            r: ["Cedula","Libreta","Servicios recibo","Declaracion","2 fotos"],
            c: "Bs. 15", t: "2-3 p'unchay", dep: "Registro Social",
            p: ["Formulariota apakamuy","Formulariota qillqay","Requisitokuna","Cajapi pagay","Chaskikuy"],
            u: ""
        }
    },
    funcionamiento: {
        es: {
            n: "Licencia de Funcionamiento", icon: "\uD83C\uDFE2",
            d: "Permiso municipal (patente) para operar un negocio o actividad economica en Sacaba. Se tramita en la Direccion de Ingresos y Servicios Municipales.",
            donde: "Direccion de Ingresos y Servicios Municipales - Municipalidad de Sacaba (caja central o subalcaldias).",
            cuanto: "Bs. 60 (licencia nueva), Bs. 40 (renovacion) - valores municipales.",
            cuanto_detail: "Los valores se compran en Caja Central o subalcaldias. Segun el rubro puede pedirse licencia ambiental o contrato GERES.",
            que_necesito: ["Formulario de solicitud con caracter de Declaracion Jurada (DJ)","Fotocopia de carnet de identidad del propietario","Fotocopia de contrato de alquiler y/o anticretico (si corresponde)","Licencia ambiental o certificacion (si el rubro lo exige)","Contrato o certificacion de GERES (segun rubro)","Valores municipales: Bs. 60 nuevo o Bs. 40 renovacion"],
            como: ["Acude a la caja central o subalcaldia y compra los valores municipales (Bs. 60 o Bs. 40)","Llena el formulario de solicitud (Declaracion Jurada)","Adjunta fotocopia de CI y contrato de alquiler del local","Presenta licencia ambiental y contrato GERES si tu rubro lo exige","Cancela en caja y recoge tu licencia"],
            cuanto_tarda: "Con los requisitos completos se gestiona en la municipalidad.",
            horario: "Lunes a viernes en horario habil.",
            consejo: "Verifica los requisitos de tu rubro antes de ir. Los rubros van desde industrias, comercio y restaurantes, hasta talleres, servicios de salud y educacion.",
            r: ["Formulario DJ","CI","Contrato","Licencia ambiental","GERES"],
            c: "Bs. 60 (nuevo) / Bs. 40 (renov.)", t: "Gestion directa", dep: "Ingresos y Servicios",
            p: ["Valores","Formulario","Requisitos","Licencia ambiental","Licencia"],
            u: ""
        },
        qu: {
            n: "Licencia Funcionamiento", icon: "\uD83C\uDFE2",
            d: "Munisipyuq suyúnpi negociota ruwanaykipaq permiso.",
            donde: "Ingresos y Servicios oficinaqpi, Sacaba Municipalidad.",
            cuanto: "Bs. 60 (mushuq licencia), Bs. 40 (renovacion) - valores municipales.",
            cuanto_detail: "Valores Caja Centralpi utaq subalcaldiaspi rantikun. Rubro mañaptinqa licencia ambiental utaq contrato GERES mañakun.",
            que_necesito: ["Mañakuy qillqa (Declaracion Jurada)","Propietarioq cedula fotocopia","Contrato de alquiler utaq anticretico fotocopia","Licencia ambiental utaq certificacion (rubro mañaptin)","GERES contrato utaq certificacion (rurun jina)","Valores: Bs. 60 nuevo utaq Bs. 40 renovacion"],
            como: ["Caja centralman utaq subalcaldiaman riy, valores rantikuy (Bs. 60 utaq Bs. 40)","Mañakuy qillqata qillqay (Declaracion Jurada)","Cedula nitaq localq contrato fotocopiata churay","Licencia ambiental nitaq GERES contrato rikuchiy (rubro mañaptin)","Cajapi pagay, licenciata chaskikuy"],
            cuanto_tarda: "Requisitos tukukuptiykiqa municipalidadpi rurasqa kan.",
            horario: "Lun-Vie horario habilpi.",
            consejo: "Rillasqayki, rubroykiq requisitunkunata qhaway. Industrias, comercio, restaurantes, talleres, salud utaq educacion — tukuy ruwaykuna.",
            r: ["Formulario DJ","Cedula","Contrato","Licencia ambiental","GERES"],
            c: "Bs. 60 (nuevo) / Bs. 40 (renov.)", t: "Gestion directa", dep: "Ingresos y Servicios",
            p: ["Valores rantikuy","Formulariota qillqay","Requisitokuna","Licencia ambiental","Licenciata chaskikuy"],
            u: ""
        }
    },
    construccion: {
        es: {
            n: "Permiso de Construccion (Plano de Vivienda)", icon: "\uD83C\uDFD7\uFE0F",
            d: "Aprobacion de plano para construir o legalizar una vivienda u obra nueva en Sacaba (tramite de Urbanismo).",
            donde: "Direccion de Urbanismo - Municipalidad de Sacaba (Gestion Urbana y Territorial).",
            cuanto: "Costo por valores municipales (folder administrativo y timbres).",
            que_necesito: ["Memorial dirigido al Alcalde o Subalcalde","Titulo de propiedad y folio real (no mayor a 1 anio)","Comprobante de pago de impuestos IPBI de la ultima gestion","Planos del proyecto elaborados por arquitecto (3 ejemplares + digital)","Certificado catastral actualizado","Fotocopia de CI vigente","Compra de valores municipales"],
            como: ["Prepara los planos con un arquitecto colegiado","Reune titulo, folio real y pago de IPBI","Presenta memorial y requisitos en Urbanismo","Adjunta certificado catastral y plano de lote","Cancela valores municipales y espera la aprobacion"],
            cuanto_tarda: "Se revisa por la Direccion de Urbanismo; el plazo depende del proyecto.",
            horario: "Lunes a viernes en horario habil.",
            consejo: "Para legalizar una obra ya construida se necesita ademas declaracion jurada, carta notariada y fotografias de la fachada e interiores.",
            r: ["Memorial","Titulo y folio real","IPBI","Planos del arquitecto","Certificado catastral"],
            c: "Valores municipales", t: "Segun proyecto", dep: "Urbanismo",
            p: ["Planos","IPBI","Memorial","Valores","Aprobacion"],
            u: ""
        },
        qu: {
            n: "Construccion Permiso", icon: "\uD83C\uDFD7\uFE0F",
            d: "Wasi ruwana utaq allchasqanapaq permiso, Urbanismoqpi rurasqa.",
            donde: "Urbanismo Oficina - Sacaba Municipalidad (Gestion Urbana y Territorial).",
            cuanto: "Valores municipales (folder administrativo utaq timbres).",
            que_necesito: ["Memorial (Alcalde utaq Subalcalde llamkan)","Titulo de propiedad nitaq folio real (mana huk watamanta aswan)","IPBI impuesto pagasqayki comprobante (qhipa gestion)","Arquitectop planos (3 ejemplares + digital)","Certificado catastral musuq","Cedula fotocopia","Valores municipales rantikuy"],
            como: ["Arquitectowan planosta pukllachiy","Titulo, folio real nitaq IPBI paguytantachiy","Urbanismoqpi memorial nitaq requisitosta rikuchiy","Certificado catastral nitaq lotep plano churay","Valores municipales pagay, aprobacion suyay"],
            cuanto_tarda: "Urbanismoq qhawariyninman jina; proyectoq plazunman.",
            horario: "Lun-Vie horario habilpi.",
            consejo: "Rurasqa wasita legalizayta munaqtinqa: declaracion jurada, carta notariada nitaq fachada fotokuna apamuy.",
            r: ["Memorial","Titulo y folio real","IPBI","Planos","Certificado catastral"],
            c: "Valores municipales", t: "Segun proyecto", dep: "Urbanismo",
            p: ["Planosta pukllachiy","IPBI paguy","Memorial","Valores pagay","Aprobacion"],
            u: ""
        }
    },
    propiedad: {
        es: {
            n: "Registro de Propiedad", icon: "\uD83D\uDCDC",
            d: "Inscripcion de bienes inmuebles para legalizar tu propiedad.",
            donde: "Direccion de Derechos Reales.",
            cuanto: "Bs. 50 - 200 (segun valor catastral).",
            que_necesito: ["Titulo de propiedad original","Plano de ubicacion","Cedula de identidad","Pago de tasa"],
            como: ["Reune los documentos","Presenta en Derechos Reales","Realiza el pago","Espera la inscripcion","Retira tu certificado"],
            cuanto_tarda: "15 a 30 dias habiles.",
            horario: "Lunes a viernes en horario habil.",
            consejo: "Verifica que no haya deudas pendientes.",
            r: ["Titulo","Plano","Cedula","Pago"],
            c: "Bs. 50-200", t: "15-30 dias", dep: "Derechos Reales",
            p: ["Documentos","Derechos Reales","Pago","Inscripcion","Certificado"],
            u: ""
        },
        qu: {
            n: "Propiedad Registro", icon: "\uD83D\uDCDC",
            d: "Propiedadyki munisipyuq registronpi qillchachikuy.",
            donde: "Derechos Reales Oficinaqpi.",
            cuanto: "Bs. 50 - 200 (valor catastralman jina).",
            que_necesito: ["Titulo de propiedad original","Ubicacion plano","Cedula","Tasa pagay"],
            como: ["Documentosta tantachiy","Derechos Realesqpi rikuchiy","Pagay","Inscripcion suyay","Certificadota chaskikuy"],
            cuanto_tarda: "15-30 p'unchay llamkaq.",
            horario: "Lun-Vie horario habilpi.",
            consejo: "Manaraq mana deudas kashasqanta qhaway.",
            r: ["Titulo","Plano","Cedula","Tasa"],
            c: "Bs. 50-200", t: "15-30 p'unchay", dep: "Derechos Reales",
            p: ["Documentosta tantachiy","Rikuchiy","Pagay","Inscripcion","Certificado"],
            u: ""
        }
    },
    solteria: {
        es: {
            n: "Constancia de Solteria", icon: "\uD83D\uDC8D",
            d: "Certificado que acredita tu estado civil soltero.",
            donde: "Direccion de Registro Civil.",
            cuanto: "Bs. 10.",
            que_necesito: ["Cedula de identidad","Dos testigos con cedula","Pago de tasa"],
            como: ["Acude a Registro Civil con tus testigos","Presenta la cedula","Firma la declaracion","Paga la tasa","Recibe tu constancia"],
            cuanto_tarda: "Inmediato.",
            horario: "Lunes a viernes en horario habil.",
            consejo: "Lleva testigos que te conozcan personalmente.",
            r: ["Cedula","2 testigos","Pago"],
            c: "Bs. 10", t: "Inmediato", dep: "Registro Civil",
            p: ["Testigos","Declaracion","Pago","Constancia"],
            u: ""
        },
        qu: {
            n: "Solteria Constancia", icon: "\uD83D\uDC8D",
            d: "Mana casarakusqa kasqaykita riqsichiq documento.",
            donde: "Registro Civil Oficinaqpi.",
            cuanto: "Bs. 10.",
            que_necesito: ["Cedula","Iskay willaqkuna cedulawan","Tasa pagay"],
            como: ["Registro Civilman riy willaqkunawan","Cedulata rikuchiy","Declaracionta firmay","Tasata pagay","Constanciata chaskikuy"],
            cuanto_tarda: "Chay p'unchaylla.",
            horario: "Lun-Vie horario habilpi.",
            consejo: "Kikiykita riqsikuq willaqkunata apamuy.",
            r: ["Cedula","Iskay willaqkuna","Tasa"],
            c: "Bs. 10", t: "Chaylla", dep: "Registro Civil",
            p: ["Registro Civilman riy","Cedulata rikuchiy","Declaracionta firmay","Tasata pagay","Chaskikuy"],
            u: ""
        }
    },
    prediales: {
        es: {
            n: "Impuestos Prediales", icon: "\uD83D\uDCB0",
            d: "Impuesto anual que grava la propiedad de bienes inmuebles.",
            donde: "Direccion de Rentas Internas de la municipalidad.",
            cuanto: "0.5% - 1% del valor catastral del inmueble.",
            que_necesito: ["Cedula de identidad","Titulo de propiedad","Certificado catastral actualizado"],
            como: ["Consulta el monto en Rentas Internas","Realiza el pago en caja municipal","Guarda tu comprobante","Presenta el comprobante si es necesario"],
            cuanto_tarda: "Inmediato al pagar.",
            horario: "Lunes a viernes en horario habil.",
            consejo: "Paga antes de la fecha de vencimiento para evitar recargos.",
            r: ["Cedula","Titulo","Certificado catastral"],
            c: "0.5-1%", t: "Inmediato", dep: "Rentas Internas",
            p: ["Consulta","Pago","Comprobante"],
            u: ""
        },
        qu: {
            n: "Predial Impuestokuna", icon: "\uD83D\uDCB0",
            d: "Sapa wata propiedadyuq impuestota pagay.",
            donde: "Rentas Internas Oficinaqpi, municipalidadpi.",
            cuanto: "0.5% - 1% valor catastralmanta.",
            que_necesito: ["Cedula","Titulo de propiedad","Certificado catastral musuq"],
            como: ["Rentas Internaspi monto qhaway","Caja municipalpi pagay","Comprobanteta waqaychay","Comprobante rikuchiy (mañaptinqa)"],
            cuanto_tarda: "Pagayta ruwaspa chay p'unchaylla.",
            horario: "Lun-Vie horario habilpi.",
            consejo: "Vencimiento fecha riman, mana recargo kananpaq.",
            r: ["Cedula","Titulo","Certificado"],
            c: "0.5-1%", t: "Chaylla", dep: "Rentas Internas",
            p: ["Monto qhaway","Cajapi pagay","Comprobante"],
            u: ""
        }
    },
    agua: {
        es: {
            n: "Servicio de Agua Potable", icon: "\uD83D\uDCA7",
            d: "Tramite para conectar o regularizar el servicio de agua potable.",
            donde: "Empresa de Agua Potable de Sacaba.",
            cuanto: "Bs. 50 - 200 (segun tipo de conexion).",
            que_necesito: ["Solicitud formal","Cedula de identidad","Constancia de propiedad o recibo de alquiler","Pago de conexion"],
            como: ["Presenta tu solicitud","Paga la conexion","Espera la inspeccion","Recibe tu servicio"],
            cuanto_tarda: "5 a 10 dias habiles.",
            horario: "Lunes a viernes en horario habil.",
            consejo: "Verifica tu deuda antes de solicitar.",
            r: ["Solicitud","Cedula","Propiedad/Alquiler","Pago"],
            c: "Bs. 50-200", t: "5-10 dias", dep: "Empresa de Agua",
            p: ["Solicitud","Pago","Inspeccion","Servicio"],
            u: ""
        },
        qu: {
            n: "Yaku (Agua Potable)", icon: "\uD83D\uDCA7",
            d: "Munisipyuq yakunmanta servicio.",
            donde: "Empresa de Agua Potable Sacabaqpi.",
            cuanto: "Bs. 50 - 200 (conexionjina).",
            que_necesito: ["Mañakuy qillqa formal","Cedula","Tiyay constancia utaq alquiler recibo","Conexion pagay"],
            como: ["Mañakuy qillqata rikuchiy","Conexion pagay","Inspeccion suyay","Serviciota chaskikuy"],
            cuanto_tarda: "5-10 p'unchay llamkaq.",
            horario: "Lun-Vie horario habilpi.",
            consejo: "Mañakuy rawayki, deudaykita qhaway.",
            r: ["Mañakuy qillqa","Cedula","Propiedad o alquiler","Conexion pago"],
            c: "Bs. 50-200", t: "5-10 p'unchay", dep: "Empresa de Agua",
            p: ["Mañakuy","Conexion pagay","Inspeccion","Serviciota chaskikuy"],
            u: ""
        }
    },
    eventos: {
        es: {
            n: "Permiso para Eventos", icon: "\uD83C\uDF89",
            d: "Autorizacion para realizar eventos publicos o privados.",
            donde: "Direccion de Seguridad Ciudadana.",
            cuanto: "Bs. 30 - 300 (segun tipo de evento).",
            que_necesito: ["Solicitud con detalles del evento","Cedula del organizador","Poliza de responsabilidad civil","Pago de tasa"],
            como: ["Presenta la solicitud","Adjunta los documentos","Paga la tasa","Obten el permiso","Cumple las condiciones"],
            cuanto_tarda: "3 a 5 dias habiles.",
            horario: "Lunes a viernes en horario habil.",
            consejo: "Solicita con anticipacion para evitar problemas.",
            r: ["Solicitud","Cedula","Poliza","Pago"],
            c: "Bs. 30-300", t: "3-5 dias", dep: "Seguridad Ciudadana",
            p: ["Solicitud","Documentos","Pago","Permiso"],
            u: ""
        },
        qu: {
            n: "Eventopaq Permiso", icon: "\uD83C\uDF89",
            d: "Eventokunata ruwanaykipaq munisipyuq permiso.",
            donde: "Seguridad Ciudadana Oficinaqpi.",
            cuanto: "Bs. 30 - 300 (eventojina).",
            que_necesito: ["Mañakuy qillqa (eventop detallenkuna)","Organizadorq cedula","Poliza responsabilidad civil","Tasa pagay"],
            como: ["Mañakuy qillqata rikuchiy","Documentosta apuy","Tasata pagay","Permisota chaskikuy","Kamachikunata huntay"],
            cuanto_tarda: "3-5 p'unchay llamkaq.",
            horario: "Lun-Vie horario habilpi.",
            consejo: "Unayta mañakuy, problemas kananpaq.",
            r: ["Mañakuy qillqa","Cedula","Poliza","Tasa"],
            c: "Bs. 30-300", t: "3-5 p'unchay", dep: "Seguridad Ciudadana",
            p: ["Mañakuy","Documentosta","Tasata pagay","Permisota chaskikuy"],
            u: ""
        }
    },
    vehiculos: {
        es: {
            n: "Registro de Vehiculos", icon: "\uD83D\uDE97",
            d: "Inscripcion de vehiculos motorizados.",
            donde: "Direccion de Transito y Transporte.",
            cuanto: "Bs. 30 - 150.",
            que_necesito: ["Cedula","Libreta de transito","Revision vehicular","SOAT"],
            como: ["Solicita en Transito","Presenta documentos","Revision tecnica","Paga","Obten placa y libreta"],
            cuanto_tarda: "2 a 5 dias habiles.",
            horario: "Lunes a viernes en horario habil.",
            consejo: "Ten todos los documentos al dia.",
            r: ["Cedula","Libreta","Revision","SOAT"],
            c: "Bs. 30-150", t: "2-5 dias", dep: "Transito",
            p: ["Solicitud","Documentos","Revision","Pago","Placa"],
            u: ""
        },
        qu: {
            n: "Vehiculo Registro", icon: "\uD83D\uDE97",
            d: "Vehiculokunata munisipyuqpi registray.",
            donde: "Transito y Transporte Oficinaqpi.",
            cuanto: "Bs. 30 - 150.",
            que_necesito: ["Cedula","Transito libreta","Revision vehicular","SOAT"],
            como: ["Transitoqpi mañakuy","Documentosta rikuchiy","Revision tecnica","Pagay","Placa nitaq libreta chaskikuy"],
            cuanto_tarda: "2-5 p'unchay llamkaq.",
            horario: "Lun-Vie horario habilpi.",
            consejo: "Tukuy documentosta p'unchaysapa allinchay.",
            r: ["Cedula","Libreta","Revision","SOAT"],
            c: "Bs. 30-150", t: "2-5 p'unchay", dep: "Transito",
            p: ["Mañakuy","Documentosta","Revision","Pagay","Placa chaskikuy"],
            u: ""
        }
    },
    nodeuda: {
        es: {
            n: "Constancia de No Deuda", icon: "\u2705",
            d: "Certifica que no tienes deudas con el municipio.",
            donde: "Direccion de Rentas Internas.",
            cuanto: "Bs. 10.",
            que_necesito: ["Cedula de identidad","Certificado de propiedad"],
            como: ["Acude a Rentas Internas","Presenta los documentos","Verifican tus deudas","Paga si tienes deudas","Emite la constancia"],
            cuanto_tarda: "1 a 2 dias habiles.",
            horario: "Lunes a viernes en horario habil.",
            consejo: "Verifica tus deudas antes de solicitar.",
            r: ["Cedula","Certificado"],
            c: "Bs. 10", t: "1-2 dias", dep: "Rentas",
            p: ["Rentas","Documentos","Verificar","Pagar","Emitir"],
            u: ""
        },
        qu: {
            n: "Mana Deuda Constancia", icon: "\u2705",
            d: "Munisipyuwan mana deudayuq kasqaykita riqsichiq.",
            donde: "Rentas Internas Oficinaqpi.",
            cuanto: "Bs. 10.",
            que_necesito: ["Cedula","Certificado de propiedad"],
            como: ["Rentas Internasman riy","Documentosta rikuchiy","Deudaykita qhaway","Deudayuq kaspaqqa pagay","Constanciata qillqay"],
            cuanto_tarda: "1-2 p'unchay llamkaq.",
            horario: "Lun-Vie horario habilpi.",
            consejo: "Mañakuy rawayki, deudaykita qhaway.",
            r: ["Cedula","Certificado"],
            c: "Bs. 10", t: "1-2 p'unchay", dep: "Rentas",
            p: ["Rentasman riy","Documentosta","Deudayta qhaway","Pagay","Constanciata qillqay"],
            u: ""
        }
    },
    catastro_empadronamiento: {
        es: {
            n: "Empadronamiento Predial", icon: "\uD83C\uDFE0",
            d: "Registro de tu predio (terreno/lote) en el sistema catastral de Sacaba, con titulo de propiedad o en calidad de poseedor.",
            donde: "Unidad de Catastro - Municipalidad de Sacaba.",
            cuanto: "Valores municipales (folder administrativo y timbres de Bs. 10).",
            que_necesito: ["Memorial dirigido al Alcalde o Subalcalde firmado por el propietario","Titulo de propiedad registrado en Derechos Reales y folio real (no mayor a 1 anio), fotocopia con timbre de Bs. 10","Plano de lote georeferenciado por profesional colegiado (impreso y shapefile en CD)","Formulario de Declaracion Jurada EMP-CAT-01","Fotocopia de identidad o cedula de extranjeria","Compra de valores (folder y timbres Bs. 10)"],
            como: ["Prepara memorial, titulo, folio real y plano georeferenciado","Llena el formulario EMP-CAT-01 con tu profesional","Presenta todo en la Unidad de Catastro","Cancela los valores municipales","Se registra tu predio y queda listo"],
            cuanto_tarda: "Se gestiona en la Unidad de Catastro (Decreto Municipal 014/2024).",
            horario: "Lunes a viernes en horario habil.",
            consejo: "Si eres poseedor (sin titulo), tambien puedes empadronar: lleva minuta de compra-venta, boletas de servicios y declaracion voluntaria notariada.",
            c: "Valores municipales", t: "Gestion directa", dep: "Catastro",
            u: ""
        }
    },
    catastro_certificado: {
        es: {
            n: "Certificado Catastral", icon: "\uD83D\uDCC4",
            d: "Documento que certifica los datos del predio (ubicacion, superficie, codigo catastral) ante la municipalidad.",
            donde: "Unidad de Catastro - Municipalidad de Sacaba.",
            cuanto: "Valores municipales (folder administrativo y timbres).",
            que_necesito: ["Memorial dirigido al Alcalde o Subalcalde","Titulo de propiedad y folio real actualizado (no mayor a 1 anio)","Reporte sin deudas con timbre de Bs. 5","Fotocopia del plano de lote aprobado y RTA","Fotocopia de identidad del propietario","Compra de valores municipales"],
            como: ["Reune titulo, folio real y reporte sin deudas","Adjunta plano aprobado y resolucion tecnica","Presenta el memorial en Catastro","Cancela valores municipales","Retira tu certificado catastral"],
            cuanto_tarda: "Se gestiona en la Unidad de Catastro.",
            horario: "Lunes a viernes en horario habil.",
            consejo: "Tambien puedes pedir reimpresion o actualizacion del certificado catastral.",
            c: "Valores municipales", t: "Gestion directa", dep: "Catastro",
            u: ""
        }
    },
    catastro_avaluo: {
        es: {
            n: "Avaluo Catastral", icon: "\uD83D\uDCB0",
            d: "Calculo del valor oficial de tu inmueble para impuestos, transferencias o regularizaciones.",
            donde: "Unidad de Catastro - Municipalidad de Sacaba.",
            cuanto: "Valores municipales (folder administrativo).",
            que_necesito: ["Memorial dirigido al Alcalde solicitando el avaluo","Titulo de propiedad y folio real actualizado","Fotocopia del ultimo impuesto o IPBI","Plano de lote aprobado o georeferenciado","Fotocopia de identidad","Compra de valores municipales"],
            como: ["Presenta el memorial y documentos en Catastro","Adjunta titulo, folio real y ultimo impuesto","Entrega el plano del lote","Cancela los valores","Recibe el informe de avaluo"],
            cuanto_tarda: "Se gestiona en la Unidad de Catastro.",
            horario: "Lunes a viernes en horario habil.",
            consejo: "El avaluo es la base para calcular impuestos prediales y tasas.",
            c: "Valores municipales", t: "Gestion directa", dep: "Catastro",
            u: ""
        }
    },
    urbanismo_plano: {
        es: {
            n: "Aprobacion de Plano (Terreno/Lote)", icon: "\uD83C\uDFD7\uFE0F",
            d: "Aprobacion, anexion, division o subdivision de plano de terreno o lote (regularizacion predial).",
            donde: "Direccion de Urbanismo - Municipalidad de Sacaba.",
            cuanto: "Valores municipales (folder administrativo y timbres).",
            que_necesito: ["Memorial dirigido al Alcalde o Subalcalde","Titulo de propiedad y folio real (no mayor a 1 anio)","Comprobante de pago de impuestos IPBI de la ultima gestion","Planos elaborados por arquitecto/ingeniero (5 ejemplares + shapefile)","Fotocopia de identidad vigente","Compra de valores municipales"],
            como: ["Contrata un profesional para los planos (5 ejemplares)","Reune titulo, folio real y recibo de IPBI","Presenta memorial y expediente en Urbanismo","Cancela los valores municipales","Espera la revision y aprobacion"],
            cuanto_tarda: "Revisado por la Direccion de Urbanismo.",
            horario: "Lunes a viernes en horario habil.",
            consejo: "Incluye aqui: aprobacion de plano, anexion de terrenos, division y subdivision de lotes.",
            c: "Valores municipales", t: "Segun revision", dep: "Urbanismo",
            u: ""
        }
    },
    urbanismo_ampliacion: {
        es: {
            n: "Ampliacion o Remodelacion de Construccion", icon: "\uD83C\uDFD8\uFE0F",
            d: "Aprobacion municipal para ampliar o remodelar una construccion, casa o edificio.",
            donde: "Direccion de Urbanismo - Municipalidad de Sacaba.",
            cuanto: "Valores municipales (folder administrativo y timbres).",
            que_necesito: ["Memorial dirigido al Alcalde o Subalcalde","Titulo de propiedad y folio real actualizado","Comprobante de IPBI de la ultima gestion","Proyecto de ampliacion o remodelacion por arquitecto (3 ejemplares + CAD)","Certificado catastral actualizado","Plano de terreno aprobado","Fotocopia de identidad","Compra de valores"],
            como: ["Prepara el proyecto con un arquitecto","Reune titulo, IPBI y certificado catastral","Presenta memorial y planos en Urbanismo","Cancela valores municipales","Se aprueba el plano de ampliacion/remodelacion"],
            cuanto_tarda: "Revisado por Urbanismo (edificios de 4+ niveles piden mas requisitos).",
            horario: "Lunes a viernes en horario habil.",
            consejo: "Para edificios de 4 niveles o mas se suman memorias de calculo sanitario, electrico y estructural.",
            c: "Valores municipales", t: "Segun proyecto", dep: "Urbanismo",
            u: ""
        }
    },
    urbanismo_horizontal: {
        es: {
            n: "Propiedad Horizontal o Condominio", icon: "\uD83C\uDFE8",
            d: "Adecuacion de un inmueble a propiedad horizontal o condominio (departamentos, parqueos, bauleras).",
            donde: "Direccion de Urbanismo - Municipalidad de Sacaba.",
            cuanto: "Valores municipales (folder administrativo y timbres).",
            que_necesito: ["Memorial dirigido al Alcalde o Subalcalde","Titulo de propiedad y folio real actualizado","Comprobante de IPBI de la ultima gestion","Plano de adecuacion a propiedad horizontal por arquitecto (3 ejemplares + CAD/Excel)","Certificado catastral actualizado","Plano de terreno aprobado","Fotocopia de identidad","Compra de valores"],
            como: ["Contrata un arquitecto para el plano de adecuacion","Reune titulo, IPBI y certificado catastral","Presenta el expediente en Urbanismo","Cancela valores municipales","Recibe la resolucion de propiedad horizontal"],
            cuanto_tarda: "Revisado por la Direccion de Urbanismo.",
            horario: "Lunes a viernes en horario habil.",
            consejo: "Sirve para regularizar departamentos, locales, parqueos y bauleras de un edificio.",
            c: "Valores municipales", t: "Segun revision", dep: "Urbanismo",
            u: ""
        }
    },
    urbanismo_uso_suelo: {
        es: {
            n: "Certificacion de Uso de Suelo", icon: "\uD83C\uDFDB\uFE0F",
            d: "Certificaciones de urbanismo: uso de suelo, fijacion de rasante, linea nivel, zona y distrito, verificacion de medidas.",
            donde: "Direccion de Urbanismo - Municipalidad de Sacaba.",
            cuanto: "Valores municipales (folder administrativo y timbres).",
            que_necesito: ["Memorial o carta dirigida al Alcalde","Titulo de propiedad y folio real actualizado","Comprobante de IPBI (cuando corresponda)","Plano de lote georeferenciado o plano aprobado","Fotocopia de identidad","Compra de valores"],
            como: ["Indica el motivo de la solicitud en el memorial","Adjunta titulo, folio real e IPBI","Incluye el plano correspondiente","Cancela valores municipales","Recibe la certificacion solicitada"],
            cuanto_tarda: "Gestion en la Direccion de Urbanismo.",
            horario: "Lunes a viernes en horario habil.",
            consejo: "Tambien se emiten certificaciones por orden judicial y de limites de areas protegidas.",
            c: "Valores municipales", t: "Gestion directa", dep: "Urbanismo",
            u: ""
        }
    },
    urbanismo_verja: {
        es: {
            n: "Permiso de Trabajos Menores (Verja)", icon: "\uD83E\uDDF1",
            d: "Permiso para construccion de verja, cerco o muro (trabajos menores de construccion).",
            donde: "Direccion de Urbanismo - Municipalidad de Sacaba.",
            cuanto: "Valores municipales (folder administrativo y timbres).",
            que_necesito: ["Memorial dirigido al Alcalde o Subalcalde firmado por el propietario","Titulo de propiedad y folio real actualizado","Comprobante de IPBI","Planos de verja por arquitecto (3 ejemplares)","Plano de lote aprobado","Fotocopia de identidad","Compra de valores"],
            como: ["Prepara los planos de la verja con un arquitecto","Reune titulo, IPBI y plano de lote","Presenta el memorial en Urbanismo","Cancela valores municipales","Aprueban el permiso de trabajos menores"],
            cuanto_tarda: "Gestion en la Direccion de Urbanismo.",
            horario: "Lunes a viernes en horario habil.",
            consejo: "Aplica para verjas, cercos y muros; es un tramite mas simple que el plano de vivienda.",
            c: "Valores municipales", t: "Gestion directa", dep: "Urbanismo",
            u: ""
        }
    },
    vehiculo_inscripcion: {
        es: {
            n: "Inscripcion de Vehiculo", icon: "\uD83D\uDE97",
            d: "Registro RUAT de un vehiculo automotor nuevo (importacion directa o casa comercial) en Sacaba.",
            donde: "Unidad de Vehiculos - Municipalidad de Sacaba.",
            cuanto: "Folder administrativo y valores segun el tramite (Decreto Municipal 015/2024).",
            que_necesito: ["Declaracion de Importacion/Poliza o DUI y Formulario de Registro Vehicular (FRV)","Fotocopia de CI vigente del propietario o representante legal","Certificado de inscripcion a Impuestos Nacionales (persona juridica)","Testimonio de poder (si compra una sociedad)","Fotografia fondo rojo 3x3 cm (persona natural)","Folder comun"],
            como: ["Reune la documentacion de importacion o factura comercial","Adjunta CI, fotografia y folder","Presenta en la Unidad de Vehiculos","Cancela los valores","Se inscribe tu vehiculo en RUAT"],
            cuanto_tarda: "Gestion en la Unidad de Vehiculos.",
            horario: "Lunes a viernes en horario habil.",
            consejo: "El decreto municipal 015/2024 regula todos los tramites de vehiculos en Sacaba.",
            c: "Segun tramite", t: "Gestion directa", dep: "Vehiculos",
            u: ""
        }
    },
    vehiculo_transferencia: {
        es: {
            n: "Transferencia de Vehiculo", icon: "\uD83D\uDD04",
            d: "Cambio de propietario (traspaso) de un vehiculo automotor registrado en el RUAT.",
            donde: "Unidad de Vehiculos - Municipalidad de Sacaba.",
            cuanto: "2 timbres municipales de Bs. 10 y folder administrativo.",
            que_necesito: ["Minuta de compra-venta (original y 2 ejemplares)","CRPVA original y fotocopia (RUAT 03)","Fotocopia de CI del comprador y vendedor","Fotografia fondo rojo 3x3 cm (persona natural)","2 timbres de Bs. 10","Folder administrativo","El vehiculo sin deudas tributarias"],
            como: ["Firma la minuta de compra-venta","Reune CRPVA, CI y fotografia","Cancela los timbres municipales","Presenta el expediente en la Unidad de Vehiculos","Se registra el cambio de propietario"],
            cuanto_tarda: "Gestion en la Unidad de Vehiculos.",
            horario: "Lunes a viernes en horario habil.",
            consejo: "El vehiculo no debe tener deudas: impuesto, gravamenes, reporte de robado ni bloqueos.",
            c: "2 timbres Bs. 10", t: "Gestion directa", dep: "Vehiculos",
            u: ""
        }
    },
    vehiculo_radicatoria: {
        es: {
            n: "Cambio de Radicatoria", icon: "\uD83D\uDE98",
            d: "Traslado del registro de un vehiculo desde otro departamento o provincia hacia Sacaba.",
            donde: "Unidad de Vehiculos - Municipalidad de Sacaba.",
            cuanto: "Timbre municipal de Bs. 40 y folder administrativo.",
            que_necesito: ["Minuta de compra-venta si hubo transferencia (original, 2 ejemplares)","CRPVA (RUAT 03) original y fotocopia","Fotocopia de CI vigente del propietario","Certificado de inscripcion a Impuestos Nacionales (si es juridico)","Fotografia fondo rojo 3x3 cm","Timbre de Bs. 40","Folder administrativo"],
            como: ["Reune CRPVA y documentos de identidad","Adjunta minuta si hubo transferencia","Cancela el timbre de Bs. 40","Presenta en la Unidad de Vehiculos","Queda radicado en Sacaba"],
            cuanto_tarda: "Gestion en la Unidad de Vehiculos.",
            horario: "Lunes a viernes en horario habil.",
            consejo: "El vehiculo no debe tener deudas ni reporte de robado para el cambio de radicatoria.",
            c: "Timbre Bs. 40", t: "Gestion directa", dep: "Vehiculos",
            u: ""
        }
    },
    vehiculo_baja: {
        es: {
            n: "Baja Tributaria del Vehiculo", icon: "\uD83D\uDEA8",
            d: "Dar de baja el vehiculo en el RUAT por siniestro, robo, exportacion o fuera de circulacion.",
            donde: "Unidad de Vehiculos - Municipalidad de Sacaba.",
            cuanto: "Timbre municipal de Bs. 20 y folder administrativo.",
            que_necesito: ["Formulario de solicitud (ANEXO 1)","CI vigente del propietario","CRPVA (RUAT 03) original y placas","Informe de Transito o DIPROVE (siniestro), denuncia (robo) o resolucion de Aduana (exportacion)","Sin deudas de impuestos","Timbre de Bs. 20","Folder administrativo"],
            como: ["Solicita el formulario ANEXO 1","Entrega CRPVA y placas originales","Acompaña el informe de transito, denuncia o resolucion","Cancela el timbre de Bs. 20","Se da de baja el vehiculo"],
            cuanto_tarda: "Gestion en la Unidad de Vehiculos.",
            horario: "Lunes a viernes en horario habil.",
            consejo: "Para baja por fuera de circulacion el vehiculo debe tener al menos 5 anios de radicatoria en Sacaba.",
            c: "Timbre Bs. 20", t: "Gestion directa", dep: "Vehiculos",
            u: ""
        }
    },
    vehiculo_reemplaque: {
        es: {
            n: "Reemplaque de Vehiculo", icon: "\uD83D\uDE93",
            d: "Obtencion de nuevas placas para vehiculos que no fueron reemplazados (sistema PTA).",
            donde: "Unidad de Vehiculos - Municipalidad de Sacaba.",
            cuanto: "Valores segun tramite (folder administrativo).",
            que_necesito: ["Declaracion Jurada de vehiculo no reemplacado emitida por GAMS","PTA/COPO original y fotocopia","Carnet de propiedad (sistema antiguo)","Fotocopia de CI vigente del propietario","Folder administrativo"],
            como: ["Solicita la declaracion jurada en GAMS","Reune PTA/COPO, carnet de propiedad y CI","Presenta el expediente en la Unidad de Vehiculos","Cancela los valores","Recibe las nuevas placas"],
            cuanto_tarda: "Gestion en la Unidad de Vehiculos.",
            horario: "Lunes a viernes en horario habil.",
            consejo: "Si hay transferencia, se tramita el reemplaque con la minuta de compra-venta.",
            c: "Segun tramite", t: "Gestion directa", dep: "Vehiculos",
            u: ""
        }
    }
};

var MULTAS = {
    es: {
        transito: {
            n: "Multas de Transito",
            items: [
                {f: "Exceso de velocidad", m: "Bs. 100 - 300"},
                {f: "Sin licencia de conducir", m: "Bs. 200 - 500"},
                {f: "Estacionamiento prohibido", m: "Bs. 50 - 100"},
                {f: "Pasar semaforo en rojo", m: "Bs. 100 - 200"},
                {f: "Manejar en estado de ebriedad", m: "Bs. 500 - 1,000"},
                {f: "Sin cinturon de seguridad", m: "Bs. 50 - 100"},
                {f: "Uso de celular manejando", m: "Bs. 100 - 200"}
            ]
        },
        municipales: {
            n: "Multas Municipales",
            items: [
                {f: "Arrojar basura en via publica", m: "Bs. 50 - 100"},
                {f: "Ruido despues de las 22:00", m: "Bs. 100 - 200"},
                {f: "Vender sin permiso", m: "Bs. 200 - 500"},
                {f: "Danar mobiliario municipal", m: "Bs. 100 - 300"},
                {f: "Construir sin permiso", m: "Bs. 500 - 2,000"}
            ]
        },
        pago: "**Procedimiento de Pago de Multas:**\n\n1. **Verifica tu multa** en la Unidad de Multas (Plaza Principal, Sacaba).\n2. **Recibe el recibo** con el monto y el codigo de pago.\n3. **Paga en estos puntos de Sacaba:**\n   - Caja Municipal - Plaza Principal 6 de Agosto\n   - Banco Union - Av. Blanco Galindo esq. Av. Eloy Salmon\n   - BNB / BISA (agencia central de Sacaba)\n   - **Con tu banca movil** (QR)\n4. **Pago por QR paso a paso:**\n   - Abre la app de tu banco (Banca Movil)\n   - Busca \"Pago QR\" o \"Escanear QR\"\n   - Escanea el codigo QR de la municipalidad en la ventanilla\n   - Escribe el monto exacto de la multa\n   - Confirma y guarda el comprobante\n5. **Conserva el comprobante** para acreditar tu pago.\n6. **Apelacion:** tienes 5 dias habiles para apelar la multa."
    },
    qu: {
        transito: {
            n: "Transito Multakuna",
            items: [
                {f: "Exceso de velocidad", m: "Bs. 100 - 300"},
                {f: "Mana licencia", m: "Bs. 200 - 500"},
                {f: "Prohibido aparca", m: "Bs. 50 - 100"},
                {f: "Semaforota mana kasukuy", m: "Bs. 100 - 200"},
                {f: "Machasqa maneja", m: "Bs. 500 - 1,000"},
                {f: "Cinturon mana churakuy", m: "Bs. 50 - 100"},
                {f: "Celularwan maneja", m: "Bs. 100 - 200"}
            ]
        },
        municipales: {
            n: "Munisipyu Multakuna",
            items: [
                {f: "Basurata wikchuy", m: "Bs. 50 - 100"},
                {f: "Ruido 22:00manta qhipa", m: "Bs. 100 - 200"},
                {f: "Mana permiso vendiy", m: "Bs. 200 - 500"},
                {f: "Mobiliariota pakiy", m: "Bs. 100 - 300"},
                {f: "Mana permiso construir", m: "Bs. 500 - 2,000"}
            ]
        },
        pago: "**Multata Pagaypaq:**\n\n1. **Multaykita qhaway** Multas Unidadpi (Plaza Principal, Sacaba).\n2. **Recibo chaskikuy** montowan pago codigowan.\n3. **Kay puntospi pagay Sacabapi:**\n   - Caja Municipal - Plaza Principal 6 de Agosto\n   - Banco Union - Av. Blanco Galindo esq. Av. Eloy Salmon\n   - BNB / BISA (Sacabaq agencia central)\n   - **Banca movil niqkiwan** (QR)\n4. **QRwan pagay paso a paso:**\n   - Banca movil (app) kiqay bankoykiqu\n   - \"Pago QR\" utaq \"Escanear QR\" opcionta maskay\n   - Municipalidad codigo QRta escanay ventanillapi\n   - Multa monto exactu qillqay\n   - Confirmay nitaq comprobanteta waqaychay\n5. **Comprobanteta waqaychay** pagasqaykita riqsichinaykipaq.\n6. **Apelacion:** 5 p'unchay llamkaq multata apelayta atiyki."
    }
};

var UI = {
    es: {
        title: "Asistente Municipal",
        sub: "En linea",
        ph: "Escribe o habla tu consulta...",
        powered: "IA ChatGPT - Munic. Sacaba",
        greeting: "\u00a1Hola! \ud83d\ude0a Soy el chatbot municipal de **Sacaba** y estoy para ayudarte. \u00bfNecesitas sacar tu **carnet de identidad**? \u00bfQuieres informaci\u00f3n sobre **tr\u00e1mites** como residencia, licencias o veh\u00edculos? \u00bfO tal vez sobre **multas y c\u00f3mo pagarlas**? D\u00edme, \u00bfen qu\u00e9 te ayudo hoy?",
        smalltalk: "\u00a1Bien, muy bien! \ud83d\ude0a Gracias por preguntar. Estoy para guiarte en tus tr\u00e1mites: carnet, residencia, licencias, catastro, veh\u00edculos y el pago de multas. \u00bfDe qu\u00e9 te gustar\u00eda informarte?",
        identity: "Soy **Tu Gobierno en Sacaba**, el asistente virtual oficial con inteligencia artificial del municipio. Te oriento en tr\u00e1mites como **carnet de identidad**, constancias, licencias, catastro, veh\u00edculos y te ayudo con **multas** (montos y pago en banco o con QR). Adem\u00e1s \u00a1aprendo de cada conversaci\u00f3n para ayudarte mejor!",
        greeting2: "Puedo ayudarte con:\n\n\ud83e\udeaa **Tr\u00e1mites** - Carnet, residencia, licencia, catastro, veh\u00edculos...\n\ud83d\udcb0 **Multas** - Montos, pago en banco o con QR\n\ud83d\udccb **Informaci\u00f3n** - Horarios, requisitos, costos\n\n**Preg\u00fandame lo que necesites o presiona el micr\u00f3fono para hablar:**",
        farewell: "\u00a1Gracias por tu consulta! \ud83d\ude0a Si tienes otra pregunta, escr\u00edbeme. \u00a1Que tengas un excelente d\u00eda!",
        greeting_opts: ["\ud83e\udeaa Ver tr\u00e1mites", "\ud83d\udcb0 Multas", "\ud83d\udd50 Horarios", "\ud83d\udcde Contacto"],
        tramite_opts: ["\ud83d\udccd Donde hago...?", "\ud83d\udcb0 Cuanto cuesta?", "\ud83d\udccb Que necesito?", "\ud83d\udcdd Como tramito...?"]
    },
    qu: {
        title: "Munisipyu Yanapay",
        sub: "Kachkani",
        ph: "Tapukuyniykita qillqay o wasinchik...",
        powered: "IA - Munis. Sakaba",
        greeting: "Imaynallan! \ud83d\udc4b Noqaqa **Sakaba Munisipyuq** asistente kachkani. Tramitekuna, multakuna nitaq serviciosmanta yanapayta atiymanni.",
        smalltalk: "Allinmi, allinmi kachkani! \ud83d\ude0a Tapukusqaykimanta yusulpayki. Sakaba municipalidadpaq tramite utaq servicio mañaptiykiqa kaypi kachkani. Imawan yanapaykayman?",
        identity: "Noqaqa **Sakaba Munisipyuq Asistente** kachkani, inteligencia artificialwan (ChatGPT) ruwasqa. Carnet, residencia, licencia, multas, horariospi yanapayta atiymi.",
        greeting2: "Kaykunapi yanapayta atiymi:\n\n\ud83e\udeaa **Tramitekuna** - Carnet, residencia, licencia...\n\ud83d\udcb0 **Multakuna** - Transito, munisipyu\n\ud83d\udccb **Yachaykuna** - Horarios, requisitokuna, qullqikuna\n\n**Imata munanki qillqaway utaq micrófonoqta rimariy:**",
        farewell: "\u00a1Yusulpayki! \ud83d\ude0a Huk tapukuypipas kaptinqa qillqaway. \u00a1Allin p'unchay kachun!",
        greeting_opts: ["\ud83e\udeaa Tramitekuna", "\ud83d\udcb0 Multakuna", "\ud83d\udd50 Horarios", "\ud83d\udcde Contacto"],
        tramite_opts: ["\ud83d\udccd Maypitaq?", "\ud83d\udcb0 Hayk'a qullqi?", "\ud83d\udccb Imatataq necesitani?", "\ud83d\udcdd Imaynataq tramitaykuni?"]
    }
};

/* ===== STATE ===== */
var S = { open: false, lang: 'es', busy: false, recording: false, mediaRecorder: null, audioChunks: [], recognition: null, sttFinal: '', sttHeard: false, log: [], silent: false, logoSrc: '/static/img/logo-sacaba.svg' };

/* ===== AUDIO EFFECTS ===== */
var AudioCtx = window.AudioContext || window.webkitAudioContext;
var audioCtx = null;

function playSound(type) {
    try {
        if (!audioCtx) audioCtx = new AudioCtx();
        var osc = audioCtx.createOscillator();
        var gain = audioCtx.createGain();
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        gain.gain.value = 0.05;
        if (type === 'open') { osc.frequency.value = 600; gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.15); }
        else if (type === 'message') { osc.frequency.value = 800; gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.1); }
        else if (type === 'send') { osc.frequency.value = 500; gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.08); }
        else if (type === 'record') { osc.frequency.value = 440; gain.gain.value = 0.08; gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.3); }
        else if (type === 'stop') { osc.frequency.value = 330; gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.2); }
        osc.start(audioCtx.currentTime);
        osc.stop(audioCtx.currentTime + 0.3);
    } catch(e) {}
}

/* ===== NLP ===== */
function detectTramite(text) {
    var t = text.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
    var patterns = [
        { keys: ['carnet','cedula','identidad','segepi','segip','biometrico','huellas'], key: 'carnet' },
        { keys: ['antecedentes','conducta','certificado de conducta','record policial','papelito'], key: 'carnet_conducta' },
        { keys: ['licencia de conducir','licencia de manejo','licencia para manejar','carnet de conducir'], key: 'licencia_conducir' },
        { keys: ['certificado de nacimiento','registro civil','partida de nacimiento','acta de nacimiento','nacimiento','certificado de matrimonio'], key: 'registro_civil' },
        { keys: ['residencia','constancia de residencia','vivo en'], key: 'residencia' },
        { keys: ['funcionamiento','licencia de funcionamiento','negocio','tienda','comercio','abrir negocio','patente'], key: 'funcionamiento' },
        { keys: ['construccion','construir','permiso de construccion','edificar','plano de vivienda','obra nueva'], key: 'construccion' },
        { keys: ['certificado catastral','catastral'], key: 'catastro_certificado' },
        { keys: ['empadronamiento','empadronar','registro predial','predio','catastro'], key: 'catastro_empadronamiento' },
        { keys: ['avaluo','avaluar','tasar','valor catastral'], key: 'catastro_avaluo' },
        { keys: ['propiedad','registro de propiedad','mi terreno','mi casa propia'], key: 'propiedad' },
        { keys: ['solteria','solteria','constancia de solteria','casarse','matrimonio','soltero'], key: 'solteria' },
        { keys: ['predial','prediales','impuesto','impuestos prediales'], key: 'prediales' },
        { keys: ['agua','agua potable','servicio de agua','conexion de agua'], key: 'agua' },
        { keys: ['evento','eventos','permiso para evento','fiesta','concierto','festival'], key: 'eventos' },
        { keys: ['aprobacion de plano','aprobacion de planos','plano de terreno','division de lotes','subdivision','anexion de terreno','regularizacion predial'], key: 'urbanismo_plano' },
        { keys: ['ampliacion','ampliar','remodelacion de casa','remodelar mi casa','remodelar'], key: 'urbanismo_ampliacion' },
        { keys: ['uso de suelo','rasante','linea nivel','zona y distrito','certificacion de urbanismo'], key: 'urbanismo_uso_suelo' },
        { keys: ['propiedad horizontal','condominio'], key: 'urbanismo_horizontal' },
        { keys: ['verja','cerco','muro'], key: 'urbanismo_verja' },
        { keys: ['no deuda','deuda','deudayuq','sin deuda','libre de deuda'], key: 'nodeuda' },
        { keys: ['transferencia','transferir','traspaso','traspasar','cambio de propietario','compra venta de vehiculo','comprar carro','comprar auto'], key: 'vehiculo_transferencia' },
        { keys: ['inscripcion de vehiculo','inscribir vehiculo','registrar mi vehiculo','registro de vehiculo nuevo','ruat'], key: 'vehiculo_inscripcion' },
        { keys: ['radicatoria','cambio de radicatoria'], key: 'vehiculo_radicatoria' },
        { keys: ['reemplaque','reemplacar','placas nuevas','cambio de placas'], key: 'vehiculo_reemplaque' },
        { keys: ['baja tributaria','dar de baja','baja del vehiculo','baja de vehiculo','siniestro vehicular'], key: 'vehiculo_baja' },
        { keys: ['vehiculo','vehiculos','registro de vehiculo','carro','auto','camioneta','placa'], key: 'vehiculos' }
    ];
    for (var i = 0; i < patterns.length; i++) {
        for (var j = 0; j < patterns[i].keys.length; j++) {
            if (t.indexOf(patterns[i].keys[j]) !== -1) return patterns[i].key;
        }
    }
    return null;
}

function detectIntent(text) {
    var t = text.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
    if (/^(hola|buenos|buenas|saludos|hey|imaynallan|napa|alli|kamisaki|que tal)/.test(t)) return 'greeting';
    if (/^(gracias|adios|chau|hasta|yusulpakuy|tupananchiskama|hamusaq)/.test(t)) return 'farewell';
    if (/como estas|cómo estás|como te sientes|como te encuentras|como te va|como estas tu|como van las cosas|allillanchu|allinllachu/.test(t)) return 'smalltalk';
    if (/quien eres|quién eres|quien sos|que eres|como te llamas|para que sirves|para que eres|que puedes hacer|iman kanki/.test(t)) return 'identity';
    if (/donde|dónde|ubicación|ubicacion|luhuynin|direction|dirección|mapa|maypitaq|maypi/.test(t)) return 'donde';
    if (/cuanto|cuánto|cuesta|costo|precio|chaki|cuantos|pagan|hayka|hayk'ataq|qullqi/.test(t)) return 'cuanto';
    if (/que necesito|qué necesito|requisitos|documentos|papeles|que llevo|que debo|imakunata|requisitokuna/.test(t)) return 'que_necesito';
    if (/como|cómo|pasos|procedimiento|hacer|tramito|gestiono|obtengo|sacar|proceso|imaynata/.test(t)) return 'como';
    if (/cuando|cuánto tarda|tiempo|plazo|dias|días|rapido|inmediato|duracion|hayka pacha/.test(t)) return 'cuando';
    if (/horario|horarios|atención|atencion|abierto|abren|hora|horariokuna/.test(t)) return 'horarios';
    if (/contacto|telefono|teléfono|correo|email|direccion|yupay/.test(t)) return 'contacto';
    if (/multa|multas|infraccion|panku|sancion|multakuna/.test(t)) return 'multas';
    if (/tramite|trámite|tramites|tramitekuna|lista|todos/.test(t)) return 'menu_tramites';
    if (/consejo|tip|recomendacion|consejos/.test(t)) return 'consejo';
    return 'question';
}

function buildCard(t, lang) {
    var qu = lang === 'qu';
    var L = qu ? {donde:"Maypi", costo:"Qullqi", tiempo:"Pacha", consejo:"Kunan", ub:"Ubicacion"} : {donde:"Donde", costo:"Costo", tiempo:"Tiempo", consejo:"Consejo", ub:"Ubicacion"};
    var lines = [];
    lines.push(t.icon + " **" + t.n + "**\n");
    lines.push(t.d + "\n");
    lines.push("\ud83d\udccd **" + L.donde + ":** " + t.donde);
    lines.push("\ud83d\udcb0 **" + L.costo + ":** " + t.c);
    lines.push("\u23f1 **" + L.tiempo + ":** " + t.t);
    if (t.consejo) lines.push("\ud83d\udca1 **" + L.consejo + ":** " + t.consejo);
    if (t.u) lines.push("\n\ud83d\uddfa **" + L.ub + ":** " + t.u);
    return lines.join("\n");
}

function tiempoEsAQu(textoES) {
    var t = (textoES || '').trim();
    var exactos = {
        'inmediato': 'Chaylla',
        'gestion directa': 'Usqaylla gestiona',
        'gestion directa.': 'Usqaylla gestiona',
        'segun proyecto': 'Proyecto nisqaman jina',
        'segun revision': 'Qhawariy nisqaman jina',
        '1 dia': "1 p'unchay"
    };
    var cl = t.toLowerCase();
    if (exactos[cl]) return exactos[cl];

    var m;
    m = t.match(/^([\d\s\-]+)\s*(dia|dias|semana|semanas)$/i);
    if (m) {
        var num = m[1].replace(/\s*-\s*/g, '-').trim();
        if (m[2].toLowerCase().indexOf('semana') === 0) return num + ' simana';
        return num + " p'unchay";
    }
    m = t.match(/^(\d+)\s*(?:dia|dias)?\s*al?\s*(\d+)\s*(dia|dias|semana|semanas)?$/i);
    if (m) {
        var a = m[1], b = m[2];
        if (m[3] && m[3].toLowerCase().indexOf('semana') === 0) return a + '-' + b + ' simana';
        return a + '-' + b + " p'unchay";
    }
    return t;
}

function buildTramiteList(lang) {
    var keys = Object.keys(KB);
    var lines = lang === 'qu' ? "\ud83d\udccb **Tramitekuna:**\n" : "\ud83d\udccb **Tramites Disponibles:**\n\n";
    keys.forEach(function(k, i) {
        var t = KB[k][lang] || KB[k].es;
        var tiempo = t.t;
        if (lang === 'qu' && KB[k].es && KB[k].es.t) tiempo = tiempoEsAQu(KB[k].es.t);
        lines += (i + 1) + ". " + t.icon + " **" + t.n + "** - " + t.c + " | " + tiempo + "\n";
    });
    lines += lang === 'qu' ? "\nIma tramite munanki? Qillqaway:" : "\nQue tramite te interesa? Preguntame:";
    return lines;
}

function buildMultasString(lang) {
    var m = MULTAS[lang];
    var lines = lang === 'qu' ? "\ud83d\udcb0 **Multakuna Yachay:**\n\n" : "\ud83d\udcb0 **Informacion de Multas:**\n\n";
    lines += "\ud83d\ude97 **Transito:**\n";
    m.transito.items.forEach(function(item) { lines += "- " + item.f + ": " + item.m + "\n"; });
    lines += lang === 'qu' ? "\n\ud83c\udfe2 **Munisipyu:**\n" : "\n\ud83c\udfe2 **Municipales:**\n";
    m.municipales.items.forEach(function(item) { lines += "- " + item.f + ": " + item.m + "\n"; });
    lines += "\n" + m.pago;
    return lines;
}

function getResp(msg) {
    var lang = S.lang;
    var intent = detectIntent(msg);
    var tramite = detectTramite(msg);

    if (intent === 'greeting') return UI[lang].greeting + "\n\n" + UI[lang].greeting2;
    if (intent === 'farewell') return UI[lang].farewell;
    if (intent === 'smalltalk') return UI[lang].smalltalk || UI.es.smalltalk;
    if (intent === 'identity') return UI[lang].identity || UI.es.identity;

    if (tramite) {
        var t = KB[tramite][lang] || KB[tramite].es;
        var qu = lang === 'qu';
        var L = qu ? {donde:"Maypi", costo:"Qullqi", tiempo:"Pacha", tiempoE:"Pacha", consejo:"Kunan", ub:"Ubicacion", req:"Requisitokuna", pasos:"Ruwanakuna", horario:"Horario"} : {donde:"Donde", costo:"Costo", tiempo:"Tiempo", tiempoE:"Tiempo estimado", consejo:"Consejo", ub:"Ubicacion", req:"Requisitos", pasos:"Procedimiento", horario:"Horario"};
        if (intent === 'donde') return t.icon + " **" + t.n + "**\n\n\ud83d\udccd " + t.donde + (t.donde_link ? "\n\n\ud83d\uddfa **" + L.ub + ":** " + t.donde_link : "");
        if (intent === 'cuanto') return t.icon + " **" + t.n + "**\n\n\ud83d\udcb0 **" + L.costo + ":** " + t.cuanto + "\n" + (t.cuanto_detail || "") + "\n\u23f1 **" + L.tiempo + ":** " + t.cuanto_tarda;
        if (intent === 'que_necesito') {
            var reqs = "\ud83d\udccb **" + t.n + " - " + L.req + ":**\n\n";
            t.que_necesito.forEach(function(r, i) { reqs += (i+1) + ". " + r + "\n"; });
            reqs += "\n\ud83d\udca1 " + L.consejo + ": " + t.consejo;
            return reqs;
        }
        if (intent === 'como') {
            var steps = "\ud83d\udcdd **" + t.n + " - " + L.pasos + ":**\n\n";
            t.como.forEach(function(s, i) { steps += (i + 1) + ". " + s + "\n"; });
            steps += "\n\u23f1 **" + L.tiempo + ":** " + t.cuanto_tarda;
            return steps;
        }
        if (intent === 'cuando') return t.icon + " **" + t.n + "**\n\n\u23f1 **" + L.tiempoE + ":** " + t.cuanto_tarda + "\n\ud83d\udd50 **" + L.horario + ":** " + t.horario;
        if (intent === 'consejo') return t.icon + " **" + t.n + "**\n\n\ud83d\udca1 **" + L.consejo + ":** " + t.consejo;
        return buildCard(t, lang);
    }

    if (intent === 'multas') return buildMultasString(lang);
    if (intent === 'horarios') return lang === 'qu' ?
        "\ud83d\udd50 **Horario Atencion:**\n- Lun-Vie: 8:00 - 12:00 / 14:30 - 18:30\n- Sab: 8:00 - 12:00\n- Dom: Wisqasqa" :
        "\ud83d\udd50 **Horarios de Atencion:**\n- Lunes a Viernes: 8:00 - 12:00 / 14:30 - 18:30\n- Sabados: 8:00 - 12:00\n- Domingos: Cerrado";
    if (intent === 'contacto') return "\ud83d\udcde **Contacto - Municipal de Sacaba:**\n\n- \ud83d\udcf1 Tel: (591) 4-XXXXXX\n- \ud83d\udce7 Email: info@sacaba.gob.bo\n- \ud83d\uddfa SEGIP: https://maps.app.goo.gl/f27gLh5Accp2UmKW9\n- \ud83c\udf10 Web: sacaba.gob.bo";
    if (intent === 'menu_tramites') return buildTramiteList(lang);

    /* APRENDIZAJE: comando "aprende: pregunta = respuesta" */
    var lc = parseLearnCommand(msg);
    if (lc) {
        var stored = storeLearned(lc.q, lc.a);
        return "\ud83d\udca1 \u00a1Listo! He aprendido esa respuesta. De ahora en adelante la usar\u00e9 para ayudarte mejor.";
    }
    var learned = lookupLearned(msg);
    if (learned) return "\ud83d\udca1 " + learned;

    return lang === 'qu' ?
        "\ud83e\udd14 A\u00fan no tengo la respuesta a esa consulta, pero **puedo aprenderla**. Escribe **aprende: tu pregunta = tu respuesta**. Ejemplo:\n`aprende: \u00bfcu\u00e1nto cuesta el certificado? = Bs. 10`\n\nMientras, te recuerdo:\n\n- \ud83e\udeaa \"\u00bfC\u00f3mo saco mi carnet?\"\n- \ud83d\udccd \"\u00bfD\u00f3nde hago la residencia?\"\n- \ud83d\udcb0 \"\u00bfCu\u00e1nto cuesta la licencia?\"\n- \ud83d\udc54 \"\u00bfQu\u00e9 necesito para...?\"" :
        "\ud83e\udd14 A\u00fan no tengo la respuesta a esa consulta, pero **puedo aprenderla**. Ay\u00fadame escribiendo:\n\n**aprende: tu pregunta = la respuesta**\n\nEjemplo:\n`aprende: \u00bfcu\u00e1nto cuesta el certificado? = Bs. 10`\n\nO consulta estos temas:\n\n- \ud83e\udeaa \"\u00bfC\u00f3mo saco mi carnet?\"\n- \ud83d\udccd \"\u00bfD\u00f3nde hago la residencia?\"\n- \ud83d\udcb0 \"\u00bfCu\u00e1nto cuesta la licencia?\"\n- \ud83d\udc54 \"\u00bfQu\u00e9 necesito para...?\"";
}

function getOpts() { return UI[S.lang].opts || UI[S.lang].greeting_opts; }

/* ===== APRENDIZAJE local en el widget (memoria por navegador) ===== */
var LEARN_KEY = 'sacaba_aprendido_v1';
function loadLearned() {
    try { return JSON.parse(localStorage.getItem(LEARN_KEY)) || []; } catch (e) { return []; }
}
function saveLearned(list) {
    try { localStorage.setItem(LEARN_KEY, JSON.stringify(list)); } catch (e) {}
}
function pubTokens(t) {
    var norms = (t || '').toLowerCase(); var out = [];
    var parts = norms.split(/[^a-z\u00e0-\u00ff]+/);
    for (var i = 0; i < parts.length; i++) { var p = parts[i]; if (p.length > 2) out.push(p); }
    return out;
}
function similarEnough(stored, qList) {
    if (!qList.length) return false;
    var sList = stored.qt || [];
    if (!sList.length) return false;
    var hit = 0; for (var i = 0; i < sList.length; i++) { if (qList.indexOf(sList[i]) >= 0) hit++; }
    return (hit / Math.max(sList.length, qList.length)) >= 0.5;
}
function parseLearnCommand(msg) {
    var low = (msg || '').toLowerCase();
    if (low.indexOf('aprende') === -1) return null;
    var idx = low.indexOf('aprende');
    var body = msg.slice(idx + 'aprende'.length).replace(/^:?\s*/, '');
    var eq = body.indexOf('=');
    if (eq === -1) return null;
    var q = body.slice(0, eq).replace(/^["']|["']$/g, '').trim();
    var a = body.slice(eq + 1).replace(/^["']|["']$/g, '').trim();
    if (!q || !a) return null;
    return { q: q, a: a };
}
function storeLearned(q, a) {
    var list = loadLearned(); var qt = pubTokens(q); var qf = q.toLowerCase();
    for (var i = 0; i < list.length; i++) { if (list[i].qf === qf) { list[i].a = a; saveLearned(list); return true; } }
    list.push({ q: q, qt: qt, qf: qf, a: a });
    saveLearned(list); return true;
}
function lookupLearned(msg) {
    var list = loadLearned(); if (!list.length) return null;
    var qList = pubTokens(msg); var qf = msg.toLowerCase();
    var best = null; var bestRatio = 0;
    for (var i = 0; i < list.length; i++) {
        if (list[i].qf === qf) return list[i].a;
        if (similarEnough(list[i], qList)) {
            var inter = 0; var s = list[i].qt || [];
            for (var j = 0; j < s.length; j++) { if (qList.indexOf(s[j]) >= 0) inter++; }
            var ratio = inter / Math.max(1, (new Set(s.concat(qList))).size);
            if (ratio > bestRatio) { bestRatio = ratio; best = list[i].a; }
        }
    }
    return best;
}

/* ===== AUDIO/VIDA: RECONOCIMIENTO EN VIVO (tecleo) o grabacion de audio ===== */
function startRecording() {
    stopSpeaking();
    if (S.recording) return stopRecording();
    var SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (S.lang !== 'qu' && SR) { startLiveSTT(SR); }
    else { startAudioRecording(); }
}

function startLiveSTT(SR) {
    var inp = document.getElementById('cw-in');
    var rec = new SR();
    S.sttFinal = '';
    S.sttHeard = false;
    rec.lang = 'es-BO';
    rec.continuous = true;
    rec.interimResults = true;
    rec.maxAlternatives = 1;
    rec.onresult = function(event) {
        S.sttHeard = true;
        var finalText = '';
        var interim = '';
        for (var i = event.resultIndex; i < event.results.length; i++) {
            var r = event.results[i];
            if (r.isFinal) { finalText += r[0].transcript + ' '; }
            else { interim += r[0].transcript; }
        }
        S.sttFinal += finalText;
        inp.value = S.sttFinal + (interim ? ' ' + interim : '');
        var msgs = document.getElementById('cw-msgs');
        msgs.scrollTop = msgs.scrollHeight;
    };
    rec.onerror = function(event) {
        if (event.error === 'not-allowed' || event.error === 'service-not-allowed') {
            addMsg("No se pudo acceder al microfono. Verifica los permisos del navegador.", 'bot');
        } else if (event.error === 'no-speech') {
            // se espera que termine onend y se avise
        } else {
            // navegador o idioma no soportado -> grabar y transcribir en el servidor
            try { rec.abort(); } catch (e) {}
            S.recognition = null;
            S.recording = false;
            updateMicUI(false);
            startAudioRecording();
        }
    };
    rec.onend = function() {
        S.recording = false;
        S.recognition = null;
        updateMicUI(false);
        var msg = (S.sttFinal || '').trim();
        S.sttFinal = '';
        if (!S.sttHeard) {
            addMsg("No pude escuchar nada. Intenta de nuevo hablando mas claro.", 'bot');
            return;
        }
        if (msg) {
            inp.value = '';
            addMsg(msg, 'user');
            playSound('send');
            document.getElementById('cw-opts').innerHTML = '';
            setTimeout(function() { sendToAI(msg); }, 200);
        }
    };
    S.recognition = rec;
    S.recording = true;
    updateMicUI(true);
    playSound('record');
    rec.start();
}

function startAudioRecording() {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        addMsg("Tu navegador no soporta reconocimiento de voz. Usa Chrome o Edge, o escribe tu mensaje.", 'bot');
        return;
    }
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(function(stream) {
            S.recording = true;
            S.audioChunks = [];
            S.mediaRecorder = new MediaRecorder(stream);
            S.mediaRecorder.ondataavailable = function(e) { if (e.data.size > 0) S.audioChunks.push(e.data); };
            S.mediaRecorder.onstop = function() {
                stream.getTracks().forEach(function(t) { t.stop(); });
                processAudio();
            };
            S.mediaRecorder.start();
            updateMicUI(true);
            playSound('record');
        })
        .catch(function(err) {
            addMsg("No se pudo acceder al microfono. Verifica los permisos del navegador.", 'bot');
        });
}

function stopRecording() {
    if (S.recognition && S.recording) { S.recognition.stop(); return; }
    if (S.mediaRecorder && S.recording) {
        S.recording = false;
        S.mediaRecorder.stop();
        updateMicUI(false);
        playSound('stop');
    }
}

function processAudio() {
    if (S.audioChunks.length === 0) return;
    var blob = new Blob(S.audioChunks, { type: 'audio/webm' });
    var reader = new FileReader();
    reader.onload = function() {
        var b64 = reader.result.split(',')[1];
        addMsg("\ud83c\udfa4 Grabando audio...", 'user');
        showTyping();

        fetch('/audio-to-text', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ audio: b64, language: S.lang })
        })
        .then(function(r) { return r.json(); })
        .then(function(data) {
            hideTyping();
            if (data.error) {
                addMsg("Error al procesar audio: " + data.error, 'bot');
                return;
            }
            var text = data.text || '';
            if (!text.trim()) {
                addMsg("No pude escuchar nada. Intenta de nuevo hablando mas claro.", 'bot');
                return;
            }
            document.getElementById('cw-msgs').lastChild.remove();
            addMsg(text, 'user');
            playSound('send');
            sendToAI(text);
        })
        .catch(function(err) {
            hideTyping();
            addMsg("Error de conexion al procesar audio.", 'bot');
        });
    };
    reader.readAsDataURL(blob);
}

function updateMicUI(isRecording) {
    var micBtn = document.getElementById('cw-mic');
    if (!micBtn) return;
    if (isRecording) {
        micBtn.classList.add('recording');
        micBtn.innerHTML = '<svg viewBox="0 0 24 24"><rect x="6" y="6" width="12" height="12" rx="2" fill="white"/></svg>';
    } else {
        micBtn.classList.remove('recording');
        micBtn.innerHTML = '<svg viewBox="0 0 24 24"><path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3zm-1-9c0-.55.45-1 1-1s1 .45 1 1v6c0 .55-.45 1-1 1s-1-.45-1-1V5z"/><path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"/></svg>';
    }
}

/* ===== ENVIAR A AI ===== */
function sendToAI(text) {
    S.busy = true;
    showTyping();

    fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text, language: S.lang === 'qu' ? 'qu' : 'auto', useAI: true })
    })
    .then(function(r) { return r.json(); })
    .then(function(data) {
        hideTyping();
        var resp = data.response || UI[S.lang].default;
        addMsg(resp, 'bot');
        S.log.push({ type: 'user', text: text });
        S.log.push({ type: 'bot', query: text, resp: resp });
        playSound('message');
        var tramite = detectTramite(text);
        if (tramite) {
            setTimeout(function() { showOpts(UI[S.lang].tramite_opts); }, 500);
        } else {
            setTimeout(function() { showOpts(getOpts()); }, 500);
        }
        S.busy = false;
    })
    .catch(function() {
        hideTyping();
        var resp = getResp(text);
        addMsg(resp, 'bot');
        S.log.push({ type: 'user', text: text });
        S.log.push({ type: 'bot', query: text, resp: resp });
        playSound('message');
        S.busy = false;
    });
}

/* ===== SPEAK RESPONSE (voz natural en espanol, menos robotica) ===== */
function pickEspVoice(needQu) {
    var voices = window.speechSynthesis.getVoices();
    if (!voices || !voices.length) return null;
    var pool = [];
    for (var i = 0; i < voices.length; i++) {
        var l = (voices[i].lang || '').toLowerCase();
        if (needQu && (l.indexOf('qu') === 0 || l.indexOf('quz') === 0 || l.indexOf('ay') === 0)) pool.push(voices[i]);
        else if (!needQu && l.indexOf('es') === 0) pool.push(voices[i]);
    }
    if (!pool.length) {
        for (var k = 0; k < voices.length; k++) {
            var lk = (voices[k].lang || '').toLowerCase();
            if (needQu ? lk.indexOf('es') === 0 : lk.indexOf('es') === 0) pool.push(voices[k]);
        }
    }
    if (!pool.length) return null;

    var female = /helena|sabina|andrea|laura|marta|maria|mari[aá]|raquel|camila|elena|fernanda|paulina|karina|silvia|sonia|paloma|patricia|rosa|valeria|julia|sofia|sara|nuria|lupe|delia|esmeralda|gabriela|evita|dalia|gemma|alba|carmen|adriana|miguel|raul|jorge|pablo|diego|luis|antonio|francisco|jose|pedro/i;
    var best = null;
    var bestScore = -1;
    for (var j = 0; j < pool.length; j++) {
        var v = pool[j];
        var nm = v.name || '';
        var score = 0;
        if (/sabina|helena|gd_/i.test(nm)) score += 60;
        if (/natural|neural|online|premium|wavenet|xbox|narrator/i.test(nm)) score += 45;
        if (/microsoft|edge|google/i.test(nm)) score += 20;
        if (/\b(es-mx|es-es|qu-pe|qu-ec|quz)\b/i.test(v.lang)) score += 8;
        if (female.test(nm)) score += 12;
        if (/local/i.test(nm)) score -= 40;
        if (score > bestScore) { bestScore = score; best = v; }
    }
    return best || pool[0];
}

function stopSpeaking() {
    if (window.speechSynthesis) window.speechSynthesis.cancel();
}

function speakText(text, lang) {
    if (!window.speechSynthesis) return;
    window.speechSynthesis.cancel();
    var clean = String(text)
        // 1) Quitar enlaces y citas antes de limpiar simbolos.
        .replace(/\[([^\]]+)\]\([^)]*\)/g, '$1')
        .replace(/https?:\/\/\S+/g, ' ')
        .replace(/&nbsp;/g, ' ')
        .replace(/&amp;/g, 'y')
        // 2) Unidades y abreviaturas para leer con naturalidad.
        .replace(/\bBs\.?\s*(\d+(?:[.,]\d+)?)/gi, '$1 bolivianos')
        .replace(/\bAv\.\b/gi, 'avenida')
        .replace(/\bSt\.\b/gi, 'santo')
        // 3) Listas y saltos de linea -> frases fluidas con pausa.
        .replace(/^\s*[-•·◦▪–—]\s*/gm, '')
        .replace(/\n{2,}/g, '. ')
        .replace(/\n/g, '. ')
        // 4) QUITAR TODO LO QUE NO SEA LETRA, NUMERO, ESPACIO O PUNTUACION BASICA.
        //    Asi la voz NUNCA pronuncia emojis ni simbolos (cualquier rango Unicode).
        .replace(/[^\p{L}\p{N}\s.,;:!?¿¡'"()%+/&@-]/gu, ' ')
        // 5) Puntuacion: pausa despues de cada signo, sin romper decimales ni abreviaturas.
        .replace(/([,;:!?¿¡.])(?![ \s\d])/g, '$1 ')
        .replace(/\s+([,.!?;:])/g, '$1')
        .replace(/\s+/g, ' ')
        .replace(/^[.?\s]+/, '')
        .trim();

    if (!clean) return;
    if (clean.length > 600) clean = clean.substring(0, 600).replace(/[^.!?;:]*$/, '') + '...';

    var utterance = new SpeechSynthesisUtterance(clean);
    // Voz conversacional natural: velocidad un poco mas lenta y tono calido,
    // para que la voz (Sabina/Helena/Google) se entienda con claridad.
    var qu = lang === 'qu';
    utterance.rate = qu ? 0.92 : 0.96;
    utterance.pitch = 1.02;
    var v = pickEspVoice(qu);
    if (v) {
        utterance.voice = v;
        utterance.lang = v.lang;
    } else {
        utterance.lang = qu ? 'es-BO' : 'es-BO';
    }
    window.speechSynthesis.speak(utterance);
}

/* ===== CONSTRUIR HTML ===== */
function buildHTML() {
    return '<button class="cw-fab" id="cw-fab">' +
        '<span class="cw-pulse"></span>' +
        '<img class="cw-fab-logo" src="/static/img/logo-sacaba.svg" alt="Asistente Municipal de Sacaba">' +
        '<svg class="cw-fab-close" viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg>' +
        '<span class="cw-badge" id="cw-badge">1</span></button>' +
    '<div class="cw-window" id="cw-window">' +
        '<div class="cw-header"><div class="cw-h-left"><div class="cw-h-avatar"><img class="cw-h-logo" src="/static/img/logo-sacaba.svg" alt="Escudo de Sacaba"></div>' +
        '<div class="cw-h-info"><h3 id="cw-title">' + UI.es.title + '</h3><span id="cw-sub"><span class="cw-online-dot"></span>' + UI.es.sub + '</span></div></div>' +
        '<div class="cw-h-actions">' +
            '<div class="cw-lang"><button class="active" data-lang="es">ES</button><button data-lang="qu">QU</button></div>' +
        '</div></div>' +
        '<div class="cw-msgs" id="cw-msgs"></div>' +
        '<div class="cw-typing" id="cw-typing"><span></span><span></span><span></span></div>' +
        '<div class="cw-opts" id="cw-opts"></div>' +
        '<div class="cw-input">' +
            '<button id="cw-mic" class="cw-mic-btn" title="Hablar - Grabar audio"><svg viewBox="0 0 24 24"><path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3zm-1-9c0-.55.45-1 1-1s1 .45 1 1v6c0 .55-.45 1-1 1s-1-.45-1-1V5z"/><path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"/></svg></button>' +
            '<input type="text" id="cw-in" placeholder="' + UI.es.ph + '" autocomplete="off">' +
            '<button id="cw-send" title="Enviar mensaje"><svg viewBox="0 0 24 24"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/></svg></button>' +
        '</div>' +
        '<div class="cw-powered">' + UI.es.powered + '</div></div>';
}

function addMsg(text, type) {
    if (type === 'user') stopSpeaking();
    var msgs = document.getElementById('cw-msgs');
    var d = document.createElement('div');
    d.className = 'cw-msg ' + type;
    var av = type === 'bot' ? '<div class="cw-msg-av"><img src="' + S.logoSrc + '" alt="Sacaba"></div>' : '<div class="cw-msg-av"><i class="fas fa-user"></i></div>';
    var formatted = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/\n/g, '<br>');
    var speakBtn = type === 'bot' ? '<button class="cw-speak-btn" onclick="window._speakMsg(this)" title="Escuchar respuesta"><svg viewBox="0 0 24 24" width="14" height="14"><path d="M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z"/></svg></button>' : '';
    d.innerHTML = av + '<div class="cw-msg-b">' + formatted + '</div>' + speakBtn;
    msgs.appendChild(d);
    msgs.scrollTop = msgs.scrollHeight;
    if (type === 'bot' && !S.silent) speakText(text, S.lang);
}

window._speakMsg = function(btn) {
    var msgEl = btn.closest('.cw-msg');
    if (msgEl) {
        var textEl = msgEl.querySelector('.cw-msg-b');
        if (textEl) speakText(textEl.textContent, S.lang);
    }
};

function showTyping() {
    document.getElementById('cw-typing').classList.add('show');
    var msgs = document.getElementById('cw-msgs');
    msgs.scrollTop = msgs.scrollHeight;
}

function hideTyping() {
    document.getElementById('cw-typing').classList.remove('show');
}

function showOpts(opts) {
    var c = document.getElementById('cw-opts');
    c.innerHTML = '';
    opts.forEach(function(o) {
        var b = document.createElement('button');
        b.className = 'cw-opt';
        b.textContent = o;
        b.onclick = function() {
            addMsg(o, 'user');
            c.innerHTML = '';
            playSound('send');
            sendToAI(o);
        };
        c.appendChild(b);
    });
}

/* ===== RE-RENDER conversacion traducida (ES <-> QU) ===== */
function translateUser(text, lang) {
    if (lang === 'es') {
        if (text === 'Tramitekuna' || text === '🪪 Tramitekuna') return 'Trámites';
        if (text === 'Multakuna' || text === '💵 Multakuna') return 'Multas';
        if (text === 'Yusulpayki' || text === 'Imaynata' || text === 'Haykataq') return text;
    }
    return text;
}

function renderConversation(lang) {
    var msgs = document.getElementById('cw-msgs');
    msgs.innerHTML = '';
    document.getElementById('cw-opts').innerHTML = '';
    S.silent = true;

    if (!S.log.length) {
        showTyping();
        setTimeout(function() {
            hideTyping();
            S.silent = false;
            addMsg(UI[lang].greeting, 'bot');
            setTimeout(function() {
                addMsg(UI[lang].greeting2, 'bot');
                showOpts(UI[lang].greeting_opts);
            }, 500);
        }, 400);
        return;
    }

    var i = 0;
    function next() {
        if (i >= S.log.length) {
            S.silent = false;
            showOpts(getOpts());
            S.busy = false;
            return;
        }
        var entry = S.log[i]; i++;
        if (entry.type === 'user') {
            addMsg(translateUser(entry.text, lang), 'user');
            next();
        } else {
            fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: entry.query, language: lang === 'qu' ? 'qu' : 'auto', useAI: false })
            }).then(function(r) { return r.json(); })
              .then(function(data) {
                  addMsg(data.response || getResp(entry.query), 'bot');
                  next();
              })
              .catch(function() {
                  addMsg(getResp(entry.query), 'bot');
                  next();
              });
        }
    }
    next();
}

function init() {
    var el = document.getElementById('chatbot-widget');
    if (!el) return;
    el.innerHTML = buildHTML();

    document.getElementById('cw-fab').onclick = function() {
        S.open = !S.open;
        document.getElementById('cw-window').classList.toggle('open', S.open);
        document.getElementById('cw-fab').classList.toggle('open', S.open);
        document.getElementById('cw-badge').style.display = 'none';
        playSound('open');
        if (S.open && document.getElementById('cw-msgs').children.length === 0) {
            showTyping();
            setTimeout(function() {
                hideTyping();
                addMsg(UI[S.lang].greeting, 'bot');
                playSound('message');
                setTimeout(function() {
                    addMsg(UI[S.lang].greeting2, 'bot');
                    showOpts(UI[S.lang].greeting_opts);
                }, 600);
            }, 1000);
        }
    };

    document.getElementById('cw-send').onclick = function() {
        var inp = document.getElementById('cw-in');
        var msg = inp.value.trim();
        if (!msg || S.busy) return;
        addMsg(msg, 'user');
        inp.value = '';
        playSound('send');
        document.getElementById('cw-opts').innerHTML = '';
        sendToAI(msg);
    };

    document.getElementById('cw-in').onkeydown = function() { stopSpeaking(); };
    document.getElementById('cw-in').onkeypress = function(e) {
        if (e.key === 'Enter') document.getElementById('cw-send').click();
    };

    document.getElementById('cw-mic').onclick = function() { startRecording(); };

    document.querySelectorAll('.cw-lang button').forEach(function(btn) {
        btn.onclick = function() {
            if (S.lang === this.dataset.lang) return;
            S.lang = this.dataset.lang;
            document.querySelectorAll('.cw-lang button').forEach(function(b) { b.classList.remove('active'); });
            this.classList.add('active');
            document.getElementById('cw-title').textContent = UI[S.lang].title;
            document.getElementById('cw-sub').innerHTML = '<span class="cw-online-dot"></span>' + UI[S.lang].sub;
            document.getElementById('cw-in').placeholder = UI[S.lang].ph;
            document.querySelector('.cw-powered').textContent = UI[S.lang].powered;
            renderConversation(S.lang);
        };
    });

    setTimeout(function() { document.getElementById('cw-badge').style.display = 'flex'; }, 2000);

    if (window.speechSynthesis) {
        window.speechSynthesis.onvoiceschanged = function() { window.speechSynthesis.getVoices(); };
    }
}

window.initChatbotWidget = init;
window.openChatbot = function() { if (!S.open) document.getElementById('cw-fab').click(); };
window.openChatWithQuery = function(q) {
    if (!S.open) document.getElementById('cw-fab').click();
    setTimeout(function() {
        addMsg(q, 'user');
        playSound('send');
        document.getElementById('cw-opts').innerHTML = '';
        sendToAI(q);
    }, 400);
};

})();
