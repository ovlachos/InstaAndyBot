import subprocess

username = 'lentotheeye'
devices = [
    {
        'name': 'LGV5005ed279c7',
        'lowerScreenBound': 1700,
        'upperScreenBound': 280,
    },
    {
        'name': '08021b480705',
        'lowerScreenBound': 1960,
        'upperScreenBound': 260,
    },
]


def getDeviceName():
    test = subprocess.Popen(["adb", "devices"], stdout=subprocess.PIPE)
    output = str(test.communicate()[0])
    deviceName = output.split('attached\\n')[1].split('\\tdevice')[0]

    # output_size, output_density = getScreenSizeAndSensity()
    # print(f"Device {deviceName} with {output_size} and {output_density}")
    return deviceName


def getScreenSizeAndSensity():
    size = subprocess.Popen(["adb shell wm", "size"], stdout=subprocess.PIPE)
    density = subprocess.Popen(["adb shell wm", "density"], stdout=subprocess.PIPE)
    output_size = str(size.communicate()[0])
    output_density = str(density.communicate()[0])

    return output_size, output_density


def getDevice():
    connectedDevicename = getDeviceName()
    for device in devices:
        name = device.get('name')
        if name == connectedDevicename:
            return device
