from pywm import (
    PYWM_MOD_LOGO,
    # PYWM_MOD_ALT
)

output_scale = 2.0
pywm = {
    'xkb_model': "macintosh",
    'xkb_layout': "de,de",
    'xkb_options': "caps:escape",

    'encourage_csd': False,

    # See comments in view.py
    'enable_output_manager': False,
}

view = {
    # See comments in view.py
    'xwayland_handle_scale_clientside': True,
}

mod = PYWM_MOD_LOGO
wallpaper = '/etc/wallpaper.jpg'
panel_dir = '/lib/node_modules/newm-panel'
