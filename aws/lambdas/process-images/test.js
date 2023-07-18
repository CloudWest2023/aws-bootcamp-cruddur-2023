const {getClient, getOriginalImage, processImage, uploadProcessedImage} = require('./s3-image-processing.js')

async function main(){
  client = getClient()
  const srcBucket = process.env.ASSETS_S3_FOLDER_INPUT
  const srcKey = 'avatar/original/data.jpg'
  const dstBucket = process.env.ASSETS_S3_FOLDER_OUTPUT
  const dstKey = 'avatar/processed/data.png'
  const width = 256
  const height = 256

  const originalImage = await getOriginalImage(client, srcBucket, srcKey)
  console.log(originalImage)
  const processedImage = await processImage(originalImage, width, height)
  await uploadProcessedImage(client, dstBucket, dstKey, processedImage)
}

main()