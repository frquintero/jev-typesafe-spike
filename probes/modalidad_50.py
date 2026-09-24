"""Spike: 50 sentencias x 7 modalidades en un request (Choice x50)."""
import json
import os
import urllib.request

SENTS = [
    ("enunciativa", "La fotosíntesis ocurre en los cloroplastos de la célula vegetal."),
    ("enunciativa", "El río Magdalena desemboca en el mar Caribe."),
    ("enunciativa", "Los hongos micorrícicos conectan las raíces de los árboles."),
    ("enunciativa", "La ley 1581 de 2012 regula la protección de datos personales."),
    ("enunciativa", "El cobre conduce la electricidad mejor que el hierro."),
    ("enunciativa", "Las ballenas azules se alimentan de krill."),
    ("enunciativa", "El pH del suelo determina la absorción de nutrientes."),
    ("enunciativa", "Bogotá está a 2600 metros sobre el nivel del mar."),
    ("interrogativa", "¿Qué pigmento capta la luz durante la fotosíntesis?"),
    ("interrogativa", "¿Quién presentó la demanda de inconstitucionalidad?"),
    ("interrogativa", "¿Cuántos electrones tiene un átomo de carbono neutro?"),
    ("interrogativa", "¿Dónde desemboca el río Magdalena?"),
    ("interrogativa", "¿Por qué el cielo se ve azul al mediodía?"),
    ("interrogativa", "¿Cuál es la capital del departamento de Nariño?"),
    ("interrogativa", "¿En qué año se promulgó la Constitución vigente?"),
    ("exclamativa", "¡Qué red tan compleja forman los hongos bajo el bosque!"),
    ("exclamativa", "¡Cuánta agua desperdicia esa tubería rota!"),
    ("exclamativa", "¡Qué noche tan despejada para observar las estrellas!"),
    ("exclamativa", "¡Vaya tormenta la que cayó sobre la cordillera!"),
    ("exclamativa", "¡Cómo creció este árbol en apenas cinco años!"),
    ("exclamativa", "¡Qué sabor tan amargo deja este café mal tostado!"),
    ("exclamativa", "¡Menudo susto nos dio el temblor de anoche!"),
    ("imperativa", "Añade el reactivo gota a gota sin dejar de agitar."),
    ("imperativa", "Firma el formulario y entrégalo en la ventanilla tres."),
    ("imperativa", "Riega las plántulas cada mañana antes del mediodía."),
    ("imperativa", "Apaga el equipo antes de abrir la carcasa."),
    ("imperativa", "Lee el instructivo completo antes de usar la herramienta."),
    ("imperativa", "Guarda silencio durante la deliberación del jurado."),
    ("imperativa", "Calienta la muestra a ochenta grados por diez minutos."),
    ("desiderativa", "Ojalá la muestra no se contamine durante el traslado."),
    ("desiderativa", "Que el jurado delibere con serenidad y justicia."),
    ("desiderativa", "Ojalá llueva esta semana sobre los cultivos del valle."),
    ("desiderativa", "Que tengas un viaje seguro de regreso a casa."),
    ("desiderativa", "Ojalá el experimento confirme la hipótesis planteada."),
    ("desiderativa", "Que la cosecha alcance para todo el semestre."),
    ("desiderativa", "Ojalá me equivoque y el diagnóstico sea benigno."),
    ("dubitativa", "Quizá el resultado se deba a la acidez del suelo."),
    ("dubitativa", "Tal vez el testigo mintió durante el interrogatorio."),
    ("dubitativa", "Posiblemente la falla esté en el sensor de presión."),
    ("dubitativa", "A lo mejor el paquete llega antes del viernes."),
    ("dubitativa", "Quizás convenga repetir la medición con otro equipo."),
    ("dubitativa", "Puede que el retraso se deba al tráfico del puerto."),
    ("dubitativa", "Tal vez la respuesta esté en el archivo del juzgado."),
    ("frase_nominal", "Hechos relevantes."),
    ("frase_nominal", "Ectomicorrizas y endomicorrizas."),
    ("frase_nominal", "Problema jurídico."),
    ("frase_nominal", "Objeto del contrato."),
    ("frase_nominal", "Consideraciones de la Sala."),
    ("frase_nominal", "Disposiciones generales."),
    ("frase_nominal", "Análisis de los resultados obtenidos."),
]

CRITERIA = {
    "enunciativa": "Expresa una afirmación o negación completa, con predicado: algo que puede ser verdadero o falso",
    "interrogativa": "Formula una pregunta",
    "exclamativa": "Expresa emoción o énfasis con exclamación",
    "imperativa": "Da una orden, instrucción o ruego directo",
    "desiderativa": "Expresa un deseo",
    "dubitativa": "Expresa duda o posibilidad",
    "frase_nominal": "Solo nombra, sin afirmar nada: etiquetas, nombres propios, números o códigos aislados, cantidades con unidad, letras sueltas; sin predicado",
}

state = {f"s{i:02d}": s for i, (_, s) in enumerate(SENTS, 1)}
questions = {
    f"q{i:02d}": {
        "type": "choice",
        "instructions": f"Clasifica la oración en `s{i:02d}` según su modalidad.",
        "criteria": CRITERIA,
    }
    for i in range(1, len(SENTS) + 1)
}
body = {"model": "jev-latest", "state": state, "questions": questions}

req = urllib.request.Request(
    "https://api.typesafe.ai/v1/systemone",
    data=json.dumps(body).encode(),
    headers={
        "Content-Type": "application/json",
    },
    method="POST",
)
with urllib.request.urlopen(req, timeout=120) as r:
    resp = json.loads(r.read().decode())

os.makedirs("spike-jev/cache", exist_ok=True)
with open("spike-jev/cache/modalidad-50.json", "w") as f:
    json.dump({"request": body, "response": resp}, f, ensure_ascii=False)

ok = 0
print(f"{'id':4} {'esperado':14} {'jev':14} {'conf':6} resto-distribucion")
for i, (gold, _) in enumerate(SENTS, 1):
    a = resp["answers"][f"q{i:02d}"]
    got, conf = a["choice"], a["confidence"]
    mark = "✓" if got == gold else "✗"
    ok += got == gold
    rest = {k: v for k, v in a["probabilities"].items() if v > 0.01 and k != got}
    print(f"q{i:02d} {gold:14} {got:14} {conf:.2f} {mark} {rest}")
print(f"\nEXACTITUD: {ok}/{len(SENTS)}")
print("USAGE:", json.dumps(resp.get("usage")))
