# backend/agentes/arquitecto_checkin.py
import os
from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama
from langchain.chains import LLMChain
from .chroma_manager import guardar_checkin

# Configurar conexión al modelo Ollama
model = os.getenv("OLLAMA_MODEL")
base_url = os.getenv("OLLAMA_BASE_URL")

if not model or not base_url:
    raise EnvironmentError("Faltan variables de entorno OLLAMA_MODEL y/o OLLAMA_BASE_URL")

llm = Ollama(model=model, base_url=base_url)

# Paso 1: Clasificar el objetivo
prompt_clasificar = PromptTemplate(
    input_variables=["objetivo"],
    template="""Dado el siguiente objetivo: "{objetivo}".
Clasificá el tipo de objetivo que representa.
Opciones posibles: [curso, aplicación, evento, campaña, sistema, otro].
Respondé SOLO el tipo."""
)
chain_clasificar = LLMChain(llm=llm, prompt=prompt_clasificar, output_key="clasificacion")

# Paso 2: Detectar preguntas
prompt_detectar_preguntas = PromptTemplate(
    input_variables=["objetivo", "clasificacion"],
    template="""Objetivo: "{objetivo}".
Clasificación previa: "{clasificacion}".

Detectá si falta información crítica para avanzar.
Listá hasta 3 preguntas si falta algo. Si no falta, escribí "completo"."""
)
chain_detectar_preguntas = LLMChain(llm=llm, prompt=prompt_detectar_preguntas, output_key="preguntas")

# Paso 3: Sugerir estructura
prompt_sugerir_estructura = PromptTemplate(
    input_variables=["objetivo", "clasificacion", "preguntas"],
    template="""Objetivo: "{objetivo}".
Clasificación: "{clasificacion}".
Preguntas detectadas: "{preguntas}".

Sugerí una estructura previa (índice de temas, módulos, fases) para desarrollar el objetivo.
Si no es necesario, indicá "no necesario"."""
)
chain_sugerir_estructura = LLMChain(llm=llm, prompt=prompt_sugerir_estructura, output_key="estructura")

# Paso 4: Detectar dependencias
prompt_detectar_dependencias = PromptTemplate(
    input_variables=["objetivo", "estructura"],
    template="""Objetivo: "{objetivo}".
Estructura previa: "{estructura}".

Listá las principales dependencias lógicas o técnicas iniciales necesarias para llevar a cabo el objetivo."""
)
chain_detectar_dependencias = LLMChain(llm=llm, prompt=prompt_detectar_dependencias, output_key="dependencias")

# Paso 5: Validar razonabilidad
prompt_validacion = PromptTemplate(
    input_variables=["clasificacion", "estructura", "dependencias", "preguntas"],
    template="""Plan a validar:
- Tipo de objetivo: {clasificacion}
- Estructura sugerida: {estructura}
- Dependencias detectadas: {dependencias}
- Preguntas detectadas: {preguntas}

¿Es razonable proceder?"""
)
chain_validacion = LLMChain(llm=llm, prompt=prompt_validacion, output_key="validacion")

# Paso 6: Confirmar razonabilidad final
prompt_confirmar = PromptTemplate(
    input_variables=["validacion"],
    template="""Dado el siguiente resultado de validación:

{validacion}

Respondé solamente: SÍ o NO. ¿Es razonable proceder?"""
)
chain_confirmar = LLMChain(llm=llm, prompt=prompt_confirmar, output_key="confirmacion")

# 🔥 Función principal
def checkin_arquitecto(objetivo, objetivo_id=None):
    result = {}

    # Paso 1: Clasificar
    clasificacion = chain_clasificar.run(objetivo=objetivo)
    if objetivo_id: guardar_checkin(objetivo_id, {"clasificacion": clasificacion})
    result["clasificacion"] = clasificacion

    # Paso 2: Detectar preguntas
    preguntas = chain_detectar_preguntas.run(objetivo=objetivo, clasificacion=clasificacion)
    if objetivo_id: guardar_checkin(objetivo_id, {"preguntas": preguntas})
    result["preguntas"] = preguntas

    # Paso 3: Sugerir estructura
    estructura = chain_sugerir_estructura.run(objetivo=objetivo, clasificacion=clasificacion, preguntas=preguntas)
    if objetivo_id: guardar_checkin(objetivo_id, {"estructura": estructura})
    result["estructura"] = estructura

    # Paso 4: Detectar dependencias
    dependencias = chain_detectar_dependencias.run(objetivo=objetivo, estructura=estructura)
    if objetivo_id: guardar_checkin(objetivo_id, {"dependencias": dependencias})
    result["dependencias"] = dependencias

    # Paso 5: Validar plan
    validacion = chain_validacion.run(clasificacion=clasificacion, estructura=estructura, dependencias=dependencias, preguntas=preguntas)
    if objetivo_id: guardar_checkin(objetivo_id, {"validacion": validacion})
    result["validacion"] = validacion

    # Paso 6: Confirmar razonabilidad
    confirmacion_completa = chain_confirmar.run(validacion=validacion)
    if objetivo_id: guardar_checkin(objetivo_id, {"confirmacion": confirmacion_completa})
    result["confirmacion"] = confirmacion_completa

    # 🔥 Interpretar confirmacion final
    confirmacion_final = confirmacion_completa.strip().lower()
    if "sí" in confirmacion_final or "si" in confirmacion_final or "yes" in confirmacion_final:
        result["confirmacion_final"] = "sí"
    else:
        result["confirmacion_final"] = "no"

    result["objetivo"] = objetivo
    return result
