function Get-StackOutput {

    param ($StackName,$OutputName)

    $OutputValue = ((aws cloudformation describe-stacks --stack-name "$StackName" |ConvertFrom-Json).Stacks[0].Outputs | Where-Object { $_.OutputKey -eq "$OutputName" }).OutputValue
	return $OutputValue

}

# Get the name of the S3 bucket created by the secretmanagerS3 stack
$bucketName = Get-StackOutput -StackName secretmanagerS3 -OutputName LambdaBucketName

# Delete the objects in the S3 bucket
aws s3 rm s3://$bucketName --recursive

# Delete the poemgenerator stack and wait for completion
aws cloudformation delete-stack --stack-name poemgenerator

Write-Host "Deleting poemGenerator stack..."

aws cloudformation wait stack-delete-complete --stack-name poemgenerator

# Delete the secretmanagerS3 stack and wait for completion
aws cloudformation delete-stack --stack-name secretmanagerS3

Write-Host "Deleting secretmanagerS3 stack..."

aws cloudformation wait stack-delete-complete --stack-name secretmanagerS3

Write-Host "Stacks deleted successfully"
