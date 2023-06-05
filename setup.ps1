function Get-StackOutput {

    param ($StackName,$OutputName)

    $OutputValue = ((aws cloudformation describe-stacks --stack-name "$StackName" |ConvertFrom-Json).Stacks[0].Outputs | Where-Object { $_.OutputKey -eq "$OutputName" }).OutputValue
	return $OutputValue

}
# Create secret manager (storing api key) and s3 bucket (storing lambda code)
aws cloudformation create-stack --stack-name secretmanagerS3 --template-body file://template.yaml --capabilities CAPABILITY_NAMED_IAM --parameters file://api_key.json

aws cloudformation wait stack-create-complete --stack-name secretmanagerS3

$bucketName = Get-StackOutput -StackName secretmanagerS3 -OutputName LambdaBucketName

Write-Host "Bucket name: $bucketName"

Compress-Archive -Path poem-generator.py -DestinationPath poem-generator.zip -Force

# Upload lambda code to s3 bucket
aws s3 cp poem-generator.zip s3://$bucketName

# Create lambda function and lex bot
aws cloudformation create-stack --stack-name poemgenerator --template-body file://poemGenerator.yaml --capabilities CAPABILITY_NAMED_IAM

aws cloudformation wait stack-create-complete --stack-name poemgenerator

Write-Host "poemGenerator stack created successfully"
