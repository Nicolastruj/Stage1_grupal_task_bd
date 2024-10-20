class Word:
    def __init__(self, id_name, dictionary=None):
        """
        Initialize a Word object.

        :param id_name: The name or identifier of the word.
        :param dictionary: An optional dictionary to hold positions of the word. Defaults to an empty dictionary if not provided.
        """
        self.id_name = id_name
        self.dictionary = dictionary if dictionary is not None else {}

    def __str__(self):
        """
        Create a string representation of the Word object, including its id_name and dictionary.

        :return: A string representation of the Word object.
        """
        result = f"Word: {self.id_name}\nDictionary:\n"
        for key, values in self.dictionary.items():
            values_str = ', '.join(map(str, values))
            result += f"  {key}: [{values_str}]\n"
        return result

    def to_dict(self):
        """
        Convert the Word object to a dictionary for JSON serialization.

        :return: A dictionary representation of the Word object.
        """
        return {
            'id_name': self.id_name,
            'dictionary': self.dictionary
        }

    @staticmethod
    def from_dict(data):
        """
        Create a Word object from a dictionary.

        :param data: A dictionary containing the word's id_name and its dictionary.
        :return: A Word object created from the provided dictionary.
        """
        return Word(
            id_name=data['id_name'],
            dictionary=data['dictionary']
        )
