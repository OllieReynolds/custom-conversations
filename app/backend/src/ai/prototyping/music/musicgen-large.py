import torch
from transformers import pipeline
import scipy
import numpy as np

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

with torch.no_grad():
    synthesiser = pipeline("text-to-audio", "facebook/musicgen-small", device=0 if device.type == "cuda" else -1)
    music = synthesiser("lo-fi music with a soothing melody", forward_params={"do_sample": True})

scipy.io.wavfile.write("musicgen_out.wav", rate=music["sampling_rate"], data=np.array(music["audio"]))
