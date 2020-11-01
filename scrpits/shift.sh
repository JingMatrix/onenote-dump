#!/bin/zsh

(($+2)) || {
    echo 'Usage: merge index *.txt'
    return
}
for name ($*[2,-1]) {
    # num = ${filename%.*} + $index
    ((index = ${name%.*} + $1))
    sed -i 's/琐记.*]/琐记]/' $name
    sed -i  -e 's/"[0-9][0-9]*"$/"'${index}'"/' $name
    sed -i  -e 's/^# [0-9][0-9]*$/# '${index}/ $name
    # echo $index.md
    # sed -i '/^title/d' $name
    mv -v $name /home/jing/Téléchargements/OneNotes/OtherNotes/notes/$index.md
}