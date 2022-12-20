

def setup():
    #@title Run this cell to Setup CorentinJ/Real-Time-Voice-Cloning
    
    #@markdown * clone the project
    #@markdown * download pretrained models
    #@markdown * initialize the voice cloning models
    
    %tensorflow_version 1.x
    import os
    from os.path import exists, join, basename, splitext
    
    git_repo_url = 'https://github.com/CorentinJ/Real-Time-Voice-Cloning.git'
    project_name = splitext(basename(git_repo_url))[0]
    if not exists(project_name):
        # clone and install
        !git clone -q --recursive {git_repo_url}
        # install dependencies
        !cd {project_name} && pip install -q -r requirements.txt
        !pip install -U --no-cache-dir gdown --pre
        !apt-get install -qq libportaudio2
        !pip install -q https://github.com/tugstugi/dl-colab-notebooks/archive/colab_utils.zip
    
        download_ids = ['1n1sPXvT34yXFLT47QZA6FIRGrwMeSsZc',
                        '1jhlkXcYYsiP_eXeqxIqcnOHqAoFEwINY',
                        '1z3RV1oUzEhGTnbv3pBc3OVFFc_79fI0W',
                        '1-fpRMhyIbf_Ijm197pVEg6IzyKDxxTLh',
                        '148UUYI9yheoUZqztGwO4HOKql8Tt-ZVs']
    
        for id in download_ids:
            print("Attept download from", id)
            response = !cd {project_name} && gdown --id $id --output pretrained.zip && unzip pretrained.zip
            if response[0] == 'Downloading...':
                break
            else:
                continue
        # download pretrained model
        # response = !cd {project_name} && gdown https://drive.google.com/uc?id=1n1sPXvT34yXFLT47QZA6FIRGrwMeSsZc && unzip pretrained.zip
    import sys
    sys.path.append(project_name)
    
    from IPython.display import display, Audio, clear_output
    from IPython.utils import io
    import ipywidgets as widgets
    import numpy as np
    from dl_colab_notebooks.audio import record_audio, upload_audio
    
    from synthesizer.inference import Synthesizer
    from encoder import inference as encoder
    from vocoder import inference as vocoder
    from pathlib import Path
    
    encoder.load_model(project_name / Path("encoder/saved_models/pretrained.pt"))
    synthesizer = Synthesizer(project_name / Path("synthesizer/saved_models/logs-pretrained/taco_pretrained"))
    vocoder.load_model(project_name / Path("vocoder/saved_models/pretrained/pretrained.pt"))


#@title Run this cell to Record or Upload Audio
#@markdown * Either record audio from microphone or upload audio from file (.mp3 or .wav) 

SAMPLE_RATE = 22050
record_or_upload = "Record" #@param ["Record", "Upload (.mp3 or .wav)"]
record_seconds =   10#@param {type:"number", min:1, max:10, step:1}

embedding = None
def _compute_embedding(audio):
    display(Audio(audio, rate=SAMPLE_RATE, autoplay=True))
    global embedding
    embedding = None
    embedding = encoder.embed_utterance(encoder.preprocess_wav(audio, SAMPLE_RATE))
def _record_audio(b):
    clear_output()
    audio = record_audio(record_seconds, sample_rate=SAMPLE_RATE)
    _compute_embedding(audio)
def _upload_audio(b):
    clear_output()
    audio = upload_audio(sample_rate=SAMPLE_RATE)
    _compute_embedding(audio)

if record_or_upload == "Record":
    button = widgets.Button(description="Record Your Voice")
    button.on_click(_record_audio)
    display(button)
else:
    #button = widgets.Button(description="Upload Voice File")
    #button.on_click(_upload_audio)
    _upload_audio("")

#@title Run this to Synthesize a text (result) { run: "auto" }
text = "One of the two people who tested positive for the novel coronavirus in the United Kingdom is a student at the University of York in northern England." #@param {type:"string"}

def synthesize(embed, text):
    print("Synthesizing new audio...")
    #with io.capture_output() as captured:
    specs = synthesizer.synthesize_spectrograms([text], [embed])
    generated_wav = vocoder.infer_waveform(specs[0])
    generated_wav = np.pad(generated_wav, (0, synthesizer.sample_rate), mode="constant")
    clear_output()
    display(Audio(generated_wav, rate=synthesizer.sample_rate, autoplay=True))

if embedding is None:
    print("first record a voice or upload a voice file!")
else:
    synthesize(embedding, text)