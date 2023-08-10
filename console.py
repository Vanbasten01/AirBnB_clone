#!/usr/bin/python3
'''The HBNBCCommand Class'''
import cmd
from models.base_model import BaseModel
import models
import re
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):

    prompt = "(hbnb)"
    __classes = {
            "BaseModel": BaseModel,
            "User": User,
            "Place": Place,
            "State": State,
            "City": City,
            "Amenity": Amenity,
            "Review": Review
            }

    '''Create a new instance of BaseModel, Save, Print id'''
    def do_create(self, arg):
        if arg:
            if arg in self.__classes:
                new_instance = self.__classes[arg]()
                new_instance.save()
                print(f"{new_instance.id}")
            else:
                print("** class doesn't exist **")
        else:
            print("** class name missing **")

    '''Print the string representation of an instance'''
    def do_show(self, arg):
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in self.__classes:
            print("** class doesn't exist **")
        elif len(args) != 2:
            print("** instance id missing **")
        else:
            all_objects = models.storage.all()
            for key in all_objects.keys():
                class_name, obj_id = key.split('.')
                if args[0] == class_name and args[1] == obj_id:
                    print(all_objects[key])
                    return
            print("** no instance found **")

    '''Delete an instance'''
    def do_destroy(self, arg):
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in self.__classes:
            print("** class doesn't exist **")
        elif len(args) != 2:
            print("** instance id missing **")
        else:
            all_objects = models.storage.all()
            for key in all_objects.keys():
                class_name, obj_id = key.split('.')
                if args[0] == class_name and args[1] == obj_id:
                    del all_objects[key]
                    models.storage.save()
                    return
            print("** no instance found **")

    '''Print all string representation of all instances'''
    def do_all(self, arg):
        args = arg.split()
        if len(args) == 0:
            all_objects = models.storage.all()
            for key in all_objects.keys():
                print(all_objects[key])
        elif len(args) == 1 and args[0] in self.__classes:
            all_objects = models.storage.all()
            for key in all_objects.keys():
                class_name, obj_id = key.split('.')
                if class_name == args[0]:
                    print(all_objects[key])
        else:
            print("** class doesn't exist **")

    '''Ubdate an instance'''
    def do_update(self, arg):
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in self.__classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        instance_id = args[1]
        instance_key = f"{class_name}.{instance_id}"
        obj_dict = models.storage.all()
        if instance_key not in obj_dict:
            print("** no instance found **")
            return
        instance = obj_dict[instance_key]
        if len(args) < 3:
            print("** attribute name missing **")
            return
        attribute_name = args[2]
        if attribute_name in ["id", "created_at", "updated_at"]:
            print("** can't update this attribute **")
            return
        if len(args) < 4:
            print("** value missing **")
            return
        attribute_value = args[3].strip('"')
        setattr(instance, attribute_name, attribute_value)
        instance.save()

    '''Define the count'''
    def do_count(self, arg):
        args = arg.split()
        if len(args) != 1:
            print("** Class name missing **")
        else:
            class_name = args[0]
            if class_name in self.__classes:
                all_objects = models.storage.all()
                count = sum(1 for key in all_objects if key.split('.')[0] == class_name)
                print(count)
            else:
                print("** class doesn't exist **")

    '''Define default'''
    def default(self, arg):
        cmdPattern = r"^([A-Za-z]+)\.([a-z]+)\(([^)]*)\)"
        meth = re.match(cmdPattern, arg)
        if not meth:
            super().default(arg)
            return
        class_name, method, j = meth.groups()
        if class_name not in self.__classes:
            print("** Unknown class:", class_name)
            return
        if method == 'all':
            self.do_all(class_name)
        if method == 'count':
            self.do_count(class_name)
        if method == 'show':
            instance_id = j.strip('"')
            if not instance_id:
                print("** Instance id missing **")
                return
            delf.do_show("{} {}".format(class_name, instance_id))
        if method == 'destroy':
            instance_id = j.strip('"')
            if not instance_id:
                print("** Instance id missing **")
                return
            self.do_destroy("{} {}".format(class_name, instance_id))
        if method == 'update':
            attrib_name, attrib_value = j.split(',', 1)
            attrib_name = attrib_name.strip('"')
            attrib_value = attrib_value.strip('"')
            if not attrib_name or not attrib_value:
                print("** Attribute name or value missing **")
                return
            instance_id = attrib_value.strip('"')
            if not instance_id:
                print("** Instance id missing **")
                return
            self.do_update("{} {} {} {}".format(class_name, instance_id, attrib_name, attrib_value))

    '''Quit command to exit the program'''
    def do_quit(self, arg):
        return True

    '''Exit the program using EOF'''
    def do_EOF(self, arg):
        print()
        return True

    '''Do nothing on an empty line'''
    def emptyline(self):
        pass


if __name__ == "__main__":
    HBNBCommand().cmdloop()
