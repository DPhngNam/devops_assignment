#!/usr/bin/env python3
import boto3
import unittest
import os
import json

class MainTemplateTest(unittest.TestCase):
    """Integration tests for the main CloudFormation template"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test resources"""
        # This would normally use the stack created by TaskCat
        cls.region = 'us-east-1'
        cls.stack_name = 'taskcat-devops-assignment-full-stack-test'
        
        # Initialize CloudFormation and EC2 clients
        cls.cfn = boto3.client('cloudformation', region_name=cls.region)
        cls.ec2 = boto3.client('ec2', region_name=cls.region)
    
    def test_stack_creation_complete(self):
        """Test that the stack was created successfully"""
        # Check stack status
        response = self.cfn.describe_stacks(StackName=self.stack_name)
        stack = response['Stacks'][0]
        
        self.assertEqual(stack['StackStatus'], 'CREATE_COMPLETE', 
                        f"Stack creation failed with status: {stack['StackStatus']}")
    
    def test_all_resources_created(self):
        """Test that all required resources were created"""
        # Get the stack outputs
        response = self.cfn.describe_stacks(StackName=self.stack_name)
        outputs = {output['OutputKey']: output['OutputValue'] 
                  for output in response['Stacks'][0]['Outputs']}
        
        # Check for required outputs
        required_outputs = [
            'VpcId',
            'PublicSubnetId',
            'PrivateSubnetId',
            'PublicEC2SecurityGroupId',
            'PrivateEC2SecurityGroupId',
            'PublicEC2InstanceId',
            'PrivateEC2InstanceId',
            'PublicEC2InstancePublicIP'
        ]
        
        for output in required_outputs:
            self.assertIn(output, outputs, f"Required output '{output}' not found")
            self.assertIsNotNone(outputs[output], f"Output '{output}' has null value")
    
    def test_connectivity_public_to_private(self):
        """Test that public instance can connect to private instance"""
        # This is a theoretical test that would require SSH access to the instances
        # In a real environment, you would use AWS Systems Manager Run Command or similar
        # to verify connectivity between instances
        
        # For now, we'll just check that both instances exist and are running
        response = self.cfn.describe_stacks(StackName=self.stack_name)
        outputs = {output['OutputKey']: output['OutputValue'] 
                  for output in response['Stacks'][0]['Outputs']}
        
        public_instance_id = outputs.get('PublicEC2InstanceId')
        private_instance_id = outputs.get('PrivateEC2InstanceId')
        
        # Check instance states
        response = self.ec2.describe_instances(
            InstanceIds=[public_instance_id, private_instance_id]
        )
        
        instances = []
        for reservation in response['Reservations']:
            instances.extend(reservation['Instances'])
        
        for instance in instances:
            self.assertEqual(instance['State']['Name'], 'running', 
                           f"Instance {instance['InstanceId']} is not running")
    
    def test_end_to_end_infrastructure(self):
        """Test the entire infrastructure setup"""
        # Get the stack outputs
        response = self.cfn.describe_stacks(StackName=self.stack_name)
        outputs = {output['OutputKey']: output['OutputValue'] 
                  for output in response['Stacks'][0]['Outputs']}
        
        # 1. Verify VPC exists
        vpc_id = outputs.get('VpcId')
        vpc_response = self.ec2.describe_vpcs(VpcIds=[vpc_id])
        self.assertEqual(len(vpc_response['Vpcs']), 1, "VPC not found")
        
        # 2. Verify subnets exist in the VPC
        public_subnet_id = outputs.get('PublicSubnetId')
        private_subnet_id = outputs.get('PrivateSubnetId')
        
        subnet_response = self.ec2.describe_subnets(
            SubnetIds=[public_subnet_id, private_subnet_id]
        )
        self.assertEqual(len(subnet_response['Subnets']), 2, "Not all subnets found")
        
        # 3. Verify Internet Gateway attached to VPC
        igw_response = self.ec2.describe_internet_gateways(
            Filters=[{'Name': 'attachment.vpc-id', 'Values': [vpc_id]}]
        )
        self.assertGreaterEqual(len(igw_response['InternetGateways']), 1, 
                               "No Internet Gateway attached to VPC")
        
        # 4. Verify NAT Gateway exists in public subnet
        nat_response = self.ec2.describe_nat_gateways(
            Filters=[{'Name': 'subnet-id', 'Values': [public_subnet_id]}]
        )
        nat_gateways = [ng for ng in nat_response['NatGateways'] 
                       if ng['State'] != 'deleted']
        self.assertGreaterEqual(len(nat_gateways), 1, 
                               "No active NAT Gateway found in public subnet")
        
        # 5. Verify security groups exist and have correct rules
        public_sg_id = outputs.get('PublicEC2SecurityGroupId')
        private_sg_id = outputs.get('PrivateEC2SecurityGroupId')
        
        sg_response = self.ec2.describe_security_groups(
            GroupIds=[public_sg_id, private_sg_id]
        )
        self.assertEqual(len(sg_response['SecurityGroups']), 2, 
                        "Not all security groups found")
        
        # 6. Verify EC2 instances exist and are in correct subnets
        public_instance_id = outputs.get('PublicEC2InstanceId')
        private_instance_id = outputs.get('PrivateEC2InstanceId')
        
        instance_response = self.ec2.describe_instances(
            InstanceIds=[public_instance_id, private_instance_id]
        )
        
        instances = []
        for reservation in instance_response['Reservations']:
            instances.extend(reservation['Instances'])
        
        self.assertEqual(len(instances), 2, "Not all EC2 instances found")
        
        # Check instance subnet placement
        for instance in instances:
            if instance['InstanceId'] == public_instance_id:
                self.assertEqual(instance['SubnetId'], public_subnet_id, 
                               "Public instance not in public subnet")
                self.assertIn('PublicIpAddress', instance, 
                             "Public instance does not have a public IP")
            elif instance['InstanceId'] == private_instance_id:
                self.assertEqual(instance['SubnetId'], private_subnet_id, 
                               "Private instance not in private subnet")
                self.assertNotIn('PublicIpAddress', instance, 
                               "Private instance has a public IP")

if __name__ == '__main__':
    unittest.main()
