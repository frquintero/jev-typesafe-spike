# Reporte FU1 — ficha por unidad sobre gen1, DeepSeek frente a NotebookLM (r1)

Ronda FU1 de `nblm-grafo-semantico/PLAN.md`. Sin veredicto; juzgan Frat y Cowork leyendo.

## Comandos y crudos

Desde la raíz, sin modificar nada (salidas tal como las imprimieron los scripts):

```bash
# 1. DeepSeek (con el proxy)
export HTTPS_PROXY=http://127.0.0.1:8080 SSL_CERT_FILE=$HOME/.mitmproxy/mitmproxy-ca-cert.pem
python3 nblm-grafo-semantico/ficha_unidad_deepseek.py gen1 deepseek ficha_v1 r1 \
  unidades/cache/unidades-gen1-deepseek-unidades_v5-r1.json
# {"U1": 51.4, ...} ... hecho -> .../fu-gen1-deepseek-ficha_v1-r1.json (186.1 s)

# 2. NotebookLM (sin el proxy)
env -u HTTPS_PROXY -u SSL_CERT_FILE \
  /home/fratquintero/.local/share/nblm-spike/venv-notebooklm-py/bin/python \
  nblm-grafo-semantico/ficha_unidad_nblm.py gen1 ficha_v1 r1 \
  unidades/cache/unidades-gen1-deepseek-unidades_v5-r1.json \
  --storage /home/fratquintero/.notebooklm/profiles/nblm-spike/storage_state.json \
  --sonda-unidad U2 --sonda-pregunta "¿Qué altura tiene el volcán Tumbal?"
# etapas crear..sonda ... completed True, segundos_total 461.754
```

Crudos (no se borran ni se sobrescriben):

- `nblm-grafo-semantico/cache/fu-gen1-deepseek-ficha_v1-r1.json` (15 509 882 bytes;
  incluye request/response completos por unidad).
- `nblm-grafo-semantico/cache/fu-gen1-nblm-ficha_v1-r1.json` (62 657 bytes;
  `completed: true`, sin campo `error`).

Unidades (del paso 1, `unidades/cache/unidades-gen1-deepseek-unidades_v5-r1.json`):
U1 or. 1–3, U2 or. 4, U3 or. 5+9, U4 or. 6–8, U5 or. 10. Prompt `unidades/prompts/ficha_v1.md`
en ambos. Pregunta enviada a NotebookLM por unidad (verbatim):
«Reconstruye la ficha JSON del texto de la fuente seleccionada, según tus
instrucciones. Responde solo con el JSON.»
El `custom_prompt` completo enviado a `chat.configure` (6476 caracteres) está
verbatim en el crudo NBLM (`custom_prompt_enviado`); los request de DeepSeek,
en el suyo (`request` por unidad).

## Tiempos (segundos)

DeepSeek, total 186,1:

| unidad | s |
|---|---|
| U1 | 51,4 |
| U2 | 25,1 |
| U3 | 47,6 |
| U4 | 43,4 |
| U5 | 18,5 |

NotebookLM, total 461,754 (`segundos_total`): crear 0,449; configurar 0,354;
cargar U1–U5 1,042 / 1,208 / 1,053 / 1,140 / 1,161; lista+texto por fuente
0,2–0,5; preguntar U1 75,535 / U2 61,233 / U3 82,02 / U4 137,305 / U5 34,0;
borrar_conv 0,167–0,624; sonda 59,732.

Modelo efectivo: DeepSeek `response.model = "deepseek-flash"` en las 5
unidades (coincide con el alias `deepseek` esperado). NotebookLM no expone
modelo (`"modelo": "notebooklm (Gemini Notebook, modelo no expuesto)"`,
cliente `notebooklm-py==0.8.4`).

## Por unidad: listas, mecánica, foco

Conteo en orden casos / relaciones / capas / determinaciones / acciones /
marcas / dudas. `fragmentos` y `no_literales` salen del verificador
(`verificar`); `error_parseo` y `venia_con_cerca` de `extract_json`.

DeepSeek (las 5 con `error_parseo: null`, `venia_con_cerca: false`):

| unidad | listas | fragmentos | no_literales |
|---|---|---|---|
| U1 | 5 / 3 / 0 / 5 / 0 / 3 / 0 | 20 | 0 ([]) |
| U2 | 4 / 2 / 0 / 1 / 0 / 0 / 2 | 10 | 0 ([]) |
| U3 | 4 / 3 / 0 / 4 / 0 / 4 / 1 | 20 | 0 ([]) |
| U4 | 4 / 0 / 0 / 4 / 1 / 4 / 1 | 17 | 0 ([]) |
| U5 | 1 / 0 / 0 / 1 / 0 / 2 / 0 | 5 | 0 ([]) |

NotebookLM (`fuente_igual_al_texto: true` en las 5; `citas_total: 0` y
`citas_fuera_de_la_unidad: []` en las 5; `error_parseo: null`,
`venia_con_cerca: false` en las 5):

| unidad | s | listas | fragmentos | no_literales |
|---|---|---|---|---|
| U1 | 75,535 | 4 / 2 / 0 / 6 / 0 / 4 / 0 | 22 | 0 ([]) |
| U2 | 61,233 | 2 / 0 / 0 / 1 / 0 / 1 / 0 | 5 | 0 ([]) |
| U3 | 82,02 | 4 / 3 / 0 / 4 / 0 / 3 / 0 | 18 | 0 ([]) |
| U4 | 137,305 | 5 / 3 / 0 / 4 / 1 / 7 / 0 | 24 | 0 ([]) |
| U5 | 34,0 | 1 / 0 / 0 / 1 / 0 / 2 / 0 | 5 | 0 ([]) |

Hechos mecánicos (ver anexo para el JSON completo):

- Las siete listas están presentes en las 10 fichas; `listas_faltantes: []`
  en todas.
- `chat.ask` no devolvió referencias en ninguna de las 5 preguntas ni en la
  sonda (`referencias: []`); por eso `citas_total` es 0 y no hay citas fuera
  de la unidad en ningún caso. Sin marcas `[n]` del chat en ningún valor del
  `parsed` (búsqueda de `[n]`/`[n, m]` sobre las 5 fichas: 0 hits).
- NotebookLM U2 (1/1) y U3 (4/4) traen determinaciones **sin campo `id`**,
  mientras sus `marcas` apuntan a `D1` (U2) y `D2`/`D3`/`D4` (U3). U1, U4 y
  U5 sí traen `id` (D1–D6, D1–D4, D1). DeepSeek trae `id` en todas.
- NotebookLM no registró ninguna `duda` en las 5 unidades; DeepSeek registró
  2 en U2, 1 en U3 y 1 en U4.

## Gold de gen1 (13 ítems)

`unidades/gold/gen1.json`: 6 firmes (or. 5–8), 1 borde (or. 5), 6 no_dato
(or. 1, 2, 3, 4, 9, 10). Dónde aparece cada uno:

- DeepSeek: los 6 firmes como determinaciones (altura U3-D2; fecha U4-D1;
  duración U4-D2; temperatura U4-D3; superficie U4-D4; cráter U3-D4), el
  borde como U3-D1 (tipo «volcán de escudo»), y los 6 no_dato (or. 1: U1-D1
  «suaves», U1-D4 «muy fluida»; or. 2: U1-D2, U1-D3; or. 3: U1-D5 con
  modalidad «suele»; or. 4: U2-D1 «esencial» con condición
  «para la seguridad de las islas»; or. 9: U3-D3 «majestuosas»; or. 10:
  U5-D1 con condición «En el siglo pasado» y cambio «se convirtió en»).
- NotebookLM: los 6 firmes como determinaciones (mismas posiciones: U3 y
  U4-D1–D4), el borde como U3 primera determinación (tipo «volcán de
  escudo»), y los 6 no_dato (or. 1: U1-D2, U1-D3; or. 2: U1-D4, U1-D5;
  or. 3: U1-D6 con modalidad «suele alcanzar»; or. 4: U2-D1 con condición;
  or. 9: U3 «majestuosas»; or. 10: U5-D1 con condición y cambio).

Diferencias de registro que se ven en el anexo (guía: los 11 errores de la
memoria §2.4):

- U1: NotebookLM agrega U1-D1 (caso C1, aspecto «clasificación», valor
  «volcán», respaldo «es un volcán») y normaliza el valor a dígitos en
  U1-D5 («menor de 10», respaldo literal «menor de diez grados»); DeepSeek
  registra «menor de diez» con unidad «grados». NotebookLM no separa
  «coladas» y «lava» en casos (4 casos frente a 5).
- U2: DeepSeek crea C1 «El estudio de estos volcanes» además de C2 «estos
  volcanes», unidos por R1 («estudio de»), y deja 2 dudas (a qué volcanes /
  a qué islas se refiere); NotebookLM crea 2 casos, sin relaciones ni
  dudas.
- U3: casi idénticas (mismos 4 casos; R2/R3 «parte de» con
  `inferido: true` en ambas; D4 «el más ancho» con condición «de la isla»).
  DeepSeek agrega marca «volcán de escudo» y una duda sobre el conjunto de
  comparación de «el más ancho»; NotebookLM omite ambas.
- U4 (referente perdido: «Su última erupción» con antecedente en U3):
  DeepSeek no crea caso Tumbal (C2 «lava del Tumbal» sale de la mención
  explícita de or. 7) y deja Q1: «No se especifica en el texto a qué o
  quién refiere 'Su' en 'Su última erupción'». NotebookLM crea C1 «Tumbal»
  con menciones o.6 «Su» y o.7 «Tumbal», R1 («erupción de», C2→C1) con
  `inferido: true`, marcas «Su» (remite→C1) y «esa» (remite→C2), y ninguna
  duda. Ambas marcan R-inferidas donde resuelven anáfora con `inferido`
  (U3-R2/R3 en las dos; NBLM además U4-R1/R3).
- U5: misma determinación (D1 «ciencia de campo», condición «En el siglo
  pasado», cambio «se convirtió en»); DeepSeek nombra el caso
  «vulcanología», NotebookLM «la vulcanología».

## Sonda de aislamiento (verbatim)

Desde U2 (or. 4), pregunta: «¿Qué altura tiene el volcán Tumbal?»
(`source_ids` = fuente de U2, 59,732 s). `referencias: []`,
`citas_fuera_de_la_unidad: []`. La respuesta mantuvo la forma de ficha y no
da altura ni cita otra fuente; su única duda dice (verbatim):

> Q1: «El texto no menciona la altura del volcán Tumbal ni contiene
> información sobre dicho volcán.» (respaldo o.4: «El estudio de estos
> volcanes es esencial para la seguridad de las islas.»)

Respuesta completa en el anexo S.

## Anexo P: `parsed` por unidad, tal como llegó

*(generado por código desde los crudos)*

### DeepSeek U1 (oraciones [1, 2, 3], 51.4 s)

```json
{
 "casos": [
  {
   "id": "C1",
   "nombre": "volcán de escudo",
   "menciones": [
    {
     "o": 1,
     "f": "Un volcán de escudo"
    },
    {
     "o": 2,
     "f": "Se llama de escudo"
    },
    {
     "o": 2,
     "f": "al volcán cuyas laderas"
    }
   ]
  },
  {
   "id": "C2",
   "nombre": "laderas del volcán de escudo",
   "menciones": [
    {
     "o": 1,
     "f": "laderas suaves"
    },
    {
     "o": 2,
     "f": "cuyas laderas"
    }
   ]
  },
  {
   "id": "C3",
   "nombre": "coladas",
   "menciones": [
    {
     "o": 1,
     "f": "coladas de lava muy fluida"
    }
   ]
  },
  {
   "id": "C4",
   "nombre": "lava",
   "menciones": [
    {
     "o": 1,
     "f": "lava muy fluida"
    }
   ]
  },
  {
   "id": "C5",
   "nombre": "lava basáltica",
   "menciones": [
    {
     "o": 3,
     "f": "La lava basáltica"
    }
   ]
  }
 ],
 "relaciones": [
  {
   "id": "R1",
   "tipo": "parte de",
   "de": "C2",
   "a": "C1",
   "dentro_de": null,
   "condiciones": [],
   "inferido": false,
   "respaldo": [
    {
     "o": 2,
     "f": "cuyas laderas"
    }
   ]
  },
  {
   "id": "R2",
   "tipo": "formado por",
   "de": "C1",
   "a": "C3",
   "dentro_de": null,
   "condiciones": [],
   "inferido": false,
   "respaldo": [
    {
     "o": 1,
     "f": "formado por coladas de lava muy fluida"
    }
   ]
  },
  {
   "id": "R3",
   "tipo": "de",
   "de": "C3",
   "a": "C4",
   "dentro_de": null,
   "condiciones": [],
   "inferido": false,
   "respaldo": [
    {
     "o": 1,
     "f": "coladas de lava"
    }
   ]
  }
 ],
 "capas": [],
 "determinaciones": [
  {
   "id": "D1",
   "dentro_de": null,
   "caso": "C2",
   "aspecto": "característica",
   "valor": "suaves",
   "unidad": null,
   "cambio": null,
   "condiciones": [],
   "modalidad": null,
   "inferido": false,
   "respaldo": [
    {
     "o": 1,
     "f": "laderas suaves"
    }
   ]
  },
  {
   "id": "D2",
   "dentro_de": null,
   "caso": "C2",
   "aspecto": "pendiente",
   "valor": "menor de diez",
   "unidad": "grados",
   "cambio": null,
   "condiciones": [],
   "modalidad": null,
   "inferido": false,
   "respaldo": [
    {
     "o": 2,
     "f": "tienen una pendiente menor de diez grados"
    }
   ]
  },
  {
   "id": "D3",
   "dentro_de": null,
   "caso": "C1",
   "aspecto": "denominación",
   "valor": "de escudo",
   "unidad": null,
   "cambio": null,
   "condiciones": [
    {
     "texto": "cuyas laderas tienen una pendiente menor de diez grados",
     "ref": "D2",
     "respaldo": [
      {
       "o": 2,
       "f": "cuyas laderas tienen una pendiente menor de diez grados"
      }
     ]
    }
   ],
   "modalidad": null,
   "inferido": false,
   "respaldo": [
    {
     "o": 2,
     "f": "Se llama de escudo"
    }
   ]
  },
  {
   "id": "D4",
   "dentro_de": null,
   "caso": "C4",
   "aspecto": "fluidez",
   "valor": "muy fluida",
   "unidad": null,
   "cambio": null,
   "condiciones": [],
   "modalidad": null,
   "inferido": false,
   "respaldo": [
    {
     "o": 1,
     "f": "lava muy fluida"
    }
   ]
  },
  {
   "id": "D5",
   "dentro_de": null,
   "caso": "C5",
   "aspecto": "temperatura",
   "valor": "entre 1100 y 1200",
   "unidad": "grados Celsius",
   "cambio": null,
   "condiciones": [],
   "modalidad": "suele",
   "inferido": false,
   "respaldo": [
    {
     "o": 3,
     "f": "suele alcanzar temperaturas de entre 1100 y 1200 grados Celsius"
    }
   ]
  }
 ],
 "acciones": [],
 "marcas": [
  {
   "marca": "diez grados",
   "o": 2,
   "funciones": [
    {
     "funcion": "posición",
     "refs": [
      "D2"
     ]
    }
   ]
  },
  {
   "marca": "1100",
   "o": 3,
   "funciones": [
    {
     "funcion": "posición",
     "refs": [
      "D5"
     ]
    }
   ]
  },
  {
   "marca": "1200",
   "o": 3,
   "funciones": [
    {
     "funcion": "posición",
     "refs": [
      "D5"
     ]
    }
   ]
  }
 ],
 "dudas": []
}
```

### DeepSeek U2 (oraciones [4], 25.1 s)

```json
{
 "casos": [
  {
   "id": "C1",
   "nombre": "El estudio de estos volcanes",
   "menciones": [
    {
     "o": 4,
     "f": "El estudio de estos volcanes"
    }
   ]
  },
  {
   "id": "C2",
   "nombre": "estos volcanes",
   "menciones": [
    {
     "o": 4,
     "f": "estos volcanes"
    }
   ]
  },
  {
   "id": "C3",
   "nombre": "la seguridad de las islas",
   "menciones": [
    {
     "o": 4,
     "f": "la seguridad de las islas"
    }
   ]
  },
  {
   "id": "C4",
   "nombre": "las islas",
   "menciones": [
    {
     "o": 4,
     "f": "las islas"
    }
   ]
  }
 ],
 "relaciones": [
  {
   "id": "R1",
   "tipo": "estudio de",
   "de": "C1",
   "a": "C2",
   "dentro_de": null,
   "condiciones": [],
   "inferido": false,
   "respaldo": [
    {
     "o": 4,
     "f": "El estudio de estos volcanes"
    }
   ]
  },
  {
   "id": "R2",
   "tipo": "seguridad de",
   "de": "C3",
   "a": "C4",
   "dentro_de": null,
   "condiciones": [],
   "inferido": false,
   "respaldo": [
    {
     "o": 4,
     "f": "la seguridad de las islas"
    }
   ]
  }
 ],
 "capas": [],
 "determinaciones": [
  {
   "id": "D1",
   "dentro_de": null,
   "caso": "C1",
   "aspecto": "carácter",
   "valor": "esencial",
   "unidad": null,
   "cambio": null,
   "condiciones": [
    {
     "texto": "para la seguridad de las islas",
     "ref": "C3",
     "respaldo": [
      {
       "o": 4,
       "f": "para la seguridad de las islas"
      }
     ]
    }
   ],
   "modalidad": null,
   "inferido": false,
   "respaldo": [
    {
     "o": 4,
     "f": "es esencial"
    }
   ]
  }
 ],
 "acciones": [],
 "marcas": [],
 "dudas": [
  {
   "id": "Q1",
   "texto": "A qué volcanes se refiere «estos volcanes».",
   "respaldo": [
    {
     "o": 4,
     "f": "estos volcanes"
    }
   ]
  },
  {
   "id": "Q2",
   "texto": "A qué islas se refiere «las islas».",
   "respaldo": [
    {
     "o": 4,
     "f": "las islas"
    }
   ]
  }
 ]
}
```

### DeepSeek U3 (oraciones [5, 9], 47.6 s)

```json
{
 "casos": [
  {
   "id": "C1",
   "nombre": "volcán Tumbal",
   "menciones": [
    {
     "o": 5,
     "f": "El volcán Tumbal"
    },
    {
     "o": 9,
     "f": "Sus"
    },
    {
     "o": 9,
     "f": "su"
    }
   ]
  },
  {
   "id": "C2",
   "nombre": "isla de Arén",
   "menciones": [
    {
     "o": 5,
     "f": "la isla de Arén"
    },
    {
     "o": 9,
     "f": "la isla"
    }
   ]
  },
  {
   "id": "C3",
   "nombre": "laderas del volcán Tumbal",
   "menciones": [
    {
     "o": 9,
     "f": "Sus laderas"
    }
   ]
  },
  {
   "id": "C4",
   "nombre": "cráter del volcán Tumbal",
   "menciones": [
    {
     "o": 9,
     "f": "su cráter"
    }
   ]
  }
 ],
 "relaciones": [
  {
   "id": "R1",
   "tipo": "ubicado en",
   "de": "C1",
   "a": "C2",
   "dentro_de": null,
   "condiciones": [],
   "inferido": false,
   "respaldo": [
    {
     "o": 5,
     "f": "en la isla de Arén"
    }
   ]
  },
  {
   "id": "R2",
   "tipo": "parte de",
   "de": "C3",
   "a": "C1",
   "dentro_de": null,
   "condiciones": [],
   "inferido": true,
   "respaldo": [
    {
     "o": 9,
     "f": "Sus laderas"
    }
   ]
  },
  {
   "id": "R3",
   "tipo": "parte de",
   "de": "C4",
   "a": "C1",
   "dentro_de": null,
   "condiciones": [],
   "inferido": true,
   "respaldo": [
    {
     "o": 9,
     "f": "su cráter"
    }
   ]
  }
 ],
 "capas": [],
 "determinaciones": [
  {
   "id": "D1",
   "dentro_de": null,
   "caso": "C1",
   "aspecto": "tipo",
   "valor": "volcán de escudo",
   "unidad": null,
   "cambio": null,
   "condiciones": [],
   "modalidad": null,
   "inferido": false,
   "respaldo": [
    {
     "o": 5,
     "f": "es un volcán de escudo"
    }
   ]
  },
  {
   "id": "D2",
   "dentro_de": null,
   "caso": "C1",
   "aspecto": "altura",
   "valor": "2300",
   "unidad": "metros",
   "cambio": null,
   "condiciones": [],
   "modalidad": null,
   "inferido": false,
   "respaldo": [
    {
     "o": 5,
     "f": "de 2300 metros de altura"
    }
   ]
  },
  {
   "id": "D3",
   "dentro_de": null,
   "caso": "C3",
   "aspecto": "carácter",
   "valor": "majestuosas",
   "unidad": null,
   "cambio": null,
   "condiciones": [],
   "modalidad": null,
   "inferido": false,
   "respaldo": [
    {
     "o": 9,
     "f": "Sus laderas son majestuosas"
    }
   ]
  },
  {
   "id": "D4",
   "dentro_de": null,
   "caso": "C4",
   "aspecto": "ancho",
   "valor": "el más ancho",
   "unidad": null,
   "cambio": null,
   "condiciones": [
    {
     "texto": "de la isla",
     "ref": "C2",
     "respaldo": [
      {
       "o": 9,
       "f": "de la isla"
      }
     ]
    }
   ],
   "modalidad": null,
   "inferido": false,
   "respaldo": [
    {
     "o": 9,
     "f": "su cráter es el más ancho de la isla"
    }
   ]
  }
 ],
 "acciones": [],
 "marcas": [
  {
   "marca": "volcán de escudo",
   "o": 5,
   "funciones": [
    {
     "funcion": "posición",
     "refs": [
      "D1"
     ]
    }
   ]
  },
  {
   "marca": "2300 metros",
   "o": 5,
   "funciones": [
    {
     "funcion": "posición",
     "refs": [
      "D2"
     ]
    }
   ]
  },
  {
   "marca": "majestuosas",
   "o": 9,
   "funciones": [
    {
     "funcion": "posición",
     "refs": [
      "D3"
     ]
    }
   ]
  },
  {
   "marca": "el más ancho",
   "o": 9,
   "funciones": [
    {
     "funcion": "posición",
     "refs": [
      "D4"
     ]
    }
   ]
  }
 ],
 "dudas": [
  {
   "id": "Q1",
   "texto": "«el más ancho de la isla»: no se explicita si el conjunto de comparación son los cráteres de la isla o todos los elementos de la isla.",
   "respaldo": [
    {
     "o": 9,
     "f": "su cráter es el más ancho de la isla"
    }
   ]
  }
 ]
}
```

### DeepSeek U4 (oraciones [6, 7, 8], 43.4 s)

```json
{
 "casos": [
  {
   "id": "C1",
   "nombre": "última erupción",
   "menciones": [
    {
     "o": 6,
     "f": "Su última erupción"
    },
    {
     "o": 7,
     "f": "esa erupción"
    }
   ]
  },
  {
   "id": "C2",
   "nombre": "lava del Tumbal",
   "menciones": [
    {
     "o": 7,
     "f": "la lava del Tumbal"
    }
   ]
  },
  {
   "id": "C3",
   "nombre": "colada principal",
   "menciones": [
    {
     "o": 8,
     "f": "La colada principal"
    }
   ]
  },
  {
   "id": "C4",
   "nombre": "cultivos",
   "menciones": [
    {
     "o": 8,
     "f": "cultivos"
    }
   ]
  }
 ],
 "relaciones": [],
 "capas": [],
 "determinaciones": [
  {
   "id": "D1",
   "dentro_de": null,
   "caso": "C1",
   "aspecto": "fecha de inicio",
   "valor": "4 de marzo de 2019",
   "unidad": null,
   "cambio": null,
   "condiciones": [],
   "modalidad": null,
   "inferido": false,
   "respaldo": [
    {
     "o": 6,
     "f": "comenzó el 4 de marzo de 2019"
    }
   ]
  },
  {
   "id": "D2",
   "dentro_de": null,
   "caso": "C1",
   "aspecto": "duración",
   "valor": "41",
   "unidad": "días",
   "cambio": null,
   "condiciones": [],
   "modalidad": null,
   "inferido": false,
   "respaldo": [
    {
     "o": 6,
     "f": "duró 41 días"
    }
   ]
  },
  {
   "id": "D3",
   "dentro_de": null,
   "caso": "C2",
   "aspecto": "temperatura",
   "valor": "1150",
   "unidad": "grados Celsius",
   "cambio": null,
   "condiciones": [
    {
     "texto": "Durante esa erupción",
     "ref": "C1",
     "respaldo": [
      {
       "o": 7,
       "f": "Durante esa erupción"
      }
     ]
    }
   ],
   "modalidad": null,
   "inferido": false,
   "respaldo": [
    {
     "o": 7,
     "f": "la lava del Tumbal alcanzó 1150 grados Celsius"
    }
   ]
  },
  {
   "id": "D4",
   "dentro_de": null,
   "caso": "C3",
   "aspecto": "superficie cubierta",
   "valor": "12",
   "unidad": "kilómetros cuadrados",
   "cambio": null,
   "condiciones": [
    {
     "texto": "de cultivos",
     "ref": "C4",
     "respaldo": [
      {
       "o": 8,
       "f": "de cultivos"
      }
     ]
    }
   ],
   "modalidad": null,
   "inferido": false,
   "respaldo": [
    {
     "o": 8,
     "f": "cubrió 12 kilómetros cuadrados de cultivos"
    }
   ]
  }
 ],
 "acciones": [
  {
   "id": "A1",
   "agente": "C3",
   "accion": "cubrió",
   "objeto": "C4",
   "negada": false,
   "dentro_de": null,
   "condiciones": [],
   "respaldo": [
    {
     "o": 8,
     "f": "cubrió 12 kilómetros cuadrados de cultivos"
    }
   ]
  }
 ],
 "marcas": [
  {
   "marca": "4 de marzo de 2019",
   "o": 6,
   "funciones": [
    {
     "funcion": "posición",
     "refs": [
      "D1"
     ]
    }
   ]
  },
  {
   "marca": "41 días",
   "o": 6,
   "funciones": [
    {
     "funcion": "posición",
     "refs": [
      "D2"
     ]
    }
   ]
  },
  {
   "marca": "1150 grados Celsius",
   "o": 7,
   "funciones": [
    {
     "funcion": "posición",
     "refs": [
      "D3"
     ]
    }
   ]
  },
  {
   "marca": "12 kilómetros cuadrados",
   "o": 8,
   "funciones": [
    {
     "funcion": "posición",
     "refs": [
      "D4"
     ]
    }
   ]
  }
 ],
 "dudas": [
  {
   "id": "Q1",
   "texto": "No se especifica en el texto a qué o quién refiere 'Su' en 'Su última erupción'.",
   "respaldo": [
    {
     "o": 6,
     "f": "Su última erupción"
    }
   ]
  }
 ]
}
```

### DeepSeek U5 (oraciones [10], 18.5 s)

```json
{
 "casos": [
  {
   "id": "C1",
   "nombre": "vulcanología",
   "menciones": [
    {
     "o": 10,
     "f": "la vulcanología"
    }
   ]
  }
 ],
 "relaciones": [],
 "capas": [],
 "determinaciones": [
  {
   "id": "D1",
   "dentro_de": null,
   "caso": "C1",
   "aspecto": "carácter",
   "valor": "ciencia de campo",
   "unidad": null,
   "cambio": "se convirtió en",
   "condiciones": [
    {
     "texto": "En el siglo pasado",
     "ref": null,
     "respaldo": [
      {
       "o": 10,
       "f": "En el siglo pasado"
      }
     ]
    }
   ],
   "modalidad": null,
   "inferido": false,
   "respaldo": [
    {
     "o": 10,
     "f": "la vulcanología se convirtió en una ciencia de campo"
    }
   ]
  }
 ],
 "acciones": [],
 "marcas": [
  {
   "marca": "siglo pasado",
   "o": 10,
   "funciones": [
    {
     "funcion": "posición",
     "refs": [
      "D1"
     ]
    }
   ]
  },
  {
   "marca": "ciencia de campo",
   "o": 10,
   "funciones": [
    {
     "funcion": "posición",
     "refs": [
      "D1"
     ]
    }
   ]
  }
 ],
 "dudas": []
}
```

### NotebookLM U1 (oraciones [1, 2, 3], 75.535 s)

```json
{
 "casos": [
  {
   "id": "C1",
   "nombre": "volcán de escudo",
   "menciones": [
    {
     "o": 1,
     "f": "Un volcán de escudo"
    },
    {
     "o": 1,
     "f": "un volcán"
    },
    {
     "o": 2,
     "f": "de escudo"
    },
    {
     "o": 2,
     "f": "al volcán"
    }
   ]
  },
  {
   "id": "C2",
   "nombre": "laderas del volcán de escudo",
   "menciones": [
    {
     "o": 1,
     "f": "laderas"
    },
    {
     "o": 2,
     "f": "cuyas laderas"
    }
   ]
  },
  {
   "id": "C3",
   "nombre": "coladas de lava",
   "menciones": [
    {
     "o": 1,
     "f": "coladas de lava"
    }
   ]
  },
  {
   "id": "C4",
   "nombre": "lava basáltica",
   "menciones": [
    {
     "o": 3,
     "f": "La lava basáltica"
    }
   ]
  }
 ],
 "relaciones": [
  {
   "id": "R1",
   "tipo": "parte de",
   "de": "C2",
   "a": "C1",
   "dentro_de": null,
   "condiciones": [],
   "inferido": false,
   "respaldo": [
    {
     "o": 1,
     "f": "un volcán de laderas suaves"
    },
    {
     "o": 2,
     "f": "al volcán cuyas laderas"
    }
   ]
  },
  {
   "id": "R2",
   "tipo": "formado por",
   "de": "C1",
   "a": "C3",
   "dentro_de": null,
   "condiciones": [],
   "inferido": false,
   "respaldo": [
    {
     "o": 1,
     "f": "formado por coladas de lava"
    }
   ]
  }
 ],
 "capas": [],
 "determinaciones": [
  {
   "id": "D1",
   "dentro_de": null,
   "caso": "C1",
   "aspecto": "clasificación",
   "valor": "volcán",
   "unidad": null,
   "cambio": null,
   "condiciones": [],
   "modalidad": null,
   "inferido": false,
   "respaldo": [
    {
     "o": 1,
     "f": "es un volcán"
    }
   ]
  },
  {
   "id": "D2",
   "dentro_de": null,
   "caso": "C2",
   "aspecto": "forma",
   "valor": "suaves",
   "unidad": null,
   "cambio": null,
   "condiciones": [],
   "modalidad": null,
   "inferido": false,
   "respaldo": [
    {
     "o": 1,
     "f": "laderas suaves"
    }
   ]
  },
  {
   "id": "D3",
   "dentro_de": null,
   "caso": "C3",
   "aspecto": "fluidez",
   "valor": "muy fluida",
   "unidad": null,
   "cambio": null,
   "condiciones": [],
   "modalidad": null,
   "inferido": false,
   "respaldo": [
    {
     "o": 1,
     "f": "muy fluida"
    }
   ]
  },
  {
   "id": "D4",
   "dentro_de": null,
   "caso": "C1",
   "aspecto": "denominación",
   "valor": "de escudo",
   "unidad": null,
   "cambio": null,
   "condiciones": [
    {
     "texto": "cuyas laderas tienen una pendiente menor de diez grados",
     "ref": "D5",
     "respaldo": [
      {
       "o": 2,
       "f": "cuyas laderas tienen una pendiente menor de diez grados"
      }
     ]
    }
   ],
   "modalidad": null,
   "inferido": false,
   "respaldo": [
    {
     "o": 2,
     "f": "Se llama de escudo"
    }
   ]
  },
  {
   "id": "D5",
   "dentro_de": null,
   "caso": "C2",
   "aspecto": "pendiente",
   "valor": "menor de 10",
   "unidad": "grados",
   "cambio": null,
   "condiciones": [],
   "modalidad": null,
   "inferido": false,
   "respaldo": [
    {
     "o": 2,
     "f": "tienen una pendiente menor de diez grados"
    }
   ]
  },
  {
   "id": "D6",
   "dentro_de": null,
   "caso": "C4",
   "aspecto": "temperatura",
   "valor": "1100 y 1200",
   "unidad": "grados Celsius",
   "cambio": null,
   "condiciones": [],
   "modalidad": "suele alcanzar",
   "inferido": false,
   "respaldo": [
    {
     "o": 3,
     "f": "suele alcanzar temperaturas de entre 1100 y 1200 grados Celsius"
    }
   ]
  }
 ],
 "acciones": [],
 "marcas": [
  {
   "marca": "suaves",
   "o": 1,
   "funciones": [
    {
     "funcion": "posición",
     "refs": [
      "D2"
     ]
    }
   ]
  },
  {
   "marca": "muy fluida",
   "o": 1,
   "funciones": [
    {
     "funcion": "posición",
     "refs": [
      "D3"
     ]
    }
   ]
  },
  {
   "marca": "diez grados",
   "o": 2,
   "funciones": [
    {
     "funcion": "posición",
     "refs": [
      "D5"
     ]
    }
   ]
  },
  {
   "marca": "1100 y 1200 grados Celsius",
   "o": 3,
   "funciones": [
    {
     "funcion": "posición",
     "refs": [
      "D6"
     ]
    }
   ]
  }
 ],
 "dudas": []
}
```

### NotebookLM U2 (oraciones [4], 61.233 s)

```json
{
 "casos": [
  {
   "id": "C1",
   "nombre": "estudio de estos volcanes",
   "menciones": [
    {
     "o": 4,
     "f": "El estudio de estos volcanes"
    }
   ]
  },
  {
   "id": "C2",
   "nombre": "seguridad de las islas",
   "menciones": [
    {
     "o": 4,
     "f": "la seguridad de las islas"
    }
   ]
  }
 ],
 "relaciones": [],
 "capas": [],
 "determinaciones": [
  {
   "dentro_de": null,
   "caso": "C1",
   "aspecto": "carácter",
   "valor": "esencial",
   "unidad": null,
   "cambio": null,
   "condiciones": [
    {
     "texto": "para la seguridad de las islas",
     "ref": "C2",
     "respaldo": [
      {
       "o": 4,
       "f": "para la seguridad de las islas"
      }
     ]
    }
   ],
   "modalidad": null,
   "inferido": false,
   "respaldo": [
    {
     "o": 4,
     "f": "es esencial"
    }
   ]
  }
 ],
 "acciones": [],
 "marcas": [
  {
   "marca": "esencial",
   "o": 4,
   "funciones": [
    {
     "funcion": "posición",
     "refs": [
      "D1"
     ]
    }
   ]
  }
 ],
 "dudas": []
}
```

### NotebookLM U3 (oraciones [5, 9], 82.02 s)

```json
{
 "casos": [
  {
   "id": "C1",
   "nombre": "volcán Tumbal",
   "menciones": [
    {
     "o": 5,
     "f": "El volcán Tumbal"
    },
    {
     "o": 9,
     "f": "Sus"
    },
    {
     "o": 9,
     "f": "su"
    }
   ]
  },
  {
   "id": "C2",
   "nombre": "isla de Arén",
   "menciones": [
    {
     "o": 5,
     "f": "la isla de Arén"
    },
    {
     "o": 9,
     "f": "la isla"
    }
   ]
  },
  {
   "id": "C3",
   "nombre": "laderas del volcán Tumbal",
   "menciones": [
    {
     "o": 9,
     "f": "Sus laderas"
    }
   ]
  },
  {
   "id": "C4",
   "nombre": "cráter del volcán Tumbal",
   "menciones": [
    {
     "o": 9,
     "f": "su cráter"
    }
   ]
  }
 ],
 "relaciones": [
  {
   "id": "R1",
   "tipo": "ubicado en",
   "de": "C1",
   "a": "C2",
   "dentro_de": null,
   "condiciones": [],
   "inferido": false,
   "respaldo": [
    {
     "o": 5,
     "f": "en la isla de Arén"
    }
   ]
  },
  {
   "id": "R2",
   "tipo": "parte de",
   "de": "C3",
   "a": "C1",
   "dentro_de": null,
   "condiciones": [],
   "inferido": true,
   "respaldo": [
    {
     "o": 9,
     "f": "Sus laderas"
    }
   ]
  },
  {
   "id": "R3",
   "tipo": "parte de",
   "de": "C4",
   "a": "C1",
   "dentro_de": null,
   "condiciones": [],
   "inferido": true,
   "respaldo": [
    {
     "o": 9,
     "f": "su cráter"
    }
   ]
  }
 ],
 "capas": [],
 "determinaciones": [
  {
   "dentro_de": null,
   "caso": "C1",
   "aspecto": "tipo",
   "valor": "volcán de escudo",
   "unidad": null,
   "cambio": null,
   "condiciones": [],
   "modalidad": null,
   "inferido": false,
   "respaldo": [
    {
     "o": 5,
     "f": "es un volcán de escudo"
    }
   ]
  },
  {
   "dentro_de": null,
   "caso": "C1",
   "aspecto": "altura",
   "valor": "2300",
   "unidad": "metros",
   "cambio": null,
   "condiciones": [],
   "modalidad": null,
   "inferido": false,
   "respaldo": [
    {
     "o": 5,
     "f": "de 2300 metros de altura"
    }
   ]
  },
  {
   "dentro_de": null,
   "caso": "C3",
   "aspecto": "aspecto",
   "valor": "majestuosas",
   "unidad": null,
   "cambio": null,
   "condiciones": [],
   "modalidad": null,
   "inferido": false,
   "respaldo": [
    {
     "o": 9,
     "f": "son majestuosas"
    }
   ]
  },
  {
   "dentro_de": null,
   "caso": "C4",
   "aspecto": "ancho",
   "valor": "el más ancho",
   "unidad": null,
   "cambio": null,
   "condiciones": [
    {
     "texto": "de la isla",
     "ref": "C2",
     "respaldo": [
      {
       "o": 9,
       "f": "de la isla"
      }
     ]
    }
   ],
   "modalidad": null,
   "inferido": false,
   "respaldo": [
    {
     "o": 9,
     "f": "es el más ancho de la isla"
    }
   ]
  }
 ],
 "acciones": [],
 "marcas": [
  {
   "marca": "2300",
   "o": 5,
   "funciones": [
    {
     "funcion": "posición",
     "refs": [
      "D2"
     ]
    }
   ]
  },
  {
   "marca": "majestuosas",
   "o": 9,
   "funciones": [
    {
     "funcion": "posición",
     "refs": [
      "D3"
     ]
    }
   ]
  },
  {
   "marca": "el más ancho",
   "o": 9,
   "funciones": [
    {
     "funcion": "posición",
     "refs": [
      "D4"
     ]
    }
   ]
  }
 ],
 "dudas": []
}
```

### NotebookLM U4 (oraciones [6, 7, 8], 137.305 s)

```json
{
 "casos": [
  {
   "id": "C1",
   "nombre": "Tumbal",
   "menciones": [
    {
     "o": 6,
     "f": "Su"
    },
    {
     "o": 7,
     "f": "Tumbal"
    }
   ]
  },
  {
   "id": "C2",
   "nombre": "última erupción del Tumbal",
   "menciones": [
    {
     "o": 6,
     "f": "Su última erupción"
    },
    {
     "o": 7,
     "f": "esa erupción"
    }
   ]
  },
  {
   "id": "C3",
   "nombre": "lava del Tumbal",
   "menciones": [
    {
     "o": 7,
     "f": "la lava del Tumbal"
    }
   ]
  },
  {
   "id": "C4",
   "nombre": "colada principal",
   "menciones": [
    {
     "o": 8,
     "f": "La colada principal"
    }
   ]
  },
  {
   "id": "C5",
   "nombre": "cultivos",
   "menciones": [
    {
     "o": 8,
     "f": "cultivos"
    }
   ]
  }
 ],
 "relaciones": [
  {
   "id": "R1",
   "tipo": "erupción de",
   "de": "C2",
   "a": "C1",
   "dentro_de": null,
   "condiciones": [],
   "inferido": true,
   "respaldo": [
    {
     "o": 6,
     "f": "Su última erupción"
    }
   ]
  },
  {
   "id": "R2",
   "tipo": "procede de",
   "de": "C3",
   "a": "C1",
   "dentro_de": null,
   "condiciones": [],
   "inferido": false,
   "respaldo": [
    {
     "o": 7,
     "f": "la lava del Tumbal"
    }
   ]
  },
  {
   "id": "R3",
   "tipo": "procede de",
   "de": "C4",
   "a": "C3",
   "dentro_de": null,
   "condiciones": [],
   "inferido": true,
   "respaldo": [
    {
     "o": 8,
     "f": "La colada principal"
    }
   ]
  }
 ],
 "capas": [],
 "determinaciones": [
  {
   "id": "D1",
   "dentro_de": null,
   "caso": "C2",
   "aspecto": "comienzo",
   "valor": "4 de marzo de 2019",
   "unidad": null,
   "cambio": null,
   "condiciones": [],
   "modalidad": null,
   "inferido": false,
   "respaldo": [
    {
     "o": 6,
     "f": "comenzó el 4 de marzo de 2019"
    }
   ]
  },
  {
   "id": "D2",
   "dentro_de": null,
   "caso": "C2",
   "aspecto": "duración",
   "valor": "41",
   "unidad": "días",
   "cambio": null,
   "condiciones": [],
   "modalidad": null,
   "inferido": false,
   "respaldo": [
    {
     "o": 6,
     "f": "duró 41 días"
    }
   ]
  },
  {
   "id": "D3",
   "dentro_de": null,
   "caso": "C3",
   "aspecto": "temperatura",
   "valor": "1150",
   "unidad": "grados Celsius",
   "cambio": null,
   "condiciones": [
    {
     "texto": "durante esa erupción",
     "ref": "C2",
     "respaldo": [
      {
       "o": 7,
       "f": "Durante esa erupción"
      }
     ]
    }
   ],
   "modalidad": null,
   "inferido": false,
   "respaldo": [
    {
     "o": 7,
     "f": "la lava del Tumbal alcanzó 1150 grados Celsius"
    }
   ]
  },
  {
   "id": "D4",
   "dentro_de": null,
   "caso": "C4",
   "aspecto": "superficie cubierta",
   "valor": "12",
   "unidad": "kilómetros cuadrados",
   "cambio": null,
   "condiciones": [
    {
     "texto": "de cultivos",
     "ref": "C5",
     "respaldo": [
      {
       "o": 8,
       "f": "de cultivos"
      }
     ]
    }
   ],
   "modalidad": null,
   "inferido": false,
   "respaldo": [
    {
     "o": 8,
     "f": "cubrió 12 kilómetros cuadrados de cultivos"
    }
   ]
  }
 ],
 "acciones": [
  {
   "id": "A1",
   "agente": "C4",
   "accion": "cubrió",
   "objeto": "C5",
   "negada": false,
   "dentro_de": null,
   "condiciones": [],
   "respaldo": [
    {
     "o": 8,
     "f": "La colada principal cubrió 12 kilómetros cuadrados de cultivos"
    }
   ]
  }
 ],
 "marcas": [
  {
   "marca": "Su",
   "o": 6,
   "funciones": [
    {
     "funcion": "remite",
     "refs": [
      "C1"
     ]
    }
   ]
  },
  {
   "marca": "última",
   "o": 6,
   "funciones": [
    {
     "funcion": "posición",
     "refs": [
      "C2"
     ]
    }
   ]
  },
  {
   "marca": "4 de marzo de 2019",
   "o": 6,
   "funciones": [
    {
     "funcion": "posición",
     "refs": [
      "D1"
     ]
    }
   ]
  },
  {
   "marca": "41 días",
   "o": 6,
   "funciones": [
    {
     "funcion": "posición",
     "refs": [
      "D2"
     ]
    }
   ]
  },
  {
   "marca": "esa",
   "o": 7,
   "funciones": [
    {
     "funcion": "remite",
     "refs": [
      "C2"
     ]
    }
   ]
  },
  {
   "marca": "1150 grados Celsius",
   "o": 7,
   "funciones": [
    {
     "funcion": "posición",
     "refs": [
      "D3"
     ]
    }
   ]
  },
  {
   "marca": "12 kilómetros cuadrados",
   "o": 8,
   "funciones": [
    {
     "funcion": "posición",
     "refs": [
      "D4"
     ]
    }
   ]
  }
 ],
 "dudas": []
}
```

### NotebookLM U5 (oraciones [10], 34.0 s)

```json
{
 "casos": [
  {
   "id": "C1",
   "nombre": "la vulcanología",
   "menciones": [
    {
     "o": 10,
     "f": "la vulcanología"
    }
   ]
  }
 ],
 "relaciones": [],
 "capas": [],
 "determinaciones": [
  {
   "id": "D1",
   "dentro_de": null,
   "caso": "C1",
   "aspecto": "tipo de ciencia",
   "valor": "ciencia de campo",
   "unidad": null,
   "cambio": "se convirtió en",
   "condiciones": [
    {
     "texto": "En el siglo pasado",
     "ref": null,
     "respaldo": [
      {
       "o": 10,
       "f": "En el siglo pasado"
      }
     ]
    }
   ],
   "modalidad": null,
   "inferido": false,
   "respaldo": [
    {
     "o": 10,
     "f": "En el siglo pasado, la vulcanología se convirtió en una ciencia de campo."
    }
   ]
  }
 ],
 "acciones": [],
 "marcas": [
  {
   "marca": "el siglo pasado",
   "o": 10,
   "funciones": [
    {
     "funcion": "posición",
     "refs": [
      "D1"
     ]
    }
   ]
  },
  {
   "marca": "ciencia de campo",
   "o": 10,
   "funciones": [
    {
     "funcion": "posición",
     "refs": [
      "D1"
     ]
    }
   ]
  }
 ],
 "dudas": []
}
```

## Anexo S: sonda verbatim

Pregunta: ¿Qué altura tiene el volcán Tumbal? (fuente: U2). Referencias: []. Citas fuera: [].

```json
{
 "casos": [
  {
   "id": "C1",
   "nombre": "estudio de estos volcanes",
   "menciones": [
    {
     "o": 4,
     "f": "El estudio de estos volcanes"
    }
   ]
  },
  {
   "id": "C2",
   "nombre": "estos volcanes",
   "menciones": [
    {
     "o": 4,
     "f": "estos volcanes"
    }
   ]
  },
  {
   "id": "C3",
   "nombre": "las islas",
   "menciones": [
    {
     "o": 4,
     "f": "las islas"
    }
   ]
  },
  {
   "id": "C4",
   "nombre": "seguridad de las islas",
   "menciones": [
    {
     "o": 4,
     "f": "la seguridad de las islas"
    }
   ]
  }
 ],
 "relaciones": [],
 "capas": [],
 "determinaciones": [
  {
   "id": "D1",
   "dentro_de": null,
   "caso": "C1",
   "aspecto": "carácter",
   "valor": "esencial",
   "unidad": null,
   "cambio": null,
   "condiciones": [
    {
     "texto": "para la seguridad de las islas",
     "ref": "C4",
     "respaldo": [
      {
       "o": 4,
       "f": "para la seguridad de las islas"
      }
     ]
    }
   ],
   "modalidad": null,
   "inferido": false,
   "respaldo": [
    {
     "o": 4,
     "f": "es esencial"
    }
   ]
  }
 ],
 "acciones": [],
 "marcas": [],
 "dudas": [
  {
   "id": "Q1",
   "texto": "El texto no menciona la altura del volcán Tumbal ni contiene información sobre dicho volcán.",
   "respaldo": [
    {
     "o": 4,
     "f": "El estudio de estos volcanes es esencial para la seguridad de las islas."
    }
   ]
  }
 ]
}
```
