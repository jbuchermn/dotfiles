import os

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
pywm = {
    'xkb_model': "macintosh",
    'xkb_layout': "de,de",
    'xkb_options': "caps:escape",

    'encourage_csd': False,

    # See comments in view.py
    'enable_output_manager': OUTPUT_MANAGER,
}

view = {
    # See comments in view.py
    'xwayland_handle_scale_clientside': not OUTPUT_MANAGER,
}

swipe_zoom = {
    'grid_m': 1,
    'grid_ovr': 0.02,
}

mod = PYWM_MOD_LOGO
wallpaper = '/home/jonas/wallpaper.jpg'
panel_dir = '/lib/node_modules/newm-panel'

key_bindings = lambda layout: [
    ("M-h", lambda: layout.move(-1, 0)),
    ("M-j", lambda: layout.move(0, 1)),
    ("M-k", lambda: layout.move(0, -1)),
    ("M-l", lambda: layout.move(1, 0)),

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

    ("M-f", lambda: layout.toggle_fullscreen()),

    ("ModPress", lambda: layout.enter_overview_overlay())
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
