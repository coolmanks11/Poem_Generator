% Cloud Architecture CA2

**Weight:** 20%

**Deadline:** as displayed on Moodle

# Introduction

The aim of this CA is to show that you can employ a number of cloud services to perform a simple task. 
It is *not* necessary to construct an enterprise-grade solution!

# Deliverables

In a single ZIP file named CA2 you must submit: 

aim.txt:
	What is your solution designed to do?
	Approx 4-5 bullet points.
	
template.yaml:
	Your system architecture.
	
setup.ps1 / setup.py file: 
	Should create instance of your template.
	And do any other setup tasks (e.g. copying files)

Other files as appropriate.
	
# Grading

## Aim (10%)

Basic aim of your system explained in 4-5 bullet points. 

## Basic Architecture (30%)

Assessed from cloudformation template + items created in Setup file.
To maximise marks:
- Create as much as possible in CloudFormation rather than code.
- Use CloudFormation features rather than hard-coding
- Use Input Parameters and Outputs as appropriate to provide information. 


## Chatbot or Web frontend (20%)

Provide a chatbot that provides input to your system using AWS Lex. 
The Lambda code may be in separate files or in the CloudFormation template.


## Permissions (10%)

Permissions necessary for services to interact.
To maximise marks you should restrict to necessary operations and source/target resources. 


## New service usage (30%)

Utilise at least 2 services. 


# Demonstration

Demonstration will be required after the submission date.
Schedule will be announced closer to the time.
