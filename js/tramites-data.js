/* ============================================
   DATOS DE TRÁMITES - G.A.M. SACABA 2026
   Exportado global para renderizar la grilla.
   ============================================ */
var TRAMITES_DATA = [
  {
    id: "carnet", num: "01", cat: "identidad", icon: "fas fa-id-card",
    n: "Carnet de Identidad (Cédula)",
    d: "Documento de identificación personal obligatorio para todos los bolivianos. Emisión o renovación en oficinas del SEGIP.",
    c: "Bs. 17", t: "Inmediato", dep: "SEGIP",
    where: "Oficinas del SEGIP de Sacaba", map: "https://maps.app.goo.gl/f27gLh5Accp2UmKW9",
    costDetail: "Se paga en Banco Unión u otras entidades financieras autorizadas.",
    req: ["Comprobante de pago de Bs. 17", "Cédula anterior (si es renovación)", "Denuncia policial (en caso de pérdida)"],
    pasos: ["Realiza el pago de Bs. 17 en Banco Unión", "Acude a las oficinas del SEGIP", "Presenta tu comprobante y cédula anterior", "Registran tus huellas dactilares", "Te toman una fotografía digital", "Listo, retiras tu carnet"],
    horario: "Lunes a viernes en horario hábil de oficina.", consejo: "Ve temprano para evitar filas y lleva todos tus documentos."
  },
  {
    id: "carnet_conducta", num: "02", cat: "identidad", icon: "fas fa-check-circle",
    n: "Certificado de Conducta (Antecedentes)",
    d: "Documento que certifica que no tienes antecedentes penales ni policiales en Bolivia. Se pide para empleo, estudios y trámites en el exterior.",
    c: "Bs. 20", t: "1 día", dep: "Policía (FELCC)",
    where: "Oficinas de la Policía (FELCC) - Sacaba", map: "",
    costDetail: "Tasa de ley del certificado.",
    req: ["Cédula de identidad vigente", "Formulario de solicitud", "Pago de la tasa correspondiente"],
    pasos: ["Reúne tu cédula de identidad", "Llena el formulario de solicitud", "Cancela el valor del certificado", "Te lo entregan impreso y firmado"],
    horario: "Lunes a viernes en horario hábil.", consejo: "También puedes tramitarlo en línea a través del portal policial."
  },
  {
    id: "licencia_conducir", num: "03", cat: "identidad", icon: "fas fa-car-side",
    n: "Licencia de Conducir",
    d: "Obtención o renovación de la licencia de conducir para vehículos livianos, pesados o motocicletas, a través del SEGIP.",
    c: "Según categoría", t: "1-2 semanas", dep: "SEGIP - Tránsito",
    where: "Centro de Licencias SEGIP - Sacaba o Cochabamba", map: "",
    costDetail: "El valor varía según la categoría (liviana, pesada, moto) y el curso.",
    req: ["Cédula de identidad vigente", "Certificado de conducta (antecedentes)", "Certificado médico de salud", "Comprobante de pago", "Fotografías (para el expediente)"],
    pasos: ["Reúne tus documentos", "Cancela el valor de la categoría", "Aprueba el examen teórico y práctico", "Entregan tu licencia"],
    horario: "Lunes a viernes en horario hábil.", consejo: "Renueva tu licencia antes del vencimiento para evitar sanciones."
  },
  {
    id: "registro_civil", num: "04", cat: "identidad", icon: "fas fa-stamp",
    n: "Registro Civil (Certificado de Nacimiento)",
    d: "Certificado de nacimiento, matrimonio o defunción expedido por el Registro Civil de Sacaba.",
    c: "Bs. 10", t: "Inmediato", dep: "Registro Civil",
    where: "Oficina del Registro Civil - Municipalidad de Sacaba", map: "",
    costDetail: "Bs. 10 por certificado (el valor puede variar).",
    req: ["Cédula de identidad del solicitante", "Datos del inscrito (nombres, fecha y lugar)", "En caso de aclaración, partida original"],
    pasos: ["Acude al Registro Civil de Sacaba", "Solicita el certificado con los datos", "Cancela el valor", "Retira tu certificado"],
    horario: "Lunes a viernes en horario hábil.", consejo: "Lleva los datos exactos del inscrito para una búsqueda rápida."
  },
  {
    id: "residencia", num: "05", cat: "vivienda", icon: "fas fa-home",
    n: "Constancia de Residencia",
    d: "Certifica que vives en el municipio de Sacaba. Se usa para trámites educativos, laborales y de servicios.",
    c: "Bs. 15", t: "2-3 días", dep: "Registro Social",
    where: "Dirección de Registro Social - Municipalidad de Sacaba", map: "",
    costDetail: "Pago en caja municipal.",
    req: ["Fotocopia de cédula de identidad", "Fotocopia de libreta de servicio militar", "Recibo de servicios básicos", "Declaración jurada de residencia", "Dos fotografías tamaño carnet"],
    pasos: ["Recoge el formulario en Ventanilla Única", "Llénalo con tus datos", "Presenta los requisitos", "Paga en caja", "Retira la constancia en 2-3 días"],
    horario: "Lun-Vie 8:00-12:00 / 14:30-18:30", consejo: "Lleva todos los requisitos para hacerlo en un solo viaje."
  },
  {
    id: "funcionamiento", num: "06", cat: "negocio", icon: "fas fa-store",
    n: "Licencia de Funcionamiento",
    d: "Permiso municipal (patente) para operar un negocio o actividad económica en Sacaba.",
    c: "Bs. 60 nuevo / Bs. 40 renov.", t: "Gestión directa", dep: "Ingresos y Servicios",
    where: "Dirección de Ingresos y Servicios Municipales - Caja Central o Subalcaldías", map: "",
    costDetail: "Los valores se compran en Caja Central o subalcaldías. Según el rubro puede pedirse licencia ambiental o contrato GERES.",
    req: ["Formulario de solicitud (Declaración Jurada)", "Fotocopia de CI del propietario", "Contrato de alquiler y/o anticrético", "Licencia ambiental o certificación (según rubro)", "Contrato o certificación de GERES (según rubro)", "Valores municipales: Bs. 60 o Bs. 40"],
    pasos: ["Compra los valores municipales (Bs. 60 o Bs. 40)", "Llena el formulario de solicitud", "Adjunta fotocopia de CI y contrato del local", "Presenta licencia ambiental y GERES si tu rubro lo exige", "Cancela en caja y recoge tu licencia"],
    horario: "Lunes a viernes en horario hábil", consejo: "Verifica los requisitos de tu rubro: industrias, comercio, restaurantes, talleres, salud y educación."
  },
  {
    id: "construccion", num: "07", cat: "vivienda", icon: "fas fa-building",
    n: "Permiso de Construcción (Plano de Vivienda)",
    d: "Aprobación de plano para construir o legalizar una vivienda u obra nueva en Sacaba.",
    c: "Valores municipales", t: "Según revisión", dep: "Urbanismo",
    where: "Dirección de Urbanismo - Gestión Urbana y Territorial", map: "",
    costDetail: "Costos por valores municipales (folder administrativo y timbres).",
    req: ["Memorial dirigido al Alcalde o Subalcalde", "Título de propiedad y folio real (máx. 1 año)", "Comprobante de pago IPBI de la última gestión", "Planos del proyecto por arquitecto (3 ejemplares + digital)", "Certificado catastral actualizado", "Fotocopia de CI vigente"],
    pasos: ["Prepara los planos con un arquitecto colegiado", "Reúne título, folio real y pago de IPBI", "Presenta memorial y requisitos en Urbanismo", "Adjunta certificado catastral y plano de lote", "Cancela valores y espera la aprobación"],
    horario: "Lunes a viernes en horario hábil", consejo: "Para legalizar obra construida se necesita además declaración jurada, carta notariada y fotos de la fachada."
  },
  {
    id: "catastro_empadronamiento", num: "08", cat: "vivienda", icon: "fas fa-map-marked-alt",
    n: "Empadronamiento Predial",
    d: "Registro de tu predio (terreno/lote) en el sistema catastral de Sacaba, con título o en calidad de poseedor.",
    c: "Valores municipales", t: "Gestión directa", dep: "Catastro",
    where: "Unidad de Catastro - Municipalidad de Sacaba", map: "",
    costDetail: "Folder administrativo y timbres de Bs. 10 (Decreto Municipal 014/2024).",
    req: ["Memorial firmado por el propietario", "Título de propiedad + folio real (con timbre Bs. 10)", "Plano de lote georreferenciado (impreso + shapefile)", "Formulario Declaración Jurada EMP-CAT-01", "Fotocopia de CI o cédula de extranjería"],
    pasos: ["Prepara memorial, título, folio real y plano georreferenciado", "Llena el formulario EMP-CAT-01", "Presenta todo en la Unidad de Catastro", "Cancela los valores municipales", "Queda registrado tu predio"],
    horario: "Lunes a viernes en horario hábil", consejo: "Si eres poseedor (sin título) también puedes empadronar: lleva minuta, boletas de servicios y declaración notariada."
  },
  {
    id: "catastro_certificado", num: "09", cat: "vivienda", icon: "fas fa-file-alt",
    n: "Certificado Catastral",
    d: "Certifica los datos de tu predio: ubicación, superficie y código catastral.",
    c: "Valores municipales", t: "Gestión directa", dep: "Catastro",
    where: "Unidad de Catastro - Municipalidad de Sacaba", map: "",
    costDetail: "Folder administrativo y timbres.",
    req: ["Memorial al Alcalde o Subalcalde", "Título de propiedad y folio real actualizado", "Reporte sin deudas (timbre Bs. 5)", "Fotocopia del plano aprobado y RTA", "Fotocopia de CI del propietario"],
    pasos: ["Reúne título, folio real y reporte sin deudas", "Adjunta plano aprobado y resolución técnica", "Presenta el memorial en Catastro", "Cancela valores", "Retira tu certificado catastral"],
    horario: "Lunes a viernes en horario hábil", consejo: "También puedes solicitar reimpresión o actualización del certificado."
  },
  {
    id: "catastro_avaluo", num: "10", cat: "vivienda", icon: "fas fa-money-check-alt",
    n: "Avalúo Catastral",
    d: "Cálculo del valor oficial de tu inmueble para impuestos, transferencias o regularizaciones.",
    c: "Valores municipales", t: "Gestión directa", dep: "Catastro",
    where: "Unidad de Catastro - Municipalidad de Sacaba", map: "",
    costDetail: "Folder administrativo.",
    req: ["Memorial solicitando el avalúo", "Título de propiedad y folio real actualizado", "Fotocopia del último impuesto o IPBI", "Plano de lote aprobado o georreferenciado", "Fotocopia de CI"],
    pasos: ["Presenta memorial y documentos en Catastro", "Adjunta título, folio real y último impuesto", "Entrega el plano del lote", "Cancela los valores", "Recibe el informe de avalúo"],
    horario: "Lunes a viernes en horario hábil", consejo: "El avalúo es la base para calcular impuestos prediales y tasas."
  },
  {
    id: "urbanismo_plano", num: "11", cat: "vivienda", icon: "fas fa-draw-polygon",
    n: "Aprobación de Plano (Terreno/Lote)",
    d: "Aprobación, anexión, división o subdivisión de plano de terreno lote (regularización predial).",
    c: "Valores municipales", t: "Según revisión", dep: "Urbanismo",
    where: "Dirección de Urbanismo - Municipalidad de Sacaba", map: "",
    costDetail: "Folder administrativo y timbres.",
    req: ["Memorial al Alcalde o Subalcalde", "Título de propiedad y folio real (máx. 1 año)", "Comprobante de IPBI de la última gestión", "Planos por arquitecto/ingeniero (5 ejemplares + shapefile)", "Fotocopia de CI vigente"],
    pasos: ["Contrata un profesional para los planos", "Reúne título, folio real y recibo de IPBI", "Presenta memorial y expediente en Urbanismo", "Cancela los valores municipales", "Espera la revisión y aprobación"],
    horario: "Lunes a viernes en horario hábil", consejo: "Incluye aprobación de plano, anexión y división/subdivisión de lotes."
  },
  {
    id: "urbanismo_ampliacion", num: "12", cat: "vivienda", icon: "fas fa-hammer",
    n: "Ampliación o Remodelación",
    d: "Aprobación municipal para ampliar o remodelar una construcción, casa o edificio.",
    c: "Valores municipales", t: "Según proyecto", dep: "Urbanismo",
    where: "Dirección de Urbanismo - Municipalidad de Sacaba", map: "",
    costDetail: "Folder administrativo y timbres.",
    req: ["Memorial al Alcalde o Subalcalde", "Título de propiedad y folio real actualizado", "Comprobante de IPBI", "Proyecto por arquitecto (3 ejemplares + CAD)", "Certificado catastral actualizado", "Plano de terreno aprobado"],
    pasos: ["Prepara el proyecto con un arquitecto", "Reúne título, IPBI y certificado catastral", "Presenta memorial y planos en Urbanismo", "Cancela valores", "Se aprueba el plano"],
    horario: "Lunes a viernes en horario hábil", consejo: "Edificios de 4+ niveles suman memorias sanitario, eléctrico y estructural."
  },
  {
    id: "urbanismo_uso_suelo", num: "13", cat: "vivienda", icon: "fas fa-landmark",
    n: "Certificación de Uso de Suelo",
    d: "Certificaciones de urbanismo: uso de suelo, rasante, línea nivel, zona y distrito, verificación de medidas.",
    c: "Valores municipales", t: "Gestión directa", dep: "Urbanismo",
    where: "Dirección de Urbanismo - Municipalidad de Sacaba", map: "",
    costDetail: "Folder administrativo y timbres.",
    req: ["Memorial o carta dirigida al Alcalde", "Título de propiedad y folio real actualizado", "Comprobante de IPBI (cuando corresponda)", "Plano de lote georreferenciado aprobado", "Fotocopia de CI"],
    pasos: ["Indica el motivo en el memorial", "Adjunta título, folio real e IPBI", "Incluye el plano correspondiente", "Cancela valores", "Recibe la certificación"],
    horario: "Lunes a viernes en horario hábil", consejo: "También se emiten por orden judicial y límites de áreas protegidas."
  },
  {
    id: "urbanismo_verja", num: "14", cat: "vivienda", icon: "fas fa-fence",
    n: "Permiso de Trabajos Menores (Verja)",
    d: "Permiso para construcción de verja, cerco o muro (trabajos menores de construcción).",
    c: "Valores municipales", t: "Gestión directa", dep: "Urbanismo",
    where: "Dirección de Urbanismo - Municipalidad de Sacaba", map: "",
    costDetail: "Folder administrativo y timbres.",
    req: ["Memorial firmado por el propietario", "Título de propiedad y folio real actualizado", "Comprobante de IPBI", "Planos de verja por arquitecto (3 ejemplares)", "Plano de lote aprobado"],
    pasos: ["Prepara los planos de la verja", "Reúne título, IPBI y plano de lote", "Presenta el memorial en Urbanismo", "Cancela valores", "Aprueban el permiso"],
    horario: "Lunes a viernes en horario hábil", consejo: "Aplica para verjas, cercos y muros; trámite más simple que el plano de vivienda."
  },
  {
    id: "urbanismo_horizontal", num: "15", cat: "vivienda", icon: "fas fa-building",
    n: "Propiedad Horizontal o Condominio",
    d: "Adecuación de un inmueble a propiedad horizontal (departamentos, parqueos, bauleras).",
    c: "Valores municipales", t: "Según revisión", dep: "Urbanismo",
    where: "Dirección de Urbanismo - Municipalidad de Sacaba", map: "",
    costDetail: "Folder administrativo y timbres.",
    req: ["Memorial al Alcalde o Subalcalde", "Título de propiedad y folio real", "Comprobante de IPBI", "Plano de adecuación por arquitecto (3 ejemplares)", "Certificado catastral", "Plano de terreno aprobado"],
    pasos: ["Contrata un arquitecto para el plano", "Reúne título, IPBI y certificado catastral", "Presenta el expediente en Urbanismo", "Cancela valores", "Recibe la resolución"],
    horario: "Lunes a viernes en horario hábil", consejo: "Sirve para regularizar departamentos, locales, parqueos y bauleras."
  },
  {
    id: "vehiculo_inscripcion", num: "16", cat: "servicios", icon: "fas fa-car-side",
    n: "Inscripción de Vehículo (RUAT)",
    d: "Registro RUAT de un vehículo automotor nuevo (importación directa o casa comercial).",
    c: "Según trámite", t: "Gestión directa", dep: "Vehículos",
    where: "Unidad de Vehículos - Municipalidad de Sacaba", map: "",
    costDetail: "Folder administrativo y valores según trámite (Decreto Municipal 015/2024).",
    req: ["Declaración de importación o DUI y FRV", "Fotocopia de CI del propietario", "Certificado de inscripción a Impuestos Nacionales (jurídico)", "Testimonio de poder (si compra sociedad)", "Foto fondo rojo 3x3 (persona natural)"],
    pasos: ["Reúne documentación de importación o factura", "Adjunta CI, fotografía y folder", "Presenta en la Unidad de Vehículos", "Cancela los valores", "Se inscribe tu vehículo en RUAT"],
    horario: "Lunes a viernes en horario hábil", consejo: "El Decreto Municipal 015/2024 regula todos los trámites vehiculares."
  },
  {
    id: "vehiculo_transferencia", num: "17", cat: "servicios", icon: "fas fa-exchange-alt",
    n: "Transferencia de Vehículo",
    d: "Cambio de propietario (traspaso) de un vehículo registrado en el RUAT.",
    c: "2 timbres Bs. 10", t: "Gestión directa", dep: "Vehículos",
    where: "Unidad de Vehículos - Municipalidad de Sacaba", map: "",
    costDetail: "2 timbres municipales de Bs. 10 y folder administrativo.",
    req: ["Minuta de compra-venta (original + 2 copias)", "CRPVA original y fotocopia (RUAT 03)", "Fotocopia de CI de comprador y vendedor", "Foto fondo rojo 3x3", "Vehículo sin deudas tributarias"],
    pasos: ["Firma la minuta de compra-venta", "Reúne CRPVA, CI y fotografía", "Cancela los timbres municipales", "Presenta el expediente en Vehículos", "Se registra el cambio de propietario"],
    horario: "Lunes a viernes en horario hábil", consejo: "El vehículo no debe tener impuesto, gravámenes, reporte de robado ni bloqueos."
  },
  {
    id: "vehiculo_radicatoria", num: "18", cat: "servicios", icon: "fas fa-truck-moving",
    n: "Cambio de Radicatoria",
    d: "Traslado del registro de un vehículo desde otro departamento o provincia hacia Sacaba.",
    c: "Timbre Bs. 40", t: "Gestión directa", dep: "Vehículos",
    where: "Unidad de Vehículos - Municipalidad de Sacaba", map: "",
    costDetail: "Timbre municipal de Bs. 40 y folder administrativo.",
    req: ["Minuta de compra-venta si hubo transferencia", "CRPVA (RUAT 03) original y fotocopia", "Fotocopia de CI del propietario", "Certificado de inscripción (jurídico)", "Foto fondo rojo 3x3"],
    pasos: ["Reúne CRPVA y documentos", "Adjunta minuta si hubo transferencia", "Cancela el timbre de Bs. 40", "Presenta en la Unidad de Vehículos", "Queda radicado en Sacaba"],
    horario: "Lunes a viernes en horario hábil", consejo: "El vehículo no debe tener deudas ni reporte de robado."
  },
  {
    id: "vehiculo_reemplaque", num: "19", cat: "servicios", icon: "fas fa-car",
    n: "Reemplaque de Vehículo",
    d: "Obtención de nuevas placas para vehículos no reemplazados (sistema PTA).",
    c: "Según trámite", t: "Gestión directa", dep: "Vehículos",
    where: "Unidad de Vehículos - Municipalidad de Sacaba", map: "",
    costDetail: "Valores según trámite (folder administrativo).",
    req: ["Declaración jurada de vehículo no reemplazado (GAMS)", "PTA/COPO original y fotocopia", "Carnet de propiedad (sistema antiguo)", "Fotocopia de CI", "Folder administrativo"],
    pasos: ["Solicita la declaración jurada en GAMS", "Reúne PTA/COPO, carnet y CI", "Presenta el expediente en Vehículos", "Cancela los valores", "Recibe las nuevas placas"],
    horario: "Lunes a viernes en horario hábil", consejo: "Si hay transferencia, tramita el reemplaque con la minuta de compra-venta."
  },
  {
    id: "vehiculo_baja", num: "20", cat: "servicios", icon: "fas fa-ban",
    n: "Baja Tributaria del Vehículo",
    d: "Dar de baja el vehículo en el RUAT por siniestro, robo, exportación o fuera de circulación.",
    c: "Timbre Bs. 20", t: "Gestión directa", dep: "Vehículos",
    where: "Unidad de Vehículos - Municipalidad de Sacaba", map: "",
    costDetail: "Timbre municipal de Bs. 20 y folder administrativo.",
    req: ["Formulario ANEXO 1", "CI vigente del propietario", "CRPVA original y placas", "Informe de Tránsito/DIPROVE, denuncia o resolución de Aduana", "Sin deudas de impuestos"],
    pasos: ["Solicita el formulario ANEXO 1", "Entrega CRPVA y placas originales", "Acompaña informe, denuncia o resolución", "Cancela el timbre de Bs. 20", "Se da de baja el vehículo"],
    horario: "Lunes a viernes en horario hábil", consejo: "Baja por fuera de circulación exige al menos 5 años de radicatoria en Sacaba."
  },
  {
    id: "prediales", num: "21", cat: "servicios", icon: "fas fa-receipt",
    n: "Impuestos Prediales",
    d: "Pago anual del impuesto a la propiedad inmueble en la municipalidad.",
    c: "0.5% - 1%", t: "Inmediato", dep: "Rentas Internas",
    where: "Dirección de Rentas Internas - Municipalidad de Sacaba", map: "",
    costDetail: "0.5% - 1% sobre el valor catastral del inmueble.",
    req: ["Cédula de identidad", "Título de propiedad", "Certificado catastral actualizado"],
    pasos: ["Consulta el monto en Rentas Internas", "Paga en caja municipal o bancos", "Guarda tu comprobante", "Muéstralo si lo requieren"],
    horario: "Lunes a viernes en horario hábil", consejo: "Paga antes del vencimiento para evitar recargos y multas."
  },
  {
    id: "agua", num: "22", cat: "servicios", icon: "fas fa-tint",
    n: "Servicio de Agua Potable",
    d: "Trámite para conectar o regularizar el servicio de agua potable.",
    c: "Bs. 50-200", t: "5-10 días", dep: "Empresa de Agua",
    where: "Empresa de Agua Potable de Sacaba", map: "",
    costDetail: "Según tipo de conexión.",
    req: ["Solicitud formal", "Cédula de identidad", "Constancia de propiedad o recibo de alquiler", "Pago de conexión"],
    pasos: ["Presenta tu solicitud", "Paga la conexión", "Espera la inspección", "Recibe tu servicio"],
    horario: "Lunes a viernes en horario hábil", consejo: "Verifica tu deuda antes de solicitar."
  },
  {
    id: "eventos", num: "23", cat: "negocio", icon: "fas fa-calendar-alt",
    n: "Permiso para Eventos",
    d: "Autorización para realizar eventos públicos o privados en Sacaba.",
    c: "Bs. 30-300", t: "3-5 días", dep: "Seguridad Ciudadana",
    where: "Dirección de Seguridad Ciudadana", map: "",
    costDetail: "Según tipo y magnitud del evento.",
    req: ["Solicitud con detalles del evento", "Cédula del organizador", "Póliza de responsabilidad civil", "Pago de tasa"],
    pasos: ["Presenta la solicitud", "Adjunta los documentos", "Paga la tasa", "Recibe el permiso", "Cumple las condiciones"],
    horario: "Lunes a viernes en horario hábil", consejo: "Solicita con anticipación para evitar contratiempos."
  },
  {
    id: "solteria", num: "24", cat: "identidad", icon: "fas fa-user",
    n: "Constancia de Soltería",
    d: "Certificado que acredita tu estado civil soltero.",
    c: "Bs. 10", t: "Inmediato", dep: "Registro Civil",
    where: "Dirección de Registro Civil", map: "",
    costDetail: "Pago de tasa en caja.",
    req: ["Cédula de identidad", "Dos testigos con cédula", "Pago de tasa"],
    pasos: ["Acude a Registro Civil con tus testigos", "Presenta la cédula", "Firma la declaración", "Paga la tasa", "Recibe tu constancia"],
    horario: "Lunes a viernes en horario hábil", consejo: "Lleva testigos que te conozcan personalmente."
  },
  {
    id: "propiedad", num: "25", cat: "vivienda", icon: "fas fa-file-contract",
    n: "Registro de Propiedad",
    d: "Inscripción de bienes inmuebles para legalizar tu propiedad.",
    c: "Bs. 50-200", t: "15-30 días", dep: "Derechos Reales",
    where: "Dirección de Derechos Reales", map: "",
    costDetail: "Según el valor catastral del inmueble.",
    req: ["Título de propiedad original", "Plano de ubicación", "Cédula de identidad", "Pago de tasa"],
    pasos: ["Reúne los documentos", "Presenta en Derechos Reales", "Realiza el pago", "Espera la inscripción", "Retira tu certificado"],
    horario: "Lunes a viernes en horario hábil", consejo: "Verifica que no haya deudas pendientes."
  },
  {
    id: "nodeuda", num: "26", cat: "servicios", icon: "fas fa-check-circle",
    n: "Constancia de No Deuda",
    d: "Certifica que no tienes deudas tributarias con el municipio.",
    c: "Bs. 10", t: "1-2 días", dep: "Rentas Internas",
    where: "Dirección de Rentas Internas", map: "",
    costDetail: "Tasa municipal.",
    req: ["Cédula de identidad", "Certificado de propiedad"],
    pasos: ["Acude a Rentas Internas", "Presenta los documentos", "Verifican tus deudas", "Paga si tienes deudas", "Se emite la constancia"],
    horario: "Lunes a viernes en horario hábil", consejo: "Verifica tus deudas antes de solicitar."
  }
];

/* ============================================
   TRADUCCIÓN AL QUECHUA (runasimi boliviano)
   Usada por la grilla cuando la página está en quechua.
   ============================================ */
var TRAMITES_QU = {
  carnet: { qn: "Carnet de Identidad (Cédula)", qd: "Tukuy bolivianopaq obligatorio riqsichinaykuna documento. SEGIP oficinaspi hurqokunki utaq musuqmanta ruwakunki." },
  carnet_conducta: { qn: "Conducta Certificado (Antecedente)", qd: "Boliviapi mana penaltapas ni policial yachaycachay kasqaykita riqsichiq documento. Llankay, yachay nitaq huk paíspi trámitespaq mañakun." },
  licencia_conducir: { qn: "Manejo Licencia", qd: "Vehículokunata manejaspa licenciaykita hurqoy utaq renovay (SEGIP librupi)." },
  registro_civil: { qn: "Registro Civil (Nacimiento Certificado)", qd: "Sacabapi Registro Civil hurqun nacimiento, casamiento utaq wañuymanta certificadota." },
  residencia: { qn: "Tiyay Constancia", qd: "Sacaba munisipyupi tiyaq kasqaykita riqsichin. Educación, llankay nitaq servicios trámitespaq sumaqmi." },
  funcionamiento: { qn: "Funcionamiento Licencia", qd: "Sacabapi negocio utaq actividad económica ruwanapaq munisipyu permiso (patente)." },
  construccion: { qn: "Construcción Permiso (Wasimanta Plano)", qd: "Sacabapi wasita utaq musuq obrata ruwanapaq planota aprobana nitaq legalizana." },
  catastro_empadronamiento: { qn: "Empadronamiento Predial", qd: "Predioyki (terreno/lote) Sacabaq catastro sistemapi registro." },
  catastro_certificado: { qn: "Certificado Catastral", qd: "Predioykimanta datosniyki riqsichin: maypim kachkan, superficie nitaq catastro código." },
  catastro_avaluo: { qn: "Avalúo Catastral", qd: "Impuestos, transferencia utaq regularizaciónpaq inmuebleykimanta oficial valoryuq yupay." },
  urbanismo_plano: { qn: "Plano Aprobación (Terreno/Lote)", qd: "Terreno loteq plano aprobación, anexión, división utaq subdivisión (predial regularización)." },
  urbanismo_ampliacion: { qn: "Ampliación utaq Remodelación", qd: "Construcción, wasi utaq edificiota amplianapaq utaq remodelanapaq munisipyu aprobación." },
  urbanismo_uso_suelo: { qn: "Uso de Suelo Certificación", qd: "Urbanismo certificaciones: suelo uso, rasante, línea nivel, zona utaq distrito, medidas verificación." },
  urbanismo_verja: { qn: "Trabajos Menores Permiso (Verja)", qd: "Verja, cerco utaq muro ruwanapaq permiso (menor construcción trabajos)." },
  urbanismo_horizontal: { qn: "Propiedad Horizontal utaq Condominio", qd: "Inmuebleta propiedad horizontal nisqanman acomoday (departamentos, parqueos, bauleras)." },
  vehiculo_inscripcion: { qn: "Vehículo Inscripción (RUAT)", qd: "Musuq vehículo automotor RUATpi registro (importación directa utaq casa comercial)." },
  vehiculo_transferencia: { qn: "Vehículo Transferencia", qd: "RUATpi registrasqa vehículoq dueño cambio (traspaso)." },
  vehiculo_radicatoria: { qn: "Radicatoria Cambio", qd: "Vehículoq registro huk departamento utaq provincia suyumanta Sacabaman apamuy." },
  vehiculo_reemplaque: { qn: "Vehículo Reemplaque", qd: "Mana reemplazasqa vehículokunapaq placas musuqmanta hurquy (PTA sistema)." },
  vehiculo_baja: { qn: "Vehículo Baja Tributaria", qd: "Vehículota RUATpi baja ruray siniestro, robo, exportación utaq mana circulaciónpaq." },
  prediales: { qn: "Predial Impuestukuna", qd: "Munisipyupi inmueble propiedad impuesto sapa wata pagana." },
  agua: { qn: "Yaku (Agua Potable) Servicio", qd: "Agua potable servicio conectay utaq regularizay trámite." },
  eventos: { qn: "Eventopaq Permiso", qd: "Sacabapi público utaq privado eventos ruwanapaq autorización." },
  solteria: { qn: "Soltería Constancia", qd: "Soltero kasqaykita riqsichiq estado civil certificado." },
  propiedad: { qn: "Propiedad Registro", qd: "Propiedad legalizaypaq bienes inmuebles inscripción." },
  nodeuda: { qn: "Mana Deuda Constancia", qd: "Munisipyuwan tributaria deudas mana kasqaykita riqsichin." }
};