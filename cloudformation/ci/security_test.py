#!/usr/bin/env python3
import boto3
import unittest
import os
import json

class SecurityTemplateTest(unittest.TestCase):
    """Tests for the Security Groups CloudFormation template"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test resources"""
        # This would normally use the stack created by TaskCat
        cls.region = 'us-east-1'
        cls.stack_name = 'taskcat-devops-assignment-security-test'
        
        # Initialize CloudFormation and EC2 clients
        cls.cfn = boto3.client('cloudformation', region_name=cls.region)
        cls.ec2 = boto3.client('ec2', region_name=cls.region)
    
    def test_security_groups_exist(self):
        """Test that both security groups were created"""
        # Get the stack outputs
        response = self.cfn.describe_stacks(StackName=self.stack_name)
        outputs = {output['OutputKey']: output['OutputValue'] 
                  for output in response['Stacks'][0]['Outputs']}
        
        # Verify security group IDs exist in outputs
        public_sg_id = outputs.get('PublicEC2SecurityGroupId')
        private_sg_id = outputs.get('PrivateEC2SecurityGroupId')
        
        self.assertIsNotNone(public_sg_id, "Public Security Group ID not found")
        self.assertIsNotNone(private_sg_id, "Private Security Group ID not found")
        
        # Verify security groups in AWS
        response = self.ec2.describe_security_groups(
            GroupIds=[public_sg_id, private_sg_id]
        )
        self.assertEqual(len(response['SecurityGroups']), 2, "Not all security groups found in AWS")
    
    def test_public_security_group_rules(self):
        """Test that public security group has correct rules"""
        # Get the public security group ID from stack outputs
        response = self.cfn.describe_stacks(StackName=self.stack_name)
        outputs = {output['OutputKey']: output['OutputValue'] 
                  for output in response['Stacks'][0]['Outputs']}
        public_sg_id = outputs.get('PublicEC2SecurityGroupId')
        
        # Get security group details
        response = self.ec2.describe_security_groups(GroupIds=[public_sg_id])
        sg = response['SecurityGroups'][0]
        
        # Check ingress rules - should allow SSH from specified IP
        has_ssh_rule = False
        for rule in sg['IpPermissions']:
            if rule.get('IpProtocol') == 'tcp' and rule.get('FromPort') == 22 and rule.get('ToPort') == 22:
                has_ssh_rule = True
                break
        
        self.assertTrue(has_ssh_rule, "Public security group missing SSH ingress rule")
        
        # Check egress rules - should allow all outbound traffic
        has_all_egress = False
        for rule in sg['IpPermissionsEgress']:
            if rule.get('IpProtocol') == '-1':
                has_all_egress = True
                break
        
        self.assertTrue(has_all_egress, "Public security group missing all traffic egress rule")
    
    def test_private_security_group_rules(self):
        """Test that private security group has correct rules"""
        # Get the security group IDs from stack outputs
        response = self.cfn.describe_stacks(StackName=self.stack_name)
        outputs = {output['OutputKey']: output['OutputValue'] 
                  for output in response['Stacks'][0]['Outputs']}
        private_sg_id = outputs.get('PrivateEC2SecurityGroupId')
        public_sg_id = outputs.get('PublicEC2SecurityGroupId')
        
        # Get security group details
        response = self.ec2.describe_security_groups(GroupIds=[private_sg_id])
        sg = response['SecurityGroups'][0]
        
        # Check ingress rules - should allow SSH from public security group
        has_ssh_from_public = False
        for rule in sg['IpPermissions']:
            if rule.get('IpProtocol') == 'tcp' and rule.get('FromPort') == 22 and rule.get('ToPort') == 22:
                for source in rule.get('UserIdGroupPairs', []):
                    if source.get('GroupId') == public_sg_id:
                        has_ssh_from_public = True
                        break
        
        self.assertTrue(has_ssh_from_public, "Private security group missing SSH ingress rule from public security group")
        
        # Check egress rules - should allow all outbound traffic
        has_all_egress = False
        for rule in sg['IpPermissionsEgress']:
            if rule.get('IpProtocol') == '-1':
                has_all_egress = True
                break
        
        self.assertTrue(has_all_egress, "Private security group missing all traffic egress rule")

if __name__ == '__main__':
    unittest.main()
