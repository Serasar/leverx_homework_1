import json
import argparse
import xml_converter



class FileParser:
    def __init__(self):
        self.students = []
        self.rooms = []

    def load_students(self, filepath):
        self.students = json.loads(open(filepath).read())

    def load_rooms(self, filepath):
        self.rooms = json.loads(open(filepath).read())

    def search_for_student(self, student_room):
        return [student for student in self.students if student["room"] == student_room]

    def assign_students_to_rooms(self):
        for room in self.rooms:
            room["student_list"] = self.search_for_student(room["id"])

    def save_rooms_to_json(self, filepath):
        open(filepath, "w").write(json.dumps(self.rooms, indent=4, sort_keys=True))

    def save_rooms_to_xml(self, filepath):
        open(filepath, "w").write(xml_converter.dicttoxml(self.rooms, attr_type=False).decode('utf-8'))


class CLI:
    def __init__(self):
        self.cli_parser = argparse.ArgumentParser()

        self.cli_parser.add_argument('--students')
        self.cli_parser.add_argument('--rooms')
        self.cli_parser.add_argument('--format')

        self.cli_args = self.cli_parser.parse_args()

    def process_args(self):
        parser_instance = FileParser()
        parser_instance.load_rooms(self.cli_args.rooms)
        parser_instance.load_students(self.cli_args.students)
        parser_instance.assign_students_to_rooms()
        if self.cli_args.format.lower() == "json":
            parser_instance.save_rooms_to_json("output.json")
        elif self.cli_args.format.lower() == "xml":
            parser_instance.save_rooms_to_xml("output.xml")
        else:
            print("format must be JSON or XML")


cli_instance = CLI()
cli_instance.process_args()
