import os

def runJmeterFromBars(script_name, key):
    os.system(f"sudo rm -f temp/{key}")
    command = f"sudo /opt/jmeter/bin/jmeter -n -t /var/www/ovirtmedicinovich/conf/jmeter_profiles/local_profiles/{script_name}"
    os.system(command)