import platform

def check_availability():
    sistema = platform.system()
    if sistema == 'Windows':
        return check_windows()
    elif sistema == 'Linux':
        return check_linux()
    elif sistema == 'Darwin':
        return check_macos()
    else:
        return ''

def check_windows():
    import wmi
    w = wmi.WMI()
    available = []
    cam_index = 0
    for i, cam in enumerate(w.Win32_PnPEntity()):
        if 'camera' in str(cam.Caption).lower():
            available.append(cam_index)
            cam_index += 1

    return available

def check_linux():
    import subprocess
    available = []
    try:
        lsusb_out = subprocess.check_output(['lsusb']).decode('utf-8')
        for i, line in enumerate(lsusb_out.split('\n')):
            if 'camera' in line.lower():
                available.append(i)
    except subprocess.CalledProcessError:
        pass
    return available

def check_macos():
    import subprocess
    import re
    available = []
    try:
        sp_out = subprocess.check_output(['system_profiler', 'SPCameraDataType']).decode('utf-8')
        for line in sp_out.split('\n'):
            if 'camera' in line.lower() and 'built-in' not in line.lower():
                cam = re.search(r'(?<=Location ID: )\w+', line)
                if cam:
                    available.append(int(cam.group(), 16))
    except subprocess.CalledProcessError:
        pass
    return available