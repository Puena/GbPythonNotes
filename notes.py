import json
import argparse
import datetime
import os

# Set the default file path for saving notes
NOTE_FILE = 'notes.json'

# Check if the notes file exists, if not create an empty dictionary
if not os.path.isfile(NOTE_FILE):
    with open(NOTE_FILE, 'w') as f:
        json.dump({}, f)


# Add note
def add_note(title, message):
    #validation 
    if title == None or title == "":
        print("title can not be empty")
        return

    # Load existing notes from the file
    with open(NOTE_FILE, 'r') as f:
        notes = json.load(f)

    # Get the current time
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Generate a unique ID for the new note
    note_id = int(max(notes.keys(), default=0)) + 1

    # Add the new note to the dictionary
    notes[note_id] = {'title': title, 'message': message, 'timestamp': timestamp}

    # Write the updated notes dictionary to the file
    with open(NOTE_FILE, 'w') as f:
        json.dump(notes, f)

    print(f'Note added with ID: {note_id}')


# Read note
def read_notes(filter_date):
    # Load existing notes from the file
    with open(NOTE_FILE, 'r') as f:
        notes = json.load(f)

    # Print out each note in the dictionary or print empty
    if len(notes) == 0:
        print("you dont have any notes")
        return

    for note_id, note in notes.items():
        # Do filtration if filter exists
        if filter_date != None:
            f_date = datetime.datetime.strptime(filter_date, "%Y-%m-%d")
            note_date = datetime.datetime.strptime(note["timestamp"].split(" ")[0], "%Y-%m-%d")
            # filter by day
            if f_date != note_date:
                continue

        print(f'ID: {note_id}\nTitle: {note["title"]}\nMessage: {note["message"]}\nCreatedAt: {note["timestamp"]}\n')



# Edit note
def edit_note(note_id, title, message):
    # validation
    if note_id == None: 
        print("wrong id")
        return
    if title == None or title == "": 
        print("title can not be empty")
        return

    # Load existing notes from the file
    with open(NOTE_FILE, 'r') as f:
        notes = json.load(f)

    # Check if the note_id exists in the dictionary
    if note_id not in notes:
        print(f'Note with ID {note_id} does not exist')
        return

    # Update the title and message for the note
    notes[note_id]['title'] = title
    notes[note_id]['message'] = message
    notes[note_id]['timestamp'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Write the updated notes dictionary to the file
    with open(NOTE_FILE, 'w') as f:
        json.dump(notes, f)

    print(f'Note with ID {note_id} updated')


# Delete note
def delete_note(note_id):
    #validation
    if note_id == None:
        print("wrong id")
        return
    # Load existing notes from the file
    with open(NOTE_FILE, 'r') as f:
        notes = json.load(f)

    # Check if the note_id exists in the dictionary
    if note_id not in notes:
        print(f'Note with ID {note_id} does not exist')
        return

    # Delete the note with the given ID
    del notes[note_id]

    # Write the updated notes dictionary to the file
    with open(NOTE_FILE, 'w') as f:
        json.dump(notes, f)

    print(f'Note with ID {note_id} deleted')


# Command line argument parser
parser = argparse.ArgumentParser(description='Note console application')
parser.add_argument('action', choices=['add', 'read', 'edit', 'delete'],
                    help='Action to perform on the notes')
parser.add_argument('--id', help='ID of the note to edit or delete')
parser.add_argument('--title', help='Title of the new note or updated note')
parser.add_argument('--msg', help='Message body of the')
parser.add_argument('--date', help='Filter by timestamp when reading notes, format (Y-m-d)')

# Parse the command line arguments
args = parser.parse_args()

# Call the appropriate function based on the action and arguments
if args.action == 'add':
    add_note(args.title, args.msg)
elif args.action == 'read':
    read_notes(args.date)
elif args.action == 'edit':
    edit_note(args.id, args.title, args.msg)
elif args.action == 'delete':
    delete_note(args.id)
