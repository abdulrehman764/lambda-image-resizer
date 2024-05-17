# S3 Image Resizer

This AWS Lambda function processes uploaded images in an S3 bucket, resizes them if they exceed a certain size threshold, and updates the environment variable with the name of the last processed image to avoid redundant processing.

## Functionality

Upon receiving an S3 event trigger, the function performs the following tasks:

1. **Check if the uploaded image is the same as the last processed image:**
    - If it's the same, the function exits.
    - If it's a new image, the process continues.

2. **Download the image from S3:**
    - Fetch the image bytes from the specified S3 bucket.

3. **Check image size:**
    - If the image size is greater than 200KB, continue resizing.
    - Otherwise, skip resizing.

4. **Resize the image:**
    - Open the image using the Python Imaging Library (PIL).
    - Resize the image to 1200x1200 pixels using Lanczos resampling.

5. **Save the resized image:**
    - Save the resized image to a BytesIO object with reduced quality to minimize storage usage.

6. **Upload the resized image:**
    - Replace the original image in the same S3 bucket with the resized image.

## Environment Variable

The function utilizes an environment variable `LAST_PROCESSED_IMAGE` to store the name of the last processed image. This ensures that redundant processing is avoided if the same image is uploaded multiple times.

## Usage

To deploy and utilize this function:

1. **Configure AWS Lambda:**
    - Create a new Lambda function in the AWS Management Console.
    - Set the runtime to Python 3.8 or later.
    - Configure the function with appropriate permissions to access S3.

2. **Set up S3 trigger:**
    - Add an S3 trigger to the Lambda function, specifying the bucket and event type (e.g., ObjectCreated).

3. **Environment Variable:**
    - Define an environment variable `LAST_PROCESSED_IMAGE` in the Lambda configuration.

4. **Deploy the function:**
    - Copy the function code into the Lambda function editor or package it as a deployment package.

5. **Test the function:**
    - Upload images to the specified S3 bucket and observe the resizing process.

