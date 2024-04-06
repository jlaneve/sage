# tbd.plugin.zsh

api_url="localhost:8000"

# Function to capture and process commands
function command_capture_preexec() {
    local command="$1"
    local root_dir=$(git rev-parse --show-toplevel 2> /dev/null || echo "$HOME")
    local user="$USER"
    local time=$(date)
    local cwd=$(pwd)

    # escape the command
    command=$(echo $command | sed 's/"/\\"/g')

    # make a request to $api_url/insert_command with the command, user, time, pwd, root_dir
    # as a subshell to avoid blocking the shell
    (
        curl -s -X POST -H "Content-Type: application/json" -d "{\"command\": \"$command\", \"user\": \"$user\", \"timestamp\": \"$time\", \"cwd\": \"$cwd\", \"base_dir\": \"$root_dir\"}" $api_url/insert_command > /dev/null
    ) &!
}

# Register the preexec function as a hook
autoload -Uz add-zsh-hook
add-zsh-hook preexec command_capture_preexec

echo "tbd.plugin.zsh loaded"