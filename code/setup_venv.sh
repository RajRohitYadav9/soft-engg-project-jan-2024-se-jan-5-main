#!/bin/bash
PWD =`pwd`
python3 -m venv .venv
echo $PWD
activate(){
    ./.venv/Scripts/activate
}
activate

pause
