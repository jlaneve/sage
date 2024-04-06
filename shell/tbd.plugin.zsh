# tbd.plugin.zsh

# Function to capture and process commands
function command_capture_preexec() {
    local command="$1"
    local root_dir=$(git rev-parse --show-toplevel 2> /dev/null || echo "$HOME")
    
    # Add your custom logic here to process or log the command
    echo "Intercepted command: $command"
    echo "User: $USER"
    echo "Directory: $PWD"
    echo "Root dir: $root_dir"
    echo "Time: $(date)"
}

# Register the preexec function as a hook
autoload -Uz add-zsh-hook
add-zsh-hook preexec command_capture_preexec

echo "tbd.plugin.zsh loaded"