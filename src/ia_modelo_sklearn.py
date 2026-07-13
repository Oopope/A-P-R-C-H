import os
from typing import Tuple
import joblib
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'ia_modelo.pkl')


def _build_activity_dataset():
    # Import aquí para evitar dependencias circulares al importar el paquete
    from src.sensor_simulado import SensorSimulado
    samples = []
    labels = []
    for escenario, claves in SensorSimulado.ACTIVIDAD_POR_ESCOPEGIO:
        for frase in claves:
            samples.append(frase)
            labels.append(escenario)

    # Añadir variaciones sintéticas
    augment = [
        ("me voy a duchar", "Ducha Activa"),
        ("voy a lavar los platos", "Lavar Platos"),
        ("voy a lavar ropa", "Lavadora Activa"),
        ("voy a regar las plantas", "Riego de Jardín"),
        ("hay una fuga", "Fuga Silenciosa"),
        ("se está goteando", "Goteo Constante"),
        ("voy a trapear", "Limpieza Doméstica"),
        ("voy a lavar el carro", "Lavado de Auto"),
        ("voy a cocinar", "Cocina Activa"),
    ]
    for txt, lbl in augment:
        samples.append(txt)
        labels.append(lbl)

    return samples, labels


def _build_intent_dataset():
    # Frases de ejemplo para clasificar intenciones de usuario
    X = [
        "¿Cómo va el tanque?", "¿Cuántos litros quedan?", "estado del agua",
        "¿Tengo una fuga?", "¿Se está perdiendo agua?", "goteo",
        "¿Cuántos minutos me quedan para la ducha?", "minutos de ducha", "¿cuánto dura una ducha?",
        "¿Qué me recomienda la IA?", "consejo para ahorrar agua", "recomienda",
        "¿Qué es el medidor?", "explica el sensor", "cómo funciona el medidor",
        "hola", "buenas", "buenos días",
    ]
    y = [
        "estado", "estado", "estado",
        "fuga", "fuga", "fuga",
        "minutos", "minutos", "minutos",
        "consejo", "consejo", "consejo",
        "medidor", "medidor", "medidor",
        "saludo", "saludo", "saludo",
    ]
    return X, y


class IAEnsemble:
    def __init__(self):
        self.activity_clf = Pipeline([
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2), analyzer="word")),
            ("clf", MultinomialNB()),
        ])

        self.intent_clf = Pipeline([
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2), analyzer="word")),
            ("clf", MultinomialNB()),
        ])

        self._trained = False

    def train(self):
        X_a, y_a = _build_activity_dataset()
        self.activity_clf.fit(X_a, y_a)

        X_i, y_i = _build_intent_dataset()
        self.intent_clf.fit(X_i, y_i)

        self._trained = True

    def predict_activity(self, texto: str) -> Tuple[str, float]:
        if not self._trained:
            self.train()
        proba = max(self.activity_clf.predict_proba([texto])[0])
        label = self.activity_clf.predict([texto])[0]
        return label, float(proba * 100)

    def predict_intent(self, texto: str) -> Tuple[str, float]:
        if not self._trained:
            self.train()
        proba = max(self.intent_clf.predict_proba([texto])[0])
        label = self.intent_clf.predict([texto])[0]
        return label, float(proba * 100)


_GLOBAL = None


def get_model() -> IAEnsemble:
    global _GLOBAL
    if _GLOBAL is not None:
        return _GLOBAL

    model = IAEnsemble()
    # Intent: try to load persisted model; if missing, train in-memory
    try:
        if os.path.exists(MODEL_PATH):
            _GLOBAL = joblib.load(MODEL_PATH)
        else:
            model.train()
            _GLOBAL = model
    except Exception:
        # En caso de error, usar modelo entrenado en memoria
        model.train()
        _GLOBAL = model

    return _GLOBAL


def predict_activity(texto: str) -> Tuple[str, float]:
    m = get_model()
    return m.predict_activity(texto)


def predict_intent(texto: str) -> Tuple[str, float]:
    m = get_model()
    return m.predict_intent(texto)


def save_model(path: str = None):
    """Persiste el modelo global entrenado a disco usando joblib.

    Si no existe el directorio destino, lo crea.
    """
    global _GLOBAL
    if _GLOBAL is None:
        # Forzar entrenamiento
        _GLOBAL = get_model()

    destino = path or MODEL_PATH
    parent = os.path.dirname(destino)
    if not os.path.exists(parent):
        os.makedirs(parent, exist_ok=True)

    try:
        joblib.dump(_GLOBAL, destino)
        return destino
    except Exception:
        return None
