# tbd.plugin.zsh

# Function to capture and process commands
function command_capture_preexec() {
    local command="$1"
    
    # Add your custom logic here to process or log the command
    echo "Intercepted command: $command"
}

# Register the preexec function as a hook
autoload -Uz add-zsh-hook
add-zsh-hook preexec command_capture_preexec

echo "tbd.plugin.zsh loaded"