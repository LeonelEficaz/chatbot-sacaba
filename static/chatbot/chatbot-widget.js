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
        presentando: "Escuchando la presentaci\u00f3n...",
        powered: "Sami - Municipio de Sacaba",
        greeting: "\u00a1Hola! \ud83d\ude0a Soy **Sami**, tu asistente municipal de Sacaba. Cu\u00e9ntame qu\u00e9 necesitas y preparo la ficha completa en pantalla mientras conversamos.",
        smalltalk: "\u00a1Muy bien, gracias por preguntar! \ud83d\ude0a \u00bfEn qu\u00e9 tr\u00e1mite te acompa\u00f1o hoy?",
        identity: "Soy **Sami**, la asistente del Municipio de Sacaba. Te oriento en tr\u00e1mites, licencias, catastro, veh\u00edculos y multas, y te muestro la ficha completa mientras conversamos.",
        greeting2: "Preg\u00fantame como se lo dir\u00edas a una amiga: \u00abquiero sacar mi carnet\u00bb, \u00aby d\u00f3nde pago mi multa?\u00bb.",
        farewell: "\u00a1Gracias a ti! \ud83d\ude0a Que te vaya muy bien en tu tr\u00e1mite.",
        greeting_opts: ["\u2728 Ver consultas disponibles"],
        consultas_btn: "\u2728 Ver consultas disponibles",
        consultas_titulo: "\ud83d\udccb Consultas disponibles",
        consultas_hint: "Toca una consulta y te la explico con datos oficiales.",
        consultas_volver: "\u2190 Volver",
        consulta_prefijo: "Quiero consultar sobre ",
        escuchando: "Te escucho...",
        no_entendi: "No pude escuchar bien. \u00bfMe lo repites, por favor?",
        manos_libres_on: "Modo manos libres activo. Di \u00abSami...\u00bb y te escucho.",
        manos_libres_off: "Modo manos libres desactivado.",
        wake_ack: "\u00bfS\u00ed? Te escucho.",
        stop_ack: "Listo, me quedo en silencio. \ud83d\ude0a",
        mic_denegado: "No tengo permiso para usar el micr\u00f3fono. Toca el candado de la barra de direcciones, permite el micr\u00f3fono y vuelve a intentar.",
        mic_error: "No pude escuchar. Revisa tu micr\u00f3fono o escr\u00edbeme la consulta.",
        mic_inseguro: "El navegador solo permite el micr\u00f3fono en localhost o HTTPS. Abre el portal en http://127.0.0.1:5000 y vuelve a probar.",
        mic_no_soportado: "Este navegador no permite dictado por voz. Abre Sami en Microsoft Edge o Google Chrome.",
        mic_sin_equipo: "No encuentro un micr\u00f3fono conectado. Revisa que est\u00e9 enchufado y activo en Windows.",
        mic_ocupado: "Otro programa est\u00e1 usando el micr\u00f3fono. Ci\u00e9rralo y vuelve a intentar.",
        mic_red: "El servicio de voz del navegador no respondi\u00f3. Revisa tu conexi\u00f3n a internet e int\u00e9ntalo otra vez.",
        mic_espera: "Pidiendo permiso para el micr\u00f3fono...",
        idioma_ack: "\u00a1Listo! Desde ahora te hablo en **espa\u00f1ol**. \u00bfEn qu\u00e9 te ayudo?",
        idioma_corto: "Ahora te hablo en espa\u00f1ol.",
        tramite_opts: []
    },
    qu: {
        title: "Munisipyu Yanapay",
        sub: "Kachkani",
        ph: "Tapukuyniykita qillqay utaq rimay...",
        presentando: "Napaykuta uyarishayku...",
        powered: "Sami - Sakaba Munisipyu",
        greeting: "Imaynallan! \ud83d\udc4b Noqaqa **Sami**, Sakaba Munisipyuq yanapayniyki. Imata munanki niway, noqataq pantallapi fichata rikuchisaq.",
        smalltalk: "Allinmi, tapukusqaykimanta yusulpayki! \ud83d\ude0a \u00bfIma tramitepi yanapaykayman?",
        identity: "Noqaqa **Sami** kani, Sakaba Munisipyuq yanapaq. Tramitekuna, licenciakuna, catastro, carrokuna nitaq multakunapi yanapayta atiymi.",
        greeting2: "Tapuway imayna rimasqaykita: \u00abcarnetyta horqoyta munani\u00bb, \u00abmaypitaq multayta pagani?\u00bb.",
        farewell: "\u00a1Yusulpayki! \ud83d\ude0a Allin p'unchay kachun.",
        greeting_opts: ["\u2728 Tapukuykunata qhaway"],
        consultas_btn: "\u2728 Tapukuykunata qhaway",
        consultas_titulo: "\ud83d\udccb Tapukuykuna",
        consultas_hint: "Huk tapukuyta akllay, chiqa willaywan willasqayki.",
        consultas_volver: "\u2190 Kutiy",
        consulta_prefijo: "Tapuyta munani kaymanta: ",
        escuchando: "Uyarishayki...",
        no_entendi: "Allinta uyarirqanichu. \u00bfKutin niway, ama hina kaspa?",
        manos_libres_on: "Manos libres kachkan. \u00abSami...\u00bb niy, uyarisqayki.",
        manos_libres_off: "Manos libres wa\u00f1uchisqa.",
        wake_ack: "\u00bfAr\u00ed? Uyarishayki.",
        stop_ack: "Ar\u00ed, ch'inlla\u00f1a kasqani. \ud83d\ude0a",
        mic_denegado: "Micr\u00f3fonoq permisonniyuq kani\u00f1achu. Barra de direccionespi candadota kichay, micr\u00f3fonota saqilliy, hinaspa kutiy.",
        mic_error: "Manan uyarirqanichu. Micr\u00f3fonoykita qhaway utaq qillqaway.",
        mic_inseguro: "Navegadorqa localhost utaq HTTPS llallipim micr\u00f3fonota saqillin. http://127.0.0.1:5000 llallipim kichay.",
        mic_no_soportado: "Kay navegadorqa rimay dictadota manan saqillinchu. Microsoft Edge utaq Google Chrome llallipim Samita kichay.",
        mic_sin_equipo: "Manan micr\u00f3fonota tarinichu. Enchufasqa kasqanta qhaway.",
        mic_ocupado: "Huk programa micr\u00f3fonota apaykachashan. Chayta wisq'ay hinaspa kutiy.",
        mic_red: "Navegadorpa rimayninqa manan kutichinchu. Internetniykita qhaway hinaspa kutiy.",
        mic_espera: "Micr\u00f3fonoq permisonta mashkhaspa...",
        idioma_ack: "\u00a1Ar\u00ed! Kunanmanta **quechua**pi rimasaq. \u00bfImawan yanapaykayman?",
        idioma_corto: "Kunanmanta quechuapi rimasaq.",
        tramite_opts: []
    }
};

/* ===== STATE ===== */
var S = { open: false, lang: 'es', busy: false, recording: false, recognition: null, hfPause: false, sttFallo: false, sttFinal: '', sttHeard: false, log: [], silent: false, silentFijo: false, embedded: false, voice: true, audio: null, speakSeq: 0, logoSrc: '/static/img/sami-gato.svg', handsFree: false, speaking: false, consultas: false, sttTimer: null, restartSTT: false, vozCola: [], vozActual: null, vozOcupada: false, vozGen: 0, presentado: false, presentando: false, bloqueado: false, autoListen: false, autoTurno: false, autoIntentos: 0, micListo: null, modoServidor: false, recLang: null, sttReintento: false };

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

function getOpts() {
    var o = UI[S.lang].greeting_opts || [];
    return [UI[S.lang].consultas_btn || o[0] || 'Consultas'];
}

/* ===== CONSULTAS DISPONIBLES (unica lista predeterminada) ===== */
function consultasDisponibles() {
    var keys = Object.keys(KB);
    var items = [];
    for (var i = 0; i < keys.length; i++) {
        var t = KB[keys[i]][S.lang] || KB[keys[i]].es;
        if (t && t.n) items.push(t.n);
    }
    return items;
}

function showConsultas() {
    var c = document.getElementById('cw-opts');
    if (!c) return;
    S.consultas = true;
    c.innerHTML = '';
    c.classList.add('is-open');

    var items = consultasDisponibles();
    var box = document.createElement('div');
    box.className = 'cw-consultas';
    var head = document.createElement('div');
    head.className = 'cw-consultas-head';
    head.innerHTML = '<b>' + UI[S.lang].consultas_titulo +
        ' <em>' + items.length + '</em></b><span>' + UI[S.lang].consultas_hint + '</span>';
    box.appendChild(head);

    var list = document.createElement('div');
    list.className = 'cw-consultas-list';
    items.forEach(function (nombre) {
        var b = document.createElement('button');
        b.className = 'cw-consulta';
        b.type = 'button';
        b.textContent = nombre;
        b.onclick = function () {
            c.innerHTML = '';
            c.classList.remove('is-open');
            S.consultas = false;
            var q = UI[S.lang].consulta_prefijo + nombre.toLowerCase();
            addMsg(nombre, 'user');
            playSound('send');
            sendToAI(q, { etiqueta: nombre });
        };
        list.appendChild(b);
    });
    box.appendChild(list);

    var back = document.createElement('button');
    back.className = 'cw-opt cw-consultas-back';
    back.type = 'button';
    back.textContent = UI[S.lang].consultas_volver;
    back.onclick = function () {
        S.consultas = false;
        c.classList.remove('is-open');
        showOpts(getOpts());
    };
    box.appendChild(back);
    c.appendChild(box);
    var msgs = document.getElementById('cw-msgs');
    if (msgs) msgs.scrollTop = msgs.scrollHeight;
}

function bindConsultaBtn(btn) {
    btn.onclick = function () {
        playSound('open');
        showConsultas();
    };
}

/* ===== IDIOMA AUTOMATICO (quechua) ===== */
var QU_HINTS = ['imaynalla', 'imaynallan', 'allillan', 'allinlla', 'yusulpayki', 'yuspagara',
    'maypi', 'maypitaq', 'hayka', 'haykataq', 'imata', 'imatataq', 'imayna', 'imaynata',
    'munani', 'munayman', 'qullqi', 'kullki', 'tramitayta', 'rimay', 'niway', 'tapuy', 'wasiy',
    'carnetyta', 'multayta', 'ñan', 'ama hina', 'upallay', 'kanchu', 'tiyanchu', 'chayqa',
    'horqoy', 'horqoyta', 'ruway', 'ruwayta', 'ruwakun', 'ruwana', 'qhaway', 'willay',
    'apay', 'pusay', 'pagay', 'pagayta', 'yachay', 'llamkay', 'qhatu', 'wasita', 'yaku',
    'punchaw', 'p\'unchaw', 'simana', 'qillqay', 'kasqan', 'nitaq', 'utaq', 'paykuna',
    'yupay', 'waqaychay', 'apamuy', 'qhapaq', 'tramitata', 'multata'];

var QU_SUFIJOS = /(yta|manta|kuna|nchik|yman|puni|qta|yki|niy|chik|qti)$/;
var QU_SIN_SUFIJO = { manta: 1, amamanta: 1 };

function looksQuechua(text) {
    var t = String(text || '').toLowerCase();
    for (var i = 0; i < QU_HINTS.length; i++) {
        if (t.indexOf(QU_HINTS[i]) !== -1) return true;
    }
    // El dictado devuelve una grafia aproximada: los sufijos quechuas
    // (horqoyta, wasimanta, tramitekuna...) delatan el idioma sin depender
    // de que el reconocedor escriba la palabra exacta.
    var palabras = t.split(/[^a-z\u00e0-\u00ff']+/);
    for (var j = 0; j < palabras.length; j++) {
        var p = palabras[j];
        if (p.length >= 6 && !QU_SIN_SUFIJO[p] && QU_SUFIJOS.test(p)) return true;
    }
    return false;
}

/* ===== INTERPRETACION DEL QUECHUA DICTADO ===== */
function sinAcentos(t) {
    return String(t == null ? '' : t).toLowerCase()
        .normalize('NFD').replace(/[\u0300-\u036f]/g, '');
}

var QU_FIX = {
    kechua: 'quechua', quichua: 'quechua', kichua: 'quechua', qhechua: 'quechua',
    qhechwa: 'quechua', yuspagara: 'yusulpayki', allinllachu: 'allillanchu',
    multacuna: 'multakuna', multakunas: 'multakuna',
    tramitecuna: 'tramitekuna', tramitekunata: 'tramitekuna'
};
var QU_STOP = {
    la: 1, el: 1, los: 1, las: 1, un: 1, una: 1, unos: 1, unas: 1, de: 1, del: 1,
    al: 1, que: 1, mi: 1, mis: 1, su: 1, sus: 1, tu: 1, tus: 1, en: 1, y: 1, o: 1,
    a: 1, para: 1, por: 1, con: 1, sin: 1, es: 1, son: 1, como: 1, lo: 1, se: 1,
    me: 1, te: 1, nos: 1
};
var QU_PRESTAMOS = {
    multa: 1, multas: 1, tramite: 1, tramites: 1, carnet: 1, licencia: 1,
    licencias: 1, requisito: 1, requisitos: 1, documento: 1, documentos: 1,
    pago: 1, pagos: 1, banco: 1, oficina: 1, constancia: 1, permiso: 1,
    certificado: 1, vehiculo: 1, auto: 1, carro: 1, casa: 1, terreno: 1,
    predio: 1, impuesto: 1, servicio: 1, horario: 1, caja: 1, municipal: 1,
    sacaba: 1, segip: 1, geres: 1
};
var QU_SUFIJOS_SUELTOS = {
    cuna: 'kuna', kuna: 'kuna', yta: 'yta', ta: 'ta', manta: 'manta',
    pi: 'pi', paq: 'paq', wan: 'wan', chik: 'chik', qa: 'qa'
};
var QU_FRASES = {
    'multa cuna': 'multakuna', 'multas cuna': 'multakuna',
    'multa kuna': 'multakuna', 'multa cunas': 'multakuna',
    'trami te': 'tramite', 'trami te kuna': 'tramitekuna',
    'tramite cuna': 'tramitekuna', 'tramite kuna': 'tramitekuna',
    'carnet yta': 'carnetyta', 'carnet ta': 'carnetta',
    'licencia ta': 'licenciata', 'licencia yta': 'licenciayta',
    'paga yta': 'pagayta', 'paga na': 'pagana',
    'ruwa y': 'ruway', 'ruwa yta': 'ruwayta', 'ruwa na': 'ruwana',
    'horqoy ta': 'horqoyta', 'hurqoy ta': 'hurqoyta',
    'ima yna': 'imayna', 'imay nata': 'imaynata', 'ima ynata': 'imaynata',
    'may pi': 'maypi', 'may pitaq': 'maypitaq', 'may pi taq': 'maypitaq',
    'hay ka': 'hayka', 'hay ka taq': 'haykataq',
    'kull qi': 'kullqi', 'qul qi': 'qullqi', 'qul lqi': 'qullqi',
    'culle qui': 'qullqi',
    'allin lla': 'allinlla', 'allin llanchu': 'allillanchu',
    'allin llan chu': 'allillanchu', 'imay nallan': 'imaynallan',
    'ima y nallan': 'imaynallan', 'ima ynan': 'imaynallan',
    'tupanan chiskama': 'tupananchiskama', 'tupanan chikama': 'tupananchikama',
    'yanapa way': 'yanapaway', 'yanapa ykuy': 'yanapaykuy',
    'yanapa wanki': 'yanapawanki', 'ni way': 'niway', 'ni wa y': 'niway',
    'uyari y': 'uyariy', 'waqay cha y': 'waqaychay',
    'was i': 'wasi', 'wasi ta': 'wasita', 'wasi manta': 'wasimanta',
    'runa simi': 'runasimi', 'runa simita': 'runasimita',
    'ima ta': 'imata', 'ima taq': 'imataq', 'ima nataq': 'imanataq'
};
var QU_FRASES_ORDEN = Object.keys(QU_FRASES).sort(function (a, b) { return b.length - a.length; });

function interpretarQuechua(texto) {
    var t = String(texto == null ? '' : texto).replace(/\s+/g, ' ').trim();
    if (!t) return t;
    t = t.replace(/[A-Za-z\u00c1\u00c9\u00cd\u00d3\u00da\u00d1\u00e1\u00e9\u00ed\u00f3\u00fa\u00f1]+/g, function (w) {
        return QU_FIX[sinAcentos(w)] || w;
    });
    for (var i = 0; i < QU_FRASES_ORDEN.length; i++) {
        var mal = QU_FRASES_ORDEN[i];
        var re = new RegExp('(^|[^a-z\\u00e1\\u00e9\\u00ed\\u00f3\\u00fa\\u00f1])' +
            mal.split(' ').join('\\s+') + '(?![a-z\\u00e1\\u00e9\\u00ed\\u00f3\\u00fa\\u00f1])', 'gi');
        t = t.replace(re, function (m, pre) { return pre + QU_FRASES[mal]; });
    }
    var partes = t.split(' ');
    var salida = [];
    for (var j = 0; j < partes.length; j++) {
        var p = partes[j];
        var suf = QU_SUFIJOS_SUELTOS[sinAcentos(p)];
        if (suf && salida.length) {
            var prev = sinAcentos(salida[salida.length - 1]).replace(/[.,;:!?]+$/, '');
            if (!QU_STOP[prev] && prev.length >= 3 && QU_PRESTAMOS[prev]) {
                salida[salida.length - 1] = salida[salida.length - 1] + (suf === 'kuna' ? 'kuna' : p);
                continue;
            }
        }
        salida.push(p);
    }
    return salida.join(' ');
}

/* ===== COMANDOS DE IDIOMA ===== */
var LANG_QU_RE = /\b(?:habla|hablar|h\u00e1blame|hablame|responde|resp\u00f3ndeme|contesta|c\u00e1mbiate|cambia|ponte|parla|rimay|rimaykuy|rimaykuway|rimariy|rimasunchik)\b[^.!?\n]{0,40}\b(?:quechua|quichua|qhichwa|runasimi|kichwa|kechua)\b|\b(?:en|al|hacia)\s+(?:quechua|quichua|qhichwa|runasimi|kichwa|kechua)\b|\b(?:quechuapi|quechuata|runasimipi)\b/i;
var LANG_ES_RE = /\b(?:habla|hablar|h\u00e1blame|hablame|responde|resp\u00f3ndeme|contesta|c\u00e1mbiate|cambia|ponte|parla)\b[^.!?\n]{0,40}\b(?:espa\u00f1ol|espanol|castellano)\b|\b(?:en|al)\s+(?:espa\u00f1ol|espanol|castellano)\b/i;
var NO_CMD_RE = /\b(?:como se dice|como digo|traduce|traducir|traducci\u00f3n|traduccion|significa)\b/i;

function detectarComandoIdioma(texto) {
    var t = String(texto == null ? '' : texto).trim();
    if (!t) return null;
    var low = sinAcentos(t);
    if (low.split(/\s+/).length > 8 || NO_CMD_RE.test(t)) return null;
    var pals = low.match(/[a-z]+/g) || [];
    if (pals.length <= 3) {
        for (var i = 0; i < pals.length; i++) {
            if (/^(quechua|quichua|qhichwa|runasimi|kichwa|kechua)$/.test(pals[i])) return 'qu';
            if (/^(espanol|castellano)$/.test(pals[i])) return 'es';
        }
    }
    if (LANG_QU_RE.test(t)) return 'qu';
    if (LANG_ES_RE.test(t)) return 'es';
    return null;
}

function avisarIdioma(lang) {
    if (UI[lang] && UI[lang].idioma_corto) speakText(UI[lang].idioma_corto, lang, true);
}

function switchLang(lang, quiet, ack) {
    if (lang !== 'es' && lang !== 'qu') return;
    if (S.lang === lang) {
        if (ack) { stopSpeaking(); avisarIdioma(lang); }
        return;
    }
    // El cambio de idioma corta la voz en curso de inmediato: no se espera a
    // que termine la frase en el idioma anterior.
    stopSpeaking();
    applyLanguageUI(lang);
    if (quiet) {
        if (window.SacabaApplyPageLanguage) window.SacabaApplyPageLanguage(lang, { quiet: true });
    } else {
        renderConversation(lang);
        if (window.SacabaSetLang) window.SacabaSetLang(lang);
    }
    if (ack) avisarIdioma(lang);
}

function historyForAI() {
    var out = [];
    for (var i = 0; i < S.log.length; i++) {
        var e = S.log[i];
        if (e.type === 'user') out.push({ role: 'user', content: e.text });
        else if (e.resp && e.respLang === S.lang) out.push({ role: 'assistant', content: e.resp });
    }
    return out.slice(-8);
}

/* ===== COMANDOS DE VOZ ===== */
var STOP_RE = /(ya no hables|no hables mas|no hables más|deja de hablar|dejá de hablar|callate|cállate|silencio|detente|para de hablar|basta de hablar|upallay|amaña rimaychu|ama rimaychu|ch\'inlla)/i;

function isStopCommand(text) {
    var t = String(text || '').toLowerCase().trim();
    if (!t || t.split(/\s+/).length > 6) return false;
    return STOP_RE.test(t);
}

function isMuteCommand(text) {
    return /^(sami[,\s]+)?(ya no hables|no hables|cállate|callate|silencio|detente|para)(\s+por favor)?[.!]?$/i.test(String(text || '').trim());
}

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

/* ===== VOZ: dictado, manos libres y comandos ===== */
function avisoMic(clave) {
    addMsg(UI[S.lang][clave] || UI[S.lang].mic_error, 'bot', { silent: true });
}

function hayMicSeguro() {
    var host = location.hostname;
    return !!window.isSecureContext || host === 'localhost' || host === '127.0.0.1' || host === '';
}

function claveErrorMic(nombre) {
    if (nombre === 'NotAllowedError' || nombre === 'SecurityError') return 'mic_denegado';
    if (nombre === 'NotFoundError' || nombre === 'OverconstrainedError') return 'mic_sin_equipo';
    if (nombre === 'NotReadableError' || nombre === 'AbortError') return 'mic_ocupado';
    return 'mic_error';
}

function pedirPermisoMic() {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        return Promise.reject('mic_no_soportado');
    }
    return navigator.mediaDevices.getUserMedia({ audio: true }).then(function (stream) {
        stream.getTracks().forEach(function (t) { t.stop(); });
        return true;
    }).catch(function (err) {
        throw claveErrorMic((err && err.name) || '');
    });
}

function retomarManosLibres() {
    if (!S.handsFree || !S.open || S.hfPause) return;
    if (S.speaking) { setTimeout(retomarManosLibres, 700); return; }
    if (!S.recognition && !S.recording) empezarManosLibres();
}

function startRecording() {
    stopSpeaking();
    if (S.recording) return stopRecording();
    var SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SR) return avisoMic('mic_no_soportado');
    if (!hayMicSeguro()) return avisoMic('mic_inseguro');

    if (S.handsFree) {
        S.hfPause = true;
        if (S.recognition) { try { S.recognition.abort(); } catch (e) {} }
        S.recognition = null;
    } else if (S.recognition) {
        try { S.recognition.abort(); } catch (e) {}
        S.recognition = null;
    }

    var micBtn = document.getElementById('cw-mic');
    if (micBtn) micBtn.classList.add('waiting');
    pedirPermisoMic().then(function () {
        if (micBtn) micBtn.classList.remove('waiting');
        if (S.open) startLiveSTT(SR);
    }).catch(function (clave) {
        if (micBtn) micBtn.classList.remove('waiting');
        S.hfPause = false;
        avisoMic(clave);
        retomarManosLibres();
    });
}

function enviarTexto(msg) {
    var inp = document.getElementById('cw-in');
    if (inp) inp.value = '';
    // El dictado separa el quechua ("multa cuna"): se muestra ya interpretado.
    msg = interpretarQuechua(msg);
    var opts = document.getElementById('cw-opts');
    if (opts) { opts.innerHTML = ''; opts.classList.remove('is-open'); }
    if (isMuteCommand(msg)) {
        stopSpeaking();
        addMsg(UI[S.lang].stop_ack, 'bot', { silent: true });
        return;
    }
    addMsg(msg, 'user');
    playSound('send');
    sendToAI(msg, { porVoz: true });
}

function startLiveSTT(SR) {
    var inp = document.getElementById('cw-in');
    var rec = new SR();
    S.sttFinal = '';
    S.sttHeard = false;
    S.restartSTT = false;
    rec.lang = S.recLang || ((S.lang === 'qu') ? 'qu-BO' : 'es-BO');
    rec.continuous = true;
    rec.interimResults = true;
    rec.maxAlternatives = 1;

    function cerrarPorSilencio() {
        clearTimeout(S.sttTimer);
        S.sttTimer = setTimeout(function () {
            if (S.recording) stopRecording();
        }, 2400);
    }

    rec.onresult = function (event) {
        S.sttHeard = true;
        var finalText = '';
        var interim = '';
        for (var i = event.resultIndex; i < event.results.length; i++) {
            var r = event.results[i];
            if (r.isFinal) { finalText += r[0].transcript + ' '; }
            else { interim += r[0].transcript; }
        }
        S.sttFinal += finalText;
        if (inp) inp.value = (S.sttFinal + (interim ? ' ' + interim : '')).trim();
        var msgs = document.getElementById('cw-msgs');
        if (msgs) msgs.scrollTop = msgs.scrollHeight;
        if (isStopCommand(S.sttFinal + ' ' + interim)) {
            S.sttFinal = '';
            if (inp) inp.value = '';
            stopRecording();
            stopSpeaking();
            addMsg(UI[S.lang].stop_ack, 'bot', { silent: true });
            return;
        }
        cerrarPorSilencio();
    };
    rec.onerror = function (event) {
        clearTimeout(S.sttTimer);
        var err = event.error;
        if (err === 'no-speech' || err === 'aborted') return;
        // Si el navegador no puede reconocer (servicio de voz bloqueado o
        // idioma sin modelo) se pasa al dictado del servidor, que si funciona.
        if (err === 'network' || err === 'service-not-allowed') {
            S.modoServidor = true;
            S.sttFallo = true;
            S.sttReintento = true;
            try { rec.abort(); } catch (e) {}
            if (S.recognition === rec) S.recognition = null;
            S.recording = false;
            updateMicUI(false);
            return;
        }
        if (err === 'language-not-supported') {
            var intentado = rec.lang;
            var siguiente = intentado === 'qu-BO' ? 'es-BO' : (intentado === 'es-BO' ? 'es-ES' : null);
            if (siguiente) S.recLang = siguiente;
            else S.modoServidor = true;
            S.sttReintento = true;
            S.sttFallo = true;
            try { rec.abort(); } catch (e) {}
            if (S.recognition === rec) S.recognition = null;
            S.recording = false;
            updateMicUI(false);
            return;
        }
        var clave = 'mic_error';
        if (err === 'not-allowed') clave = 'mic_denegado';
        else if (err === 'audio-capture') clave = 'mic_sin_equipo';
        S.sttFallo = true;
        try { rec.abort(); } catch (e) {}
        if (S.recognition === rec) S.recognition = null;
        S.recording = false;
        updateMicUI(false);
        avisoMic(clave);
    };
    rec.onend = function () {
        clearTimeout(S.sttTimer);
        S.recording = false;
        if (S.recognition === rec) S.recognition = null;
        updateMicUI(false);
        if (S.sttReintento) {
            S.sttReintento = false;
            S.sttFallo = false;
            S.sttFinal = '';
            S.sttHeard = false;
            S.hfPause = false;
            if (S.open) {
                if (S.modoServidor) grabarServidor(!S.autoListen);
                else startLiveSTT(SR);
            }
            return;
        }
        var fallo = S.sttFallo;
        var msg = (S.sttFinal || '').trim();
        S.sttFallo = false;
        S.sttFinal = '';
        S.hfPause = false;
        if (!fallo) {
            if (msg) {
                S.autoTurno = !!S.autoListen;
                S.autoIntentos = 0;
                enviarTexto(msg);
            } else if (!S.sttHeard && !S.autoListen) {
                addMsg(UI[S.lang].no_entendi, 'bot', { silent: true });
            }
        }
        if (!fallo && S.autoListen && !msg && !S.sttHeard && S.autoIntentos < 3) {
            S.autoIntentos++;
            setTimeout(function () {
                if (S.autoListen && !S.recording && !S.recognition) iniciarEscuchaAuto();
            }, 400);
        } else if (!fallo && S.autoListen && !msg && !S.sttHeard) {
            // El dictado del navegador no devolvio nada: se graba en el servidor.
            S.modoServidor = true;
            if (S.open) grabarServidor(false);
        } else if (!S.autoListen) {
            setTimeout(retomarManosLibres, 500);
        }
    };
    S.recognition = rec;
    S.recording = true;
    updateMicUI(true);
    playSound('record');
    try { rec.start(); }
    catch (e) {
        if (S.recognition === rec) S.recognition = null;
        S.recording = false;
        S.hfPause = false;
        updateMicUI(false);
        avisoMic('mic_error');
        setTimeout(retomarManosLibres, 500);
    }
}

/* ===== DICTADO DEL SERVIDOR (Web Speech no disponible) ===== */
var GRAB = { activa: false, media: null, stream: null, ctx: null, vigia: null, tope: null, trozos: [], hablo: false, inicio: 0, ultimoRuido: 0, manual: false };

/* Abre el microfono con reintentos: al terminar el dictado del navegador
   el dispositivo puede seguir ocupado unos instantes. */
function abrirMic(intentos) {
    var pedido = {
        audio: {
            channelCount: 1,
            echoCancellation: true,
            noiseSuppression: true,
            autoGainControl: true
        }
    };
    return navigator.mediaDevices.getUserMedia(pedido).catch(function (err) {
        var nombre = (err && err.name) || '';
        if (intentos > 1 && (nombre === 'NotReadableError' || nombre === 'AbortError')) {
            return new Promise(function (listo) { setTimeout(listo, 350); })
                .then(function () { return abrirMic(intentos - 1); });
        }
        throw claveErrorMic(nombre);
    });
}

function grabarServidor(manual) {
    if (GRAB.activa) return;
    if (!navigator.mediaDevices || !window.MediaRecorder) { avisoMic('mic_no_soportado'); return; }
    if (!hayMicSeguro()) { avisoMic('mic_inseguro'); return; }
    GRAB.manual = !!manual;
    abrirMic(3).then(function (stream) {
        GRAB.stream = stream;
        GRAB.trozos = [];
        GRAB.hablo = false;
        GRAB.inicio = Date.now();
        GRAB.ultimoRuido = Date.now();
        var preferidos = ['audio/webm;codecs=opus', 'audio/ogg;codecs=opus', 'audio/webm'];
        var opciones = {};
        for (var i = 0; i < preferidos.length; i++) {
            if (window.MediaRecorder.isTypeSupported && window.MediaRecorder.isTypeSupported(preferidos[i])) {
                opciones = { mimeType: preferidos[i] };
                break;
            }
        }
        GRAB.media = new MediaRecorder(stream, opciones);
        GRAB.media.ondataavailable = function (e) { if (e.data && e.data.size) GRAB.trozos.push(e.data); };
        GRAB.media.onstop = finalizarGrabacion;
        GRAB.activa = true;
        GRAB.media.start(200);
        S.recording = true;
        updateMicUI(true);
        var campo = document.getElementById('cw-in');
        if (campo) campo.placeholder = UI[S.lang].escuchando;
        playSound('record');
        GRAB.tope = setTimeout(detenerGrabacionServidor, manual ? 25000 : 15000);
        vigilarNivel();
    }).catch(function (clave) {
        avisoMic(typeof clave === 'string' ? clave : claveErrorMic((clave && clave.name) || ''));
    });
}

/* Detecta el volumen del microfono para cortar solo cuando el usuario calla. */
function vigilarNivel() {
    try {
        var AC = window.AudioContext || window.webkitAudioContext;
        var ctx = new AC();
        var fuente = ctx.createMediaStreamSource(GRAB.stream);
        var anal = ctx.createAnalyser();
        anal.fftSize = 1024;
        fuente.connect(anal);
        var datos = new Uint8Array(anal.fftSize);
        GRAB.ctx = ctx;
        GRAB.vigia = setInterval(function () {
            anal.getByteTimeDomainData(datos);
            var suma = 0;
            for (var i = 0; i < datos.length; i++) {
                var v = (datos[i] - 128) / 128;
                suma += v * v;
            }
            var rms = Math.sqrt(suma / datos.length);
            var ahora = Date.now();
            if (rms > 0.012) { GRAB.hablo = true; GRAB.ultimoRuido = ahora; }
            var silencio = GRAB.manual ? 2600 : 2200;
            var espera = GRAB.manual ? 12000 : 9000;
            var tope = GRAB.manual ? 25000 : 15000;
            if (GRAB.hablo && ahora - GRAB.ultimoRuido > silencio) return detenerGrabacionServidor();
            if (!GRAB.hablo && ahora - GRAB.inicio > espera) return detenerGrabacionServidor();
            if (ahora - GRAB.inicio > tope) return detenerGrabacionServidor();
        }, 100);
    } catch (e) {}
}

function detenerGrabacionServidor() {
    if (GRAB.vigia) { clearInterval(GRAB.vigia); GRAB.vigia = null; }
    if (GRAB.tope) { clearTimeout(GRAB.tope); GRAB.tope = null; }
    if (GRAB.media && GRAB.media.state !== 'inactive') {
        try { GRAB.media.stop(); } catch (e) {}
    }
}

function finalizarGrabacion() {
    var hablo = GRAB.hablo;
    GRAB.activa = false;
    GRAB.media = null;
    if (GRAB.vigia) { clearInterval(GRAB.vigia); GRAB.vigia = null; }
    if (GRAB.tope) { clearTimeout(GRAB.tope); GRAB.tope = null; }
    if (GRAB.ctx) { try { GRAB.ctx.close(); } catch (e) {} GRAB.ctx = null; }
    if (GRAB.stream) {
        GRAB.stream.getTracks().forEach(function (t) { t.stop(); });
        GRAB.stream = null;
    }
    updateMicUI(false);
    var campo = document.getElementById('cw-in');
    if (campo) campo.placeholder = S.bloqueado ? UI[S.lang].presentando : UI[S.lang].ph;
    var trozos = GRAB.trozos;
    GRAB.trozos = [];
    if (!hablo || !trozos.length) {
        sinVozDetectada();
        return;
    }
    var blob = new Blob(trozos, { type: trozos[0].type || 'audio/webm' });
    showTyping();
    convertirAWav(blob).then(function (base64) {
        return fetch('/api/stt', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ audio: base64, language: S.lang })
        });
    }).then(function (r) {
        if (!r.ok) throw new Error('stt ' + r.status);
        return r.json();
    }).then(function (d) {
        hideTyping();
        var texto = ((d && d.text) || '').trim();
        if (!texto) {
            addMsg(UI[S.lang].no_entendi, 'bot', { silent: true });
            return;
        }
        S.autoTurno = !!S.autoListen;
        S.autoIntentos = 0;
        enviarTexto(texto);
    }).catch(function () {
        hideTyping();
        avisoMic('mic_red');
    });
}

/* No se detecto voz: en modo automatico reintenta un par de veces antes de avisar. */
function sinVozDetectada() {
    if (S.autoListen && S.autoIntentos < 2) {
        S.autoIntentos++;
        S.autoTurno = false;
        setTimeout(iniciarEscuchaAuto, 700);
        return;
    }
    S.autoIntentos = 0;
    addMsg(UI[S.lang].no_entendi, 'bot', { silent: true });
}

/* Convierte el audio grabado a WAV 16 kHz mono (lo que espera el servidor). */
function convertirAWav(blob) {
    var AC = window.AudioContext || window.webkitAudioContext;
    var ctx = new AC();
    return blob.arrayBuffer().then(function (buffer) {
        return new Promise(function (resolve, reject) {
            ctx.decodeAudioData(buffer, resolve, reject);
        });
    }).then(function (audio) {
        try { ctx.close(); } catch (e) {}
        var ritmo = 16000;
        var destino = new OfflineAudioContext(1, Math.ceil(audio.duration * ritmo), ritmo);
        var fuente = destino.createBufferSource();
        fuente.buffer = audio;
        fuente.connect(destino.destination);
        fuente.start(0);
        return destino.startRendering();
    }).then(function (render) {
        return wavBase64(render.getChannelData(0), render.sampleRate);
    });
}

function wavBase64(muestras, ritmo) {
    var total = muestras.length;
    var buffer = new ArrayBuffer(44 + total * 2);
    var vista = new DataView(buffer);
    function escribir(pos, texto) {
        for (var i = 0; i < texto.length; i++) vista.setUint8(pos + i, texto.charCodeAt(i));
    }
    escribir(0, 'RIFF');
    vista.setUint32(4, 36 + total * 2, true);
    escribir(8, 'WAVE');
    escribir(12, 'fmt ');
    vista.setUint32(16, 16, true);
    vista.setUint16(20, 1, true);
    vista.setUint16(22, 1, true);
    vista.setUint32(24, ritmo, true);
    vista.setUint32(28, ritmo * 2, true);
    vista.setUint16(32, 2, true);
    vista.setUint16(34, 16, true);
    escribir(36, 'data');
    vista.setUint32(40, total * 2, true);
    var pos = 44;
    for (var i = 0; i < total; i++, pos += 2) {
        var m = Math.max(-1, Math.min(1, muestras[i]));
        vista.setInt16(pos, m < 0 ? m * 0x8000 : m * 0x7FFF, true);
    }
    var bytes = new Uint8Array(buffer);
    var binario = '';
    for (var j = 0; j < bytes.length; j += 0x8000) {
        binario += String.fromCharCode.apply(null, bytes.subarray(j, j + 0x8000));
    }
    return btoa(binario);
}

/* ===== MANOS LIBRES: escucha "Sami" y obedece ordenes ===== */
function toggleHandsFree() {
    S.handsFree = !S.handsFree;
    if (S.handsFree) S.autoListen = false;
    S.autoTurno = false;
    updateHandsFreeUI();
    if (S.handsFree) {
        playSound('open');
        addMsg(UI[S.lang].manos_libres_on, 'bot', { silent: true });
        empezarManosLibres();
    } else {
        playSound('stop');
        S.restartSTT = false;
        S.hfPause = false;
        if (S.recognition && !S.recording) { try { S.recognition.abort(); } catch (e) {} }
        addMsg(UI[S.lang].manos_libres_off, 'bot', { silent: true });
    }
}

function empezarManosLibres() {
    if (!S.handsFree) return;
    var SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SR) { S.handsFree = false; updateHandsFreeUI(); return avisoMic('mic_no_soportado'); }
    if (!hayMicSeguro()) { S.handsFree = false; updateHandsFreeUI(); return avisoMic('mic_inseguro'); }
    if (S.recording || S.recognition) return;

    var rec = new SR();
    rec.lang = 'es-BO';
    rec.continuous = true;
    rec.interimResults = true;
    rec.maxAlternatives = 1;

    rec.onresult = function (event) {
        var dicho = '';
        for (var i = event.resultIndex; i < event.results.length; i++) {
            var r = event.results[i];
            if (r.isFinal) dicho += r[0].transcript + ' ';
        }
        dicho = dicho.trim();
        if (dicho) manejarManosLibres(dicho);
    };
    rec.onerror = function (event) {
        var err = event.error;
        if (err === 'no-speech' || err === 'aborted') return;
        var clave = 'mic_error';
        if (err === 'not-allowed' || err === 'service-not-allowed') clave = 'mic_denegado';
        else if (err === 'audio-capture') clave = 'mic_sin_equipo';
        else if (err === 'network') clave = 'mic_red';
        S.handsFree = false;
        if (S.recognition === rec) S.recognition = null;
        updateHandsFreeUI();
        avisoMic(clave);
    };
    rec.onend = function () {
        if (S.recognition === rec) S.recognition = null;
        setTimeout(retomarManosLibres, 300);
    };
    S.recognition = rec;
    try { rec.start(); }
    catch (e) {
        if (S.recognition === rec) S.recognition = null;
        S.handsFree = false;
        updateHandsFreeUI();
        avisoMic('mic_error');
    }
}

function manejarManosLibres(texto) {
    var t = String(texto || '').trim();
    if (!t) return;

    if (isStopCommand(t)) {
        if (S.speaking) stopSpeaking();
        addMsg(UI[S.lang].stop_ack, 'bot', { silent: true });
        return;
    }
    // El cambio de idioma se atiende aunque Sami este hablando y sin exigir
    // la palabra "Sami": es un comando directo.
    var cmdLang = detectarComandoIdioma(t);
    if (cmdLang) {
        switchLang(cmdLang, true, false);
        addMsg(UI[cmdLang].idioma_ack, 'bot');
        return;
    }
    if (S.speaking || S.busy) return;

    var low = t.toLowerCase();
    var m = low.match(/\b(sami|samita|samiy)\b/);
    if (!m) return;

    var cola = t.slice(m.index + m[1].length).replace(/^[\s,.:;¡!¿?\-]+/, '').trim();
    if (!cola) {
        addMsg(UI[S.lang].wake_ack, 'bot', { silent: true });
        return;
    }
    var opts = document.getElementById('cw-opts');
    if (opts) { opts.innerHTML = ''; opts.classList.remove('is-open'); }
    addMsg(cola, 'user');
    playSound('send');
    sendToAI(cola, { porVoz: true });
}

function stopRecording() {
    clearTimeout(S.sttTimer);
    if (GRAB.activa) { detenerGrabacionServidor(); return; }
    if (S.recognition && S.recording) { try { S.recognition.stop(); } catch (e) {} }
}

function updateMicUI(isRecording) {
    S.recording = !!isRecording;
    var micBtn = document.getElementById('cw-mic');
    if (micBtn) {
        if (isRecording) {
            micBtn.classList.add('recording');
            micBtn.innerHTML = '<svg viewBox="0 0 24 24"><rect x="6" y="6" width="12" height="12" rx="2" fill="white"/></svg>';
        } else {
            micBtn.classList.remove('recording');
            micBtn.innerHTML = MIC_ICON;
        }
    }
    var input = document.querySelector('.cw-input');
    if (input) input.classList.toggle('is-listening', !!isRecording);
}

function updateHandsFreeUI() {
    var btn = document.getElementById('cw-hf');
    if (!btn) return;
    btn.classList.toggle('active', S.handsFree);
    btn.setAttribute('aria-pressed', S.handsFree ? 'true' : 'false');
    btn.title = S.handsFree ? 'Manos libres activo' : 'Activar manos libres (di "Sami...")';
    var input = document.querySelector('.cw-input');
    if (input) input.classList.toggle('is-handsfree', S.handsFree);
}

/* ===== PRESENTACION INICIAL Y MICROFONO AUTOMATICO ===== */
function bloquearChat(on) {
    S.bloqueado = !!on;
    var win = document.getElementById('cw-window');
    if (win) win.classList.toggle('cw-presentando', !!on);
    var ids = ['cw-in', 'cw-send', 'cw-mic', 'cw-hf'];
    for (var i = 0; i < ids.length; i++) {
        var el = document.getElementById(ids[i]);
        if (el) el.disabled = !!on;
    }
    var inp = document.getElementById('cw-in');
    if (inp) inp.placeholder = on ? UI[S.lang].presentando : UI[S.lang].ph;
}

function textoPresentacion(lang) {
    var ui = UI[lang] || UI.es;
    return ui.greeting + ' ' + ui.greeting2;
}

function iniciarEscuchaAuto() {
    if (!S.embedded || !S.autoListen || S.handsFree || S.bloqueado || !S.open) return;
    if (S.presentando || S.micListo !== true) return;
    if (!hayMicSeguro()) return;
    if (S.recording || S.recognition || GRAB.activa) return;
    if (S.busy || S.speaking || S.vozOcupada) { setTimeout(iniciarEscuchaAuto, 700); return; }
    // El dictado del servidor escucha de verdad en cualquier navegador;
    // el reconocimiento propio del navegador solo se usa si no hay grabadora.
    if (navigator.mediaDevices && window.MediaRecorder) {
        grabarServidor(false);
        return;
    }
    var SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SR) { avisoMic('mic_no_soportado'); return; }
    startLiveSTT(SR);
}

function reanudarEscuchaAuto() {
    if (!S.autoListen || !S.autoTurno) return;
    S.autoTurno = false;
    iniciarEscuchaAuto();
}

/* La cola de voz se vacio: si el turno vino del microfono, se vuelve a escuchar. */
function alQuedarEnSilencio() {
    if (!S.autoListen || !S.autoTurno) return;
    setTimeout(reanudarEscuchaAuto, 600);
}

function presentarSami() {
    if (S.presentado) { bloquearChat(false); iniciarEscuchaAuto(); return; }
    if (S.presentando) return;
    S.presentado = true;
    S.presentando = true;
    bloquearChat(true);
    encolarVoz(textoPresentacion(S.lang), S.lang, true).then(function () {
        S.presentando = false;
        S.silentFijo = false;
        bloquearChat(false);
        if (S.micListo !== true && typeof S.micListo === 'string') avisoMic(S.micListo);
        iniciarEscuchaAuto();
    });
}

window.SacabaStartPresentation = function () {
    if (!S.embedded) return;
    S.autoListen = true;
    S.autoIntentos = 0;
    presentarSami();
};

window.SacabaSkipPresentation = function () {
    if (!S.embedded || S.presentado) return;
    S.presentado = true;
    S.presentando = false;
    S.silentFijo = false;
    S.autoListen = true;
    S.autoIntentos = 0;
    bloquearChat(false);
    iniciarEscuchaAuto();
};

window.SacabaPrepararMicro = function () {
    if (S.micListo === true) return Promise.resolve(true);
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        S.micListo = 'mic_no_soportado';
        return Promise.resolve(false);
    }
    return pedirPermisoMic().then(function () {
        S.micListo = true;
        // Si la presentacion ya termino mientras el usuario decidia el permiso.
        iniciarEscuchaAuto();
        return true;
    }).catch(function (clave) {
        S.micListo = clave || 'mic_error';
        return false;
    });
};

var MIC_ICON = '<svg viewBox="0 0 24 24"><path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3zm-1-9c0-.55.45-1 1-1s1 .45 1 1v6c0 .55-.45 1-1 1s-1-.45-1-1V5z"/><path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"/></svg>';

/* ===== PANEL DINAMICO (ficha a la derecha) ===== */
function syncPanel(text, apiTramite) {
    try {
        if (window.SacabaPanel) window.SacabaPanel.fromQuery(text, apiTramite || null);
    } catch (e) {}
}

/* ===== ENVIAR A AI ===== */
function sendToAI(text, meta) {
    if (isMuteCommand(text)) {
        stopSpeaking();
        addMsg(UI[S.lang].stop_ack, 'bot', { silent: true });
        return;
    }
    // "habla quechua" / "en español": cambia la pagina y la voz al instante,
    // sin consultar a la IA (antes respondia que no sabia).
    var cmdLang = detectarComandoIdioma(text);
    if (cmdLang) {
        switchLang(cmdLang, true, false);
        addMsg(UI[cmdLang].idioma_ack, 'bot');
        S.log.push({ type: 'user', text: text });
        S.log.push({ type: 'bot', query: text, resp: UI[cmdLang].idioma_ack, respLang: cmdLang });
        playSound('message');
        S.busy = false;
        setTimeout(showConsultaBtn, 450);
        return;
    }
    var porVoz = !!(meta && meta.porVoz);
    var vozQuechua = porVoz && looksQuechua(text);
    if (S.lang === 'es' && vozQuechua) switchLang('qu', true);

    S.busy = true;
    showTyping();
    syncPanel(text, meta && meta.tramite);

    var historial = historyForAI();
    fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            message: text,
            // Lo dictado se deja detectar al servidor: asi cambia a espanol o
            // quechua segun lo que realmente hablo el ciudadano.
            language: vozQuechua ? 'qu' : (porVoz ? 'auto' : (S.lang === 'qu' ? 'qu' : 'auto')),
            useAI: true,
            history: historial
        })
    })
    .then(function(r) { return r.json(); })
    .then(function(data) {
        hideTyping();
        if (data && data.lang_command && (data.language === 'es' || data.language === 'qu')) {
            switchLang(data.language, true, false);
        }
        var det = data && (data.detected === 'qu' || data.detected === 'es') ? data.detected : null;
        if (vozQuechua) det = 'qu';
        // Por voz se sigue el idioma detectado en los dos sentidos; al escribir
        // solo se pasa a quechua para no cambiar la pagina por un descuido.
        if (det && det !== S.lang && (porVoz || det === 'qu')) switchLang(det, true);
        var resp = (data && data.response) || getResp(text);
        addMsg(resp, 'bot');
        S.log.push({ type: 'user', text: text });
        S.log.push({ type: 'bot', query: text, resp: resp, respLang: S.lang });
        playSound('message');
        if (data && data.tramite) syncPanel(text, data.tramite);
        setTimeout(showConsultaBtn, 450);
        S.busy = false;
        flushPendingLang();
    })
    .catch(function() {
        hideTyping();
        var resp = getResp(text);
        addMsg(resp, 'bot');
        S.log.push({ type: 'user', text: text });
        S.log.push({ type: 'bot', query: text, resp: resp, respLang: S.lang });
        playSound('message');
        S.busy = false;
        flushPendingLang();
    });
}

/* ===== VOZ (Edge TTS servidor + respaldo del navegador) ===== */
var VOCES_TTS = [
    { id: 'es-BO-SofiaNeural', nombre: 'Sofía' },
    { id: 'es-BO-MarceloNeural', nombre: 'Marcelo' }
];
var VOZ_KEY = 'sacaba_tts_voice';

function nombreVoz(id) {
    for (var i = 0; i < VOCES_TTS.length; i++) {
        if (VOCES_TTS[i].id === id) return VOCES_TTS[i].nombre;
    }
    return VOCES_TTS[0].nombre;
}

function vozGuardada() {
    try {
        var guardada = localStorage.getItem(VOZ_KEY);
        for (var i = 0; i < VOCES_TTS.length; i++) {
            if (VOCES_TTS[i].id === guardada) return guardada;
        }
    } catch (e) {}
    return VOCES_TTS[0].id;
}

S.vozTTS = vozGuardada();

function pickEspVoice(needQu) {
    if (!window.speechSynthesis) return null;
    var voices = window.speechSynthesis.getVoices();
    if (!voices || !voices.length) return null;
    var pool = [];
    for (var i = 0; i < voices.length; i++) {
        var l = (voices[i].lang || '').toLowerCase();
        if (needQu && (l.indexOf('qu') === 0 || l.indexOf('quz') === 0)) pool.push(voices[i]);
        else if (!needQu && l.indexOf('es') === 0) pool.push(voices[i]);
    }
    // Si no existe voz nativa quechua, se usa la mejor voz espanola con ritmo lento.
    if (!pool.length) {
        for (var k = 0; k < voices.length; k++) {
            if ((voices[k].lang || '').toLowerCase().indexOf('es') === 0) pool.push(voices[k]);
        }
    }
    if (!pool.length) return null;

    var best = null;
    var bestScore = -1;
    for (var j = 0; j < pool.length; j++) {
        var v = pool[j];
        var nm = v.name || '';
        var score = 0;
        if (/sofia|sabina|helena|elvira|estrella|paulina|catalina|laura|monica/i.test(nm)) score += 60;
        if (/neural|natural|online|premium|wavenet|google/i.test(nm)) score += 40;
        if (/\bes-bo\b/i.test(v.lang)) score += 30;
        if (/\bes-(ar|cl|co|pe|mx|es)\b/i.test(v.lang)) score += 10;
        if (/local|desktop/i.test(nm)) score -= 40;
        if (v.localService === false) score += 15;
        if (score > bestScore) { bestScore = score; best = v; }
    }
    return best || pool[0];
}

function terminarVoz() {
    S.speaking = false;
    if (window.sacabaMascotTalking) window.sacabaMascotTalking(false);
}

function stopSpeaking() {
    // Corta lo que suena y vacia la cola: las respuestas se leen una tras otra,
    // pero un corte explicito (escribir, dictar, silenciar) descarta lo pendiente.
    S.vozGen++;
    var cola = S.vozCola;
    var actual = S.vozActual;
    S.vozCola = [];
    S.vozActual = null;
    S.vozOcupada = false;
    S.speakSeq++;
    S.speaking = false;
    if (S.audio) {
        try { S.audio.pause(); } catch (e) {}
        S.audio = null;
    }
    if (window.speechSynthesis) window.speechSynthesis.cancel();
    if (window.sacabaMascotTalking) window.sacabaMascotTalking(false);
    for (var i = 0; i < cola.length; i++) { try { cola[i].done(); } catch (e) {} }
    if (actual) { try { actual.done(); } catch (e) {} }
    alQuedarEnSilencio();
}

/* Divide el texto en frases cortas: cada trozo suena antes y evita
   que Chrome corte la sintesis del navegador a los 15 segundos. */
function trocearVoz(texto, maximo) {
    var frases = String(texto).match(/[^.!?;:]+[.!?;:]*/g) || [String(texto)];
    var trozos = [];
    var actual = '';
    for (var i = 0; i < frases.length; i++) {
        var frase = frases[i].trim();
        if (!frase) continue;
        var junto = (actual ? actual + ' ' : '') + frase;
        if (junto.length > maximo && actual) {
            trozos.push(actual);
            actual = frase;
        } else {
            actual = junto;
        }
    }
    if (actual) trozos.push(actual);
    if (trozos.length > 6) {
        trozos = trozos.slice(0, 5).concat([trozos.slice(5).join(" ")]);
    }
    return trozos;
}

/* Adapta el quechua a la fonetica castellana (igual que el servidor):
   q->k, qu+e/i->k, h->j, sh->s, w->hu al final -u, y acento en la penultima
   silaba de las palabras graves. Los prestamos castellanos no se tocan. */
var ACENTOS_QU = { a: 'á', e: 'é', i: 'í', o: 'ó', u: 'ú' };
var LEXICO_QU = {
    'quechua': 'kechua', 'quechuapi': 'kechuapi', 'quechuata': 'kechuata',
    'quechuamanta': 'kechuamanta', 'quichua': 'kichua',
    'qhapaq': 'japak', 'qhapaqnan': 'japakñan', 'qhapaqñan': 'japakñan',
    'ñoqanchik': 'nukanchik', 'ñuqanchik': 'nukanchik',
    'ñoqayku': 'nukayku', 'ñuqayku': 'nukayku',
    'tupananchiskama': 'tupanchiskama', 'tupananchikama': 'tupanchikama'
};
var H_MUDA_QU = {
    hospital: 1, hospitales: 1, hotel: 1, hora: 1, horas: 1, horario: 1,
    horarios: 1, humano: 1, humana: 1, historia: 1, hielo: 1, alcohol: 1,
    hola: 1, hasta: 1
};

function aplicarLexicoQu(palabra) {
    var rep = LEXICO_QU[palabra.toLowerCase()];
    if (!rep) return palabra;
    if (palabra === palabra.toUpperCase()) return rep.toUpperCase();
    if (/^[A-ZÁÉÍÓÚÑ]/.test(palabra)) return rep.charAt(0).toUpperCase() + rep.slice(1);
    return rep;
}

function prepararPalabraQu(palabra) {
    var minus = palabra.toLowerCase();
    if (H_MUDA_QU[minus]) return palabra.replace(/^h/i, '');
    if (/[áéíóú]/.test(minus)) return palabra;
    return palabra
        .replace(/qu(?=[ei])/gi, 'k')
        .replace(/q/gi, 'k')
        .replace(/(?<!c)h/gi, 'j');
}

function acentuarPalabraQu(palabra) {
    var minus = palabra.toLowerCase();
    if (/[áéíóú]/.test(minus)) return palabra;
    var inicios = [];
    for (var i = 0; i < minus.length; i++) {
        if ('aeiou'.indexOf(minus[i]) >= 0 && (i === 0 || 'aeiou'.indexOf(minus[i - 1]) < 0)) inicios.push(i);
    }
    if (inicios.length < 2) return palabra;
    var fin = minus.charAt(minus.length - 1);
    if ('kqylrmpw\u0003'.indexOf(fin) < 0) return palabra;
    var pos = inicios[inicios.length - 2];
    var acento = ACENTOS_QU[minus.charAt(pos)];
    if (!acento) return palabra;
    if (palabra.charAt(pos) !== minus.charAt(pos)) acento = acento.toUpperCase();
    return palabra.slice(0, pos) + acento + palabra.slice(pos + 1);
}

function adaptarQuechua(texto) {
    var t = String(texto == null ? '' : texto);
    if (!t) return t;
    t = t.replace(/['’`]/g, '');
    t = t.replace(/[A-Za-zÁÉÍÓÚÑáéíóúñ]+/g, aplicarLexicoQu);
    t = t.replace(/chh/gi, 'ch').replace(/qh/gi, 'k').replace(/sh/gi, 's');
    t = t.replace(/[A-Za-zÁÉÍÓÚÑáéíóúñ]+/g, prepararPalabraQu);
    t = t.replace(/w(?=[aeiouáéíóú])/gi, '\u0003');
    t = t.replace(/w/gi, 'u');
    t = t.replace(/[A-Za-zÁÉÍÓÚÑáéíóúñ\u0003]+/g, acentuarPalabraQu);
    return t.replace(/\u0003/g, 'hu');
}

function speakBrowser(texto, lang, seq) {
    if (!window.speechSynthesis) return Promise.resolve();
    var qu = lang === 'qu';
    var trozos = trocearVoz(texto, 180);
    return new Promise(function (resolve) {
        var i = 0;
        function cortado() { return !S.voice || (seq != null && seq !== S.speakSeq); }
        function hablar() {
            if (cortado() || i >= trozos.length) { resolve(); return; }
            var trozo = trozos[i++];
            var u = new SpeechSynthesisUtterance(qu ? adaptarQuechua(trozo) : trozo);
            u.rate = qu ? 0.88 : 1.03;
            u.pitch = qu ? 1 : 1.04;
            u.volume = 1;
            var v = pickEspVoice(qu);
            if (v) { u.voice = v; u.lang = v.lang; }
            else { u.lang = 'es-BO'; }
            u.onend = u.onerror = function () { setTimeout(hablar, qu ? 260 : 70); };
            window.speechSynthesis.speak(u);
        }
        if (!window.speechSynthesis.getVoices().length) {
            var arrancado = false;
            var arrancar = function () {
                if (arrancado) return;
                arrancado = true;
                hablar();
            };
            window.speechSynthesis.onvoiceschanged = arrancar;
            setTimeout(arrancar, 1200);
        } else {
            hablar();
        }
    });
}

function limpiarParaVoz(text) {
    var clean = String(text)
        // 1) Quitar enlaces y citas antes de limpiar simbolos.
        .replace(/\[([^\]]+)\]\([^)]*\)/g, '$1')
        .replace(/https?:\/\/\S+/g, ' ')
        .replace(/&nbsp;/g, ' ')
        .replace(/&amp;/g, 'y')
        // 2) Unidades y abreviaturas para leer con naturalidad.
        .replace(/\bBs\.?\s*(\d+(?:[.,]\d+)?)/gi, '$1 bolivianos')
        .replace(/\bAv\.\s*/gi, 'avenida ')
        .replace(/\bSt\.\s*/gi, 'santo ')
        .replace(/\bN[°º]\s*/gi, 'número ')
        .replace(/\bS\/N\b/gi, 'sin número')
        .replace(/(\d+(?:[.,]\d+)?)\s*%/g, '$1 por ciento')
        .replace(/\bkm\/h\b/gi, 'kilómetros por hora')
        .replace(/\bkm\b/gi, 'kilómetros')
        // 3) Listas y saltos de linea -> frases fluidas con pausa.
        .replace(/^\s*[-•·◦▪–—]\s*/gm, '')
        .replace(/\n{2,}/g, '. ')
        .replace(/\n/g, '. ')
        // 4) Quitar todo lo que no sea letra, numero, espacio o puntuacion basica:
        //    la voz nunca pronuncia emojis ni simbolos.
        .replace(/[^\p{L}\p{N}\s.,;:!?¿¡'"()%+/&@-]/gu, ' ')
        // 5) Puntuacion: pausa despues de cada signo, sin romper decimales ni abreviaturas.
        .replace(/([,;:!?¿¡.])(?![ \s\d])/g, '$1 ')
        .replace(/\s+([,.!?;:])/g, '$1')
        .replace(/\s+/g, ' ')
        .replace(/^[.?\s]+/, '')
        .trim();
    if (clean.length > 1400) {
        clean = clean.substring(0, 1400);
        var corte = Math.max(clean.lastIndexOf('.'), clean.lastIndexOf('!'), clean.lastIndexOf('?'));
        clean = corte > 200 ? clean.substring(0, corte + 1) : clean;
    }
    return clean;
}

function pedirTTS(texto, lang) {
    var control = window.AbortController ? new AbortController() : null;
    var reloj = control ? setTimeout(function () { control.abort(); }, 9000) : null;
    return fetch('/api/tts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            text: texto,
            language: lang === 'qu' ? 'qu' : 'es',
            voice: S.vozTTS || ''
        }),
        signal: control ? control.signal : undefined
    })
    .then(function (r) { return r.ok ? r.json() : null; })
    .catch(function () { return null; })
    .then(function (data) {
        if (reloj) clearTimeout(reloj);
        return data;
    });
}

function reproducirAudio(url, seq) {
    return new Promise(function (resolve, reject) {
        var audio = new Audio();
        audio.preload = 'auto';
        audio.src = url;
        S.audio = audio;
        var cerrado = false;
        function fin() {
            if (cerrado) return;
            cerrado = true;
            if (S.audio === audio) S.audio = null;
            resolve();
        }
        function fallo() {
            if (cerrado) return;
            cerrado = true;
            if (S.audio === audio) S.audio = null;
            reject(new Error('sin-audio'));
        }
        audio.onended = fin;
        audio.onerror = fallo;
        audio.onpause = function () { if (seq !== S.speakSeq) fin(); };
        var intento = audio.play();
        if (intento && intento.catch) intento.catch(fallo);
    });
}

/* ===== COLA DE VOZ: cada respuesta espera su turno ===== */
function encolarVoz(text, lang, cortar) {
    if (cortar) stopSpeaking();
    if (!S.voice) return Promise.resolve();
    var clean = limpiarParaVoz(text);
    if (!clean) return Promise.resolve();
    return new Promise(function (resolve) {
        S.vozCola.push({ texto: clean, lang: lang || S.lang, done: resolve });
        reproducirCola();
    });
}

function reproducirCola() {
    if (S.vozOcupada) return;
    S.vozOcupada = true;
    var gen = S.vozGen;
    function siguiente() {
        if (gen !== S.vozGen) return;
        if (!S.vozCola.length) {
            S.vozOcupada = false;
            terminarVoz();
            alQuedarEnSilencio();
            return;
        }
        var item = S.vozCola.shift();
        S.vozActual = item;
        var cerrado = false;
        function fin() {
            if (cerrado) return;
            cerrado = true;
            if (S.vozActual === item) S.vozActual = null;
            try { item.done(); } catch (e) {}
            siguiente();
        }
        hablarItem(item, gen, fin);
    }
    siguiente();
}

function hablarItem(item, gen, fin) {
    var seq = S.speakSeq;
    S.speaking = true;
    if (window.sacabaMascotTalking) window.sacabaMascotTalking(true);

    // Red de seguridad: si el audio se queda colgado, la cola no se detiene.
    var limite = setTimeout(function () {
        item.vencido = true;
        S.speakSeq++;
        if (S.audio) { try { S.audio.pause(); } catch (e) {} S.audio = null; }
        if (window.speechSynthesis) window.speechSynthesis.cancel();
        fin();
    }, Math.max(12000, item.texto.length * 95));

    // Se piden todas las frases a la vez: la primera suena en ~1 s y las
    // demas ya estan listas mientras se reproduce la anterior.
    var trozos = trocearVoz(item.texto, 110);
    var pedidos = trozos.map(function (trozo) { return pedirTTS(trozo, item.lang); });
    function detenido() { return item.vencido || gen !== S.vozGen || seq !== S.speakSeq || !S.voice; }

    function paso(i) {
        if (detenido() || i >= pedidos.length) return Promise.resolve();
        return pedidos[i].then(function (data) {
            if (detenido()) return;
            if (!data || !data.audio_url) {
                return speakBrowser(trozos.slice(i).join(' '), item.lang, seq);
            }
            return reproducirAudio(data.audio_url, seq).then(function () {
                if (detenido()) return;
                return paso(i + 1);
            }, function () {
                if (detenido()) return;
                return speakBrowser(trozos.slice(i).join(' '), item.lang, seq);
            });
        }, function () {
            if (detenido()) return;
            return speakBrowser(trozos.slice(i).join(' '), item.lang, seq);
        });
    }

    paso(0).then(function () {
        clearTimeout(limite);
        fin();
    }, function () {
        clearTimeout(limite);
        fin();
    });
}

function speakText(text, lang, cortar) {
    if (!S.voice) return Promise.resolve();
    return encolarVoz(text, lang || S.lang, cortar);
}

/* ===== CONSTRUIR HTML ===== */
function buildHTML() {
    return '<button class="cw-fab" id="cw-fab">' +
        '<span class="cw-pulse"></span>' +
        '<img class="cw-fab-logo" src="' + S.logoSrc + '" alt="Sami, asistente de Sacaba">' +
        '<svg class="cw-fab-close" viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg>' +
        '<span class="cw-badge" id="cw-badge">1</span></button>' +
    '<div class="cw-window" id="cw-window">' +
        '<div class="cw-header"><div class="cw-h-left"><div class="cw-h-avatar"><img class="cw-h-logo" src="' + S.logoSrc + '" alt="Sami, asistente municipal"></div>' +
        '<div class="cw-h-info"><h3 id="cw-title">' + UI.es.title + '</h3><span id="cw-sub"><span class="cw-online-dot"></span>' + UI.es.sub + '</span></div></div>' +
        '<div class="cw-h-actions">' +
            '<div class="cw-voz"><button id="cw-voz" type="button" title="Voz de Sami">Voz · ' + nombreVoz(S.vozTTS) + '</button></div>' +
            '<div class="cw-lang"><button class="active" data-lang="es">ES</button><button data-lang="qu">QU</button></div>' +
        '</div></div>' +
        '<div class="cw-msgs" id="cw-msgs"></div>' +
        '<div class="cw-typing" id="cw-typing"><span></span><span></span><span></span></div>' +
        '<div class="cw-opts" id="cw-opts"></div>' +
        '<div class="cw-input">' +
            '<button id="cw-hf" class="cw-hf-btn" type="button" aria-pressed="false" title="Manos libres: di &quot;Sami, quiero saber...&quot;"><svg viewBox="0 0 24 24"><path d="M12 1a9 9 0 0 0-9 9v7a3 3 0 0 0 3 3h3v-8H5v-2a7 7 0 0 1 14 0v2h-4v8h4a3 3 0 0 0 3-3v-7a9 9 0 0 0-9-9z"/></svg></button>' +
            '<button id="cw-mic" class="cw-mic-btn" type="button" title="Hablar - dictado por voz">' + MIC_ICON + '</button>' +
            '<input type="text" id="cw-in" placeholder="' + UI.es.ph + '" autocomplete="off">' +
            '<button id="cw-send" type="button" title="Enviar mensaje"><svg viewBox="0 0 24 24"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/></svg></button>' +
        '</div>' +
        '<div class="cw-powered">' + UI.es.powered + '</div></div>';
}

function escapeHtml(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;')
        .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function linkify(html) {
    return html.replace(/(^|[\s(])((?:https?:\/\/|\/tramite\/)[^\s<>"'()]+)/g, function(m, pre, url) {
        return pre + '<a class="cw-link" href="' + url + '" target="_blank" rel="noopener">' + url + '</a>';
    });
}

function addMsg(text, type, opts) {
    if (type === 'user') stopSpeaking();
    var msgs = document.getElementById('cw-msgs');
    var d = document.createElement('div');
    d.className = 'cw-msg ' + type;
    var av = type === 'bot' ? '<div class="cw-msg-av"><img src="' + S.logoSrc + '" alt="Sami"></div>' : '<div class="cw-msg-av"><i class="fas fa-user"></i></div>';
    var formatted = linkify(escapeHtml(text).replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/\n/g, '<br>'));
    var speakBtn = type === 'bot' ? '<button class="cw-speak-btn" onclick="window._speakMsg(this)" title="Escuchar respuesta"><svg viewBox="0 0 24 24" width="14" height="14"><path d="M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z"/></svg></button>' : '';
    d.innerHTML = av + '<div class="cw-msg-b">' + formatted + '</div>' + speakBtn;
    msgs.appendChild(d);
    msgs.scrollTop = msgs.scrollHeight;
    if (type === 'bot' && !S.silent && !S.silentFijo && !(opts && opts.silent)) speakText(text, S.lang);
}

window._speakMsg = function(btn) {
    var msgEl = btn.closest('.cw-msg');
    if (msgEl) {
        var textEl = msgEl.querySelector('.cw-msg-b');
        if (textEl) speakText(textEl.textContent, S.lang, true);
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
    c.classList.remove('is-open');
    c.innerHTML = '';
    opts.forEach(function(o) {
        var b = document.createElement('button');
        b.className = 'cw-opt';
        b.type = 'button';
        b.textContent = o;
        if (o === UI.es.consultas_btn || o === UI.qu.consultas_btn) {
            bindConsultaBtn(b);
        } else {
            b.onclick = function() {
                addMsg(o, 'user');
                c.innerHTML = '';
                playSound('send');
                sendToAI(o);
            };
        }
        c.appendChild(b);
    });
}

function showConsultaBtn() {
    if (S.consultas) return;
    var c = document.getElementById('cw-opts');
    if (!c) return;
    showOpts([UI[S.lang].consultas_btn]);
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
    if (S.busy) {
        S.pendingLang = lang;
        return;
    }
    var msgs = document.getElementById('cw-msgs');
    msgs.innerHTML = '';
    document.getElementById('cw-opts').innerHTML = '';
    document.getElementById('cw-opts').classList.remove('is-open');
    S.consultas = false;
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
            showConsultaBtn();
            S.busy = false;
            return;
        }
        var entry = S.log[i]; i++;
        if (entry.type === 'user') {
            addMsg(translateUser(entry.text, lang), 'user');
            next();
            return;
        }
        if (entry.resp && entry.respLang === lang) {
            addMsg(entry.resp, 'bot');
            next();
            return;
        }
        showTyping();
        fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: entry.query, language: lang === 'qu' ? 'qu' : 'auto', useAI: false })
        }).then(function(r) { return r.json(); })
          .then(function(data) {
              hideTyping();
              entry.resp = data.response || getResp(entry.query);
              entry.respLang = lang;
              addMsg(entry.resp, 'bot');
              next();
          })
          .catch(function() {
              hideTyping();
              addMsg(getResp(entry.query), 'bot');
              next();
          });
    }
    next();
}

function flushPendingLang() {
    if (!S.pendingLang) return;
    var lang = S.pendingLang;
    S.pendingLang = null;
    renderConversation(lang);
}

function greet() {
    if (document.getElementById('cw-msgs').children.length) return;
    showTyping();
    setTimeout(function() {
        hideTyping();
        addMsg(UI[S.lang].greeting, 'bot');
        playSound('message');
        setTimeout(function() {
            addMsg(UI[S.lang].greeting2, 'bot');
            showOpts(UI[S.lang].greeting_opts);
            // La bienvenida se lee desde el inicio, sin saltar al final.
            setTimeout(function() {
                var msgs = document.getElementById('cw-msgs');
                if (msgs && !S.log.length) msgs.scrollTop = 0;
            }, 350);
        }, 600);
    }, 900);
}

function applyLanguageUI(lang) {
    S.lang = lang;
    var title = document.getElementById('cw-title');
    if (title) title.textContent = UI[lang].title;
    var sub = document.getElementById('cw-sub');
    if (sub) sub.innerHTML = '<span class="cw-online-dot"></span>' + UI[lang].sub;
    var inp = document.getElementById('cw-in');
    if (inp && !S.bloqueado) inp.placeholder = UI[lang].ph;
    var pwr = document.querySelector('.cw-powered');
    if (pwr) pwr.textContent = UI[lang].powered;
    document.querySelectorAll('.cw-lang button').forEach(function(b) {
        b.classList.toggle('active', b.dataset.lang === lang);
    });
    if (S.consultas) showConsultas();
}

function init(options) {
    var el = document.getElementById('chatbot-widget');
    if (!el) return;
    options = options || {};
    S.embedded = !!options.embedded;
    S.voice = options.voice !== false;
    el.innerHTML = buildHTML();

    var fab = document.getElementById('cw-fab');
    var win = document.getElementById('cw-window');

    if (S.embedded) {
        el.classList.add('is-embedded');
        S.open = true;
        win.classList.add('open');
        fab.setAttribute('aria-hidden', 'true');
        fab.style.display = 'none';
        if (options.defaultLanguage === 'qu') applyLanguageUI('qu');
        // La presentacion habla por su cuenta: la bienvenida escrita no debe
        // adelantarse ni duplicar el audio, y el chat espera su turno.
        S.silentFijo = true;
        greet();
        bloquearChat(true);

        // En el portal el widget va embebido y su cabecera no se muestra:
        // el selector de voz pasa a la barra visible junto al botón de reinicio.
        var barra = document.querySelector('.p-chat-top');
        var selectorVoz = document.querySelector('.cw-voz');
        var reinicio = document.getElementById('btnResetChat');
        if (barra && selectorVoz) {
            if (reinicio && reinicio.parentNode === barra) barra.insertBefore(selectorVoz, reinicio);
            else barra.appendChild(selectorVoz);
        }
    } else {
        fab.onclick = function() {
            S.open = !S.open;
            win.classList.toggle('open', S.open);
            fab.classList.toggle('open', S.open);
            document.getElementById('cw-badge').style.display = 'none';
            playSound('open');
            if (S.open) greet();
        };
        setTimeout(function() { document.getElementById('cw-badge').style.display = 'flex'; }, 2000);
    }

    document.getElementById('cw-send').onclick = function() {
        var inp = document.getElementById('cw-in');
        var msg = inp.value.trim();
        if (!msg || S.busy) return;
        // Lo escrito tambien se interpreta: "multa cuna" se muestra "multakuna".
        msg = interpretarQuechua(msg);
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

    document.getElementById('cw-mic').onclick = function() {
        // El microfono manual manda: apaga la escucha automatica y alterna dictado.
        S.autoListen = false;
        S.autoTurno = false;
        if (S.handsFree) toggleHandsFree();
        stopSpeaking();
        if (navigator.mediaDevices && window.MediaRecorder) {
            if (GRAB.activa) detenerGrabacionServidor();
            else grabarServidor(true);
            return;
        }
        startRecording();
    };
    var hf = document.getElementById('cw-hf');
    if (hf) hf.onclick = function() { toggleHandsFree(); };

    document.querySelectorAll('.cw-lang button').forEach(function(btn) {
        btn.onclick = function() {
            var lang = this.dataset.lang;
            if (S.lang === lang) return;
            // ack=true: corta la voz actual y confirma en el nuevo idioma.
            switchLang(lang, false, true);
        };
    });

    var botonVoz = document.getElementById('cw-voz');
    if (botonVoz) {
        botonVoz.title = 'Voz de Sami: ' + nombreVoz(S.vozTTS) + ' (toca para cambiar)';
        botonVoz.onclick = function() {
            var actual = 0;
            for (var i = 0; i < VOCES_TTS.length; i++) {
                if (VOCES_TTS[i].id === S.vozTTS) actual = i;
            }
            var siguiente = VOCES_TTS[(actual + 1) % VOCES_TTS.length];
            S.vozTTS = siguiente.id;
            try { localStorage.setItem(VOZ_KEY, siguiente.id); } catch (e) {}
            this.textContent = 'Voz · ' + siguiente.nombre;
            this.title = 'Voz de Sami: ' + siguiente.nombre + ' (toca para cambiar)';
            speakText(S.lang === 'qu'
                ? 'Allillanchu, kay hina rimani.'
                : 'Hola, así suena mi voz.', S.lang, true);
        };
        fetch('/api/tts/status').then(function(r) { return r.json(); }).then(function(d) {
            if (d && d.disponible === false) botonVoz.style.display = 'none';
        }).catch(function() {});
    }

    if (window.speechSynthesis) {
        window.speechSynthesis.onvoiceschanged = function() { window.speechSynthesis.getVoices(); };
    }
}

window.initChatbotWidget = init;
window.openChatbot = function() {
    if (S.embedded) return;
    if (!S.open) document.getElementById('cw-fab').click();
};
window.openChatWithQuery = function(q, opts) {
    if (!S.embedded && !S.open) document.getElementById('cw-fab').click();
    setTimeout(function() {
        addMsg(q, 'user');
        playSound('send');
        document.getElementById('cw-opts').innerHTML = '';
        sendToAI(q, opts && opts.porVoz ? { porVoz: true } : undefined);
    }, S.embedded ? 100 : 400);
};

/* ===== API PUBLICA PARA EL PORTAL ===== */
window.sacabaSpeak = function(text, lang) { return speakText(text, lang || S.lang); };
window.sacabaStopSpeaking = stopSpeaking;
window.sacabaSetVoice = function(on) { S.voice = !!on; if (!S.voice) stopSpeaking(); };
window.sacabaSetLang = function(lang) {
    if (lang !== 'es' && lang !== 'qu') return;
    if (S.lang !== lang) {
        var hablaba = S.speaking || S.vozOcupada;
        // La pagina cambio de idioma: la voz anterior se corta en el acto.
        stopSpeaking();
        applyLanguageUI(lang);
        renderConversation(lang);
        if (hablaba) avisarIdioma(lang);
    }
};
window.SacabaDetectarIdioma = looksQuechua;
window.SacabaInterpretarQuechua = interpretarQuechua;
window.SacabaDetectarComandoIdioma = detectarComandoIdioma;
window.sacabaResetChat = function() {
    stopSpeaking();
    S.log = [];
    S.busy = false;
    S.silent = true;
    S.silentFijo = false;
    document.getElementById('cw-msgs').innerHTML = '';
    document.getElementById('cw-opts').innerHTML = '';
    hideTyping();
    S.silent = false;
    greet();
};

})();
