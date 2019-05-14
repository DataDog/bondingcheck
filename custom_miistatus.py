# the following try/except block will make the custom check compatible with any Agent version
try:
	# first, try to import the base class from old versions of the Agent...
	from checks import AgentCheck

except ImportError:
	# ...if the above failed, the check is running in Agent version 6 or later
	from datadog_checks.checks import AgentCheck

# content of the special variable __version__ will be shown in the Agent status page
__version__ = "1.2.0"

import os
import subprocess
import argparse

class BondingCheck(AgentCheck):
	def check(self, instance):

		# Specify the platform's bonding directory, get a list of all the bonded interfaces
		# Loop through each bonded interface file to extract mii-status
                ############
                # REMEMBER # to modify the directory below to match your platform's /proc/net/bonding
                ############
		dir = "/home/ubuntu/bonding"
		bonds = os.listdir(dir)

		for bond in bonds:

			# Run the subprocess Python module to read the bonded interface file
			cmd = ['cat', dir+'/%s' % bond]
			output = subprocess.check_output(cmd)

			# Split the output lines
			output_lines = output.split('\n')

			# Assume the slave and bond interfaces are all up
			# Keep track of the slave interfaces
			slave_down = False
			slave_count = 0
			bond_down = False

			# Loop through the output lines to process the status
			for idx, line in enumerate(output_lines):

				# Look for evidence this is a slave interface
				if line.startswith("Slave Interface"):
					slave_count += 1

					# The next line after always has the mii-status value
					# strip all white spaces to avoid Python string check issues
					slave_miistatus_line = output_lines[idx + 1]
					slave_miistatus = slave_miistatus_line.split(":")[1].lstrip().rstrip()

					# If the status is not up, the slave is down, also assume the bond is down
					if 'up' not in slave_miistatus:
						slave_down = True
						# Check if this is the first slave otherwise if the first was up
						# but the second is down, this will incorrectly assume the entire bond
						# is down when checking the second slave. If this is the first slave 
						# then it is okay because if the second slave is up, the else: statement
						# resets this variable to false, meaning the entire bond is still up.
						if slave_count == 1:
							bond_down = True
					# If the status is up, ensure the bond is not considered down
					else:
						bond_down = False

					# Name the metric using the bonded interface name, ex: bond0_slave_down
					# Create a tag as well
					metric = bond + '_slave_down'
					tag = "hostbond:" + bond

					# If the slave is down, generate a metric, add tags and make it a value of 1
					if slave_down:
                                                ###
                                                ### REMEMBER to modify the tag owner:et below to anything desired
                                                ### Use the syntax key:value
                                                ###
						self.gauge(metric, '1', tags=["owner:et", tag])
						self.service_check('BondingCheck', self.WARNING, tags=None, message="")
					# If the slave is up, generate a metric, add tags and make it a value of 0
					else:
                                                ###
                                                ### REMEMBER to modify the tag below owner:et to anything desired
                                                ### Use the syntax key:value
                                                ###
						self.gauge(metric, '0', tags=['owner:et', tag])
						self.service_check('BondingCheck', self.OK, tags=None, message="")

					# The only time the bonded interface is down is if all slaves are down
					# If anye one slave was up, the bond_down value would be False
					# If all slaves really are down, then bond_down is true so generate an event
					# apply tags and make the value a 1 for down or 0 for up
					if bond_down:
						metric = bond + '_down'
                                                ###
                                                ### REMEMBER to modify the tag below owner:et to anything desired
                                                ### Use the syntax key:value
                                                ###
						self.gauge(metric, '1', tags=["owner:et", tag])
					else:
						metric = bond + '_down'
                                                ###
                                                ### REMEMBER to modify the tag below owner:et to anything desired
                                                ### Use the syntax key:value
                                                ###
						self.gauge(metric, '0', tags=["owner:et", tag])
