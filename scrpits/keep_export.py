"""
Export Google Keep notes to markdown files.

After obtaining your Google Keep data from https://takeout.google.com/,
unzip the folder and cd into it.

Copy this file in that folder and run:
    python export.py
"""

import os
import json
import datetime


PRINT_RAW = False
PRINT_PRETTY_JSON = True

class Note:
    def __init__(self, filename, data):
        self._name = filename.replace('.json', '')
        self._title = data['title']
        if 'labels' in data:
            self.labels = data['labels'][0]['name']
        else:
            self.labels = 'Archived'
        #self.savename = self.labels + ' -- ' + self._name
        self.savename = self._name
        self._raw_date = data['userEditedTimestampUsec']
        self._date = datetime.datetime.fromtimestamp(self._raw_date/1_000_000)
        self._isTrashed = data['isTrashed']
        self._isArchived = data['isArchived']
        self._isList = True if 'listContent' in data else False
        if self._isList:
            checklist = ""
            for item in data['listContent']:
                tick = '+' if item['isChecked'] else ' '
                checklist += "- [{}] {}\n".format(tick, item['text'])
            self._content = checklist
            del checklist
        else:
            self._content = data['textContent']

    def _format_date(self):
        # return a date of this type: Tuesday November 03, 2015, 03:20:51 PM
        return self._date # https://strftime.org/

    def isTrashed(self):
        return self._isTrashed

    def __repr__(self):
        # Add header to self._content containing title and last edited
        note = "---\ntitle: {}\n".format(self._name)
        note += "created: '{}'\nmodified: '{}'\n".format(self._format_date(),self._format_date())
        note += "tags: [Notebooks/KeepNote, '{}']\n---\n".format(self.labels)
        note += "# {} \n".format(self._name)
        # note += "Last edited: {}\n\n".format(self._format_date())
        note += self._content
        return note


if __name__ == '__main__':

    ROOT_FOLDER = 'Keep'
    notes = [filename for filename in os.listdir(ROOT_FOLDER) if '.json' in filename]

    parsed_notes = {}
    for filename in notes:

        # Parse note
        with open("{}/{}".format(ROOT_FOLDER, filename), 'r') as json_file:
            data = json.load(json_file)

            if PRINT_RAW:
                if PRINT_PRETTY_JSON:
                    print(json.dumps(data, indent=4, sort_keys=True))
                    print()
                else:
                    print("{}\n\n".format(data))

        # Save note to dictionary if not trashed
        note = Note(filename, data)
        if not note.isTrashed():
            parsed_notes[note.savename] = note

    del notes

    # Create "markdown" folder
    if not os.path.isdir('markdown'):
        os.mkdir('markdown')

    # Write dictionary to markdown files
    for savename in parsed_notes:
        name = savename.replace('/', '-', 999)
        # subdir = parsed_notes[savename].labels.replace('/', '-', 999)
        # if not os.path.isdir(os.path.join('markdown', subdir)):
            # os.mkdir(os.path.join('markdown', subdir))
        with open(os.path.join('notes', f'{name}.md'), 'w') as f:
            f.write(str(parsed_notes[savename]))
    print(f'Saved {len(parsed_notes.keys())} notes to /markdown')
