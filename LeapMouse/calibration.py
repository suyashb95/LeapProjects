import win32api

'''
For now, assume all monitors have the same resolution
'''
X_RANGE = (-400, 400)
Y_RANGE = (80, 400)

def calculate_center():
    num_monitors = win32api.GetSystemMetrics(80)
    screen_resolution = (
        win32api.GetSystemMetrics(0),
        win32api.GetSystemMetrics(1)
    )
    return {
        'x':screen_resolution[0],
        'y':screen_resolution[1] / num_monitors
    }

def calcualte_scale_factors():
    num_monitors = win32api.GetSystemMetrics(80)
    screen_resolution = (
        win32api.GetSystemMetrics(59),
        win32api.GetSystemMetrics(60)
    )
    return {
        'x':screen_resolution[0] / (X_RANGE[1] - X_RANGE[0]),
        'y':screen_resolution[1] / (Y_RANGE[1] - Y_RANGE[0])
    }
