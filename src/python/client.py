from enum import Enum

from src.python.experiments.k8s.podfault.container_kill import ContainerKill
from src.python.experiments.k8s.podfault.pod_failure import PodFailure
from src.python.experiments.k8s.podfault.pod_kill import PodKill
from src.python.experiments.k8s.stress.cpu import StressCPU
from src.python.experiments.k8s.stress.memory import StressMemory


class Experiment(Enum):
    POD_FAILURE = "POD_FAILURE"
    POD_KILL = "POD_KILL"
    CONTAINER_KILL = "CONTAINER_KILL"
    STRESS_CPU = "STRESS_CPU"
    STRESS_MEMORY = "STRESS_MEMORY"


class ExperimentFactory:
    instance = None

    experiments = {
        Experiment.POD_FAILURE: PodFailure,
        Experiment.POD_KILL: PodKill,
        Experiment.CONTAINER_KILL: ContainerKill,
        Experiment.STRESS_CPU: StressCPU,
        Experiment.STRESS_MEMORY: StressMemory
    }

    @classmethod
    def get_instance(cls):
        if cls.instance is None:
            cls.instance = ExperimentFactory()
        return cls.instance

    def get(self, e: Experiment, **kwargs):
        return self.experiments[e](**kwargs)


class ChaosMeshClient:

    def __init__(self):
        self.factory = ExperimentFactory().get_instance()

    def start(self, e: Experiment, namespace, name, **kwargs):
        self.factory.get(e, **kwargs).submit(namespace, name)

    def pause(self, e: Experiment, namespace, name, **kwargs):
        self.factory.get(e, **kwargs).pause(namespace, name)

    def delete(self, e: Experiment, namespace, name, **kwargs):
        self.factory.get(e, **kwargs).delete(namespace=namespace, name=name)
