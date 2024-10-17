import json

class Word:
    def __init__(self, id_name, dictionary=None):
        self.id_name = id_name
        self.dictionary = dictionary if dictionary is not None else {}

    def __str__(self):
        """Create the representation of the information for the dictionary and the id_name."""
        result = f"Word: {self.id_name}\nDictionary:\n"
        for key, values in self.dictionary.items():
            values_str = ', '.join(map(str, values))
            result += f"  {key}: [{values_str}]\n"
        return result

    def to_dict(self):
        """Convert the object to a dictionary for JSON serialization."""
        return {
            'id_name': self.id_name,
            'dictionary': self.dictionary
        }

    @staticmethod
    def from_dict(data):
        """Creat un Word object from a dictionary."""
        return Word(
            id_name=data['id_name'],
            dictionary=data['dictionary']
        )
