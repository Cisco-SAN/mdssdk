#!/bin/bash
unset NET_TEXTFSM
export NET_TEXTFSM=$HOME/mdssdk-templates/
echo ""
echo "PLEASE NOTE:"
echo "- 'mdssdk' requires NET_TEXTFSM environment variable to be set"
echo "- This variable points to the directory where the textfsm templates are copied to"
echo "- Currently the templates are copied to - $DIR/mdssdk-templates/"
echo "- This variable is automatically set when you install 'mdssdk'"
echo "- Its recommended that you add this env permanently into your .bashrc file"
echo "- This can be done by adding the below line to your .bashrc file"
echo "      export NET_TEXTFSM=$DIR/mdssdk-templates/"
echo ""