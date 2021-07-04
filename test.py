import subprocess
test = subprocess.Popen(["adb","devices"], stdout=subprocess.PIPE)
output = str(test.communicate()[0])

print(output.split('attached\\n')[1].split('\\tdevice')[0])
