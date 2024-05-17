import os
import boto3
from PIL import Image
from io import BytesIO

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Get the bucket and object key from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    # Check if the uploaded image is the same as the last processed image
    last_processed_image = os.getenv('LAST_PROCESSED_IMAGE')
    if last_processed_image == key:
        return {
            'statusCode': 200,
            'body': 'Image already processed. Exiting...'
        }
    
    # Download the image from S3
    response = s3.get_object(Bucket=bucket, Key=key)
    image_bytes = response['Body'].read()
    
    print("Size of Image: ", len(image_bytes))

    # Check if image size is greater than 200KB
    if len(image_bytes) > 200 * 1024:
        # Copy the original image to a new S3 bucket
        output_bucket = 'copy-original-daycare-s3-images'
        s3.copy_object(
            Bucket=output_bucket,
            Key=key,
            CopySource={'Bucket': bucket, 'Key': key}
        )
        
        # Update the environment variable with the name of the last processed image
        os.environ['LAST_PROCESSED_IMAGE'] = key
        print("ENV: ", os.environ['LAST_PROCESSED_IMAGE'])
        # Open the image using PIL
        image = Image.open(BytesIO(image_bytes))
        
        # Resize the image
        resized_image = image.resize((1200, 1200), Image.LANCZOS)
        
        image_format = image.format
        # Save the resized image to a BytesIO object
        output_image = BytesIO()
        resized_image.save(output_image, format=image_format, quality=50)
        output_image.seek(0)
        
        # Upload the resized image to the original bucket, replacing the original image
        s3.put_object(Bucket=bucket, Key=key, Body=output_image)
        

        
        return {
            'statusCode': 200,
            'body': 'Image resized and uploaded successfully!'
        }
    else:
        print(f"Image {key} is less than 200KB. Skipping resize.")
        return
