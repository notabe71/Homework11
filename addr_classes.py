from collections import UserDict
from datetime import datetime, timedelta


class Field:
    def __init__(self, value) -> None:
        self.value = value

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return str(self.value)


class Birthday(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        try:
            time_value = datetime.strptime(new_value, "%d/%m/%Y")
            self._value = time_value
        except:
            print("Invalid birthday format")
            raise ValueError("Invalid birthday format")


class Name(Field):
    pass


class Phone(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if new_value.isdigit() and len(new_value) >= 7:
            self._value = new_value
        else:
            raise ValueError("Invalid phone number format")


class Record:
    def __init__(self, name: Name, phone: Phone = None):
        self.name = name
        self.phones = []
        if phone:
            self.phones.append(phone)

        self.birthday = None

    def change_birth(self, birthday):
        self.birthday = birthday
        return f"Birthday of {self.name} is added"

    def days_to_birthday(self):
        if self.birthday == None:
            return f"Birthday of {self.name} is unknown"
        current_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        if current_date.strftime("%m%d") > self.birthday.value.strftime("%m%d"):
            next_birthday = self.birthday.value.replace(year=current_date.year + 1)
        else:
            next_birthday = self.birthday.value.replace(year=current_date.year)

        return (
            f"Birthday of {self.name} is in {(next_birthday - current_date).days} days"
        )

    def add_phone(self, phone: Phone):
        if phone.value not in [p.value for p in self.phones]:
            self.phones.append(phone)
            return f"phone {phone} add to contact {self.name}"
        return f"{phone} present in phones of contact {self.name}"

    def change_phone(self, old_phone, new_phone):
        for idx, p in enumerate(self.phones):
            if old_phone.value == p.value:
                self.phones[idx] = new_phone
                return f"old phone {old_phone} change to {new_phone}"
        return f"{old_phone} not present in phones of contact {self.name}"

    def remove_phone(self, phone) -> None:
        idx = -1

        for i, p in enumerate(self.phones):
            if phone.value == p.value:
                idx = i
                break

        if idx == -1:
            return f"There are no {phone} for {self.name}"
        else:
            self.phones.pop(idx)
            return f"{phone} was deleted successfully"

    def __str__(self) -> str:
        return f"{self.name}: {', '.join(str(p) for p in self.phones)} Birthday: {self.birthday}"


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[str(record.name)] = record
        return f"Contact {record} add success"

    def iterator(self, n):
        result = ""
        count = 0
        for h in self.data.values():
            result += str(h) + "\n"
            count += 1
            if count >= n:
                yield result
                count = 0
                result = ""
        if result:
            yield result

        return ""

    def __str__(self) -> str:
        return "\n".join(str(r) for r in self.data.values())
