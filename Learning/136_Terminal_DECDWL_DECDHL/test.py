# test.py
# Test terminal double width/double height characters
# DECDWL and DECDHL sequences
# https://vt100.net/docs/vt510-rm/contents.html
# https://gitlab.gnome.org/GNOME/vte/-/issues/195
#
# Doesn't work with VSCode (yet), but woth when starting from terminal "python test.py" or using ipython
# 2024-08-28    PV

print('\x1b#6THIS IS A TEST\nNext line normal')

print('\x1b#3THIS IS A TEST\n\x1b#4THIS IS A TEST\nNext line normal')

print('\x1b#3THIS IS A TEST\n\x1b#4ONCE UPON A TIME\nNext line normal')
