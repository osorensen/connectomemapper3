# Copyright (C) 2009-2021, Ecole Polytechnique Federale de Lausanne (EPFL) and
# Hospital Center and University of Lausanne (UNIL-CHUV), Switzerland, and CMP3 contributors
# All rights reserved.
#
#  This software is distributed under the open-source license Modified BSD.

"""Definition of config and stage classes for computing brain parcellation."""

# General imports
import os
from traits.api import *

# Nipype imports
import nipype.pipeline.engine as pe

# Own imports
from cmp.stages.common import Stage
from cmtklib.interfaces.eegloader import EEGLoader


class EEGLoaderConfig(HasTraits):
    invsol_format = Enum('Cartool-LAURA', 'Cartool-LORETA', 'mne-sLORETA',
                         desc='Cartool vs mne')


class EEGLoaderStage(Stage):
    def __init__(self, bids_dir, output_dir):
        """Constructor of a :class:`~cmp.stages.parcellation.parcellation.ParcellationStage` instance."""
        self.name = 'eeg_loader_stage'
        self.bids_dir = bids_dir
        self.output_dir = output_dir
        self.config = EEGLoaderConfig()
        self.inputs = ["subject", "base_directory", "invsol_format","output_query", "derivative_list"]
        self.outputs = ["EEG", "src", "invsol", "rois", "invsol_format"]

    def create_workflow(self, flow, inputnode, outputnode):
        eegloader_node = pe.Node(interface=EEGLoader(), name="eegloader")

        flow.connect([(inputnode, eegloader_node,
                       [('subject', 'subject'),
                        ('base_directory', 'base_directory'),
                        ('output_query', 'output_query'),
                        ('derivative_list', 'derivative_list')
                        ]
                       )])
        
        flow.connect([(inputnode, outputnode,
                       [('invsol_format','invsol_format')
                        ]     
                       )])

        flow.connect([(eegloader_node, outputnode,
                       [
                           ('EEG', 'EEG'),
                           ('src', 'src'),
                           ('invsol', 'invsol'),
                           ('rois', 'rois'),
                       ]
                       )])

    def define_inspect_outputs(self):
        raise NotImplementedError

    def has_run(self):
        """Function that returns `True` if the stage has been run successfully.

        Returns
        -------
        `True` if the stage has been run successfully
        """
        if self.config.eeg_format == ".set":
            if self.config.inverse_solution.split('-')[0] == "Cartool":
                return os.path.exists(self.config.epochs_fif)
