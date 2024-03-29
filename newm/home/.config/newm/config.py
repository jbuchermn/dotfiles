import os
import pwd
import time
import psutil

from pywm import (
    PYWM_MOD_LOGO,
    PYWM_MOD_ALT,

    PYWM_TRANSFORM_90,
    PYWM_TRANSFORM_180,
    PYWM_TRANSFORM_270,
    PYWM_TRANSFORM_FLIPPED,
    PYWM_TRANSFORM_FLIPPED_90,
    PYWM_TRANSFORM_FLIPPED_180,
    PYWM_TRANSFORM_FLIPPED_270,
)

from newm import (
    SysBackendEndpoint_alsa,
    SysBackendEndpoint_sysfs
)

def on_startup():
    os.system("dbus-update-activation-environment --systemd WAYLAND_DISPLAY XDG_CURRENT_DESKTOP=wlroots")
    os.system("catapult &")
    os.system("waybar &")

def on_reconfigure():
    os.system("notify-send newm \"Reloaded config\" &")

corner_radius = 20.5
# v0.1
# output_scale = 2.

outputs = [
    { 'name': 'eDP-1', 'pos_x': 0, 'pos_y': 0, 'scale': 2. },
    { 'name': 'virt-1', 'pos_x': 1280, 'pos_y': 0, 'width': 1280, 'height': 720, 'scale': 1., 
        'mHz': 30000, 'anim': False},
    { 'name': 'HDMI-A-2', 'pos_x': 2560, 'width': 3840, 'height': 2160, 'scale': 2.,
        'mHz': 30000}
]

pywm = {
    'xkb_model': "macintosh",
    'xkb_layout': "de,de",
    'xkb_options': "caps:escape",

    'encourage_csd': False,
    'enable_xwayland': True,

    'natural_scroll': True,

    'texture_shaders': 'basic'

    # v0.1
    # 'round_scale': 2.
}

focus = {
    'distance': 4,
    'width': 2,
    'animate_on_change': False,
    'anim_time': .25
}

def should_float(view):
    if view.app_id == "catapult":
        return True, None, (0.5, 0.25)
    if view.app_id == "pavucontrol":
        return True, (340, 600), (0.15, 0.4)
    # if view.app_id == "rofi":
    #     return True, (800, 800), (0.5, 0.5)
    if view.title is not None and view.title.strip() == "Firefox — Sharing Indicator":
        return True, (100, 40), (0.5, 0.1)
    return None

view = {
    'padding': 8,
    'fullscreen_padding': 0,
    'send_fullscreen': False,

    'should_float': should_float,
    'floating_min_size': False,

    'debug_scaling': True,
    'border_ws_switch': 100,
}

swipe_zoom = {
    'grid_m': 1,
    'grid_ovr': 0.02,
}


mod = PYWM_MOD_LOGO
background = {
    'path': '/home/jonas/wallpaper-3.jpg',
    'time_scale': 0.125,
    'anim': True,
}

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

    ("M-v", lambda: layout.toggle_focused_view_floating()),
    ("M-w", lambda: layout.change_focused_view_workspace()),
    ("M-W", lambda: layout.move_workspace()),
    ("M-S", lambda: os.system("grim -g \"$(slurp)\" &")),

    ("M-Return", lambda: os.system("alacritty &")),
    ("M-e", lambda: os.system("emacsclient -c -a \"emacs\" &")),
    ("M-c", lambda: os.system("brave --enable-features=UseOzonePlatform --ozone-platform=wayland &")),
    ("M-m", lambda: os.system("bash /$HOME/.shell/macho-gui.sh &")),
    ("M-q", lambda: layout.close_view()),

    ("M-p", lambda: layout.ensure_locked(dim=True)),
    ("M-P", lambda: layout.terminate()),
    ("M-C", lambda: layout.update_config()),

    # ("M-r", lambda: os.system("catapult &")),
    ("M-r", lambda: os.system("rofi -show run &")),
    ("M-f", lambda: layout.toggle_fullscreen()),

    ("ModPress", lambda: layout.toggle_overview(only_active_workspace=False)),
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
    'enabled': False,
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
    ]
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
        # 'cmd': 'npm run start -- lock',
        # 'cwd': '/home/jonas/newm-panel-nwjs'
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
        # 'cmd': 'npm run start -- notifiers',
        # 'cwd': '/home/jonas/newm-panel-nwjs'
    }
}

grid = {
    'throw_ps': [2, 10]
}

power_times = [180, 600]
