import boto3
import requests
import os

ec2 = boto3.resource('ec2',region_name='ap-southeast-1' )
sg = ec2.SecurityGroup('sg-85edd1e0')
# To know about the ec2 instance
# Aws ec2 describe-instances --filters "Name=tag:Name,Values=Telemetry-API" (use tags for filter )
# Aws ec2 describe-security-groups --filters GroupId=sg-66b3a71b  (add groupID )
os.system('touch ~/.newip ~/.oldip')
sh = requests.get('http://ip.42.pl/raw').text + "/32"
op = open('/root/.newip', 'r+')
op.write(sh)
op.close()

with open('/root/.oldip', 'r') as f:
    if(os.stat("/root/.oldip").st_size == 0):
      sg.authorize_ingress(DryRun=False,IpPermissions=[{'FromPort': 22,'ToPort': 22,'IpProtocol': 'tcp','IpRanges': [{'CidrIp': (sh),'Description': 'mention your purpose'},],},],)
      os.system('mv ~/.newip ~/.oldip')
    else:
      for line in f:
            if(sh == ''):
              print("no ip found")
            elif(sh != line):
              print(line.strip())
              sg.revoke_ingress(IpPermissions=[{'IpProtocol': 'tcp','FromPort': 22,'ToPort': 22,'IpRanges': [{'CidrIp': (line.strip()) },],},])
              sg.authorize_ingress(IpPermissions=[{'IpProtocol': 'tcp','FromPort': 22,'ToPort': 22,'IpRanges': [{'CidrIp': (sh)}]}])
              os.system('mv ~/.newip ~/.oldip')
            elif(sh == line):
              print("same Ip")


