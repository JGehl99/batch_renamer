from PySimpleGUI import theme, Text, Frame, Button, InputText, Window, WIN_CLOSED, Menu, FolderBrowse
from os.path import join, splitext, isfile
from os import rename, listdir


# Renames all files in provided path with the formula newname+zerofilled index+extension
def rename_files(path, i, z, name):
    for file in listdir(path):
        if isfile(join(path, file)):
            rename(join(path, file), join(path, name + str(i).zfill(z) + splitext(file)[1]))
            i += 1


# Theme
theme('DarkGrey6')

# Items in toolbar menu
menu_def = [['File', 'Exit'],
            ['Edit', 'Clear Fields'],
            ['Help', ['Tutorial', 'About', 'My Github']]]

toolbar_menu = Menu(menu_def, tearoff=True)

app_title = Text('Batch File Renamer', justification='center', size=(50, 1), key='title')

# Folder Chooser
choose_frame = Frame(layout=[[
    Text('Choose Folder:', size=(12, 1)),
    InputText('', enable_events=True, key='path', size=(30, 1)),
    FolderBrowse(target='path')]],
    title='', relief='flat')

# New Name
name_frame = Frame(layout=[[
    Text('New Name:', size=(12, 1)),
    InputText('', key='name', enable_events=False, size=(30, 1))]],
    title='', relief='flat', visible=False)

# File Name Index
index_frame = Frame(layout=[[
    Text('Index Start:', size=(12, 1)),
    InputText('1', size=(7, 1), key='i')]],
    title='', relief='flat', visible=False)

# Number of Files
file_text = Text('', size=(7, 1))
file_frame = Frame(layout=[[
    Text('# of files:', size=(12, 1)),
    file_text]],
    title='', relief='flat', visible=False)

# Number of leading zeros on index, equal to # of digits in # of files
zero_input = InputText('', size=(7, 1), key='z')
zero_frame = Frame(layout=[[
    Text('# of leading 0s:', size=(12, 1)),
    zero_input]],
    title='', relief='flat', visible=False)

# Apply button
apply_frame = Frame(layout=[[
    Button('Apply')]],
    title='', relief='flat', visible=False)

layout = [
    [toolbar_menu],
    [app_title],
    [choose_frame],
    [name_frame],
    [index_frame],
    [file_frame],
    [zero_frame],
    [apply_frame]
]

# Creating window
window = Window('File Renamer v0.1', layout, finalize=True)

while True:
    event, values = window.read()
    print(event, values)

    # If exit, end program
    if event == WIN_CLOSED or event == 'Exit':
        break

    # If path, store path and unhide other frames
    if event == 'path':
        path = str(values['path'])

        # If path is empty, skip rest of iteration
        if path is None or path is '':
            continue
        print(path)

        # Count files
        num_files = 0
        for file in listdir(path):
            if isfile(join(path, file)):
                num_files += 1
                print(file)

        window.finalize()
        name_frame.Update(visible=True)
        index_frame.Update(visible=True)
        file_frame.Update(visible=True)
        file_text.Update(value=num_files)
        zero_input.Update(value=len(str(num_files)))
        zero_frame.Update(visible=True)
        apply_frame.Update(visible=True)

    # If Apply, call function to rename files
    if event == 'Apply':
        rename_files(path=str(values['path']).replace('/', '\\'),
                     name=str(values['name']),
                     i=int(values['i']),
                     z=int(values['z']))

    # TODO: Add event handlers for toolbar

window.close()
