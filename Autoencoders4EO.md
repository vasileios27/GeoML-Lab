# Building Autoencoders from Scratch for Earth Observation: From Grayscale to Multi-Channel, Multi-Temporal Networks

By Vasileios Vatellis

Earth observation data is unique: it often comes in multiple spectral channels and even multiple time frames. However, most of the pre-trained models available in the computer vision community are built for 3-channel RGB images. This gap creates a challenge when working with satellite or satellite imagery where sensors might capture 5, 7, or more channels and where time series data is common.

In this article, we’ll walk through creating autoencoders from scratch—starting with a basic grayscale autoencoder and progressing step-by-step to a convolutional autoencoder that can handle inputs with 5 channels and 3 time frames. By the end, you'll have an understanding of how to build flexible autoencoders tailored for the Earth observation domain.

## What is an Autoencoder?
An autoencoder is a neural network that learns to compress data into a lower-dimensional representation (the encoder) and then reconstruct the original data from that representation (the decoder). This unsupervised learning approach can be particularly useful in tasks such as denoising, anomaly detection, and dimensionality reduction.

### Step 1: A Basic Autoencoder for a Single-Channel (Grayscale) Image

Let’s start with a simple fully connected (linear) autoencoder for grayscale images. For a 28×28 image, the input size is 784.

```
import torch
import torch.nn as nn

class BasicAutoencoder(nn.Module):
    def __init__(self):
        super(BasicAutoencoder, self).__init__()
        self.encoder = nn.Sequential(
            nn.Linear(28 * 28, 128),
            nn.ReLU(True),
            nn.Linear(128, 64),
            nn.ReLU(True),
            nn.Linear(64, 32),
            nn.ReLU(True)
        )
        self.decoder = nn.Sequential(
            nn.Linear(32, 64),
            nn.ReLU(True),
            nn.Linear(64, 128),
            nn.ReLU(True),
            nn.Linear(128, 28 * 28),
            nn.Sigmoid()  # Constrain outputs between 0 and 1
        )

    def forward(self, x):
        x = self.encoder(x)
        x = self.decoder(x)
        return x

# Test the model with a random grayscale image
if __name__ == "__main__":
    model = BasicAutoencoder()
    model.eval()
    random_input = torch.rand(1, 28 * 28)
    output = model(random_input)
    print("Grayscale Input Shape:", random_input.shape)
    print("Reconstructed Output Shape:", output.shape)
```
This basic autoencoder sets the foundation. However, real-world Earth observation data is rarely single-channel.

### Step 2: Extending to a 3-Channel (RGB) Autoencoder
For an RGB image of size 28×28, the input size becomes 3 × 28 × 28 = 2352. We adjust the first and last layers accordingly:

```
class RGB_Autoencoder(nn.Module):
    def __init__(self):
        super(RGB_Autoencoder, self).__init__()
        input_dim = 3 * 28 * 28
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.ReLU(True),
            nn.Linear(128, 64),
            nn.ReLU(True),
            nn.Linear(64, 32),
            nn.ReLU(True)
        )
        self.decoder = nn.Sequential(
            nn.Linear(32, 64),
            nn.ReLU(True),
            nn.Linear(64, 128),
            nn.ReLU(True),
            nn.Linear(128, input_dim),
            nn.Sigmoid()
        )

    def forward(self, x):
        x = self.encoder(x)
        x = self.decoder(x)
        return x

if __name__ == "__main__":
    model = RGB_Autoencoder()
    model.eval()
    random_input = torch.rand(1, 3 * 28 * 28)
    output = model(random_input)
    print("RGB Input Shape:", random_input.shape)
    print("RGB Output Shape:", output.shape)
```
While this fully connected approach works for simple tasks, convolutional autoencoders are often more effective for image data as they can capture spatial hierarchies.

### Step 3: A Convolutional Autoencoder for RGB Images
We now introduce convolutional layers, which are better suited for image data. Here’s a convolutional autoencoder designed for 28×28 RGB images:
```
class ConvAutoencoder(nn.Module):
    def __init__(self):
        super(ConvAutoencoder, self).__init__()
        # Encoder: [batch, 3, 28, 28] -> [batch, 64, 1, 1]
        self.encoder = nn.Sequential(
            nn.Conv2d(3, 16, kernel_size=3, stride=2, padding=1),  # -> [16, 14, 14]
            nn.ReLU(True),
            nn.Conv2d(16, 32, kernel_size=3, stride=2, padding=1), # -> [32, 7, 7]
            nn.ReLU(True),
            nn.Conv2d(32, 64, kernel_size=7)  # -> [64, 1, 1]
        )
        
        # Decoder: reconstruct the image
        self.decoder = nn.Sequential(
            nn.ConvTranspose2d(64, 32, kernel_size=7),  # -> [32, 7, 7]
            nn.ReLU(True),
            nn.ConvTranspose2d(32, 16, kernel_size=3, stride=2, padding=1, output_padding=1),  # -> [16, 14, 14]
            nn.ReLU(True),
            nn.ConvTranspose2d(16, 3, kernel_size=3, stride=2, padding=1, output_padding=1),  # -> [3, 28, 28]
            nn.Sigmoid()
        )

    def forward(self, x):
        x = self.encoder(x)
        x = self.decoder(x)
        return x

if __name__ == "__main__":
    model = ConvAutoencoder()
    model.eval()
    random_input = torch.rand(1, 3, 28, 28)
    output = model(random_input)
    print("Convolutional RGB Input Shape:", random_input.shape)
    print("Convolutional RGB Output Shape:", output.shape)
```
### Step 4: Adapting the Autoencoder for 5-Channel Images
Earth observation data often comes with additional spectral bands. For a 28×28 image with 5 channels, we update the first and last convolutional layers to handle 5 channels:
```
class ConvAutoencoder5Channels(nn.Module):
    def __init__(self):
        super(ConvAutoencoder5Channels, self).__init__()
        # Encoder: [batch, 5, 28, 28] -> latent representation
        self.encoder = nn.Sequential(
            nn.Conv2d(5, 16, kernel_size=3, stride=2, padding=1),  # -> [16, 14, 14]
            nn.ReLU(True),
            nn.Conv2d(16, 32, kernel_size=3, stride=2, padding=1), # -> [32, 7, 7]
            nn.ReLU(True),
            nn.Conv2d(32, 64, kernel_size=7)  # -> [64, 1, 1]
        )
        
        # Decoder: reconstruct to 5 channels
        self.decoder = nn.Sequential(
            nn.ConvTranspose2d(64, 32, kernel_size=7),  # -> [32, 7, 7]
            nn.ReLU(True),
            nn.ConvTranspose2d(32, 16, kernel_size=3, stride=2, padding=1, output_padding=1),  # -> [16, 14, 14]
            nn.ReLU(True),
            nn.ConvTranspose2d(16, 5, kernel_size=3, stride=2, padding=1, output_padding=1),  # -> [5, 28, 28]
            nn.Sigmoid()
        )

    def forward(self, x):
        x = self.encoder(x)
        x = self.decoder(x)
        return x

if __name__ == "__main__":
    model = ConvAutoencoder5Channels()
    model.eval()
    random_input = torch.rand(1, 5, 28, 28)
    output = model(random_input)
    print("5-Channel Input Shape:", random_input.shape)
    print("5-Channel Output Shape:", output.shape)
```

### Step 5: Incorporating Temporal Dynamics with a 3D Convolutional Autoencoder
For many Earth observation tasks, you might have images collected over multiple time frames. Let’s now build an autoencoder that processes data with 5 channels and 3 time frames. The input shape becomes [batch, channels, time, height, width] or [batch, 5, 3, 28, 28].

By using 3D convolutions, we capture both spatial and temporal patterns:
```
class Conv3DAutoencoder(nn.Module):
    def __init__(self):
        super(Conv3DAutoencoder, self).__init__()
        # Encoder: process 3D input [batch, 5, 3, 28, 28]
        self.encoder = nn.Sequential(
            # Spatial downsampling only; time remains intact
            nn.Conv3d(in_channels=5, out_channels=16, kernel_size=(1, 3, 3), 
                      stride=(1, 2, 2), padding=(0, 1, 1)),  # -> [16, 3, 14, 14]
            nn.ReLU(inplace=True),
            # Process time and space
            nn.Conv3d(in_channels=16, out_channels=32, kernel_size=(3, 3, 3), 
                      stride=(1, 2, 2), padding=(1, 1, 1)),  # -> [32, 3, 7, 7]
            nn.ReLU(inplace=True),
            # Compress time and space into a compact latent space
            nn.Conv3d(in_channels=32, out_channels=64, kernel_size=(3, 3, 3), 
                      stride=(3, 2, 2), padding=(0, 1, 1)),  # -> [64, 1, 4, 4]
            nn.ReLU(inplace=True)
        )
        
        # Decoder: reconstruct the original dimensions
        self.decoder = nn.Sequential(
            nn.ConvTranspose3d(in_channels=64, out_channels=32, kernel_size=(3, 3, 3), 
                               stride=(3, 2, 2), padding=(0, 1, 1)),  # -> [32, 3, 7, 7]
            nn.ReLU(inplace=True),
            nn.ConvTranspose3d(in_channels=32, out_channels=16, kernel_size=(1, 3, 3), 
                               stride=(1, 2, 2), padding=(0, 1, 1), output_padding=(0, 1, 1)),  # -> [16, 3, 14, 14]
            nn.ReLU(inplace=True),
            nn.ConvTranspose3d(in_channels=16, out_channels=5, kernel_size=(1, 3, 3), 
                               stride=(1, 2, 2), padding=(0, 1, 1), output_padding=(0, 1, 1)),  # -> [5, 3, 28, 28]
            nn.Sigmoid()
        )
    
    def forward(self, x):
        x = self.encoder(x)
        x = self.decoder(x)
        return x

if __name__ == "__main__":
    model = Conv3DAutoencoder()
    model.eval()
    random_input = torch.rand(1, 5, 3, 28, 28)
    output = model(random_input)
    print("3D Input Shape (5 channels, 3 time frames):", random_input.shape)
    print("3D Output Shape:", output.shape)
```
## Why Does This Matter for Earth Observation?
Most publicly available pre-trained networks—like those trained on ImageNet—are designed for 3-channel RGB images. This presents a problem for the Earth observation domain, where sensors often capture many more channels (e.g., near-infrared, thermal, etc.) and time series information is vital for monitoring environmental changes. By building autoencoders from scratch, we gain the flexibility to design networks that can process these richer data modalities.

Custom architectures like the one above allow us to leverage the full information content of multi-spectral and multi-temporal data, potentially leading to better performance in tasks such as change detection, land cover classification, and anomaly detection in satellite imagery.

## Conclusion
We started with a basic autoencoder for single-channel images and progressively extended it to handle multi-channel, multi-temporal data using both 2D and 3D convolutions. This step-by-step journey not only demystifies the process of building autoencoders from scratch but also highlights the importance of designing custom models for specialized domains like Earth observation.

As the demand for advanced Earth observation techniques grows, having the ability to build and adapt your own networks becomes invaluable. While pre-trained models for RGB images are abundant, the world of multi-channel data remains ripe for innovation.

Feel free to experiment with these architectures, adjust hyperparameters, and adapt them to your specific datasets. Happy coding, and may your models capture every nuance of our ever-changing Earth!
