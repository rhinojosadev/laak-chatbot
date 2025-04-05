# deepeval set-ollama llama3.2:3b --base-url="http://localhost:11434"

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
        input="¿Cómo se llama el proyecto?",
        actual_output="El proyecto se llama 'Construcción de un robot hexápodo para reconocimiento de plagas'.",
        expected_output="El proyecto se llama 'Construcción de un robot hexápodo para reconocimiento de plagas'.",
        retrieval_context=retrieval_context,
        context=retrieval_context
    ),
    LLMTestCase(
        input="¿De qué trata el proyecto?",
        actual_output="El proyecto se refiere al desarrollo de un robot hexápodo que esté equipado con tecnología de reconocimiento de plagas para detectar infestaciones en cultivos.",
        expected_output="El proyecto trata sobre el desarrollo de un robot hexápodo usando Python y Ubuntu para detección de plagas en cultivos.",
        retrieval_context=retrieval_context,
        context=retrieval_context
    ),
    LLMTestCase(
        input="¿Qué herramientas usa el proyecto?",
        actual_output="El proyecto utiliza las siguientes herramientas: * Python * Ubuntu * OpenCV * ROS (Robot Operating System) Además, el proyecto también requiere herramientas específicas para procesamiento de imágenes. Sin embargo, no se mencionan otras herramientas específicas en el contexto proporcionado.",
        expected_output="Las herramientas que usa el proyecto son: Python, Ubuntu, OpenCV y ROS.",
        retrieval_context=retrieval_context,
        context=retrieval_context
    ),
    LLMTestCase(
        input="¿Cuáles son los requisitos técnicos del proyecto?",
        actual_output="Sí, puedo ayudarte. Los requisitos técnicos del proyecto son: - Un procesador Intel Core i5 de décima generación o superior. - 8 GB de memoria RAM como mínimo. - Un sistema operativo compatible con las herramientas de desarrollo requeridas para el proyecto (en este caso, ROS). - Un equipo de cómputo que pueda ejecutar entornos de programación, simulación y procesamiento de imágenes de manera adecuada.",
        expected_output="Los requisitos técnicos son: procesador Intel Core i5 de décima generación o superior, 8 GB de memoria RAM como mínimo, y sistema operativo compatible con las herramientas de desarrollo requeridas para el proyecto (como Ubuntu 20.04 o Windows 10). El equipo debe poder ejecutar entornos de programación, simulación y procesamiento de imágenes.",
        retrieval_context=retrieval_context,
        context=retrieval_context
    ),
]

metrics = {
    "Answer Relevancy": AnswerRelevancyMetric(),
    "Faithfulness": FaithfulnessMetric(threshold=0.7, model="llama3.2:3b"),
    "Contextual Precision": ContextualPrecisionMetric(threshold=0.7, model="llama3.2:3b"),
    "Contextual Recall": ContextualRecallMetric(threshold=0.7, model="llama3.2:3b"),
    "Contextual Relevancy": ContextualRelevancyMetric(threshold=0.7, model="llama3.2:3b"),
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