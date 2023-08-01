const {getClient, getOriginalImage, processImage, uploadProcessedImage} = require('./s3-image-processing.js')

async function main(){
  client = getClient()
  const srcBucket = process.env.AWS_S3_FOLDER_AVATARS_INPUT
  const srcKey = '/exam tasing.png'
  const dstBucket = process.env.AWS_S3_FOLDER_AVATARS_OUTPUT
  const dstKey = '/exam tasing.png'
  const width = 256
  const height = 256

  const originalImage = await getOriginalImage(client, srcBucket, srcKey)
  console.log(originalImage)
  const processedImage = await processImage(originalImage, width, height)
  await uploadProcessedImage(client, dstBucket, dstKey, processedImage)
}

main()