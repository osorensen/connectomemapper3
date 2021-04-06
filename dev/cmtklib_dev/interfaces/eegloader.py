import pycartool as cart
import pickle
import numpy as  np
import mne 
from nipype.interfaces.base import BaseInterface, BaseInterfaceInputSpec, traits, TraitedSpec
import nipype.interfaces.io as nio
import os

class EEGLoaderInputSpec(BaseInterfaceInputSpec):
    """Input specification for EEGLAB2fif. """

    base_directory = traits.Directory(
        exists=True, desc='BIDS data directory', mandatory=True)

    subject_id = traits.Str(
        desc='subject id', mandatory=True)

    output_query = traits.Dict(
        desc='output query for BIDSDataGrabber', mandatory=True)
    
    derivative_list = traits.List(
            exists=True, desc='List of derivatives to add to the datagrabber', mandatory=True)
    

class EEGLoaderOutputSpec(TraitedSpec):
    """Input specification for EEGLAB2fif. """
    

    EEG = traits.List(
            exists=True, desc='eeg * epochs in .fif format', mandatory=True)
    src = traits.List(
            exists=True, desc='src (spi loaded with pycartool)', mandatory=True)
    invsol = traits.List(
            exists=True, desc='Inverse solution (.is file loaded with pycartool)', mandatory=True)
    rois = traits.List(
            exists=True, desc='parcellation scheme', mandatory=True)

class EEGLoader(BaseInterface):

    input_spec = EEGLoaderInputSpec
    output_spec = EEGLoaderOutputSpec
    
    def _run_interface(self, runtime):
        self.base_directory = self.inputs.base_directory
        self.subject_id = self.inputs.subject_id        
        self.derivative_list = self.inputs.derivative_list
        self._run_datagrabber()
        return runtime


    def _run_datagrabber(self):
        bidsdatagrabber = nio.BIDSDataGrabber(index_derivatives=False, extra_derivatives=[os.path.join(self.base_directory,'derivatives',elem) for elem in self.derivative_list])
        bidsdatagrabber.inputs.base_dir = self.base_directory
        bidsdatagrabber.inputs.subject = self.subject_id
        bidsdatagrabber.inputs.output_query = self.inputs.output_query
        print(bidsdatagrabber.inputs.output_query)
        print(bidsdatagrabber.inputs.base_dir)
        print(bidsdatagrabber.inputs.subject)
        self.results = bidsdatagrabber.run()
    

    def _list_outputs(self):        
        outputs = self._outputs().get()     
        
        for key, value in self.results.outputs.get().items():
            outputs[key] = value
        
        return outputs
