import subprocess

username = 'lentotheeye'
devices = [
    {
        'name': 'LGV5005ed279c7',
        'lowerScreenBound': 1650,
        'upperScreenBound': 390,
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

    return deviceName


def getDevice():
    connectedDevicename = getDeviceName()
    for device in devices:
        name = device.get('name')
        if name == connectedDevicename:
            return device
