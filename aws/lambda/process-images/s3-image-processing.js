const sharp = require('sharp');
const { S3Client, PutObjectCommand, GetObjectCommand } = require("@aws-sdk/client-s3");

function getClient(){
  const client = new S3Client();
  return client;
}

async function getOriginalImage(client, srcBucket, srcKey){
  console.log('get ========================')
  const params = {
    Bucket: srcBucket,
    Key: srcKey
  };
  console.log('params', params)
  const command = new GetObjectCommand(params);
  console.log('command: ', command)
  const response = await client.send(command);
  console.log('response: ', response)

  const chunks = [];
  for await (const chunk of response.Body) {
    chunks.push(chunk);
  }
  console.log('chunks: ', chunks)
  const buffer = Buffer.concat(chunks);
  console.log('buffer: ', buffer)
  return buffer;
}

async function processImage(image, width, height){
  const processedImage = await sharp(image)
    .resize(width, height)
    .jpeg()
    .toBuffer();
  return processedImage;
}

async function uploadProcessedImage(client, dstBucket, dstKey, image){
  console.log('upload ========================')
  const params = {
    Bucket: dstBucket,
    Key: dstKey,
    Body: image,
    ContentType: 'image/jpeg'
  };
  console.log('params', params) 
  const command = new PutObjectCommand(params);
  const response = await client.send(command);
  console.log('repsonse', response);
  return response;
}

module.exports = {
  getClient: getClient,
  getOriginalImage: getOriginalImage,
  processImage: processImage,
  uploadProcessedImage: uploadProcessedImage
}