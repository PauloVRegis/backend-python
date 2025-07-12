from .user import User
from .professor import Professor
from .training import Training, TrainingResponse, TrainingExercise
from .exercise import Exercise

# Exporta os modelos para facilitar a importação
__all__ = ["User", "Professor", "Training", "TrainingResponse", "TrainingExercise", "Exercise"]