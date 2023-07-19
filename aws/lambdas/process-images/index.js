const { getClient, getOriginalImage, processImage, uploadProcessedImage } = require('./s3-image-processing.js');
const path = require('path');
const process = require('process');

const uploadsBucketName = process.env.AVATARS_UPLOAD_BUCKET_NAME
const processedBucketName = process.env.AVATARS_PROCESSED_BUCKET_NAME
const folderInput = process.env.AVATARS_S3_FOLDER_INPUT
const folderOutput = process.env.AVATARS_S3_FOLDER_OUTPUT
const width = parseInt(process.env.PROCESS_WIDTH)
const height = parseInt(process.env.PROCESS_HEIGHT)

client = getClient();

exports.handler = async (event) => {    
    console.log('event', event)

    // Get original image
    const srcBucket = event.Records[0].s3.bucket.name;
    const srcKey = decodeURIComponent(event.Records[0].s3.object.key.replace(/\+/g, ' '));
    const originalImage = await getOriginalImage(client, srcBucket, srcKey)
    console.log('index.handler.srcBucket', srcBucket)
    console.log('index.handler.srcKey', srcKey)

    // Process image
    const processedImage = await processImage(originalImage, width, height)

    // Upload processed image
    filename = path.parse(srcKey).name;
    const dstBucket = srcBucket.replace("uploads", "avatars");
    const dstKey =  `${filename}.jpg`;
    await uploadProcessedImage(client, dstBucket, dstKey, processedImage);
    console.log('index.handler.dstBucket', dstBucket)
    console.log('index.handler.dstKey', dstKey)
};