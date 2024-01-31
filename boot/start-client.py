import subprocess

cmd = "ssh -f -N -L localhost:9090:localhost:9090 node1"
subprocess.run(cmd, shell=True)
