import os
import subprocess

from typing import List
from libqtile import qtile
from libqtile import bar, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen, hook, KeyChord, ScratchPad, DropDown
from libqtile.lazy import lazy

from qtile_extras import widget

from libqtile.widget.wlan import Wlan
from libqtile.widget.pulse_volume import PulseVolume
from qtile_extras.widget.decorations import PowerLineDecoration, RectDecoration

mod = "mod4"
alt = "mod1"
shift = "shift"
control = "control"
tab = "Tab"
pgup = "Next"
pgdn = "Prior"

left = "left"
right = "right"
down = "down"
up = "up"

terminal = "alacritty"

def toggle_keyboard_layout(qtile):
    qtile.cmd_spawn('setxkbmap $(setxkbmap -query | awk "/layout/{print $2=="us"?"es":"us"}")')

keys = [
    # Windows Control
    Key([mod], left, lazy.layout.left(), desc="Move focus to left"),
    Key([mod], right, lazy.layout.right(), desc="Move focus to right"),
    Key([mod], down, lazy.layout.down(), desc="Move focus down"),
    Key([mod], up, lazy.layout.up(), desc="Move focus up"),
    Key([alt], tab, lazy.layout.next(), desc="Move window focus to other window"),

    Key([mod, shift], left, lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, shift], right, lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, shift], down, lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, shift], up, lazy.layout.shuffle_up(), desc="Move window up"),

    Key([mod, control], left, lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, control], right, lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, control], down, lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, control], up, lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    Key(
        [mod, shift],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], tab, lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),

    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, control], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, control], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod, shift], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),

    # Launch Apps
    Key([mod], "a", lazy.spawn("rofi -show drun"), desc="Abrir menu"),
    Key([mod], "r", lazy.spawn("rofi -show run"), desc="Abrir menu"),
    Key([alt, shift], tab, lazy.spawn("rofi -show window"), desc="Abrir menu"),
    Key([mod], "s", lazy.spawn("rofi -show ssh"), desc="Abrir menu"),

    # Multimedia controls
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause"), desc='playerctl'),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous"), desc='playerctl'),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next"), desc='playerctl'),
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl s 10%+"), desc='brightness UP'),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl s 10%-"), desc='brightness Down'),

    Key([], "XF86AudioMute", lazy.spawn("amixer -c 1 Master toggle")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -c 0 set Master 2%-")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -c 0 set Master 2%+")),

    # Others controls
    Key([mod, shift], "s", lazy.spawn("flameshot gui"), desc='Screenshot'),
    Key([mod], "n", lazy.spawn("kitty ranger"), desc="Abrir Ranger"),

    # Set KeyboardLayout
    # Key([mod], "space", lazy.function(toggle_keyboard_layout), lazy.spawn('setxkbmap $(setxkbmap -query | awk "/layout/{print $2=="us"?"es":"us"}")'), desc="Toggle Keyboard Layout"),
    Key([mod], "space", lazy.spawn("setxkbmap us"), desc="Cambiar Ingés"),
    Key([mod, control], "space", lazy.spawn("setxkbmap es"), desc="Cambiar Español"),

    Key([mod], pgup, lazy.screen.next_group(), desc="Switch to next screen"),
    Key([mod], pgdn, lazy.screen.prev_group(), desc="Switch to previous screen"),
]

groups = []
group_names = [
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "0"
]
group_labels = [
    "󰣇",
    "󰈹",
    "󰨞",
    "",
    "",
    "󰈙",
    "",
    "󰝚",
    "",
    "",
]

for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            label=group_labels[i],
        )
    )

for i in groups:
    keys.extend(
            [
                Key(
                    [mod],
                    i.name,
                    lazy.group[i.name].toscreen(),
                    desc="Switch to group {}".format(i.name),
                    ),
                Key(
                    [mod, "shift"],
                    i.name,
                    lazy.window.togroup(i.name, switch_group=True),
                    desc="Switch to & move focused window to group {}".format(i.name),
                    ),
                ]
            )

layout_theme = {
    "margin":10,
    "border_width": 4,
    "border_focus": "#371B58",
    "border_normal": "#5B4B8A"
}

layouts = [
    layout.Columns(**layout_theme),
    layout.Max(**layout_theme),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(**layout_theme),
    # layout.MonadTall(**layout_theme),
    layout.MonadWide(**layout_theme),
    # layout.RatioTile(**layout_theme),
    # layout.Tile(),
    # layout.TreeTab(),
    layout.VerticalTile(**layout_theme),
    # layout.Zoomy(**layout_theme),
]

widget_defaults = dict(
    font="sans",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

def open_audio_devices():
    qtile.cmd_spawn("pavucontrol")

def system_monitor():
    qtile.cmd_spawn("kitty htop")

def system_calendar():
    qtile.cmd_spawn("gnome-calendar")

def system_network():
    qtile.cmd_spawn("kitty iwctl")

def system_power():
    qtile.cmd_spawn("kitty htop")

powerline_left = {
    "decorations": [
        RectDecoration(use_widget_background=True, padding_x=-2, filled=True, size = 8),
        PowerLineDecoration(path="arrow_left", padding_y=0)
    ]
}

powerline_right = {
    "decorations": [
        RectDecoration(use_widget_background=True, padding_x=-2, filled=True, size = 8),
        PowerLineDecoration(path="arrow_right", padding_y=0)
    ]
}

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    background="#371B58",
                    highlight_method='text',
                    this_current_screen_border="#f1f1f1",
                    active="#7858A6",
                    inactive="#4C3575",
                    **powerline_left,
                ),
                widget.Prompt(),
                widget.WindowName(),

                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                widget.Notify(),
                widget.TextBox(
                    foreground="#371B58",
                    background="#00000000",
                    **powerline_right,
                ),
                widget.TextBox(
                    background="#371B58",
                    text="󰔏",
                ),
                widget.ThermalSensor(
                    background="#371B58",
                    **powerline_right,
                ),
                widget.StatusNotifier(
                    background="#4C3575",
                ),
                widget.KeyboardLayout(
                    background="#4C3575",
                    fmt="󰌌  {}",
                ),
                widget.Systray(
                    background="#4C3575",
                ),
                widget.Clock(
                    background="#4C3575",
                    format="%Y-%m-%d %a",
                    fmt="  {}",
                    mouse_callbacks={'Button1': system_calendar},
                ),
                widget.Clock(
                    background="#4C3575",
                    format="%I:%M %p",
                    fmt="󰥔  {}",
                    mouse_callbacks={'Button1': system_calendar},
                    **powerline_right,
                ),
                widget.CheckUpdates(
                    background="#5B4B8A",
                ),
                widget.Volume(
                    background="#5B4B8A",
                    cardid="amixer",
                    fmt="󱄠",
                    mouse_callbacks={'Button1': open_audio_devices},
                ),
                widget.PulseVolume(
                    background="#5B4B8A",
                ),
                widget.Battery(
                    background="#5B4B8A",
                    charge_char="󱟠",
                    discharge_char="󱟞",
                    empty_char="󰂃",
                    full_char="󱟢",
                    not_charging_char="󱧥",
                    format='{char} {percent:2.0%}',
                    update_interval=1,
                    mouse_callbacks={'Button1': system_power},
                ),
                widget.TextBox(
                    background="#5B4B8A",
                    text="",
                ),
                widget.Net(
                    background="#5B4B8A",
                    mouse_callbacks={'Button1': system_network},
                    interface='wlp2s0',
                ),
                widget.Wlan(
                    background="#5B4B8A",
                    mouse_callbacks={'Button1': system_network},
                    **powerline_right,
                ),
                widget.QuickExit(
                    background="#7858A6",
                    fontsize=16,
                    default_text="⏻ ",
                    countdown_start=5,
                    countdown_format="{}s",
                ),
                widget.CurrentLayoutIcon(
                    background="#7858A6",
                    scale=0.6,
                ),
                widget.CurrentLayout(
                    background="#7858A6",
                ),
            ],
            24,
            opacity=1,
            background="#00000000",
            # layout_margin=10,
            # single_layout_margin=10,
            # layout_border_width=4,
            # single_border_width=4,

            #margin=[4,4,0,4]
        ),
    ),
]

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),
        Match(wm_class="makebranch"),
        Match(wm_class="maketag"),
        Match(wm_class="ssh-askpass"),
        Match(title="branchdialog"),
        Match(title="pinentry"),
    ]
)

autostart = [
    "feh --bg-fill $HOME/.local/share/backgrounds/anderon.png &",
    "xsettingsd &",
    "picom --no-vsync &",
    "xinput --set-prop 10 'libinput Natural Scrolling Enabled' 1 &",
    "syncthing -no-browser -no-restart -logflags=0 &",
]

for x in autostart:
    os.system(x)
'''
@hook.subscribe.startup_once
def start_once():
    subprocess.call(['/usr/bin/sh ~/.config/qtile/sh/autostart.sh'])
'''
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True
wl_input_rules = None

wmname = "Qtile"
