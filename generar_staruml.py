# -*- coding: utf-8 -*-
"""
Genera diagramas StarUML profesionales (.mdj)
"""
import json
import uuid
import os

def uid():
    return str(uuid.uuid4()).replace("-", "")[:22] + "="

def ref(x):
    return {"$ref": x}

class StarUMLProject:
    def __init__(self, name):
        self.pid = uid()
        self.mid = uid()
        self.project = {
            "_type": "Project",
            "_id": self.pid,
            "_parent": None,
            "name": name,
            "ownedElements": [{
                "_type": "UMLModel",
                "_id": self.mid,
                "_parent": ref(self.pid),
                "name": "Model",
                "ownedElements": []
            }]
        }
        self.model = self.project["ownedElements"][0]
        self.all_elements = []

    def add_element(self, elem):
        self.all_elements.append(elem)
        self.model["ownedElements"].append(elem)

    def save(self, filepath):
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.project, f, indent=1, ensure_ascii=False)

    def use_case_diagram(self):
        did = uid()
        diagram = {
            "_type": "UMLUseCaseDiagram",
            "_id": did,
            "_parent": ref(self.mid),
            "name": "Diagrama de Casos de Uso",
            "visible": True,
            "defaultDiagram": True,
            "ownedViews": []
        }
        self.model["ownedElements"].append(diagram)

        # Actors - left side, well spaced
        actors_data = [
            ("Ciudadano", 60, 80),
            ("Administrador", 60, 520)
        ]
        actor_ids = []
        for name, x, y in actors_data:
            aid = uid()
            actor_ids.append(aid)
            # Actor element
            self.add_element({
                "_type": "UMLActor",
                "_id": aid,
                "_parent": ref(self.mid),
                "name": name
            })
            # Actor view
            diagram["ownedViews"].append({
                "_type": "UMLActorView",
                "_id": uid(),
                "_parent": ref(did),
                "model": ref(aid),
                "subViews": [{
                    "_type": "LabelView",
                    "_id": uid(),
                    "_parent": None,
                    "visible": True,
                    "enabled": True,
                    "lineColor": "#000000",
                    "fillColor": "#ffffff",
                    "fontColor": "#000000",
                    "font": "Arial;13;0",
                    "parentStyle": True,
                    "left": x + 5,
                    "top": y + 70,
                    "width": len(name) * 8,
                    "height": 16,
                    "text": name,
                    "horizontalAlignment": 2,
                    "verticalAlignment": 5
                }],
                "visible": True,
                "enabled": True,
                "lineColor": "#000000",
                "fillColor": "#ffffff",
                "fontColor": "#000000",
                "font": "Arial;13;0",
                "parentStyle": True,
                "showShadow": True,
                "containerChangeable": False,
                "left": x,
                "top": y,
                "width": 50,
                "height": 70
            })

        # Use Cases - center/right, well spaced
        uc_data = [
            ("Consultar Trámite", 320, 60),
            ("Buscar Trámite", 320, 140),
            ("Filtrar por Categoría", 320, 220),
            ("Consultar Multas", 320, 300),
            ("Usar Chatbot", 620, 60),
            ("Enviar Mensaje de Voz", 620, 140),
            ("Cambiar Idioma (ES/QU)", 620, 220),
            ("Consultar Institución", 620, 300),
            ("Actualizar Base Conocimientos", 450, 500)
        ]
        uc_ids = []
        for name, x, y in uc_data:
            ucid = uid()
            uc_ids.append(ucid)
            self.add_element({
                "_type": "UMLUseCase",
                "_id": ucid,
                "_parent": ref(self.mid),
                "name": name
            })
            diagram["ownedViews"].append({
                "_type": "UMLUseCaseView",
                "_id": uid(),
                "_parent": ref(did),
                "model": ref(ucid),
                "subViews": [{
                    "_type": "LabelView",
                    "_id": uid(),
                    "_parent": None,
                    "visible": True,
                    "enabled": True,
                    "lineColor": "#000000",
                    "fillColor": "#ffffff",
                    "fontColor": "#000000",
                    "font": "Arial;13;0",
                    "parentStyle": True,
                    "left": x + 15,
                    "top": y + 12,
                    "width": len(name) * 7,
                    "height": 16,
                    "text": name,
                    "horizontalAlignment": 2,
                    "verticalAlignment": 5
                }],
                "visible": True,
                "enabled": True,
                "lineColor": "#000000",
                "fillColor": "#ffffff",
                "fontColor": "#000000",
                "font": "Arial;13;0",
                "parentStyle": True,
                "showShadow": True,
                "containerChangeable": False,
                "left": x,
                "top": y,
                "width": 200,
                "height": 40
            })

        # Associations with lines
        # Ciudadano -> 8 use cases
        for i in range(8):
            rid = uid()
            self.add_element({
                "_type": "UMLAssociation",
                "_id": rid,
                "_parent": ref(self.mid),
                "name": "",
                "end1": {"_type": "UMLAssociationEnd", "_id": uid(), "_parent": ref(rid), "reference": ref(actor_ids[0])},
                "end2": {"_type": "UMLAssociationEnd", "_id": uid(), "_parent": ref(rid), "reference": ref(uc_ids[i])}
            })
            ax = actors_data[0][1] + 50
            ay = actors_data[0][2] + 35
            ux = uc_data[i][1]
            uy = uc_data[i][2] + 20
            diagram["ownedViews"].append({
                "_type": "UMLAssociationView",
                "_id": uid(),
                "_parent": ref(did),
                "model": ref(rid),
                "subViews": [],
                "visible": True,
                "enabled": True,
                "lineColor": "#000000",
                "fillColor": "#000000",
                "fontColor": "#000000",
                "font": "Arial;13;0",
                "parentStyle": True,
                "showShadow": False,
                "lineStyle": 0,
                "points": f"{ax}:{ay};{ux}:{uy}",
                "head": ref(uc_ids[i]),
                "tail": ref(actor_ids[0])
            })

        # Administrador -> Actualizar KB
        rid = uid()
        self.add_element({
            "_type": "UMLAssociation",
            "_id": rid,
            "_parent": ref(self.mid),
            "name": "",
            "end1": {"_type": "UMLAssociationEnd", "_id": uid(), "_parent": ref(rid), "reference": ref(actor_ids[1])},
            "end2": {"_type": "UMLAssociationEnd", "_id": uid(), "_parent": ref(rid), "reference": ref(uc_ids[8])}
        })
        ax = actors_data[1][1] + 50
        ay = actors_data[1][2]
        ux = uc_data[8][1] + 100
        uy = uc_data[8][2] + 40
        diagram["ownedViews"].append({
            "_type": "UMLAssociationView",
            "_id": uid(),
            "_parent": ref(did),
            "model": ref(rid),
            "subViews": [],
            "visible": True,
            "enabled": True,
            "lineColor": "#000000",
            "fillColor": "#000000",
            "fontColor": "#000000",
            "font": "Arial;13;0",
            "parentStyle": True,
            "showShadow": False,
            "lineStyle": 0,
            "points": f"{ax}:{ay};{ux}:{uy}",
            "head": ref(uc_ids[8]),
            "tail": ref(actor_ids[1])
        })

        return did

    def class_diagram(self):
        did = uid()
        diagram = {
            "_type": "UMLClassDiagram",
            "_id": did,
            "_parent": ref(self.mid),
            "name": "Diagrama de Clases",
            "visible": True,
            "defaultDiagram": True,
            "ownedViews": []
        }
        self.model["ownedElements"].append(diagram)

        # Classes - well spaced, no overlap
        classes_data = [
            ("Trámite", 40, 60, 220, [
                ("- id: str", "private"),
                ("- nombre: str", "private"),
                ("- descripcion: str", "private"),
                ("- costo: str", "private"),
                ("- tiempo: str", "private"),
                ("- requisitos: list", "private"),
                ("- pasos: list", "private")
            ], [
                ("+ get_info_es(): dict", "public"),
                ("+ get_info_qu(): dict", "public")
            ]),
            ("Multa", 40, 360, 220, [
                ("- tipo: str", "private"),
                ("- infracciones: list", "private"),
                ("- montos: str", "private"),
                ("- procedimiento: str", "private")
            ], [
                ("+ get_info_transito(): str", "public"),
                ("+ get_info_municipal(): str", "public")
            ]),
            ("Chatbot", 340, 60, 300, [
                ("- KB: dict", "private"),
                ("- MULTAS: dict", "private"),
                ("- UI: dict", "private"),
                ("- _client: OpenAI", "private"),
                ("- _ai_available: bool", "private")
            ], [
                ("+ normalize(text): str", "public"),
                ("+ detect_tramite(text): str", "public"),
                ("+ detect_intent(text): str", "public"),
                ("+ get_resp(text, lang): str", "public"),
                ("+ get_ai_resp(text, lang): str", "public"),
                ("+ build_card(tramite): str", "public"),
                ("+ build_tramite_list(lang): str", "public"),
                ("+ build_multas_string(lang): str", "public")
            ]),
            ("App Flask", 740, 60, 220, [
                ("- app: Flask", "private"),
                ("- routes: dict", "private")
            ], [
                ("+ index(): Response", "public"),
                ("+ chat(): Response", "public"),
                ("+ translate(): Response", "public"),
                ("+ audio_to_text(): Response", "public")
            ]),
            ("Widget Chatbot", 740, 320, 220, [
                ("- isOpen: bool", "private"),
                ("- messages: array", "private"),
                ("- currentLang: str", "private")
            ], [
                ("+ open(): void", "public"),
                ("+ close(): void", "public"),
                ("+ send(message): void", "public"),
                ("+ receive(response): void", "public")
            ])
        ]

        class_ids = []
        for name, x, y, w, attrs, ops in classes_data:
            cid = uid()
            class_ids.append(cid)

            # Calculate heights
            attr_h = len(attrs) * 18 + 10
            op_h = len(ops) * 18 + 10
            total_h = 25 + attr_h + op_h

            # Class element
            self.add_element({
                "_type": "UMLClass",
                "_id": cid,
                "_parent": ref(self.mid),
                "name": name,
                "visibility": "public",
                "attributes": [{"_type": "UMLAttribute", "_id": uid(), "_parent": ref(cid), "name": a, "visibility": v} for a, v in attrs],
                "operations": [{"_type": "UMLOperation", "_id": uid(), "_parent": ref(cid), "name": o, "visibility": v} for o, v in ops]
            })

            # Class view
            attr_views = []
            for i, (a, v) in enumerate(attrs):
                prefix = "-" if v == "private" else "+"
                attr_views.append({
                    "_type": "UMLAttributeView",
                    "_id": uid(),
                    "_parent": None,
                    "model": None,
                    "visible": True,
                    "enabled": True,
                    "lineColor": "#000000",
                    "fillColor": "#ffffff",
                    "fontColor": "#000000",
                    "font": "Arial;12;0",
                    "parentStyle": True,
                    "left": x + 8,
                    "top": y + 42 + i * 18,
                    "width": w - 16,
                    "height": 14,
                    "text": a,
                    "horizontalAlignment": 0,
                    "verticalAlignment": 5
                })

            op_views = []
            for i, (o, v) in enumerate(ops):
                op_views.append({
                    "_type": "UMLOperationView",
                    "_id": uid(),
                    "_parent": None,
                    "model": None,
                    "visible": True,
                    "enabled": True,
                    "lineColor": "#000000",
                    "fillColor": "#ffffff",
                    "fontColor": "#000000",
                    "font": "Arial;12;0",
                    "parentStyle": True,
                    "left": x + 8,
                    "top": y + 42 + attr_h + i * 18,
                    "width": w - 16,
                    "height": 14,
                    "text": o,
                    "horizontalAlignment": 0,
                    "verticalAlignment": 5
                })

            diagram["ownedViews"].append({
                "_type": "UMLClassView",
                "_id": uid(),
                "_parent": ref(did),
                "model": ref(cid),
                "subViews": [
                    {
                        "_type": "UMLNameCompartmentView",
                        "_id": uid(),
                        "_parent": None,
                        "model": ref(cid),
                        "subViews": [{
                            "_type": "LabelView",
                            "_id": uid(),
                            "_parent": None,
                            "visible": True,
                            "enabled": True,
                            "lineColor": "#000000",
                            "fillColor": "#ffffff",
                            "fontColor": "#000000",
                            "font": "Arial;13;1",
                            "parentStyle": True,
                            "left": x + 10,
                            "top": y + 22,
                            "width": len(name) * 9,
                            "height": 15,
                            "text": name,
                            "horizontalAlignment": 2,
                            "verticalAlignment": 5
                        }],
                        "visible": True,
                        "enabled": True,
                        "lineColor": "#000000",
                        "fillColor": "#D8E4F0",
                        "fontColor": "#000000",
                        "font": "Arial;13;0",
                        "parentStyle": True,
                        "left": x,
                        "top": y + 15,
                        "width": w,
                        "height": 25
                    },
                    {
                        "_type": "UMLAttributeCompartmentView",
                        "_id": uid(),
                        "_parent": None,
                        "model": ref(cid),
                        "subViews": attr_views,
                        "visible": True,
                        "enabled": True,
                        "lineColor": "#000000",
                        "fillColor": "#ffffff",
                        "fontColor": "#000000",
                        "font": "Arial;12;0",
                        "parentStyle": True,
                        "left": x,
                        "top": y + 40,
                        "width": w,
                        "height": attr_h
                    },
                    {
                        "_type": "UMLOperationCompartmentView",
                        "_id": uid(),
                        "_parent": None,
                        "model": ref(cid),
                        "subViews": op_views,
                        "visible": True,
                        "enabled": True,
                        "lineColor": "#000000",
                        "fillColor": "#ffffff",
                        "fontColor": "#000000",
                        "font": "Arial;12;0",
                        "parentStyle": True,
                        "left": x,
                        "top": y + 40 + attr_h,
                        "width": w,
                        "height": op_h
                    }
                ],
                "visible": True,
                "enabled": True,
                "lineColor": "#000000",
                "fillColor": "#ffffff",
                "fontColor": "#000000",
                "font": "Arial;13;0",
                "parentStyle": True,
                "showShadow": True,
                "containerChangeable": False,
                "left": x,
                "top": y,
                "width": w,
                "height": total_h
            })

        # Associations with lines
        assoc_defs = [
            (2, 0, "usa", "1", "*"),    # Chatbot -> Trámite
            (2, 1, "usa", "1", "*"),    # Chatbot -> Multa
            (3, 2, "utiliza", "1", "1"),# App Flask -> Chatbot
            (3, 4, "muestra", "1", "1") # App Flask -> Widget
        ]
        for i, j, label, m1, m2 in assoc_defs:
            rid = uid()
            self.add_element({
                "_type": "UMLAssociation",
                "_id": rid,
                "_parent": ref(self.mid),
                "name": label,
                "end1": {"_type": "UMLAssociationEnd", "_id": uid(), "_parent": ref(rid), "reference": ref(class_ids[i]), "multiplicity": m1, "visibility": "public", "navigable": True},
                "end2": {"_type": "UMLAssociationEnd", "_id": uid(), "_parent": ref(rid), "reference": ref(class_ids[j]), "multiplicity": m2, "visibility": "public", "navigable": True}
            })
            x1 = classes_data[i][1] + classes_data[i][3] // 2
            y1 = classes_data[i][2] + 50
            x2 = classes_data[j][1] + classes_data[j][3] // 2
            y2 = classes_data[j][2]
            diagram["ownedViews"].append({
                "_type": "UMLAssociationView",
                "_id": uid(),
                "_parent": ref(did),
                "model": ref(rid),
                "subViews": [{
                    "_type": "EdgeLabelView",
                    "_id": uid(),
                    "_parent": None,
                    "visible": True,
                    "enabled": True,
                    "lineColor": "#000000",
                    "fillColor": "#ffffff",
                    "fontColor": "#000000",
                    "font": "Arial;12;0",
                    "parentStyle": True,
                    "left": (x1 + x2) // 2,
                    "top": (y1 + y2) // 2 - 10,
                    "width": len(label) * 7,
                    "height": 13,
                    "text": label,
                    "alpha": 0,
                    "distance": 20,
                    "hostEdge": None,
                    "edgePosition": 1
                }],
                "visible": True,
                "enabled": True,
                "lineColor": "#000000",
                "fillColor": "#000000",
                "fontColor": "#000000",
                "font": "Arial;12;0",
                "parentStyle": True,
                "showShadow": False,
                "lineStyle": 0,
                "points": f"{x1}:{y1};{x2}:{y2}",
                "head": ref(class_ids[j]),
                "tail": ref(class_ids[i])
            })

        return did

    def sequence_diagram(self):
        did = uid()
        diagram = {
            "_type": "UMLSequenceDiagram",
            "_id": did,
            "_parent": ref(self.mid),
            "name": "Diagrama de Secuencia - Consulta Trámite",
            "visible": True,
            "defaultDiagram": False,
            "ownedViews": []
        }
        self.model["ownedElements"].append(diagram)

        # Lifelines
        lifelines = [
            (":Ciudadano", 80),
            (":Widget", 250),
            (":App Flask", 420),
            (":Chatbot", 590),
            (":KB", 760)
        ]
        ll_ids = []
        for name, x in lifelines:
            llid = uid()
            ll_ids.append(llid)
            self.add_element({
                "_type": "UMLLifeline",
                "_id": llid,
                "_parent": ref(self.mid),
                "name": name
            })
            diagram["ownedViews"].append({
                "_type": "UMLLifelineView",
                "_id": uid(),
                "_parent": ref(did),
                "model": ref(llid),
                "subViews": [{
                    "_type": "LabelView",
                    "_id": uid(),
                    "_parent": None,
                    "visible": True,
                    "enabled": True,
                    "lineColor": "#000000",
                    "fillColor": "#ffffff",
                    "fontColor": "#000000",
                    "font": "Arial;13;0",
                    "parentStyle": True,
                    "left": x + 5,
                    "top": 55,
                    "width": len(name) * 8,
                    "height": 15,
                    "text": name,
                    "horizontalAlignment": 2,
                    "verticalAlignment": 5
                }],
                "visible": True,
                "enabled": True,
                "lineColor": "#000000",
                "fillColor": "#ffffff",
                "fontColor": "#000000",
                "font": "Arial;13;0",
                "parentStyle": True,
                "showShadow": True,
                "left": x,
                "top": 40,
                "width": 60,
                "height": 35
            })

        # Messages
        messages = [
            (0, 1, "1: enviar(mensaje)", 100),
            (1, 2, "2: POST /chat", 140),
            (2, 3, "3: detect_intent(text)", 180),
            (3, 4, "4: buscar_tramite(id)", 220),
            (4, 3, "5: return tramite", 260),
            (3, 2, "6: return respuesta", 300),
            (2, 1, "7: return JSON", 340),
            (1, 0, "8: mostrar respuesta", 380)
        ]
        for from_idx, to_idx, label, y in messages:
            mid = uid()
            self.add_element({
                "_type": "UMLMessage",
                "_id": mid,
                "_parent": ref(self.mid),
                "name": label
            })
            x1 = lifelines[from_idx][1] + 30
            x2 = lifelines[to_idx][1] + 30
            diagram["ownedViews"].append({
                "_type": "UMLMessageView",
                "_id": uid(),
                "_parent": ref(did),
                "model": ref(mid),
                "subViews": [{
                    "_type": "LabelView",
                    "_id": uid(),
                    "_parent": None,
                    "visible": True,
                    "enabled": True,
                    "lineColor": "#000000",
                    "fillColor": "#ffffff",
                    "fontColor": "#000000",
                    "font": "Arial;12;0",
                    "parentStyle": True,
                    "left": min(x1, x2) + 10,
                    "top": y - 8,
                    "width": len(label) * 7,
                    "height": 13,
                    "text": label,
                    "horizontalAlignment": 2,
                    "verticalAlignment": 5
                }],
                "visible": True,
                "enabled": True,
                "lineColor": "#000000",
                "fillColor": "#000000",
                "fontColor": "#000000",
                "font": "Arial;12;0",
                "parentStyle": True,
                "showShadow": False,
                "lineStyle": 0,
                "points": f"{x1}:{y};{x2}:{y}",
                "head": ref(ll_ids[to_idx]),
                "tail": ref(ll_ids[from_idx])
            })

        return did


# ===== MAIN =====
output_dir = r"C:\Users\kanit\Desktop\chatbot-sacaba\diagramas_staruml"
os.makedirs(output_dir, exist_ok=True)

# 1. Use Case Diagram
p1 = StarUMLProject("Chatbot Municipal - Casos de Uso")
p1.use_case_diagram()
p1.save(os.path.join(output_dir, "01_casos_de_uso.mdj"))
print("01_casos_de_uso.mdj generado")

# 2. Class Diagram
p2 = StarUMLProject("Chatbot Municipal - Clases")
p2.class_diagram()
p2.save(os.path.join(output_dir, "02_diagrama_clases.mdj"))
print("02_diagrama_clases.mdj generado")

# 3. Sequence Diagram
p3 = StarUMLProject("Chatbot Municipal - Secuencia")
p3.sequence_diagram()
p3.save(os.path.join(output_dir, "03_diagrama_secuencia.mdj"))
print("03_diagrama_secuencia.mdj generado")

print("\nArchivos generados en diagramas_staruml/")
