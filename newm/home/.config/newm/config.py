import os
import pwd
import time
import psutil

from pywm import (
    PYWM_MOD_LOGO,
    # PYWM_MOD_ALT
)

from newm import (
    SysBackendEndpoint_alsa,
    SysBackendEndpoint_sysfs
)

OUTPUT_MANAGER = True

output_scale = 2.0
round_scale = 2.0

pywm = {
    'xkb_model': "macintosh",
    'xkb_layout': "de,de",
    'xkb_options': "caps:escape",

    'encourage_csd': False,
    'debug_f1': True,

    # See comments in view.py
    'enable_output_manager': OUTPUT_MANAGER,
    'enable_xwayland': True,
}

view = {
    # See comments in view.py
    'xwayland_handle_scale_clientside': not OUTPUT_MANAGER,

    'padding': 8,
    'fullscreen_padding': 0,
    'send_fullscreen': False,
}

swipe_zoom = {
    'grid_m': 1,
    'grid_ovr': 0.02,
}

mod = PYWM_MOD_LOGO
wallpaper = '/home/jonas/wallpaper.jpg'

anim_time = .25
blend_time = .5

key_bindings = lambda layout: [
    ("M-h", lambda: layout.move(-1, 0)),
    ("M-j", lambda: layout.move(0, 1)),
    ("M-k", lambda: layout.move(0, -1)),
    ("M-l", lambda: layout.move(1, 0)),
    ("M-t", lambda: layout.move_in_stack(1)),

    ("M-H", lambda: layout.move_focused_view(-1, 0)),
    ("M-J", lambda: layout.move_focused_view(0, 1)),
    ("M-K", lambda: layout.move_focused_view(0, -1)),
    ("M-L", lambda: layout.move_focused_view(1, 0)),

    ("M-C-h", lambda: layout.resize_focused_view(-1, 0)),
    ("M-C-j", lambda: layout.resize_focused_view(0, 1)),
    ("M-C-k", lambda: layout.resize_focused_view(0, -1)),
    ("M-C-l", lambda: layout.resize_focused_view(1, 0)),

    ("M-Return", lambda: os.system("alacritty &")),
    ("M-c", lambda: os.system("chromium --enable-features=UseOzonePlatform --ozone-platform=wayland &")),
    ("M-q", lambda: layout.close_view()),

    ("M-p", lambda: layout.ensure_locked(dim=True)),
    ("M-P", lambda: layout.terminate()),
    ("M-C", lambda: layout.update_config()),

    ("M-a", lambda: layout.enter_launcher_overlay()),
    ("M-f", lambda: layout.toggle_fullscreen()),

    ("ModPress", lambda: layout.toggle_overview()),
]

sys_backend_endpoints = [
    SysBackendEndpoint_sysfs(
        "backlight",
        "/sys/class/backlight/intel_backlight/brightness",
        "/sys/class/backlight/intel_backlight/max_brightness"),
    SysBackendEndpoint_sysfs(
        "kbdlight",
        "/sys/class/leds/smc::kbd_backlight/brightness",
        "/sys/class/leds/smc::kbd_backlight/max_brightness"),
    SysBackendEndpoint_alsa(
        "volume")
]

def get_nw():
    ifdevice = "wlan0"
    ip = ""
    try:
        ip = psutil.net_if_addrs()[ifdevice][0].address
    except Exception:
        ip = "-/-"

    return "%s: %s" % (ifdevice, ip)

bar = {
    'top_texts': lambda: [
        pwd.getpwuid(os.getuid())[0],
        time.strftime("%c"),
        "%d%% %s" % (psutil.sensors_battery().percent, "↑" if
                     psutil.sensors_battery().power_plugged else "↓")
    ],
    'bottom_texts': lambda: [
        "CPU: %d%%" % psutil.cpu_percent(interval=1),
        get_nw(),
        "RAM: %d%%" % psutil.virtual_memory().percent
    ],
}

gestures = {
    'lp_freq': 120.,
    'lp_inertia': 0.4
}

swipe = {
    'gesture_factor': 3
}

panels = {
    'lock': {
        'cmd': 'alacritty -e newm-panel-basic lock',
        'w': 0.7,
        'h': 0.6,
        'corner_radius': 50,
    },
    'launcher': {
        'cmd': 'alacritty -e newm-panel-basic launcher',
        'w': 0.7,
        'h': 0.6,
        'corner_radius': 50,
        # 'cmd': 'npm run start -- launcher',
        # 'cwd': '/home/jonas/newm-panel-nwjs'
    },
    'notifiers': {
        'cmd': 'npm run start -- notifiers',
        'cwd': '/home/jonas/newm-panel-nwjs'
    }
}

grid = {
    'throw_ps': [2, 10]
}

power_times = [120, 300]
