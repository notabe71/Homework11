from addr_classes import Name, Phone, Birthday, Record, AddressBook

address_book = AddressBook()


def input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        except KeyError:
            return "Enter user name"
        except ValueError:
            return "Give me correct data "
        except IndexError:
            return "Invalid command or syntax"

    return wrapper


@input_error
def add_command(*args):
    name = Name(args[0])
    if len(args) > 1:
        phone = Phone(args[1])
        rec: Record = address_book.get(str(name))
        if rec:
            return rec.add_phone(phone)
        rec = Record(name, phone)
    else:
        rec = Record(name)
    return address_book.add_record(rec)


@input_error
def print_contacts(*args):
    if len(args) > 0 and args[0].isdigit():
        N = int(args[0])
    else:
        N = 5

    for rec in address_book.iterator(N):
        print(rec)
        print("-" * 40)

    return ""


@input_error
def birthday_command(*args):
    name = Name(args[0])
    birthday = Birthday(args[1])
    rec: Record = address_book.get(str(name))
    if rec:
        return rec.change_birth(birthday)
    return f"No contact {name} in address book"


@input_error
def change_command(*args):
    name = Name(args[0])
    old_phone = Phone(args[1])
    new_phone = Phone(args[2])
    rec: Record = address_book.get(str(name))
    if rec:
        return rec.change_phone(old_phone, new_phone)
    return f"No contact {name} in address book"


@input_error
def remove_command(*args):
    name = Name(args[0])
    phone = Phone(args[1])
    rec: Record = address_book.get(str(name))
    print(rec)
    if rec:
        return rec.remove_phone(phone)
    return f"No phone {phone} for contact {name}"


@input_error
def days_to_birthday(*args):
    name = Name(args[0])
    rec: Record = address_book.get(str(name))
    if rec:
        return rec.days_to_birthday()
    return f"No records for contact {name}"


def exit_command(*args):
    return "Bye"


def hello_command(*args):
    return "How can I help you?"


def unknown_command(*args):
    pass


def show_all_command(*args):
    return address_book


COMMANDS = {
    add_command: ("add", "+"),
    change_command: ("change", "зміни"),
    remove_command: ("remove", "-"),
    hello_command: ("hello",),
    exit_command: ("bye", "exit", "end", "close", "quit"),
    show_all_command: ("show all",),
    birthday_command: ("birthday",),
    days_to_birthday: ("days to birthday",),
    print_contacts: ("print contacts",),
}


def parser(text: str):
    for cmd, kwds in COMMANDS.items():
        for kwd in kwds:
            if text.lower().startswith(kwd):
                data = text[len(kwd) :].strip().split()
                return cmd, data
    return unknown_command, []


def main():
    while True:
        user_input = input(">>>")

        cmd, data = parser(user_input)

        result = cmd(*data)

        print(result)

        if cmd == exit_command:
            break


if __name__ == "__main__":
    main()
