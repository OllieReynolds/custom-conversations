import requests
import threading

class CUDAService:
    def __init__(self, backendURL):
        self.backendURL = backendURL

    def checkCUDAAvailability(self, onResult):
        def inner():
            try:
                response = requests.get(f"{self.backendURL}/check_cuda_available")
                if response.ok:
                    cudaAvailable = response.json().get('cuda_available', False)
                else:
                    cudaAvailable = False
            except Exception:
                cudaAvailable = False
            onResult(cudaAvailable)
        threading.Thread(target=inner).start()
