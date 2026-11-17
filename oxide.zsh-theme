# --------------------------------------------------
# OXIDE - Industrial Minimal Zsh Theme
# Designed for a dark Terminator colour scheme.
# --------------------------------------------------

# Colours
OXIDE_RED="%F{160}"
OXIDE_ORANGE="%F{166}"
OXIDE_GREY="%F{245}"
OXIDE_LIGHT="%F{250}"
OXIDE_MUTED="%F{240}"
OXIDE_RESET="%f"

# Git information
ZSH_THEME_GIT_PROMPT_PREFIX=" ${OXIDE_MUTED}("
ZSH_THEME_GIT_PROMPT_SUFFIX="${OXIDE_MUTED})"
ZSH_THEME_GIT_PROMPT_DIRTY=" ${OXIDE_ORANGE}*"
ZSH_THEME_GIT_PROMPT_CLEAN=""

# Prompt
PROMPT='${OXIDE_MUTED}[%n@%m] ${OXIDE_RED}%~${OXIDE_RESET}$(git_prompt_info) ${OXIDE_RED}❯${OXIDE_RESET} '

# No right prompt
RPROMPT=''
