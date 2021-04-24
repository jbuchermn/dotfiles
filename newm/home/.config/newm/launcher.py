entries = {
    "chromium": "chromium --enable-features=UseOzonePlatform --ozone-platform=wayland",
    "nautilus": "nautilus",
    "firefox": "MOZ_ENABLE_WAYLAND=1 firefox",
    "gimp": "gimp-2.99",
    "spotify": "DISPLAY=\":0\" spotify",
    "alacritty": "alacritty",
    "Termite": "termite",
    "Emacs": "emacsclient -c -a \"emacs\"",
    "OpenSCAD": "openscad",

    "nlc": "alacritty -e nlc",
    "ngp": "alacritty -e ngp",
    "nplc": "alacritty -e nplc"
}

shortcuts = {
    1: ("Chromium", "chromium --enable-features=UseOzonePlatform --ozone-platform=wayland"),
    2: ("Emacs", "emacsclient -c -a \"emacs\""),
    3: ("Nautilus", "nautilus")
}
