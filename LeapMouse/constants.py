import win32api

num_monitors = win32api.GetSystemMetrics(80)
sensitivity = 2.5
screen_resolution = (
    win32api.GetSystemMetrics(59),
    win32api.GetSystemMetrics(60)
)
center  = {
    'x':screen_resolution[0]/2,
    'y':screen_resolution[1]/2
}
scale_factor = {
    'x':screen_resolution[0]/400,
    'y':screen_resolution[1]/350
}
