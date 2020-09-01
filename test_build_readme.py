import build_readme as Subject 
import textwrap

def describe_get_public():
    def with_empty():
        given = []
        expected = []
        assert Subject.get_public(given) == expected

    def with_public_and_private_values():
        given = [
            {
                "name": "Public Item",
                "public": True
            },
            {
                "name": "Private Item",
                "public": False
            },
        ]
        expected = [
            {
                "name": "Public Item",
                "public": True
            }
        ]
        assert Subject.get_public(given) == expected