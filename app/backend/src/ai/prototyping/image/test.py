import torch
from diffusers import DiffusionPipeline
import matplotlib.pyplot as plt

# Load the diffusion model with reduced precision and smaller size
pipe = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-base-16384", torch_dtype=torch.float16, use_safetensors=True, variant="fp16")

# Move the model to the GPU
pipe.to("cuda")

# Use memory-efficient attention if using torch < 2.0
# pipe.enable_xformers_memory_efficient_attention()

# Define the prompt
prompt = "An astronaut riding a green horse"

# Generate images
with torch.no_grad():
    images = pipe(prompt=prompt).images[0]

# Ensure images are on CPU for faster processing
images = images.cpu()

# Convert the tensor to numpy array
image_array = images.permute(1, 2, 0).numpy()

# Display the image using Matplotlib
plt.imshow(image_array)
plt.axis('off')
plt.show()
