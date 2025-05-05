#!/usr/bin/env python3
import boto3
import unittest
import os
import json
import time

class VpcTemplateTest(unittest.TestCase):
    """Tests for the VPC CloudFormation template"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test resources"""
        # This would normally use the stack created by TaskCat
        # For demonstration purposes, we're showing how you would test
        cls.region = 'us-east-1'
        cls.stack_name = 'taskcat-devops-assignment-vpc-test'
        
        # Initialize CloudFormation client
        cls.cfn = boto3.client('cloudformation', region_name=cls.region)
        cls.ec2 = boto3.client('ec2', region_name=cls.region)
    
    def test_vpc_exists(self):
        """Test that the VPC was created successfully"""
        # Get the stack outputs
        response = self.cfn.describe_stacks(StackName=self.stack_name)
        outputs = {output['OutputKey']: output['OutputValue'] 
                  for output in response['Stacks'][0]['Outputs']}
        
        # Verify VPC exists
        vpc_id = outputs.get('VpcId')
        self.assertIsNotNone(vpc_id, "VPC ID not found in stack outputs")
        
        # Verify VPC in AWS
        response = self.ec2.describe_vpcs(VpcIds=[vpc_id])
        self.assertEqual(len(response['Vpcs']), 1, "VPC not found in AWS")
    
    def test_subnets_exist(self):
        """Test that public and private subnets were created"""
        # Get the stack outputs
        response = self.cfn.describe_stacks(StackName=self.stack_name)
        outputs = {output['OutputKey']: output['OutputValue'] 
                  for output in response['Stacks'][0]['Outputs']}
        
        # Verify subnet IDs exist in outputs
        public_subnet_id = outputs.get('PublicSubnetId')
        private_subnet_id = outputs.get('PrivateSubnetId')
        
        self.assertIsNotNone(public_subnet_id, "Public Subnet ID not found")
        self.assertIsNotNone(private_subnet_id, "Private Subnet ID not found")
        
        # Verify subnets in AWS
        response = self.ec2.describe_subnets(
            SubnetIds=[public_subnet_id, private_subnet_id]
        )
        self.assertEqual(len(response['Subnets']), 2, "Not all subnets found in AWS")
    
    def test_internet_gateway_exists(self):
        """Test that the Internet Gateway was created and attached to VPC"""
        # Get the VPC ID from stack outputs
        response = self.cfn.describe_stacks(StackName=self.stack_name)
        outputs = {output['OutputKey']: output['OutputValue'] 
                  for output in response['Stacks'][0]['Outputs']}
        vpc_id = outputs.get('VpcId')
        
        # Get Internet Gateways attached to the VPC
        response = self.ec2.describe_internet_gateways(
            Filters=[{'Name': 'attachment.vpc-id', 'Values': [vpc_id]}]
        )
        
        self.assertGreaterEqual(len(response['InternetGateways']), 1, 
                               "No Internet Gateway attached to VPC")

    def test_nat_gateway_exists(self):
        """Test that the NAT Gateway was created in the public subnet"""
        # Get the public subnet ID from stack outputs
        response = self.cfn.describe_stacks(StackName=self.stack_name)
        outputs = {output['OutputKey']: output['OutputValue'] 
                  for output in response['Stacks'][0]['Outputs']}
        public_subnet_id = outputs.get('PublicSubnetId')
        
        # Get NAT Gateways in the public subnet
        response = self.ec2.describe_nat_gateways(
            Filters=[{'Name': 'subnet-id', 'Values': [public_subnet_id]}]
        )
        
        # Check that at least one NAT Gateway exists in the public subnet
        nat_gateways = [ng for ng in response['NatGateways'] 
                        if ng['State'] != 'deleted']
        self.assertGreaterEqual(len(nat_gateways), 1, 
                               "No active NAT Gateway found in public subnet")

    def test_route_tables(self):
        """Test that route tables were created with correct routes"""
        # Get the VPC ID from stack outputs
        response = self.cfn.describe_stacks(StackName=self.stack_name)
        outputs = {output['OutputKey']: output['OutputValue'] 
                  for output in response['Stacks'][0]['Outputs']}
        vpc_id = outputs.get('VpcId')
        
        # Get route tables for the VPC
        response = self.ec2.describe_route_tables(
            Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}]
        )
        
        # Should have at least 2 route tables (public and private)
        self.assertGreaterEqual(len(response['RouteTables']), 2, 
                               "Not enough route tables found for VPC")
        
        # Check for internet gateway route in at least one route table
        internet_routes = 0
        nat_routes = 0
        
        for rt in response['RouteTables']:
            for route in rt['Routes']:
                if route.get('GatewayId', '').startswith('igw-'):
                    internet_routes += 1
                if route.get('NatGatewayId', '').startswith('nat-'):
                    nat_routes += 1
        
        self.assertGreaterEqual(internet_routes, 1, 
                               "No route with Internet Gateway found")
        self.assertGreaterEqual(nat_routes, 1, 
                               "No route with NAT Gateway found")

if __name__ == '__main__':
    unittest.main()
