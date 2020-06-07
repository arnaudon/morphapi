import sys

sys.path.append("./")

import pytest
import numpy as np
from random import choice
from morphapi.morphology.morphology import Neuron
from morphapi.utils.data_io import listdir
from vtkplotter import Mesh


@pytest.fixture
def neuron():
    files = listdir("tests/data")
    return Neuron(swc_file=choice(files))


args = [
    (3, "salmon", "darkseagreen", "orangered", "blackboard", "blue", True),
    (3, "salmon", None, None, "blackboard", "blue", False),
    (3, "salmon", None, None, None, None, False),
    (5, "salmon", "darkseagreen", "orangered", "blackboard", "blue", False),
]


@pytest.mark.parametrize("radius,soma,apical,basal,axon,whole,cache", args)
def test_create_mesh(neuron, radius, soma, apical, basal, axon, whole, cache):
    components, neuron = neuron.create_mesh(
        neurite_radius=radius,  #
        soma_color=soma,  # Specify colors [see vtkplotter.colors for more details]
        apical_dendrites_color=apical,
        basal_dendrites_color=basal,
        axon_color=axon,
        whole_neuron_color=whole,
        use_cache=cache,
    )

    if not isinstance(neuron, Mesh):
        raise ValueError

    if not isinstance(components, dict):
        raise ValueError

    for ntp in Neuron._neurite_types:
        if ntp not in components.keys():
            raise ValueError
        if components[ntp] is not None:
            if not isinstance(components[ntp], Mesh):
                raise ValueError


def test_create_mesh_args(neuron):
    neuron.create_mesh(
        neurite_radius=np.random.uniform(2, 20), neuron_color="red"
    )
    neuron.create_mesh(neuron_number=1, cmap="Reds")
