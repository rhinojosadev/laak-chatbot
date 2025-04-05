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
        input="¿Cómo se llama el proyecto?",
        actual_output="El nombre del proyecto es 'Construcción de un robot hexápodo para reconocimiento de plagas'.",
        expected_output="El proyecto se llama 'Construcción de un robot hexápodo para reconocimiento de plagas'.",
        retrieval_context=retrieval_context,
        context=retrieval_context
    ),
    LLMTestCase(
        input="¿De qué trata el proyecto?",
        actual_output="El proyecto trata sobre la construcción de un robot hexápodo que utiliza Python y Ubuntu para la detección y reconocimiento de plagas en cultivos. También se realiza el procesamiento de imágenes con este robot. El objetivo es desarrollar e implementar software del robot, lo cual requiere un rendimiento adecuado tanto para el desarrollo como para la simulación y procesamiento de imágenes.",
        expected_output="El proyecto trata sobre el desarrollo de un robot hexápodo usando Python y Ubuntu para detección de plagas en cultivos.",
        retrieval_context=retrieval_context,
        context=retrieval_context
    ),
    LLMTestCase(
        input="¿Qué herramientas usa el proyecto?",
        actual_output="El proyecto usa Python y Ubuntu como herramientas.",
        expected_output="Las herramientas que usa el proyecto son: Python, Ubuntu, OpenCV y ROS.",
        retrieval_context=retrieval_context,
        context=retrieval_context
    ),
    LLMTestCase(
        input="¿Cuáles son los requisitos técnicos del proyecto?",
        actual_output="Los requisitos técnicos del proyecto incluyen un procesador Intel Core i5 de décima generación o superior, 8 GB de memoria RAM mínima e sistema operativo Ubuntu 20.04. También se requiere que el equipo sea compatible con herramientas como Python, Ubuntu, OpenCV y ROS para el desarrollo e implementación del software del robot.",
        expected_output="Los requisitos técnicos son: procesador Intel Core i5 de décima generación o superior, 8 GB de memoria RAM como mínimo, y sistema operativo compatible con las herramientas de desarrollo requeridas para el proyecto (como Ubuntu 20.04 o Windows 10). El equipo debe poder ejecutar entornos de programación, simulación y procesamiento de imágenes.",
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
