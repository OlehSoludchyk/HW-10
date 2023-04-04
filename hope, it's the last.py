import re
from collections import UserDict

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            print('There isn\'t contact with this name or number.')
        except ValueError:
            print('''Please enter the correct format of name and phone number.
            Correct format:
            1. The length of the nunber must be only 12 digits.
            2. Use a gap between name and number.''')
    return wrapper

class Field:
    def __init__(self, value):
        self.value = value

class Name(Field):
    def __init__(self, value):
      if not value:
        raise ValueError('Name cannot be empty')
      self.value = value

class Phone(Field):
    def __init__(self, value=None):
        if value is not None:
            if not isinstance(value, str):
                raise TypeError('Phone must be a string')
            if not value.isdigit():
                raise ValueError('Phone must be a combination of digits')
            if len(value) != 12:
                raise ValueError('Phone number must have a 12 digits')
        self.value = value

class Record:
    def __init__(self, name, phone=None):
        self.name = name
        self.phones = []
        if phone is not None:
            self.add_phone(phone)

    def add_phone(self, phone):
        self.phones.append(phone)

    def remove_phone(self, phone):
        if phone in self.phones:
            self.phones.remove(phone)

    def edit_phone(self, old_phone, new_phone):
        for i, phone in enumerate(self.phones):
            if phone.value == old_phone.value:
                self.phones[i] = new_phone


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def remove_record(self, name):
        if name in self.data:
            del self.data[name]
            return True
        return False

    def find_records_by_name(self, name):
        found_records = []
        for record_name in self.data.keys():
            if record_name.lower() == name.lower():
                found_records.append(self.data[record_name])
        return found_records

    def find_records_by_phone(self, phone):
        found_records = []
        for record in self.data.values():
            for record_phone in record.phones:
                if record_phone.value == phone:
                    found_records.append(record)
        return found_records

    def change_phone(self, name, old_phone, new_phone):
        if name in self.data:
            record = self.data[name]
            if not isinstance(old_phone, Phone):
                old_phone = Phone(old_phone)
            if not isinstance(new_phone, Phone):
                new_phone = Phone(new_phone)
            if record.edit_phone(old_phone, new_phone):
                print(f'Phone number for contact {name} has been changed from {old_phone} to {new_phone}.')
        else:
            print(f'There is no contact with name "{name}".')

@input_error
def add_contact(user_input, address_book):
    match = re.match(r'add (\w+) (\d{12})', user_input)
    if match:
      name = match.group(1)
      phone = match.group(2)
      record_name = Name(name)
      record = Record(record_name, Phone(phone))
    # record.add_phone(phone)
      address_book.add_record(record)
      print(f'Contact {name} has been added.')
    else:
      raise ValueError


def show_all_contacts(address_book):
    if address_book:
        for record in address_book.values():
            for phone in record.phones:
                print(f'{record.name.value} - {phone.value}')
    else:
        print('There are no contacts.')

def remove_contact(user_input, address_book):
    match = re.match(r'remove (\w+)', user_input)
    if match:
        name = match.group(1)
        if address_book.remove_record(name):
            print(f'Contact {name} has been removed.')
        else:
            print(f'There is no contact with name "{name}".')

@input_error
def find_contacts(user_input, address_book):
    match = re.match(r'find (\w+)', user_input)
    if match:
        name_or_phone = match.group(1)
        records_by_name = address_book.find_records_by_name(name_or_phone)
        records_by_phone = address_book.find_records_by_phone(name_or_phone)
        if records_by_name or records_by_phone:
            print('Contacts found:')
            for record in records_by_name + records_by_phone:
                for phone in record.phones:
                    print(f'{record.name.value} - {phone.value}')
        else:
            print('No contacts were found.')
    else:
        raise KeyError

def change_phone(user_input, address_book):
    match = re.match(r'change (\w+) (\d{12}) (\d{12})', user_input)
    if match:
        name = match.group(1)
        old_phone = match.group(2)
        new_phone = match.group(3)
        address_book.change_phone(name, Phone(old_phone), Phone(new_phone))

def main():
    print('''What can this bot do?
    1. Save the contact (name and phone number). Please, remember: number - only 12 digits.
    Use command: add [name] [number]
    2. Change the phone number of the recorded contact. Please, remember: number - only 12 digits.
    Use command: change [name] [old_number] [new_number]
    3. Show all previously saved contacts.
    Use command: show all.
    4. Remove the contact.
    Use command: remove [name]
    5. Find the contact by name or by phone.
    Use command: find [name] or [phone]''')
    address_book = AddressBook()
    while True:
        user_input = input('Enter a command >>> ')
        if user_input.lower() == 'hello':
            print('How can I help you?')
        elif user_input.lower().startswith('add'):
            add_contact(user_input, address_book)
        elif user_input.lower() == 'show all':
            show_all_contacts(address_book)
        elif user_input.lower().startswith('remove'):
            remove_contact(user_input, address_book)
        elif user_input.lower().startswith('find'):
            find_contacts(user_input, address_book)
        elif user_input.lower().startswith('change'):
            change_phone(user_input, address_book)
        elif user_input.lower() in ['exit', 'close', 'good bye']:
            print('Good bye!')
            raise SystemExit
        else:
            print('Sorry, I don\'t understand you. Use the available command.')


if __name__ == '__main__':
    main()