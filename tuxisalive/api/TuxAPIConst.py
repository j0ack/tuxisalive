# -*- coding: latin1 -*-

import version
__author__ = version.author
__date__ = version.date
__version__ = version.version
__licence__ = version.licence
del version

#    Copyright (C) 2008 C2ME Sa
#    Rémi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

#
# Client levels
#
CLIENT_LEVEL_ANONYME        = -1
CLIENT_LEVEL_FREE           = 0
CLIENT_LEVEL_RESTRICTED     = 1
CLIENT_LEVEL_ROOT           = 2
CLIENT_LEVELS = [
    CLIENT_LEVEL_ANONYME,
    CLIENT_LEVEL_FREE,
    CLIENT_LEVEL_RESTRICTED,
    CLIENT_LEVEL_ROOT,
]
CLIENT_LEVELS_NAME = [
    "CLIENT_LEVEL_ANONYME",
    "CLIENT_LEVEL_FREE",
    "CLIENT_LEVEL_RESTRICTED",
    "CLIENT_LEVEL_ROOT",
]

#
# Access priority levels
#
ACCESS_PRIORITY_LOW         = 0
ACCESS_PRIORITY_NORMAL      = 1
ACCESS_PRIORITY_HIGH        = 2
ACCESS_PRIORITY_CRITICAL    = 3
ACCESS_PRIORITIES = [
    ACCESS_PRIORITY_LOW,
    ACCESS_PRIORITY_NORMAL,
    ACCESS_PRIORITY_HIGH,
    ACCESS_PRIORITY_CRITICAL,
]

#
# Statuses declaration
#

# From libtuxdriver
ST_NAME_HEAD_BUTTON         = 'head_button'
ST_NAME_LEFT_BUTTON         = 'left_wing_button'
ST_NAME_RIGHT_BUTTON        = 'right_wing_button'
ST_NAME_REMOTE_BUTTON       = 'remote_button'
ST_NAME_MOUTH_POSITION      = 'mouth_position'
ST_NAME_MOUTH_RM            = 'mouth_remaining_movements'
ST_NAME_EYES_POSITION       = 'eyes_position'
ST_NAME_EYES_RM             = 'eyes_remaining_movements'
ST_NAME_FLIPPERS_POSITION   = 'flippers_position'
ST_NAME_FLIPPERS_RM         = 'flippers_remaining_movements'
ST_NAME_SPINNING_DIRECTION  = 'spinning_direction'
ST_NAME_SPINNING_RM         = 'spinning_remaining_movements'
ST_NAME_DONGLE_PLUG         = 'dongle_plug'
ST_NAME_RADIO_STATE         = 'radio_state'
ST_NAME_LEFT_LED            = 'left_led_state'
ST_NAME_RIGHT_LED           = 'right_led_state'
ST_NAME_AUDIO_FLASH_PLAY    = 'audio_flash_play'
ST_NAME_SOUND_REFLASH_END   = 'sound_reflash_end'
ST_NAME_EYES_MOTOR_ON       = 'eyes_motor_on'
ST_NAME_MOUTH_MOTOR_ON      = 'mouth_motor_on'
ST_NAME_FLIPPERS_MOTOR_ON   = 'flippers_motor_on'
ST_NAME_SPIN_LEFT_MOTOR_ON  = 'spin_left_motor_on'
ST_NAME_SPIN_RIGHT_MOTOR_ON = 'spin_right_motor_on'
ST_NAME_DRIVER_SYMB_VER     = 'driver_symbolic_version'
ST_NAME_TUXCORE_SYMB_VER    = 'tuxcore_symbolic_version'
ST_NAME_TUXAUDIO_SYMB_VER   = 'tuxaudio_symbolic_version'
ST_NAME_FUXUSB_SYMB_VER     = 'fuxusb_symbolic_version'
ST_NAME_FUXRF_SYMB_VER      = 'fuxrf_symbolic_version'
ST_NAME_TUXRF_SYMB_VER      = 'tuxrf_symbolic_version'
ST_NAME_FLASH_SOUND_COUNT   = 'sound_flash_count'
SW_NAME_DRIVER = [
    ST_NAME_FLIPPERS_POSITION,
    ST_NAME_FLIPPERS_RM,
    ST_NAME_SPINNING_DIRECTION,
    ST_NAME_SPINNING_RM,
    ST_NAME_LEFT_BUTTON,
    ST_NAME_RIGHT_BUTTON,
    ST_NAME_HEAD_BUTTON,
    ST_NAME_REMOTE_BUTTON,
    ST_NAME_MOUTH_POSITION,
    ST_NAME_MOUTH_RM,
    ST_NAME_EYES_POSITION,
    ST_NAME_EYES_RM,
    "descriptor_complete",
    ST_NAME_RADIO_STATE,
    ST_NAME_DONGLE_PLUG,
    "charger_state",
    "battery_level",
    "battery_state",
    "light_level",
    ST_NAME_LEFT_LED,
    ST_NAME_RIGHT_LED,
    "connection_quality",
    ST_NAME_AUDIO_FLASH_PLAY,
    "audio_general_play",
    "flash_programming_current_track",
    "flash_programming_last_track_size",
    ST_NAME_TUXCORE_SYMB_VER,
    ST_NAME_TUXAUDIO_SYMB_VER,
    ST_NAME_FUXUSB_SYMB_VER,
    ST_NAME_FUXRF_SYMB_VER,
    ST_NAME_TUXRF_SYMB_VER,
    ST_NAME_DRIVER_SYMB_VER,
    "sound_reflash_begin",
    ST_NAME_SOUND_REFLASH_END,
    ST_NAME_EYES_MOTOR_ON,
    ST_NAME_MOUTH_MOTOR_ON,
    ST_NAME_FLIPPERS_MOTOR_ON,
    ST_NAME_SPIN_LEFT_MOTOR_ON,
    ST_NAME_SPIN_RIGHT_MOTOR_ON,
    ST_NAME_FLASH_SOUND_COUNT,
]

# From libtuxosl
ST_NAME_SPEAK_STATUS        = 'tts_0_speak_status'
ST_NAME_TTS_SOUND_STATE     = 'tts_0_sound_state'
ST_NAME_VOICE_LIST          = 'tts_0_voice_list'
ST_NAME_WAV_CHANNEL_START   = 'tts_wav_channel_start'
ST_NAME_WAV_0_SOUND_STATE   = 'wav_0_sound_state'
ST_NAME_WAV_1_SOUND_STATE   = 'wav_1_sound_state'
ST_NAME_WAV_2_SOUND_STATE   = 'wav_2_sound_state'
ST_NAME_WAV_3_SOUND_STATE   = 'wav_3_sound_state'
ST_NAME_OSL_SYMB_VER        = 'osl_symbolic_version'
SW_NAME_OSL = [
    ST_NAME_OSL_SYMB_VER,
    "general_sound_state",
    "wav_volume",
    "tts_volume",
    "tts_pitch",
    "tts_locutor",
    ST_NAME_WAV_0_SOUND_STATE,
    "wav_0_pause_state",
    "wav_0_stop",
    ST_NAME_WAV_1_SOUND_STATE,
    "wav_1_pause_state",
    "wav_1_stop",
    ST_NAME_WAV_2_SOUND_STATE,
    "wav_2_pause_state",
    "wav_2_stop",
    ST_NAME_WAV_3_SOUND_STATE,
    "wav_3_pause_state",
    "wav_3_stop",
    ST_NAME_TTS_SOUND_STATE,
    "tts_0_pause_state",
    "tts_0_stop",
    "tts_0_voice_loaded",
    ST_NAME_SPEAK_STATUS,
    ST_NAME_VOICE_LIST,
    ST_NAME_WAV_CHANNEL_START,
]

# From TuxAPI
ST_NAME_API_CONNECT         = 'api_connect'
SW_NAME_API = [
    ST_NAME_API_CONNECT,
]
# From external source
SW_NAME_EXTERNAL_STATUS = "external_status"
SW_NAME_EXTERNAL = [
    SW_NAME_EXTERNAL_STATUS,
]

#
# Possible string values of statuses
#
SSV_NDEF            = "NDEF"
SSV_OPEN            = "OPEN"
SSV_CLOSE           = "CLOSE"
SSV_UP              = "UP"
SSV_DOWN            = "DOWN"
SSV_LEFT            = "LEFT"
SSV_RIGHT           = "RIGHT"
SSV_ON              = "ON"
SSV_OFF             = "OFF"
SSV_CHANGING        = "CHANGING"

# Mouth and eyes positions
SSV_MOUTHEYES_POSITIONS = [
    SSV_NDEF,
    SSV_OPEN,
    SSV_CLOSE,
]

# Flippers positions
SSV_FLIPPERS_POSITIONS = [
    SSV_NDEF,
    SSV_UP,
    SSV_DOWN,
]

# Spinning directions
SSV_SPINNING_DIRECTIONS = [
    SSV_NDEF,
    SSV_LEFT,
    SSV_RIGHT,
]

# Led states
SSV_LED_STATES = [
    SSV_ON,
    SSV_OFF,
    SSV_CHANGING,
]

#
# Speed values
#
SPV_VERYSLOW    = 1
SPV_SLOW        = 2
SPV_NORMAL      = 3
SPV_FAST        = 4
SPV_VERYFAST    = 5
SPV_SPEED_VALUES = [
    SPV_VERYSLOW,
    SPV_SLOW,
    SPV_NORMAL,
    SPV_FAST,
    SPV_VERYFAST,
]

#
# Led effects
#

# Simples
LFX_NONE        = 0
LFX_FADE        = 1
LFX_STEP        = 2
LED_EFFECT_TYPE = [
    LFX_NONE,
    LFX_FADE,
    LFX_STEP,
]

# Extended
LFXEX_UNAFFECTED        = "UNAFFECTED"
LFXEX_LAST              = "LAST"
LFXEX_NONE              = "NONE"
LFXEX_DEFAULT           = "DEFAULT"
LFXEX_FADE_DURATION     = "FADE_DURATION"
LFXEX_FADE_RATE         = "FADE_RATE"
LFXEX_GRADIENT_NBR      = "GRADIENT_NBR"
LFXEX_GRADIENT_DELTA    = "GRADIENT_DELTA"
LED_EFFECT_TYPE_EX_NAMES = [
    LFXEX_UNAFFECTED,
    LFXEX_LAST,
    LFXEX_NONE,
    LFXEX_DEFAULT,
    LFXEX_FADE_DURATION,
    LFXEX_FADE_RATE,
    LFXEX_GRADIENT_NBR,
    LFXEX_GRADIENT_DELTA,
]

#
# Led names
#
LED_NAME_BOTH           = "LED_BOTH"
LED_NAME_RIGHT          = "LED_RIGHT"
LED_NAME_LEFT           = "LED_LEFT"

#
# Sound reflash errors
#
SOUND_REFLASH_NO_ERROR              = "NO_ERROR"
SOUND_REFLASH_ERROR_RF_OFFLINE      = "ERROR_RF_OFFLINE"
SOUND_REFLASH_ERROR_WAV             = "ERROR_WAV"
SOUND_REFLASH_ERROR_USB             = "ERROR_USB"
SOUND_REFLASH_ERROR_PARAMETERS      = "ERROR_PARAMETERS"
SOUND_REFLASH_ERROR_BUSY            = "ERROR_BUSY"
SOUND_REFLASH_ERROR_BADWAVFILE      = "ERROR_BADWAVFILE"
SOUND_REFLASH_ERROR_WAVSIZEEXCEDED  = "ERROR_WAVSIZEEXCEDED"

#
# Wav channels
#
WAV_CHANNELS_NAME_LIST = [
    ST_NAME_WAV_0_SOUND_STATE,
    ST_NAME_WAV_1_SOUND_STATE,
    ST_NAME_WAV_2_SOUND_STATE,
    ST_NAME_WAV_3_SOUND_STATE,
]

#
# Remote keys
#
K_0             = "K_0"
K_1             = "K_1"
K_2             = "K_2"
K_3             = "K_3"
K_4             = "K_4"
K_5             = "K_5"
K_6             = "K_6"
K_7             = "K_7"
K_8             = "K_8"
K_9             = "K_9"
K_STANDBY       = "K_STANDBY"
K_MUTE          = "K_MUTE"
K_VOLUMEPLUS    = "K_VOLUMEPLUS"
K_VOLUMEMINUS   = "K_VOLUMEMINUS"
K_ESCAPE        = "K_ESCAPE"
K_YES           = "K_YES"
K_NO            = "K_NO"
K_BACKSPACE     = "K_BACKSPACE"
K_STARTVOIP     = "K_STARTVOIP"
K_RECEIVECALL   = "K_RECEIVECALL"
K_HANGUP        = "K_HANGUP"
K_STAR          = "K_STAR"
K_SHARP         = "K_SHARP"
K_RED           = "K_RED"
K_GREEN         = "K_GREEN"
K_BLUE          = "K_BLUE"
K_YELLOW        = "K_YELLOW"
K_CHANNELPLUS   = "K_CHANNELPLUS"
K_CHANNELMINUS  = "K_CHANNELMINUS"
K_UP            = "K_UP"
K_DOWN          = "K_DOWN"
K_LEFT          = "K_LEFT"
K_RIGHT         = "K_RIGHT"
K_OK            = "K_OK"
K_FASTREWIND    = "K_FASTREWIND"
K_FASTFORWARD   = "K_FASTFORWARD"
K_PLAYPAUSE     = "K_PLAYPAUSE"
K_STOP          = "K_STOP"
K_RECORDING     = "K_RECORDING"
K_PREVIOUS      = "K_PREVIOUS"
K_NEXT          = "K_NEXT"
K_MENU          = "K_MENU"
K_MOUSE         = "K_MOUSE"
K_ALT           = "K_ALT"
K_RELEASED      = "RELEASED"

REMOTE_KEY_LIST = [
    K_0,
    K_1,
    K_2,
    K_3,
    K_4,
    K_5,
    K_6,
    K_7,
    K_8,
    K_9,
    K_STANDBY,
    K_MUTE,
    K_VOLUMEPLUS,
    K_VOLUMEMINUS,
    K_ESCAPE,
    K_YES,
    K_NO,
    K_BACKSPACE,
    K_STARTVOIP,
    K_RECEIVECALL,
    K_HANGUP,
    K_STAR,
    K_SHARP,
    K_RED,
    K_GREEN,
    K_BLUE,
    K_YELLOW,
    K_CHANNELPLUS,
    K_CHANNELMINUS,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_OK,
    K_FASTREWIND,
    K_FASTFORWARD,
    K_PLAYPAUSE,
    K_STOP,
    K_RECORDING,
    K_PREVIOUS,
    K_NEXT,
    K_MENU,
    K_MOUSE,
    K_ALT,
    K_RELEASED,
]