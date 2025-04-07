# deepeval set-ollama qwen2.5:3b --base-url="http://localhost:11434"
from deepeval.test_case import LLMTestCase
from deepeval.metrics import (
    AnswerRelevancyMetric,
    FaithfulnessMetric,
    ContextualPrecisionMetric,
    ContextualRecallMetric,
    ContextualRelevancyMetric,
    HallucinationMetric
)

def load_context(document):
    with open(document, "r", encoding="utf-8") as f:
        return [f.read()]

context_file = "../backend/documents/files/project.txt"
retrieval_context = load_context(context_file)

test_cases = [
    LLMTestCase(
        input="¿A quién le puedo preguntar mis dudas?",
        actual_output="Puedes preguntar tus dudas a Juan Pérez o a Jorge Salgado.",
        expected_output="Cualquier duda general puede dirigirse a Juan Pérez o a Jorge Salgado.",
        retrieval_context=retrieval_context,
        context=retrieval_context
    ),
    LLMTestCase(
        input="¿Qué tecnologías son utilizadas en el proyecto?",
        actual_output="Las tecnologías utilizadas en el proyecto son React, Node.js, MongoDB, Express, GitHub y Vercel.",
        expected_output="Las tecnologías utilizadas son React 18, Node.js 20, MongoDB, TailwindCSS y Express.",
        retrieval_context=retrieval_context,
        context=retrieval_context
    ),
    LLMTestCase(
        input="¿Cómo puedo acceder al repositorio en GitHub?",
        actual_output="Para acceder al repositorio en GitHub, cada membro debe tener una cuenta activa e ingresar a través de su usuario. Luego, debe clonar el repositorio localmente.",
        expected_output="Para acceder al repositorio en GitHub, cada miembro debe tener una cuenta activa, enviar su usuario al Project Manager, solicitar acceso y aceptar la invitación para luego clonar el repositorio localmente.",
        retrieval_context=retrieval_context,
        context=retrieval_context
    ),
    LLMTestCase(
        input="¿Quién es el project manager del proyecto?",
        actual_output="Pérez es el Project Manager del proyecto.",
        expected_output="Juan Pérez es el Project Manager del proyecto.",
        retrieval_context=retrieval_context,
        context=retrieval_context
    ),
    LLMTestCase(
        input="¿Cuándo es el cierre del proyecto?",
        actual_output="El cierre del proyecto será el 26 de junio.",
        expected_output="El cierre del proyecto será el 26 de junio.",
        retrieval_context=retrieval_context,
        context=retrieval_context
    ),
]

metrics = {
    "Answer Relevancy": AnswerRelevancyMetric(threshold=0.7, model="qwen2.5:3b"),
    "Faithfulness": FaithfulnessMetric(threshold=0.7, model="qwen2.5:3b"),
    "Contextual Precision": ContextualPrecisionMetric(threshold=0.7, model="qwen2.5:3b"),
    "Contextual Recall": ContextualRecallMetric(threshold=0.7, model="qwen2.5:3b"),
    "Contextual Relevancy": ContextualRelevancyMetric(threshold=0.7, model="qwen2.5:3b"),
    "Hallucination": HallucinationMetric(threshold=0.5)
}

metric_scores = {name: [] for name in metrics.keys()}

for i, test_case in enumerate(test_cases, 1):
    print(f"\n Case {i}: {test_case.input}")
    for metric_name, metric in metrics.items():
        metric.measure(test_case)
        print(f"  - {metric_name}: {metric.score:.2f}")
        metric_scores[metric_name].append(metric.score)

print("\nResults:")
for metric_name, scores in metric_scores.items():
    avg_score = sum(scores) / len(scores)
    print(f"  - {metric_name}: {avg_score:.2f}")
