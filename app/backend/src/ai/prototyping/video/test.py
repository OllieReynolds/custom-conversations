import torch
from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
from diffusers.utils import export_to_video

# Initialize the pipeline
pipe = DiffusionPipeline.from_pretrained("damo-vilab/text-to-video-ms-1.7b", torch_dtype=torch.float16, variant="fp16")
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
pipe.enable_model_cpu_offload()

# Generate video frames
prompt = "Spiderman is surfing"
output = pipe(prompt, num_inference_steps=25)
video_frames = output.frames

# Check if video_frames is a tensor with an extra dimension
if isinstance(video_frames, torch.Tensor) and video_frames.ndim == 4:
    # Convert to a list of 3D frames
    video_frames = [frame.squeeze(0) for frame in video_frames]

# Now pass the list of 3D frames to export_to_video
video_path = export_to_video(video_frames)
