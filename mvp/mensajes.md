# Los dos mensajes (y los relojes)

Cómo se arma **cualquier** llamada del MVP: qué va en el `system` y qué en el `user`. **Rige para
todos los prompts** —`paso1_unidades.py`, `paso2_datos.py`, `orq/armar_prompt.py`— y quien la
implementa es `mvp/código/mensajes.py` (`partir`).

1. **Dos marcas.** Un prompt de trabajo trae `[SISTEMA]` para lo invariante y, para el material de
   la llamada, `[TAREA]` **o** `[USUARIO]` (las dos valen). Las marcas **no llegan al modelo**:
   `partir` las consume.
2. **Qué va en cada uno.** El `system` lleva la tarea, las reglas, el formato de salida **y los
   ejemplos** —todo lo que no cambia de una llamada a otra—. El `user` lleva **el material de esta
   llamada** —el documento, las unidades, los casos, la pregunta— **y el pedido**, al final.
3. **Por qué así.** El `system` es el **prefijo invariante**: es lo que aprovecha el caché. En la
   familia `responses` viaja como `instructions`, y en las otras dos como el primer mensaje del
   sistema. Medido: con Luna el prefijo entró entero —**1.839 de 1.842** tokens de entrada en la
   segunda llamada— y con MiMo, **2.048 de 2.066** sin mandar nada por un campo aparte. Poner en el
   `system` algo que cambia por llamada se paga en cada corrida.
4. **Los relojes, en todo prompt, y cada uno en su lugar.** Dos, con el mismo formato
   —`[día-mes-año: hora]`— y armados por `mvp/código/relojes.py`:
   - **el del radicado** (`{{RELOJ_RADICADO}}`): cuándo entró el documento a Zettel
     (`documentos.fecha_radicacion`). Es **invariante por documento**, así que va en el **`system`**.
   - **el del sistema** (`{{RELOJ_SISTEMA}}`): el «ahora» de la corrida. **Cambia en cada corrida**,
     así que va en el **`user`**, con el material y **al final, después del texto**: así el prefijo
     común —las reglas y el documento— se sigue reusando, y lo que cambia queda al final.

   Van **etiquetados**, y la etiqueta no es adorno: el del radicado es el que resuelve un deíctico
   **del documento** («ayer», «en dos días»); el del sistema, el de la corrida. **Ninguno es dato
   del documento**, y el prompt lo dice. Lo propio de la consulta —los relojes de **todos** los
   documentos del dominio, y el del sistema congelado una sola vez al abrirla— está en
   `mvp/consulta-diseno.md` §4.3.
5. **Los huecos se rellenan con `str.replace`**, nunca con `str.format`: el texto del documento
   puede traer llaves. Cada acto pasa los suyos: `RELOJ_RADICADO`, `RELOJ_SISTEMA`, `TEXTO`,
   `UNIDADES`, `CASOS`, `PREGUNTA`.
6. **El material va delimitado** (`<texto> … </texto>`) y **el pedido, al final del `user`**.

Lo que **no** va en el `system`: el material de la llamada y nada que cambie entre llamadas. Y si el
prompt pide un hueco que el acto no llena, el acto **se detiene**: no se llama al modelo con el
hueco crudo.
