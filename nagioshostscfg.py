from boto import ec2
import os
import jinja2

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

ec2conn = ec2.connection.EC2Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
reservations = ec2conn.get_all_instances()
instances = [i for r in reservations for i in r.instances]
for i in instances:
        if i.private_ip_address is None: 
            pass
        else: 

            inst_nm = i.tags['Name'].encode('utf-8')
            inst_ip = i.private_ip_address.encode('utf-8')
            inst_rl = i.tags['Role'].encode('utf-8')
            env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath='templates/'))
            template = env.get_template('hosts.cfg.j2')
            display_dict = {'instances': (instances), 'inst_nm': (inst_nm), 'inst_ip': (inst_ip), 'inst_rl': (inst_rl)}
            print template.render(display_dict)
