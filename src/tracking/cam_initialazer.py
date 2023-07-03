import platform
import cv2
def check_availability():
    system = platform.system()
    if system == 'Windows':
        return check_windows()
    elif system == 'Linux':
        return check_linux()
    elif system == 'Darwin':
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
            #print(cam_index)
            available.append(cam_index)
            cam_index += 1

    return available

def check_linux():
    available = []
    for i in range(10):
        try:
            cap = cv2.VideoCapture(i)
            if cap.read()[0]:
                available.append(i)
            cap.release()
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