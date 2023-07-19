import * as cdk from 'aws-cdk-lib';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as s3n from 'aws-cdk-lib/aws-s3-notifications';
import * as sns from 'aws-cdk-lib/aws-sns';
import * as subscriptions from 'aws-cdk-lib/aws-sns-subscriptions';
import { Construct } from 'constructs';
import * as dotenv from 'dotenv'

// load env variables
// const dotenv = require('dotenv')
dotenv.config();

export class ServerlessCdkStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // The code that defines your stack goes here
    const dotenv = require('dotenv');
    dotenv.config();

    const uploadsBucketName: string = process.env.AVATARS_UPLOAD_BUCKET_NAME as string;
    const processedBucketName: string = process.env.AVATARS_PROCESSED_BUCKET_NAME as string;
    const folderInput: string = process.env.AVATARS_S3_FOLDER_INPUT as string;
    const folderOutput: string = process.env.AVATARS_S3_FOLDER_OUTPUT as string;
    const webhookUrl: string = process.env.AVATARS_WEBHOOK_URL as string;
    const topicName: string = process.env.AVATARS_TOPIC_NAME as string;
    const functionPath: string = process.env.AVATARS_FUNCTION_PATH as string;
    console.log('uploadsBucketName', uploadsBucketName);
    console.log('processedBucketName', processedBucketName);
    console.log('folderInput', folderInput);
    console.log('folderOutput', folderOutput);
    console.log('webhookUrl', webhookUrl);
    console.log('topicName', topicName);
    console.log('functionPath', functionPath);

    const uploadsBucket = this.createBucket(uploadsBucketName);
    const processedBucket = this.importBucket(processedBucketName);
    // createLambda(functionPath: string, bucketName: string, folderInput: string, folderOutput: string)
    // const lambda = this.createLambda(folderInput, folderOutput, functionPath, bucketName)
    const lambda = this.createLambda(
      functionPath,
      uploadsBucketName,
      processedBucketName,
      folderInput,
      folderOutput
    );

    // create SNS topic and subscriptions
    const snsTopic = this.createSnsTopic(topicName);
    this.createSnsSubscription(snsTopic, webhookUrl);
    // We don't need to attach the policy to Lambda because it is not Lambda that pushes to SNS. 
    // const snsPublishPolicy = this.createPolicySnSPublish(snsTopic.topicArn)
    // lambda.addToRolePolicy(snsPublishPolicy);

    // add trigger and destination
    // Send notifications to SNS and Lambda
    this.createS3NotifyToSns(folderInput, snsTopic, uploadsBucket);
    this.createS3NotifyToLambda(folderInput, lambda, processedBucket);

    // create policies
    const s3UploadsReadWritePolicy = this.createPolicyBucketAccess(uploadsBucket.bucketArn);
    const s3ProcessedReadWritePolicy = this.createPolicyBucketAccess(processedBucket.bucketArn);
    
    // attach policies for permissions
    lambda.addToRolePolicy(s3UploadsReadWritePolicy);
    lambda.addToRolePolicy(s3ProcessedReadWritePolicy);
  }

  createBucket(bucketName: string): s3.IBucket {
    const bucket = new s3.Bucket(this, 'UploadsBucket', {
      bucketName: bucketName,
      removalPolicy: cdk.RemovalPolicy.DESTROY
    });
    return bucket;
  }

  importBucket(bucketName: string): s3.IBucket {
    // new is not needed as we are calling a static function.
    const bucket = s3.Bucket.fromBucketName(this, "ProcessedBucket", bucketName); 
    return bucket;
  }

  // we no longer need uploadsBucketName as an argument 
  // because its information will be passed into the function.
  createLambda(functionPath: string, uploadsBucketName: string, processedBucketName: string, folderInput: string, folderOutput: string): lambda.IFunction {
    const lambdaFunction = new lambda.Function(this, 'ImageProcessingLambda', {
      runtime: lambda.Runtime.NODEJS_18_X,
      handler: 'index.handler',
      code: lambda.Code.fromAsset(functionPath),
      environment: {
        DEST_BUCKET_NAME: processedBucketName,
        FOLDER_INPUT: uploadsBucketName,
        FOLDER_OUTPUT: processedBucketName,
        PROCESS_WIDTH: '512',
        PROCESS_HEIGHT: '512'
      }
    });
    return lambdaFunction;
  }

  createS3NotifyToLambda(prefix: string, lambda: lambda.IFunction, bucket: s3.IBucket): void {
    const destination = new s3n.LambdaDestination(lambda);
    bucket.addEventNotification(s3.EventType.OBJECT_CREATED_PUT,
      destination,
      {prefix: prefix} // folder to contain the original images
    )
  }

  createPolicyBucketAccess(bucketArn: string) {
    const s3ReadWritePolicy = new iam.PolicyStatement({
      actions: [
        's3:GetObject',
        's3:PutObject'
      ],
      resources: [
        `${bucketArn}/*`,
      ]
    });
    return s3ReadWritePolicy
  }

  createSnsTopic(topicName: string): sns.ITopic{
    const logicalName = "Topic";
    const snsTopic = new sns.Topic(this, logicalName, {
      topicName: topicName
    });
    return snsTopic;
  }

  createSnsSubscription(snsTopic: sns.ITopic, webhookUrl: string): sns.Subscription {
    const snsSubscription = snsTopic.addSubscription(
      new subscriptions.UrlSubscription(webhookUrl)
    )
    return snsSubscription;
  }

  createS3NotifyToSns(prefix: string, snsTopic: sns.ITopic, bucket: s3.IBucket): void {
    const destination = new s3n.SnsDestination(snsTopic)
    bucket.addEventNotification(
      s3.EventType.OBJECT_CREATED_PUT, 
      destination,
      {prefix: prefix}
    );  
  }

  createPolicySnSPublish(topicArn: string) {
    const snsPublishPolicy = new iam.PolicyStatement({
      actions: [ 'sns:Publish', ],
      resources: [ topicArn ]
    });
    return snsPublishPolicy;
  }
}