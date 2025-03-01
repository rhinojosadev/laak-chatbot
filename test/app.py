# deepeval set-ollama llama3.2:3b --base-url="http://localhost:11434"
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric
from deepeval.metrics import FaithfulnessMetric
from deepeval.metrics import ContextualPrecisionMetric
from deepeval.metrics import HallucinationMetric

# Remplazar aqui con la salida actual de tu LLM
actual_output = "Mi Tiendita!"
# Remplazar aqui con la salida esperada del LLM
expected_output = "Mi Tiendita"
# Remplazar aqui el contexto
retrieval_context = ['''¡Bienvenido a Mi Tiendita! Estamos emocionados de que formes parte de Mi Tiendita, la plataforma que te ayuda a vender fácil y rápido.
                        ¿Qué puedes hacer aquí?
                        Sube tus productos en minutos.
                        Gestiona tus pedidos y clientes desde un solo lugar.
                        Recibe pagos seguros y sin complicaciones.
                        Personaliza tu tienda para que refleje tu estilo.''']


answer_relevancy_metric = AnswerRelevancyMetric()
faithful_metric = FaithfulnessMetric(
    threshold=0.7,
    model="llama3.2:3b",
    include_reason=True
)
contextual_metric = ContextualPrecisionMetric(
    threshold=0.7,
    model="llama3.2:3b",
    include_reason=True
)
hallucination_metric = HallucinationMetric(threshold=0.5)


test_case = LLMTestCase(
  input="Como se llama el proyecto?",
  actual_output=actual_output,
  expected_output=expected_output,
  retrieval_context=retrieval_context
)

test_case_hallucination = LLMTestCase(
    input="What was the blond doing?",
    actual_output=actual_output,
    context=retrieval_context
)

answer_relevancy_metric.measure(test_case)
print('AnswerRelevancyMetric')
print(answer_relevancy_metric.score)

faithful_metric.measure(test_case)
print('FaithfulnessMetric')
print(faithful_metric.score)
print(faithful_metric.reason)

contextual_metric.measure(test_case)
print('ContextualPrecisionMetric')
print(contextual_metric.score)
print(contextual_metric.reason)

hallucination_metric.measure(test_case_hallucination)
print("HallucinationMetric")
print(hallucination_metric.score)
print(hallucination_metric.reason)



