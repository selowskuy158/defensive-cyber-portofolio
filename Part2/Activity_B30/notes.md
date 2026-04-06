# B30 - Generate an AI-Created Image, Apply Watermark, and Test Detection

**Date:** 19 April, 2026

## Summary
This activity involves generating an AI-created image, applying an imperceptible watermark to it, and then performing an image-to-image reproduction or editing process to test whether the watermark is still detectable. The purpose is to understand how watermarking technology can be used to identify AI-generated content and whether such watermarks can survive common image manipulations.

## Steps Taken

### Step 1: Generating the AI Image
I used an online AI image generation tool to create a realistic looking image of a fictional cybersecurity professional working at a computer in an office. The generated image looked very realistic and could easily be mistaken for a real photograph if someone was not looking carefully. This demonstrates the quality of modern AI image generators and why watermarking is important to help people identify AI-generated content.

### Step 2: Applying a Watermark
I used a steganography technique to embed an invisible watermark into the image. I wrote a Python script using the Pillow library that modifies the least significant bits (LSB) of the pixel values in the image to encode a hidden message. The watermark text I encoded was "AI-GENERATED-CITS2006-2026" which cannot be seen by the human eye but can be detected by a program that knows where to look. The visual quality of the image was not affected at all by the watermark because only the least significant bits of the pixel values were changed, which produces a change so small that it is invisible to the human eye.

### Step 3: Testing Watermark Detection
After applying the watermark, I ran my detection script on the watermarked image and it successfully extracted the hidden message, confirming that the watermark was properly embedded. I then tested whether the watermark survived common image manipulations.

#### Test 1: JPEG Compression
I saved the watermarked image as a JPEG file with different compression levels. At high quality compression (90%), the watermark was still partially detectable. At medium quality (70%), the watermark was degraded and only fragments could be recovered. At low quality (50%), the watermark was completely destroyed.

#### Test 2: Screenshot and Re-upload
I took a screenshot of the watermarked image and ran the detection script on the screenshot. The watermark was completely undetectable in the screenshot because the screenshot process resamples the pixels and destroys the LSB data.

#### Test 3: Cropping and Resizing
I cropped the image to remove 20% from each edge and resized it. The watermark in the remaining area was partially detectable but degraded.

### Conclusion
The LSB watermarking technique is relatively easy to implement but is fragile against common image manipulations like compression, screenshotting, and resizing. More robust watermarking methods like those used by companies such as Google DeepMind (SynthID) use deep learning to embed watermarks that survive more aggressive transformations. This activity showed me that while watermarking is a promising approach for detecting AI-generated content, the technology still needs to improve to be reliable in real-world scenarios where images are commonly shared, compressed, and modified across different platforms.
