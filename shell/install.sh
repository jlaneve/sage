mkdir -p ~/.oh-my-zsh/custom/plugins/tbd
ln -s $PWD/shell/tbd.plugin.zsh ~/.oh-my-zsh/custom/plugins/tbd/tbd.plugin.zsh

[[ -e $PWD/shell/zsh-with-plugin.zshrc ]] || cp ~/.zshrc $PWD/shell/zsh-with-plugin.zshrc

echo "Make sure to add 'tbd' to the plugins list in your shell/zsh-with-plugin.zshrc file"
