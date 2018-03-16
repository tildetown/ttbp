"""
This module contains gopher-related stuff.
"""
import getpass
import os
import time
import subprocess

from . import util
#from .core import parse_date

GOPHER_PROMPT = """

GOPHER SETUP

gopher is a pre-web technology that is text-oriented and primarily used to
share folders of your files with the world.

Would you like to publish your feels to gopher?

Entries you write will automatically get linked to ~/public_gopher/feels/,
including gophermap generation. Files you manually delete will no longer be
visible from your gopherhole, and will be purged from your gophermap on your
next entry update.

If you don't know what it is or don't want it that is totally ok!

You can always change this later.""".lstrip()

GOPHERMAP_HEADER = """
 welcome to {user}'s gopherfeels.

     .::                     .::
   .:                        .::
 .:.: .:   .::       .::     .:: .::::
   .::   .:   .::  .:   .::  .::.::
   .::  .::::: .::.::::: .:: .::  .:::
   .::  .:        .:         .::    .::
   .::    .::::     .::::   .:::.:: .::

 this file is automatically generated by ttbp.

0(about ttbp)\t/~endorphant/ttbp.txt\ttilde.town\t70
1(back to user's home)\t/~{user}

entries:

"""


def select_gopher():
    return util.input_yn(GOPHER_PROMPT)

def publish_gopher(gopher_path, entry_filenames):
    """This function (re)generates a user's list of feels posts in their gopher
    directory and their gophermap."""
    entry_filenames = entry_filenames[:]  # force a copy since this might be shared state in core.py
    ttbp_gopher = os.path.join(
        os.path.expanduser('~/public_gopher'),
        gopher_path)

    if not os.path.isdir(ttbp_gopher):
        print('\n\tERROR: something is wrong. your gopher directory is missing. re-enable gopher publishing from the settings menu to fix this up!')
        return

    with open(os.path.join(ttbp_gopher, 'gophermap'), 'w') as gophermap:
        gophermap.write(GOPHERMAP_HEADER.format(
                        user=getpass.getuser()))
        for entry_filename in entry_filenames:
            filename = os.path.basename(entry_filename)

            gopher_entry_symlink = os.path.join(ttbp_gopher, os.path.basename(entry_filename))
            if not os.path.exists(gopher_entry_symlink):
                subprocess.call(["ln", "-s", entry_filename, gopher_entry_symlink])

            label = "-".join(util.parse_date(entry_filename))
            gophermap.write('0{file_label}\t{filename}\n'.format(
                file_label=label,
                filename=filename))

def setup_gopher(gopher_path):
    """Given a path relative to ~/public_gopher, this function:

    - creates a directory ~/.ttbp/gopher
    - symlinks that directory to ~/public_gopher/{gopher_path}

    It doesn't create a gophermap as that is left to the publish_gopher
    function.
    """
    public_gopher = os.path.expanduser('~/public_gopher')

    if not os.path.isdir(public_gopher):
        """
        print("\n\tERROR: you don't seem to have gopher set up (no public_gopher directory)")
        return
        """
        os.makedirs(public_gopher)

    ttbp_gopher = os.path.join(public_gopher, gopher_path)

    if os.path.isdir(ttbp_gopher):
        print("\n\tERROR: gopher path is already set up. quitting so we don't overwrite anything.")
        return

    gopher_entries = os.path.join(os.path.expanduser("~/.ttbp"), "gopher")
    if not os.path.isdir(gopher_entries):
        os.makedirs(gopher_entries)

    subprocess.call(["ln", "-s", gopher_entries, ttbp_gopher])
