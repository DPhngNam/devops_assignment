#!/usr/bin/env python3
import boto3
import unittest
import os
import json

class EC2TemplateTest(unittest.TestCase):
    """Tests for the EC2 CloudFormation template"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test resources"""
        # This would normally use the stack created by TaskCat
        cls.region = 'us-east-1'
        cls.stack_name = 'taskcat-devops-assignment-ec2-test'
        
        # Initialize CloudFormation and EC2 clients
        cls.cfn = boto3.client('cloudformation', region_name=cls.region)
        cls.ec2 = boto3.client('ec2', region_name=cls.region)
    
    def test_ec2_instances_exist(self):
        """Test that both EC2 instances were created"""
        # Get the stack outputs
        response = self.cfn.describe_stacks(StackName=self.stack_name)
        outputs = {output['OutputKey']: output['OutputValue'] 
                  for output in response['Stacks'][0]['Outputs']}
        
        # Verify instance IDs exist in outputs
        public_instance_id = outputs.get('PublicEC2InstanceId')
        private_instance_id = outputs.get('PrivateEC2InstanceId')
        
        self.assertIsNotNone(public_instance_id, "Public EC2 Instance ID not found")
        self.assertIsNotNone(private_instance_id, "Private EC2 Instance ID not found")
        
        # Verify instances in AWS
        response = self.ec2.describe_instances(
            InstanceIds=[public_instance_id, private_instance_id]
        )
        
        instances = []
        for reservation in response['Reservations']:
            instances.extend(reservation['Instances'])
        
        self.assertEqual(len(instances), 2, "Not all EC2 instances found in AWS")
    
    def test_public_instance_in_public_subnet(self):
        """Test that public instance is in the public subnet"""
        # Get the stack outputs
        response = self.cfn.describe_stacks(StackName=self.stack_name)
        outputs = {output['OutputKey']: output['OutputValue'] 
                  for output in response['Stacks'][0]['Outputs']}
        
        public_instance_id = outputs.get('PublicEC2InstanceId')
        
        # Get instance details
        response = self.ec2.describe_instances(InstanceIds=[public_instance_id])
        instance = response['Reservations'][0]['Instances'][0]
        
        # Get subnet details
        subnet_id = instance['SubnetId']
        subnet_response = self.ec2.describe_subnets(SubnetIds=[subnet_id])
        subnet = subnet_response['Subnets'][0]
        
        # Public subnet should have MapPublicIpOnLaunch set to True
        self.assertTrue(subnet['MapPublicIpOnLaunch'], 
                       "Public instance is not in a public subnet")
        
        # Public instance should have a public IP
        self.assertIn('PublicIpAddress', instance, 
                     "Public instance does not have a public IP address")
    
    def test_private_instance_in_private_subnet(self):
        """Test that private instance is in the private subnet"""
        # Get the stack outputs
        response = self.cfn.describe_stacks(StackName=self.stack_name)
        outputs = {output['OutputKey']: output['OutputValue'] 
                  for output in response['Stacks'][0]['Outputs']}
        
        private_instance_id = outputs.get('PrivateEC2InstanceId')
        
        # Get instance details
        response = self.ec2.describe_instances(InstanceIds=[private_instance_id])
        instance = response['Reservations'][0]['Instances'][0]
        
        # Get subnet details
        subnet_id = instance['SubnetId']
        subnet_response = self.ec2.describe_subnets(SubnetIds=[subnet_id])
        subnet = subnet_response['Subnets'][0]
        
        # Private subnet should have MapPublicIpOnLaunch set to False
        self.assertFalse(subnet['MapPublicIpOnLaunch'], 
                        "Private instance is not in a private subnet")
        
        # Private instance should not have a public IP
        self.assertNotIn('PublicIpAddress', instance, 
                        "Private instance has a public IP address")
    
    def test_instance_security_groups(self):
        """Test that instances have the correct security groups"""
        # Get the stack outputs
        response = self.cfn.describe_stacks(StackName=self.stack_name)
        outputs = {output['OutputKey']: output['OutputValue'] 
                  for output in response['Stacks'][0]['Outputs']}
        
        public_instance_id = outputs.get('PublicEC2InstanceId')
        private_instance_id = outputs.get('PrivateEC2InstanceId')
        
        # Get instance details
        public_response = self.ec2.describe_instances(InstanceIds=[public_instance_id])
        public_instance = public_response['Reservations'][0]['Instances'][0]
        
        private_response = self.ec2.describe_instances(InstanceIds=[private_instance_id])
        private_instance = private_response['Reservations'][0]['Instances'][0]
        
        # Check security groups
        public_sg_ids = [sg['GroupId'] for sg in public_instance['SecurityGroups']]
        private_sg_ids = [sg['GroupId'] for sg in private_instance['SecurityGroups']]
        
        # Verify against expected security group IDs from stack outputs
        expected_public_sg = outputs.get('PublicEC2SecurityGroupId')
        expected_private_sg = outputs.get('PrivateEC2SecurityGroupId')
        
        self.assertIn(expected_public_sg, public_sg_ids, 
                     "Public instance does not have the correct security group")
        self.assertIn(expected_private_sg, private_sg_ids, 
                     "Private instance does not have the correct security group")

if __name__ == '__main__':
    unittest.main()
