#!/bin/zsh
for Notebooks (Daily Philosophy Poems 不创作了 不学了 书单与读后感 写作 读书笔记) {
    python3 onenote-dump $Notebooks ~/Téléchargements/OtherNotes
}
 for section (琐记（18.8.4前） 琐记（18.8.4后） 琐记（19.11.15后） 琐记（2020.3.9） 琐记（2020.6.20） 事项) {
     python3 onenote-dump 日常生活 ~/Téléchargements/$section --section $section
 }