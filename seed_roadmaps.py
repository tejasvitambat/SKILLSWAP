from app import app
from extensions import db
from models import Skill, Roadmap, RoadmapTopic, TopicProgress, TopicTask

# ============================================================
# SKILLSWAP - FINAL ROADMAP SEED
# ============================================================
# Coding skills intentionally kept ACTIVE:
#   Python, Java, JavaScript, C++, SQL
#
# Existing non-coding skills/roadmaps are preserved.
# C, C# and PHP are deactivated because the project now keeps
# exactly five coding skills.
#
# Every coding topic contains:
#   title + explanation + code example + practical task
#
# IMPORTANT:
# This script does NOT delete users, skills, roadmaps or progress.
# It stops if learner progress exists, so topic IDs are not
# silently remapped underneath an existing learner.
# ============================================================

CODING_CURRICULUM = {}


def add(skill, title, explanation, code_example, task):
    CODING_CURRICULUM.setdefault(skill, []).append(
        (title, explanation, code_example, task)
    )


# ============================================================
# PYTHON
# ============================================================

PYTHON = "Python"

python_topics = [
    ("Introduction",
     "Python is a readable general-purpose programming language used for automation, web development, data work, scripting and many other applications.",
     'print("Hello, SkillSwap!")',
     "Write a Python program that prints your name and a welcome message."),

    ("Get Started",
     "A Python program is normally saved in a .py file and executed by the Python interpreter.",
     'print("My first Python program")',
     "Create a Python file and run it successfully with at least two print statements."),

    ("Syntax",
     "Python uses indentation to define code blocks. Correct indentation and valid statements are essential for a program to run.",
     'age = 20\nif age >= 18:\n    print("Adult")',
     "Write a program containing a variable, an if statement and a correctly indented block."),

    ("Output",
     "The print() function displays text and values. Multiple values can be printed together.",
     'name = "Tejasvi"\nage = 20\nprint("Name:", name)\nprint("Age:", age)',
     "Print your name, age and city using clear labels."),

    ("Comments",
     "Comments explain code for humans and are ignored by the Python interpreter. A single-line comment starts with #.",
     '# Store the learner name\nname = "Tejasvi"\nprint(name)',
     "Add at least two meaningful comments to a small Python program."),

    ("Variables",
     "Variables are names that refer to values. Python creates a variable when a value is assigned to it.",
     'name = "Tejasvi"\nage = 20\ncity = "Pune"\nprint(name, age, city)',
     "Create name, age and city variables and print all three."),

    ("Data Types",
     "Python commonly uses int, float, str and bool values. Each represents a different kind of data.",
     'age = 20\nheight = 1.54\nname = "Tejasvi"\nactive = True\nprint(type(age), type(height), type(name), type(active))',
     "Create one integer, one float, one string and one boolean, then display their values and types."),

    ("Numbers",
     "Python supports integers and floating-point numbers with arithmetic operations such as addition, subtraction, multiplication and division.",
     'a = 10\nb = 3\nprint(a + b)\nprint(a - b)\nprint(a * b)\nprint(a / b)',
     "Create two numbers and print their sum, difference, product and division."),

    ("Casting",
     "Casting converts a value from one compatible type to another, such as converting numeric text into an integer.",
     'age_text = "20"\nage = int(age_text)\nprint(age + 5)',
     "Convert a numeric string to an integer and use it in a calculation."),

    ("Strings",
     "Strings store text and support indexing, slicing and methods such as upper(), lower() and replace().",
     'text = "SkillSwap"\nprint(text.upper())\nprint(text.lower())\nprint(text[0:5])',
     "Create a sentence and display an uppercase version, lowercase version and a slice."),

    ("Booleans",
     "Boolean values are True and False. They are commonly produced by comparisons and used in decisions.",
     'age = 20\nis_adult = age >= 18\nprint(is_adult)',
     "Create a boolean expression that checks an eligibility condition."),

    ("Operators",
     "Python provides arithmetic, comparison, logical and assignment operators for working with values.",
     'a = 10\nb = 5\nprint(a + b)\nprint(a > b)\nprint(a > 5 and b < 10)',
     "Build a small calculator using arithmetic and comparison operators."),

    ("Lists",
     "Lists are ordered and changeable collections. Items can be accessed by index and modified with list methods.",
     'skills = ["Python", "Java", "SQL"]\nskills.append("C++")\nprint(skills)',
     "Create a five-item list, add one item, remove one item and print the final list."),

    ("Tuples",
     "Tuples are ordered collections that are normally immutable after creation and are useful for fixed groups of values.",
     'student = ("Tejasvi", 20, "Pune")\nprint(student[0])',
     "Create a tuple containing name, age and city and access each value."),

    ("Sets",
     "Sets store unique values and automatically remove duplicate values.",
     'skills = {"Python", "Java", "Python", "SQL"}\nprint(skills)',
     "Create duplicate data and use a set to keep only unique values."),

    ("Dictionaries",
     "Dictionaries store key-value pairs and are useful for structured records.",
     'student = {"name": "Tejasvi", "age": 20, "city": "Pune"}\nprint(student["name"])',
     "Create a student dictionary with at least three fields and print two values."),

    ("If Else",
     "if and else allow a program to choose between alternatives based on a condition.",
     'marks = 72\nif marks >= 40:\n    print("Pass")\nelse:\n    print("Fail")',
     "Create a pass/fail checker using if and else."),

    ("Elif",
     "elif lets a program test several conditions in sequence until one condition is true.",
     'marks = 82\nif marks >= 90:\n    print("A+")\nelif marks >= 75:\n    print("A")\nelse:\n    print("B")',
     "Create a grade program with at least four grade ranges."),

    ("Match",
     "match compares a value with several cases and is useful for menu-style decisions in modern Python.",
     'choice = 2\nmatch choice:\n    case 1: print("Add")\n    case 2: print("View")\n    case _: print("Invalid")',
     "Create a menu with at least three match cases and an invalid case."),

    ("While Loops",
     "A while loop repeats a block while its condition remains true. The loop should eventually make its condition false.",
     'i = 1\nwhile i <= 5:\n    print(i)\n    i += 1',
     "Use a while loop to print numbers from 1 through 10."),

    ("For Loops",
     "A for loop iterates through a sequence such as a list, string or range.",
     'for i in range(1, 6):\n    print(i)',
     "Use a for loop to print a multiplication table."),

    ("Break Continue Pass",
     "break stops a loop, continue skips the current iteration and pass acts as a placeholder statement.",
     'for i in range(1, 8):\n    if i == 4:\n        continue\n    print(i)',
     "Create a loop that skips one value and stops at another."),

    ("Functions",
     "Functions package reusable logic. They can accept parameters and return values.",
     'def add(a, b):\n    return a + b\n\nprint(add(10, 5))',
     "Create a function that accepts two numbers and returns their sum. Call it twice."),

    ("Lambda",
     "A lambda expression creates a small anonymous function and is useful for short expressions.",
     'square = lambda x: x * x\nprint(square(5))',
     "Create a lambda function that calculates the cube of a number."),

    ("Scope",
     "Scope controls where a variable can be accessed. Variables created inside a function are normally local to that function.",
     'name = "Global"\n\ndef show():\n    local = "Local"\n    print(name, local)\n\nshow()',
     "Create a function with a local variable and demonstrate local versus global access."),

    ("Modules",
     "Modules organize reusable Python code. Built-in and external modules can be imported when needed.",
     'import math\nprint(math.sqrt(25))\nprint(math.pi)',
     "Import a standard module and use at least two of its features."),

    ("Dates",
     "The datetime module provides tools for representing and working with dates and times.",
     'from datetime import date\nprint(date.today())',
     "Print today's date and extract its year."),

    ("Math",
     "The math module provides mathematical functions and constants such as square root, ceiling and floor.",
     'import math\nprint(math.sqrt(81))\nprint(math.ceil(4.2))\nprint(math.floor(4.8))',
     "Use sqrt, ceil and floor in one program."),

    ("JSON",
     "JSON is a common format for exchanging structured data. Python's json module converts between Python objects and JSON text.",
     'import json\ndata = {"name": "Tejasvi", "age": 20}\ntext = json.dumps(data)\nprint(text)',
     "Convert a dictionary to JSON text and print it."),

    ("Regular Expressions",
     "Regular expressions describe text patterns. Python provides regular-expression support through the re module.",
     'import re\ntext = "Email test@example.com"\nmatch = re.search(r"\\S+@\\S+", text)\nprint(match.group() if match else "Not found")',
     "Use a regular expression to find an email-like value in a string."),

    ("PIP",
     "PIP is Python's package-management tool and is commonly used to install third-party libraries.",
     'import sys\nprint(sys.version)',
     "Identify one useful Python package and document the PIP command that would install it."),

    ("Try Except",
     "try and except allow a program to handle expected runtime errors instead of terminating unexpectedly.",
     'try:\n    n = int(input("Number: "))\n    print(n)\nexcept ValueError:\n    print("Invalid number")',
     "Write a program that safely handles invalid numeric input."),

    ("File Handling",
     "Python can read, write and append text files. The with statement safely manages file resources.",
     'with open("notes.txt", "w") as f:\n    f.write("SkillSwap")\n\nwith open("notes.txt", "r") as f:\n    print(f.read())',
     "Create a text file, write a note and read it back."),

    ("Python Database",
     "Python applications can communicate with databases using database drivers or libraries and can execute SQL queries from code.",
     'import sqlite3\nconn = sqlite3.connect("example.db")\nconn.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, title TEXT)")\nconn.close()',
     "Create a small SQLite database, create one table and insert one record."),

    ("Classes and Objects",
     "Classes define attributes and methods, while objects are instances created from those classes.",
     'class Student:\n    def __init__(self, name):\n        self.name = name\n\n    def show(self):\n        print(self.name)\n\nStudent("Tejasvi").show()',
     "Create a Student class with a name attribute and a display method."),

    ("Inheritance and Polymorphism",
     "Inheritance lets a child class reuse parent behavior. Polymorphism lets different objects provide their own implementation of the same method.",
     'class Animal:\n    def sound(self):\n        print("Animal")\n\nclass Dog(Animal):\n    def sound(self):\n        print("Woof")\n\nfor item in [Animal(), Dog()]:\n    item.sound()',
     "Create a parent class and two child implementations with the same method name."),

    ("Python Mini Project",
     "A project combines core Python concepts into one useful application and gives practice in structuring a complete program.",
     'tasks = []\ntasks.append("Learn Python")\nprint(tasks)',
     "Build a small task manager, student record system or calculator using functions and at least two other Python concepts."),
]

for row in python_topics:
    add(PYTHON, *row)


# ============================================================
# JAVA
# ============================================================

JAVA = "Java"

java_topics = [
    ("Introduction", "Java is a general-purpose, object-oriented programming language used to build many kinds of applications.", 'System.out.println("Hello, SkillSwap!");'),
    ("Get Started", "The JDK provides the tools needed to write, compile and run Java programs.", 'public class Main { public static void main(String[] args) { System.out.println("Ready"); } }'),
    ("Syntax", "Java uses classes, methods, statements, braces and semicolons to structure programs.", 'public class Main { public static void main(String[] args) { System.out.println("Syntax"); } }'),
    ("Output", "System.out.println displays values in the console.", 'String name = "Tejasvi"; System.out.println("Name: " + name);'),
    ("Comments", "Java supports comments that document source code and are ignored during execution.", '// Learner name\nString name = "Tejasvi";\nSystem.out.println(name);'),
    ("Variables", "Java variables are declared with a data type and store values of that type.", 'String name = "Tejasvi";\nint age = 20;\nSystem.out.println(name + age);'),
    ("Data Types", "Java provides primitive types such as int, double, char and boolean along with reference types.", 'int age = 20;\ndouble height = 1.54;\nchar grade = \'A\';\nboolean active = true;'),
    ("Type Casting", "Casting converts a value from one compatible type to another.", 'double price = 10.8;\nint value = (int) price;\nSystem.out.println(value);'),
    ("Input", "Scanner can read values entered by a user from the console.", 'Scanner sc = new Scanner(System.in);\nString name = sc.nextLine();\nSystem.out.println(name);'),
    ("Operators", "Java supports arithmetic, comparison, logical and assignment operators.", 'int a = 10, b = 5;\nSystem.out.println(a + b);\nSystem.out.println(a > b);'),
    ("If Else", "if and else choose code based on whether a condition is true or false.", 'int marks = 70;\nif (marks >= 40) System.out.println("Pass");\nelse System.out.println("Fail");'),
    ("Switch", "switch handles multiple known choices based on the value of an expression.", 'int choice = 2;\nswitch (choice) {\n    case 1: System.out.println("Add"); break;\n    case 2: System.out.println("View"); break;\n    default: System.out.println("Invalid");\n}'),
    ("For Loop", "A for loop repeats code using initialization, a condition and an update expression.", 'for (int i = 1; i <= 5; i++) System.out.println(i);'),
    ("While Loop", "A while loop repeats while its condition remains true.", 'int i = 1;\nwhile (i <= 5) {\n    System.out.println(i);\n    i++;\n}'),
    ("Arrays", "Arrays store a fixed-size sequence of values of one type.", 'int[] marks = {80, 75, 90};\nSystem.out.println(marks[0]);'),
    ("Strings", "String provides methods for storing and manipulating text.", 'String text = "SkillSwap";\nSystem.out.println(text.toUpperCase());'),
    ("Methods", "Methods provide reusable behavior and may accept parameters and return values.", 'static int add(int a, int b) {\n    return a + b;\n}'),
    ("Classes and Objects", "Classes define fields and methods while objects are instances created from classes.", 'class Student {\n    String name;\n    void show() { System.out.println(name); }\n}'),
    ("Constructors", "Constructors initialize an object when it is created.", 'class Student {\n    String name;\n    Student(String n) { name = n; }\n}'),
    ("Encapsulation", "Encapsulation keeps data and behavior together and uses access modifiers to control visibility.", 'class Student {\n    private String name;\n    public void setName(String name) { this.name = name; }\n    public String getName() { return name; }\n}'),
    ("Inheritance", "A child class can reuse behavior from a parent class using extends.", 'class Animal { void sound() { System.out.println("Sound"); } }\nclass Dog extends Animal {}'),
    ("Interfaces and Polymorphism", "Interfaces define behavior contracts and polymorphism allows different implementations of the same contract.", 'interface Shape { void draw(); }\nclass Circle implements Shape {\n    public void draw() { System.out.println("Circle"); }\n}'),
    ("Exception Handling", "try and catch allow Java programs to handle runtime errors safely.", 'try {\n    int x = Integer.parseInt("abc");\n} catch (NumberFormatException e) {\n    System.out.println("Invalid");\n}'),
    ("Collections", "Collections such as ArrayList, HashSet and HashMap provide flexible data structures.", 'ArrayList<String> skills = new ArrayList<>();\nskills.add("Python");'),
    ("File Handling", "Java file APIs allow programs to create, write and read persistent files.", 'FileWriter writer = new FileWriter("notes.txt");\nwriter.write("SkillSwap");\nwriter.close();'),
    ("Java Mini Project", "A project combines syntax, methods, collections, OOP and error handling into a useful application.", 'System.out.println("Java Project");'),
]

for title, explanation, code in java_topics:
    add(
        JAVA,
        title,
        explanation,
        code,
        f"Complete a practical {title} exercise. Your Java program must demonstrate the concept and run without errors."
    )


# ============================================================
# JAVASCRIPT
# ============================================================

JAVASCRIPT = "JavaScript"

javascript_topics = [
    ("Introduction", "JavaScript is a programming language widely used in browsers and also in server-side environments.", 'console.log("Hello, SkillSwap!");'),
    ("Get Started", "JavaScript can be executed in a browser console or inside a script loaded by an HTML page.", 'console.log("My first JavaScript program");'),
    ("Syntax and Comments", "JavaScript uses statements, blocks and comments to organize source code.", '// greeting\nlet name = "Tejasvi";\nconsole.log(name);'),
    ("Variables", "let creates a reassignable variable while const creates a binding that should not be reassigned.", 'let age = 20;\nconst city = "Pune";\nconsole.log(age, city);'),
    ("Data Types", "JavaScript supports strings, numbers, booleans, null, undefined, arrays and objects.", 'let name = "Tejasvi";\nlet age = 20;\nlet active = true;'),
    ("Operators", "JavaScript supports arithmetic, comparison, logical and assignment operators.", 'let a = 10, b = 5;\nconsole.log(a + b, a > b);'),
    ("Conditions", "if, else if and else control which code runs based on conditions.", 'let marks = 75;\nif (marks >= 40) console.log("Pass");\nelse console.log("Fail");'),
    ("Switch", "switch selects a matching case from several known choices.", 'let choice = 2;\nswitch (choice) {\n    case 1: console.log("Add"); break;\n    case 2: console.log("View"); break;\n    default: console.log("Invalid");\n}'),
    ("For Loop", "for loops repeat code using initialization, condition and update expressions.", 'for (let i = 1; i <= 5; i++) console.log(i);'),
    ("While Loop", "while repeats code while its condition remains true.", 'let i = 1;\nwhile (i <= 5) {\n    console.log(i);\n    i++;\n}'),
    ("Functions", "Functions package reusable logic and can accept parameters and return values.", 'function add(a, b) { return a + b; }\nconsole.log(add(10, 5));'),
    ("Arrow Functions", "Arrow functions provide concise syntax for writing function expressions.", 'const square = x => x * x;\nconsole.log(square(5));'),
    ("Arrays", "Arrays store ordered collections and provide methods such as push, map, filter and pop.", 'const skills = ["Python", "Java"];\nskills.push("SQL");\nconsole.log(skills);'),
    ("Objects", "Objects store related data as properties and can contain methods.", 'const student = { name: "Tejasvi", age: 20 };\nconsole.log(student.name);'),
    ("Destructuring and Spread", "Destructuring extracts values from arrays or objects while spread syntax copies or combines collections.", 'const user = { name: "Tejasvi", age: 20 };\nconst { name, age } = user;\nconsole.log(name, age);'),
    ("DOM Fundamentals", "The DOM represents an HTML document and allows JavaScript to read and change page elements.", 'document.getElementById("title").textContent = "SkillSwap";'),
    ("Events", "Events allow JavaScript to respond to clicks, input, submit and other browser actions.", 'document.getElementById("btn").addEventListener("click", () => alert("Clicked"));'),
    ("Forms and Validation", "JavaScript can read form values and validate input before processing or submitting it.", 'const value = document.getElementById("name").value;\nif (!value) alert("Required");'),
    ("JSON", "JSON is a common text format for exchanging structured data between applications.", 'const user = { name: "Tejasvi" };\nconst text = JSON.stringify(user);\nconsole.log(text);'),
    ("Promises and Async Await", "Promises represent asynchronous work while async and await provide readable asynchronous control flow.", 'async function load() {\n    const value = await Promise.resolve("SkillSwap");\n    console.log(value);\n}\nload();'),
    ("Fetch and APIs", "fetch sends HTTP requests and can process responses such as JSON from an API.", 'fetch("/api/skills").then(r => r.json()).then(data => console.log(data));'),
    ("Local Storage", "localStorage stores small string values in the browser across page reloads.", 'localStorage.setItem("skill", "Python");\nconsole.log(localStorage.getItem("skill"));'),
    ("JavaScript Mini Project", "A project combines DOM, events, arrays, objects and browser storage into a working application.", 'const tasks = [];\ntasks.push("Learn JavaScript");\nconsole.log(tasks);'),
]

for title, explanation, code in javascript_topics:
    add(
        JAVASCRIPT,
        title,
        explanation,
        code,
        f"Complete a practical {title} exercise and verify the result in the browser or JavaScript runtime."
    )


# ============================================================
# C++
# ============================================================

CPP = "C++"

cpp_topics = [
    ("Introduction", "C++ is a compiled language supporting procedural, object-oriented and generic programming.", '#include <iostream>\nint main() { std::cout << "Hello, SkillSwap!"; }'),
    ("Get Started", "A C++ source file is compiled into an executable program before it is run.", '#include <iostream>\nint main() { std::cout << "Ready"; return 0; }'),
    ("Syntax", "C++ programs use headers, functions, statements, braces and semicolons.", '#include <iostream>\nint main() { std::cout << "Syntax"; return 0; }'),
    ("Variables and Data Types", "Common C++ types include int, double, char, bool and string.", 'int age = 20;\ndouble height = 1.54;\nchar grade = \'A\';\nbool active = true;'),
    ("Input and Output", "cin reads console input and cout displays output.", 'std::string name;\nstd::cin >> name;\nstd::cout << "Hello " << name;'),
    ("Operators", "C++ provides arithmetic, comparison, logical and assignment operators.", 'int a = 10, b = 5;\nstd::cout << a + b << " " << (a > b);'),
    ("If Else", "if and else select code based on whether a condition is true.", 'int marks = 70;\nif (marks >= 40) std::cout << "Pass";\nelse std::cout << "Fail";'),
    ("Switch", "switch selects a matching case from several choices.", 'int choice = 2;\nswitch (choice) {\n    case 1: std::cout << "Add"; break;\n    case 2: std::cout << "View"; break;\n    default: std::cout << "Invalid";\n}'),
    ("Loops", "for, while and do-while loops repeat blocks of code.", 'for (int i = 1; i <= 5; i++) std::cout << i << std::endl;'),
    ("Functions", "Functions organize reusable logic and can return values.", 'int add(int a, int b) { return a + b; }'),
    ("Arrays", "Arrays store a fixed-size sequence of values of the same type.", 'int marks[3] = {80, 75, 90};\nstd::cout << marks[0];'),
    ("Strings", "std::string stores text and provides common text operations.", 'std::string text = "SkillSwap";\nstd::cout << text.length();'),
    ("Pointers", "Pointers store memory addresses and can be dereferenced to access the value at that address.", 'int age = 20;\nint* ptr = &age;\nstd::cout << *ptr;'),
    ("References", "References provide another name for an existing variable.", 'int age = 20;\nint& ref = age;\nref = 21;\nstd::cout << age;'),
    ("Classes and Objects", "Classes define fields and methods while objects are instances of those classes.", 'class Student {\npublic:\n    std::string name;\n    void show() { std::cout << name; }\n};'),
    ("Constructors and Encapsulation", "Constructors initialize objects and access modifiers control visibility of class members.", 'class Student {\n    std::string name;\npublic:\n    Student(std::string n) : name(n) {}\n    void show() { std::cout << name; }\n};'),
    ("Inheritance", "A derived class can reuse members from a base class.", 'class Animal { public: void sound() { std::cout << "Sound"; } };\nclass Dog : public Animal {};'),
    ("Polymorphism", "Virtual functions allow derived classes to provide different implementations of the same interface.", 'class Animal { public: virtual void sound() { std::cout << "Animal"; } };\nclass Dog : public Animal { public: void sound() override { std::cout << "Dog"; } };'),
    ("STL Vector", "std::vector is a dynamic sequence container that grows as elements are added.", 'std::vector<std::string> skills = {"Python", "Java"};\nskills.push_back("SQL");'),
    ("STL Map and Set", "map stores key-value pairs while set stores unique ordered values.", 'std::map<std::string, int> ages;\nages["Tejasvi"] = 20;'),
    ("File Handling", "fstream classes allow C++ programs to write and read persistent files.", 'std::ofstream out("notes.txt");\nout << "SkillSwap";\nout.close();'),
    ("C++ Mini Project", "A project combines functions, collections, OOP and file handling into a useful application.", 'int main() { std::cout << "C++ Project"; }'),
]

for title, explanation, code in cpp_topics:
    add(
        CPP,
        title,
        explanation,
        code,
        f"Complete a practical {title} exercise and make sure the program compiles and runs correctly."
    )


# ============================================================
# SQL
# ============================================================

SQL = "SQL"

sql_topics = [
    ("Database Fundamentals", "Relational databases store structured information in tables containing rows and columns.", 'CREATE TABLE students (id INT PRIMARY KEY, name VARCHAR(100), age INT);'),
    ("SELECT", "SELECT retrieves data from one or more tables.", 'SELECT name, age FROM students;'),
    ("WHERE", "WHERE filters rows according to conditions.", 'SELECT * FROM students WHERE age >= 18;'),
    ("ORDER BY", "ORDER BY sorts returned rows in ascending or descending order.", 'SELECT * FROM students ORDER BY age DESC;'),
    ("LIMIT", "LIMIT restricts the number of rows returned in database systems that support it.", 'SELECT * FROM students ORDER BY age DESC LIMIT 5;'),
    ("INSERT", "INSERT adds new rows to a table.", "INSERT INTO students (id, name, age) VALUES (1, 'Tejasvi', 20);"),
    ("UPDATE", "UPDATE changes existing rows and should normally use WHERE for targeted changes.", 'UPDATE students SET age = 21 WHERE id = 1;'),
    ("DELETE", "DELETE removes rows and should normally use WHERE for targeted deletion.", 'DELETE FROM students WHERE id = 1;'),
    ("Aggregate Functions", "COUNT, SUM, AVG, MIN and MAX summarize data.", 'SELECT COUNT(*), AVG(age), MIN(age), MAX(age) FROM students;'),
    ("GROUP BY", "GROUP BY creates groups so aggregate calculations can be performed for each group.", 'SELECT city, COUNT(*) FROM students GROUP BY city;'),
    ("HAVING", "HAVING filters groups after GROUP BY, often using aggregate expressions.", 'SELECT city, COUNT(*) AS total FROM students GROUP BY city HAVING COUNT(*) >= 2;'),
    ("INNER JOIN", "INNER JOIN returns rows where related values exist in both tables.", 'SELECT students.name, courses.title FROM students INNER JOIN courses ON students.course_id = courses.id;'),
    ("LEFT JOIN", "LEFT JOIN keeps every row from the left table and adds matching right-side data when available.", 'SELECT students.name, courses.title FROM students LEFT JOIN courses ON students.course_id = courses.id;'),
    ("Subqueries", "A subquery is a query nested inside another query.", 'SELECT name FROM students WHERE age > (SELECT AVG(age) FROM students);'),
    ("Constraints", "PRIMARY KEY, FOREIGN KEY, UNIQUE, NOT NULL and CHECK enforce data rules.", 'CREATE TABLE users (id INT PRIMARY KEY, email VARCHAR(150) UNIQUE NOT NULL, age INT CHECK(age >= 0));'),
    ("Normalization", "Normalization separates related data into logical tables to reduce unnecessary duplication and update problems.", 'CREATE TABLE courses (id INT PRIMARY KEY, title VARCHAR(100));'),
    ("Views", "A view is a reusable query definition that can be queried like a virtual table.", 'CREATE VIEW adult_students AS SELECT * FROM students WHERE age >= 18;'),
    ("Indexes", "Indexes can speed up searches on selected columns while adding storage and write overhead.", 'CREATE INDEX idx_students_name ON students(name);'),
    ("Transactions", "Transactions group related database operations so they can be committed or rolled back together.", 'START TRANSACTION;\nUPDATE accounts SET balance = balance - 100 WHERE id = 1;\nCOMMIT;'),
    ("SQL Mini Project", "A SQL project combines schema design, constraints, CRUD, joins and reporting queries into one database task.", 'CREATE TABLE tasks (id INT PRIMARY KEY, title VARCHAR(100), completed BOOLEAN);'),
]

for title, explanation, code in sql_topics:
    add(
        SQL,
        title,
        explanation,
        code,
        f"Complete a practical {title} SQL exercise and verify the query result using sample data."
    )



# ============================================================
# NON-CODING ROADMAPS
# ============================================================
# These curricula are based on the existing roadmap source:
# Languages, Creative and Marketing category templates.
#
# Non-coding topics intentionally do not use code_example.
# They use:
#   Explanation -> Practical Task -> Evaluation/Completion
# ============================================================

NON_CODING_CURRICULUM = {
    # ========================================================
    # LANGUAGES
    # Each language has its own complete progression.
    # ========================================================

    "English": [
        ("Introduction & Communication Basics",
         "Understand the role of English in everyday communication and learn basic greetings, introductions and common expressions.",
         "Introduce yourself in English using your name, city, interests and one short goal."),
        ("Pronunciation & Sounds",
         "Practice common English sounds, word stress and clear pronunciation so that spoken communication is easier to understand.",
         "Read a short list of everyday words aloud and record yourself for comparison."),
        ("Essential Vocabulary",
         "Build useful vocabulary for people, places, time, food, study, work and daily activities.",
         "Create a 30-word everyday vocabulary list and use at least 15 words in sentences."),
        ("Sentence Formation",
         "Learn to construct clear affirmative, negative and question sentences using basic English patterns.",
         "Write 10 affirmative, 5 negative and 5 question sentences about your daily life."),
        ("Grammar Foundations",
         "Learn core grammar concepts such as nouns, pronouns, verbs, adjectives, articles and prepositions.",
         "Write a short paragraph that correctly uses the grammar structures studied."),
        ("Tenses & Time",
         "Use present, past and future forms to describe routines, completed actions and plans.",
         "Write and speak three short examples about your daily routine, yesterday and tomorrow."),
        ("Listening Comprehension",
         "Improve the ability to understand spoken English by identifying keywords, meaning and context.",
         "Listen to a short English conversation and write its main points in your own words."),
        ("Reading Comprehension",
         "Develop the ability to understand short passages, identify key ideas and infer simple meaning from context.",
         "Read a short passage and answer five comprehension questions."),
        ("Writing for Everyday Life",
         "Write practical English such as messages, emails, notes and short paragraphs with clear structure.",
         "Write a short professional-style email requesting information."),
        ("Conversation & Speaking",
         "Practice responding naturally in common conversations and expressing opinions, needs and preferences.",
         "Perform a two-person role-play covering greeting, asking questions and closing a conversation."),
        ("Fluency & Real-World Communication",
         "Combine vocabulary, grammar, listening and speaking skills in realistic situations such as shopping, travel and study.",
         "Complete a spoken role-play for one real-world situation without reading a full script."),
        ("Final English Communication Project",
         "Demonstrate integrated English communication through a structured speaking, listening, reading and writing activity.",
         "Create a short self-introduction presentation and submit a written summary plus spoken recording."),
    ],

    "Hindi": [
        ("हिंदी परिचय और संचार की शुरुआत",
         "हिंदी में अभिवादन, परिचय और रोज़मर्रा के मूल वाक्यों का प्रयोग सीखें।",
         "अपना नाम, शहर, रुचियां और सीखने का उद्देश्य हिंदी में बताइए।"),
        ("उच्चारण और ध्वनियाँ",
         "हिंदी के सामान्य अक्षरों, शब्दों और ध्वनियों का स्पष्ट उच्चारण करने का अभ्यास करें।",
         "दिए गए रोज़मर्रा के शब्दों को पढ़कर अपनी आवाज़ रिकॉर्ड करें और उच्चारण जाँचें।"),
        ("आवश्यक शब्दावली",
         "परिवार, समय, भोजन, स्थान, पढ़ाई और दैनिक गतिविधियों से जुड़े उपयोगी शब्द सीखें।",
         "कम से कम 30 शब्दों की सूची बनाकर उनमें से 15 शब्दों से वाक्य बनाइए।"),
        ("वाक्य निर्माण",
         "कर्ता, क्रिया और कर्म के सही क्रम से सरल हिंदी वाक्य बनाना सीखें।",
         "अपने दैनिक जीवन पर 15 सकारात्मक, नकारात्मक और प्रश्नवाचक वाक्य लिखें।"),
        ("व्याकरण की नींव",
         "संज्ञा, सर्वनाम, क्रिया, विशेषण, लिंग, वचन और कारक जैसी मूल व्याकरण अवधारणाएँ समझें।",
         "एक छोटा अनुच्छेद लिखें जिसमें सीखी गई व्याकरण संरचनाओं का सही प्रयोग हो।"),
        ("काल और समय",
         "वर्तमान, भूत और भविष्य काल का प्रयोग करके घटनाओं और योजनाओं का वर्णन करना सीखें।",
         "आज, कल और आने वाले कल के बारे में तीन छोटे अनुच्छेद या बोलने के उत्तर तैयार करें।"),
        ("सुनने की समझ",
         "हिंदी बातचीत सुनकर मुख्य विचार, महत्वपूर्ण शब्द और आवश्यक जानकारी पहचानना सीखें।",
         "एक छोटी हिंदी बातचीत सुनें और उसके मुख्य बिंदु अपने शब्दों में लिखें।"),
        ("पठन समझ",
         "छोटे हिंदी अनुच्छेद पढ़कर मुख्य विचार, तथ्य और संदर्भ समझें।",
         "एक अनुच्छेद पढ़कर पाँच प्रश्नों के उत्तर अपने शब्दों में दें।"),
        ("दैनिक लेखन",
         "संदेश, नोट, आवेदन और छोटे अनुच्छेद स्पष्ट तथा व्यवस्थित रूप से लिखना सीखें।",
         "किसी जानकारी के लिए एक छोटा औपचारिक संदेश या आवेदन लिखें।"),
        ("बातचीत और बोलना",
         "दैनिक परिस्थितियों में प्रश्न पूछना, उत्तर देना और अपनी बात स्पष्ट रूप से रखना सीखें।",
         "दुकान, कॉलेज या यात्रा की स्थिति पर एक छोटा संवाद प्रस्तुत करें।"),
        ("प्राकृतिक संवाद और वास्तविक जीवन",
         "सीखी हुई शब्दावली, व्याकरण और बोलने की क्षमता को वास्तविक परिस्थितियों में जोड़ें।",
         "बिना पूरा स्क्रिप्ट पढ़े किसी वास्तविक जीवन की स्थिति पर 2-3 मिनट बोलें।"),
        ("अंतिम हिंदी संचार परियोजना",
         "सुनने, पढ़ने, लिखने और बोलने की क्षमताओं को एक संयुक्त गतिविधि में प्रदर्शित करें।",
         "अपना परिचय और किसी विषय पर छोटा भाषण दें तथा उसका लिखित सारांश जमा करें।"),
    ],

    "Spanish": [
        ("Introduction & Greetings",
         "Learn basic Spanish greetings, introductions and polite expressions used in everyday situations.",
         "Introduce yourself in Spanish using your name, city, interests and a simple goal."),
        ("Pronunciation & Alphabet",
         "Practice Spanish letter sounds, common pronunciation patterns and word stress.",
         "Read a short list of Spanish words aloud and record your pronunciation."),
        ("Essential Vocabulary",
         "Build practical vocabulary for family, numbers, time, food, places and everyday activities.",
         "Create a 30-word vocabulary list and use at least 15 words in simple sentences."),
        ("Basic Sentence Structure",
         "Learn how to form simple Spanish statements, negatives and questions.",
         "Write 15 short sentences about yourself, your routine and your preferences."),
        ("Grammar Foundations",
         "Understand basic nouns, gender, articles, pronouns, adjectives and common verbs.",
         "Write a short paragraph using the grammar structures you learned."),
        ("Present, Past & Future Basics",
         "Use basic time structures to talk about routines, completed events and future plans.",
         "Create three short responses describing today, yesterday and tomorrow."),
        ("Listening Practice",
         "Develop the ability to identify familiar Spanish words and the main idea of short spoken messages.",
         "Listen to a beginner-level dialogue and write five things you understood."),
        ("Reading Practice",
         "Read short Spanish texts and identify familiar vocabulary, key information and overall meaning.",
         "Read a short passage and answer five comprehension questions."),
        ("Everyday Writing",
         "Write simple practical Spanish messages, notes and short descriptions.",
         "Write a short message inviting a friend to an activity."),
        ("Conversation & Speaking",
         "Practice simple spoken exchanges involving greetings, questions, preferences and everyday needs.",
         "Perform a short role-play involving two people meeting for the first time."),
        ("Real-World Spanish",
         "Combine vocabulary, grammar, listening and speaking in travel, shopping and social situations.",
         "Complete a spoken role-play for ordering food, asking directions or making a simple request."),
        ("Final Spanish Communication Project",
         "Demonstrate integrated beginner-to-intermediate communication through multiple language skills.",
         "Prepare a short Spanish presentation with a written summary and spoken recording."),
    ],

    "French": [
        ("Introduction & Greetings",
         "Learn basic French greetings, introductions and polite expressions for everyday communication.",
         "Introduce yourself in French using your name, city, interests and a simple goal."),
        ("Pronunciation & Sounds",
         "Practice common French pronunciation patterns, silent letters and sound combinations.",
         "Read and record a short list of French words and compare your pronunciation."),
        ("Essential Vocabulary",
         "Build useful vocabulary for numbers, family, time, food, places and daily activities.",
         "Create a 30-word vocabulary list and use at least 15 words in sentences."),
        ("Sentence Formation",
         "Learn basic French sentence patterns for statements, negatives and questions.",
         "Write 15 sentences about your identity, routine and preferences."),
        ("Grammar Foundations",
         "Understand nouns, gender, articles, pronouns, adjectives and common verb structures.",
         "Write a short paragraph applying the grammar structures learned."),
        ("Present, Past & Future Basics",
         "Use basic French time structures to describe routines, past events and future plans.",
         "Write three short responses describing your day, yesterday and tomorrow."),
        ("Listening Comprehension",
         "Improve recognition of familiar French vocabulary and the main meaning of short spoken messages.",
         "Listen to a short dialogue and record five key points you understood."),
        ("Reading Comprehension",
         "Read short French texts and identify key information using vocabulary and context.",
         "Read a short passage and answer five comprehension questions."),
        ("Practical Writing",
         "Write simple French messages, notes and short descriptions for everyday situations.",
         "Write a short French message inviting someone to an activity."),
        ("Conversation & Speaking",
         "Practice everyday spoken French through introductions, questions, answers and polite requests.",
         "Perform a short role-play between two people meeting and planning an activity."),
        ("Real-World French",
         "Use French in practical situations such as shopping, travel, ordering food and asking for help.",
         "Complete one real-world role-play without reading a complete script."),
        ("Final French Communication Project",
         "Combine speaking, listening, reading and writing into one practical communication activity.",
         "Prepare a short French presentation with a written summary and spoken recording."),
    ],

    "German": [
        ("Introduction & Greetings",
         "Learn basic German greetings, introductions and polite expressions used in everyday communication.",
         "Introduce yourself in German with your name, city, interests and learning goal."),
        ("Pronunciation & Sounds",
         "Practice common German sounds, spelling patterns and clear pronunciation.",
         "Read and record a short list of German words for pronunciation practice."),
        ("Essential Vocabulary",
         "Build useful vocabulary for numbers, family, time, food, places and daily routines.",
         "Create a 30-word vocabulary list and use at least 15 words in sentences."),
        ("Sentence Structure",
         "Learn basic German word order for statements, questions and simple negative sentences.",
         "Write 15 sentences about yourself and your daily routine."),
        ("Grammar Foundations",
         "Understand basic nouns, articles, pronouns, adjective use and common verb patterns.",
         "Write a short paragraph applying the grammar structures learned."),
        ("Present, Past & Future Basics",
         "Learn basic structures for describing current routines, past events and future plans.",
         "Create short written and spoken examples for today, yesterday and tomorrow."),
        ("Listening Comprehension",
         "Improve understanding of familiar German words and the main idea of short spoken messages.",
         "Listen to a short dialogue and write five key points you understood."),
        ("Reading Comprehension",
         "Read beginner German passages and identify important information from context.",
         "Read a short passage and answer five comprehension questions."),
        ("Everyday Writing",
         "Write practical German messages, notes and short descriptions using clear sentence structures.",
         "Write a short message making or accepting a simple plan."),
        ("Conversation & Speaking",
         "Practice everyday German conversations involving introductions, questions, preferences and requests.",
         "Perform a short role-play between two people meeting and planning an activity."),
        ("Real-World German",
         "Apply German skills to practical situations such as shopping, travel, food and asking for help.",
         "Complete a practical role-play without reading a complete script."),
        ("Final German Communication Project",
         "Combine speaking, listening, reading and writing in a structured practical communication task.",
         "Prepare a short German presentation with a written summary and spoken recording."),
    ],

    # ========================================================
    # CREATIVE
    # ========================================================

    "UI/UX": [
        ("UI/UX Fundamentals",
         "Understand the difference between user interface and user experience and how both contribute to useful digital products.",
         "Choose a simple app and identify three UI elements and three UX considerations."),
        ("User Research",
         "Learn how to collect user needs through interviews, observation and basic research.",
         "Create five user-research questions for a chosen app idea."),
        ("Personas & User Needs",
         "Translate research findings into a clear user persona and identify the user's goals and pain points.",
         "Create one persona with goals, frustrations, needs and context."),
        ("Information Architecture",
         "Organize screens and content so users can understand where information belongs and how to navigate it.",
         "Create a simple sitemap for a mobile or web application."),
        ("User Flows",
         "Map the steps a user follows to complete an important task inside a product.",
         "Create a user flow for signup, booking, purchase or another chosen task."),
        ("Wireframing",
         "Create low-fidelity layouts that focus on structure, hierarchy and functionality before visual styling.",
         "Design wireframes for at least three connected screens."),
        ("Visual Design Principles",
         "Apply hierarchy, spacing, contrast, alignment, typography and consistency to digital interfaces.",
         "Redesign one wireframe using a consistent visual system."),
        ("Design System & Components",
         "Understand reusable components, states, spacing rules and visual consistency across screens.",
         "Create a small component set containing buttons, inputs, cards and navigation."),
        ("Prototyping",
         "Connect screens into an interactive prototype so a user can experience the intended flow.",
         "Build a clickable prototype for one complete user journey."),
        ("Usability Testing",
         "Evaluate whether users can complete tasks and identify usability problems from observed behavior.",
         "Test your prototype with a small set of users and record at least five observations."),
        ("Iteration & Case Study",
         "Use feedback to improve the design and explain the decisions made during the design process.",
         "Create a before-and-after improvement and document why the changes were made."),
        ("Final UI/UX Project",
         "Combine research, structure, visual design, prototyping and testing into a complete product case study.",
         "Create a complete mini UI/UX project from problem statement to tested prototype."),
    ],

    "UI/UX Design": [
        ("UI/UX Design Fundamentals",
         "Understand user interface and user experience design and how design decisions affect usability and clarity.",
         "Select a digital product and identify three interface and three experience problems."),
        ("Design Research",
         "Learn how research helps designers understand users, competitors and product requirements.",
         "Create a short research plan with five questions and three competitor observations."),
        ("User Persona",
         "Represent a target user's goals, behavior, needs and pain points using research-based information.",
         "Create one detailed persona for a selected digital product."),
        ("Information Architecture",
         "Organize content and navigation into a structure that users can understand easily.",
         "Create a sitemap and label the major sections of your product."),
        ("User Flow",
         "Describe the exact path a user follows to complete a meaningful task.",
         "Design a flow for one core feature from entry point to successful completion."),
        ("Wireframes",
         "Use low-fidelity layouts to solve structure and usability before applying detailed visual styling.",
         "Create wireframes for three to five connected screens."),
        ("Typography & Color",
         "Use typography, color and contrast to create hierarchy, readability and visual consistency.",
         "Create a small typography and color system for your project."),
        ("Components & Design System",
         "Create reusable interface components and define consistent spacing, states and visual rules.",
         "Build a mini design system with buttons, inputs, cards and navigation components."),
        ("Interactive Prototyping",
         "Turn static screens into an interactive flow that communicates how the final product should behave.",
         "Create a clickable prototype covering one complete user journey."),
        ("Usability Testing",
         "Observe users completing tasks and use their feedback to identify usability issues.",
         "Run a small usability test and document the issues you find."),
        ("Iteration & Presentation",
         "Improve the design based on evidence and communicate the reasoning behind important decisions.",
         "Make at least three evidence-based design improvements and present them."),
        ("Final UI/UX Design Project",
         "Combine research, architecture, interface design, prototyping and testing into a complete case study.",
         "Create and present a complete UI/UX project from problem definition to tested prototype."),
    ],

    "Graphic Design": [
        ("Graphic Design Fundamentals",
         "Understand the purpose of graphic design and the basic principles used to communicate visually.",
         "Create a simple visual composition using a clear message and focal point."),
        ("Design Principles",
         "Learn balance, contrast, alignment, repetition, proximity, hierarchy and visual consistency.",
         "Create a poster that intentionally demonstrates at least four design principles."),
        ("Color Theory",
         "Understand color relationships, harmony, contrast and how color choices influence visual communication.",
         "Create three color palettes for different communication goals."),
        ("Typography",
         "Learn font selection, hierarchy, readability, spacing and pairing for visual communication.",
         "Design a typographic poster using a clear hierarchy."),
        ("Composition & Layout",
         "Arrange text and visual elements so that the viewer can follow information naturally.",
         "Create two different layouts for the same content and compare them."),
        ("Images & Visual Assets",
         "Learn how images, icons and graphical elements support a design message without creating unnecessary clutter.",
         "Create a social post combining text, imagery and supporting visual elements."),
        ("Design Tools & Workflow",
         "Understand a repeatable workflow for planning, creating, reviewing and exporting graphic designs.",
         "Complete a small design from brief to final export using your chosen design tool."),
        ("Branding Basics",
         "Understand how visual identity elements such as logo, color and typography create consistency.",
         "Create a simple visual identity board for a fictional brand."),
        ("Creative Brief",
         "Translate a communication requirement into audience, objective, message, format and visual direction.",
         "Write a complete creative brief for a poster or social media campaign."),
        ("Practical Design Project",
         "Apply design principles, typography, color and layout to a realistic communication requirement.",
         "Design a complete poster, social media set or promotional graphic."),
        ("Portfolio Presentation",
         "Present finished work clearly by explaining the objective, process, choices and final result.",
         "Prepare one portfolio case study showing brief, process, iterations and final design."),
        ("Final Graphic Design Project",
         "Demonstrate the complete design process from brief and concept through polished final artwork.",
         "Create a final campaign consisting of at least three consistent graphic assets."),
    ],

    "Video Editing": [
        ("Video Editing Fundamentals",
         "Understand the purpose of editing and how cuts, timing, sequencing and audio shape a video.",
         "Create a short sequence from several clips with a clear beginning, middle and end."),
        ("Editing Interface & Workflow",
         "Learn the basic editing workflow including importing media, organizing clips, timeline editing and exporting.",
         "Import sample footage, organize it and export a short edited sequence."),
        ("Cuts & Transitions",
         "Use clean cuts and purposeful transitions to control pace and maintain continuity.",
         "Edit a one-minute sequence using appropriate cuts and no unnecessary transitions."),
        ("Story Structure",
         "Arrange footage into a narrative or informational structure that communicates a clear message.",
         "Create a short story sequence with an opening, development and conclusion."),
        ("Audio Editing",
         "Balance dialogue, music and sound effects so the viewer can understand the message comfortably.",
         "Edit a short clip with dialogue and background music at suitable levels."),
        ("Text, Titles & Captions",
         "Use titles, captions and on-screen text to improve clarity without distracting from the content.",
         "Create an opening title and captions for a short video."),
        ("Color Correction Basics",
         "Understand basic exposure, white balance, contrast and consistency between shots.",
         "Correct a small set of clips so they appear visually consistent."),
        ("Motion & Effects",
         "Use simple motion, keyframes and effects when they support the story or information.",
         "Add a simple animated title or controlled visual effect to a short clip."),
        ("Pacing & Engagement",
         "Control shot length, rhythm and visual variety to keep a viewer engaged.",
         "Edit the same footage into a short version with deliberate pacing."),
        ("Video Project Workflow",
         "Plan a project from brief and footage organization through editing, review and final export.",
         "Complete a short project using a written brief and organized editing workflow."),
        ("Portfolio Video",
         "Present an edited project with clear purpose, polished audio, visuals and export settings.",
         "Create one portfolio-ready video and document the editing decisions."),
        ("Final Video Editing Project",
         "Combine storytelling, editing, audio, color, text and export into a complete finished video.",
         "Produce a 1-3 minute finished video based on a clear creative brief."),
    ],

    "Photography": [
        ("Photography Fundamentals",
         "Understand the purpose of photography and the relationship between subject, light, composition and camera settings.",
         "Capture five photographs of the same subject using different compositions."),
        ("Camera & Exposure",
         "Learn how aperture, shutter speed and ISO affect exposure and image appearance.",
         "Capture examples showing the visible effect of changing each exposure control."),
        ("Focus & Depth of Field",
         "Understand focus, focal points and how aperture affects background blur and depth of field.",
         "Create two photographs of the same subject with noticeably different depth of field."),
        ("Composition",
         "Use framing, rule of thirds, leading lines, symmetry and visual balance to guide attention.",
         "Create a five-photo composition exercise using different techniques."),
        ("Lighting Fundamentals",
         "Understand direction, intensity, softness and color of light and how they affect a subject.",
         "Photograph one subject under at least three different lighting conditions."),
        ("Portrait Photography",
         "Learn subject positioning, expression, background choice and lighting for stronger portraits.",
         "Create a small portrait series using controlled composition and lighting."),
        ("Street & Lifestyle Photography",
         "Capture authentic moments while considering timing, composition and context.",
         "Create a five-image visual story around an everyday activity."),
        ("Product & Creative Photography",
         "Use composition, lighting and background control to present an object clearly and attractively.",
         "Photograph one product in three different visual styles."),
        ("Photo Editing",
         "Use basic cropping, exposure, color and contrast adjustments to improve an image while preserving realism.",
         "Edit three photographs and document the changes made."),
        ("Visual Storytelling",
         "Sequence photographs so that multiple images communicate one coherent idea or story.",
         "Create a six-image photo story with a clear beginning, development and ending."),
        ("Photography Portfolio",
         "Select, organize and present strong images with consistent quality and a clear visual identity.",
         "Create a small portfolio of your strongest images with captions."),
        ("Final Photography Project",
         "Combine camera technique, composition, lighting, editing and storytelling into a complete photographic series.",
         "Produce a themed 8-10 image photo series and present the creative reasoning."),
    ],

    "Illustration": [
        ("Illustration Fundamentals",
         "Understand illustration as visual communication and learn the relationship between idea, shape, form and style.",
         "Create five simple illustrations from basic shapes."),
        ("Line, Shape & Form",
         "Use line quality, geometric shapes and organic forms to create readable illustrations.",
         "Create a small sheet showing different line and shape treatments."),
        ("Observation & Proportion",
         "Develop observation skills by studying proportions, silhouettes and relationships between visual elements.",
         "Draw or construct three objects while focusing on accurate proportion."),
        ("Color & Visual Harmony",
         "Use color relationships, contrast and palettes to support mood and readability.",
         "Create three color palettes and apply one to a simple illustration."),
        ("Composition",
         "Arrange characters, objects and negative space to create a clear focal point and visual flow.",
         "Create two compositions for the same illustration idea."),
        ("Character Design",
         "Develop recognizable characters through silhouette, proportions, expression and visual traits.",
         "Design one character with front, side and expression variations."),
        ("Environment & Backgrounds",
         "Create simple environments that establish place, depth and context for an illustration.",
         "Illustrate one scene with foreground, middle ground and background."),
        ("Digital Illustration Workflow",
         "Learn a repeatable process for sketching, refining, coloring, layering and exporting digital artwork.",
         "Complete a small illustration from rough sketch to final export."),
        ("Style Development",
         "Explore visual choices that create a consistent and recognizable illustration style.",
         "Create three variations of the same subject in different styles."),
        ("Creative Brief",
         "Translate a communication goal into subject, audience, mood, format and visual direction.",
         "Create an illustration concept from a written creative brief."),
        ("Portfolio Illustration",
         "Select and present finished illustrations while explaining the concept and process.",
         "Prepare three related illustrations as a mini portfolio set."),
        ("Final Illustration Project",
         "Combine concept development, drawing, composition, color and finishing into a complete illustration project.",
         "Create a polished illustration series based on one clear theme."),
    ],

    # ========================================================
    # MARKETING
    # ========================================================

    "Digital Marketing": [
        ("Digital Marketing Fundamentals",
         "Understand the digital marketing ecosystem, customer journey and major online channels.",
         "Create a one-page overview of how a sample business could use digital channels."),
        ("Market & Audience Research",
         "Identify target customers, their needs, problems, behaviors and decision factors.",
         "Create a target audience profile with needs, pain points and goals."),
        ("Customer Journey",
         "Map how a person moves from awareness to consideration, action and retention.",
         "Create a customer journey for a chosen product or service."),
        ("Marketing Goals & KPIs",
         "Turn business objectives into measurable marketing goals and select suitable performance indicators.",
         "Create three SMART marketing goals and matching KPIs."),
        ("Content Marketing",
         "Plan useful content around audience needs and business objectives.",
         "Create a one-week content plan with topics, formats and goals."),
        ("Social Media Marketing",
         "Understand how social platforms can be used for awareness, engagement and community building.",
         "Create a sample social media plan for one target audience."),
        ("Search & Discoverability",
         "Understand how people discover products through search and how content can support discoverability.",
         "Create a basic keyword and content idea list for a chosen topic."),
        ("Campaign Planning",
         "Plan a campaign by connecting audience, message, channel, timing and desired action.",
         "Design a complete campaign brief for a fictional product."),
        ("Analytics & Measurement",
         "Use basic marketing metrics to understand reach, engagement, traffic and conversions.",
         "Analyze a sample campaign report and identify three observations."),
        ("Optimization",
         "Use performance data and testing ideas to improve marketing decisions.",
         "Suggest three measurable improvements to the sample campaign."),
        ("Integrated Marketing Project",
         "Combine audience research, goals, content, channels, campaign planning and measurement.",
         "Create a complete digital marketing plan for a fictional business."),
        ("Final Digital Marketing Project",
         "Demonstrate the full process from research and strategy to execution planning and measurement.",
         "Present a campaign proposal containing audience, goals, content, channels, KPIs and optimization plan."),
    ],

    "SEO": [
        ("SEO Fundamentals",
         "Understand search engines, organic search and the main areas of SEO: on-page, technical and off-page.",
         "Audit a simple website concept and list its main SEO opportunities."),
        ("Search Intent",
         "Understand why users search and how content should match informational, navigational, commercial or transactional intent.",
         "Classify 15 sample search queries by intent."),
        ("Keyword Research",
         "Identify relevant search terms by considering relevance, intent and competition.",
         "Create a keyword list for a chosen topic and group related terms."),
        ("On-Page SEO",
         "Optimize titles, headings, content structure, URLs and internal links for users and search engines.",
         "Write an optimized page title, heading structure and short page outline."),
        ("Content Optimization",
         "Create useful, readable content that satisfies search intent without relying on keyword stuffing.",
         "Improve a sample article so it answers the target query clearly."),
        ("Technical SEO Basics",
         "Understand crawlability, indexing, site structure, page performance and basic technical considerations.",
         "Create a technical SEO checklist for a sample website."),
        ("Internal Linking",
         "Use internal links to connect related content and help users and search engines understand site structure.",
         "Design an internal-linking plan for five sample pages."),
        ("Local & Mobile SEO",
         "Understand the importance of mobile usability and local search for location-based businesses.",
         "Create a local SEO checklist for a fictional local business."),
        ("SEO Analytics",
         "Interpret basic search performance information such as impressions, clicks, rankings and organic traffic.",
         "Analyze a sample SEO report and identify five useful observations."),
        ("SEO Optimization",
         "Use performance information to prioritize improvements and measure their effects.",
         "Create a prioritized SEO improvement plan for a sample site."),
        ("SEO Practical Project",
         "Combine research, content, on-page and technical considerations into one optimization process.",
         "Create an SEO plan for a chosen website or fictional business."),
        ("Final SEO Audit Project",
         "Demonstrate the ability to research, audit, prioritize and communicate SEO improvements.",
         "Prepare a complete SEO audit with findings, priorities, recommendations and measurement plan."),
    ],

    "Social Media Marketing": [
        ("Social Media Fundamentals",
         "Understand how social platforms support awareness, engagement, community and business goals.",
         "Choose a fictional brand and define its social media purpose."),
        ("Audience Research",
         "Identify the target audience's interests, needs, behaviors and preferred content formats.",
         "Create a detailed social audience profile."),
        ("Platform Selection",
         "Match audience behavior and business goals to suitable social media platforms.",
         "Select two platforms for a sample brand and explain the purpose of each."),
        ("Content Pillars",
         "Create repeatable content themes that keep social communication focused and consistent.",
         "Define four content pillars and create two ideas for each."),
        ("Content Creation",
         "Plan captions, visuals, short-form content and calls to action for a target audience.",
         "Create five social posts with captions and clear objectives."),
        ("Content Calendar",
         "Organize content by date, theme, format, platform and objective.",
         "Create a seven-day social media calendar."),
        ("Community Engagement",
         "Learn how to respond to comments, questions and feedback while maintaining a consistent brand voice.",
         "Write responses to five sample community interactions."),
        ("Social Campaigns",
         "Plan campaigns around a specific objective, audience, message and call to action.",
         "Create a campaign brief for a fictional social media campaign."),
        ("Analytics & Metrics",
         "Understand reach, impressions, engagement, clicks, follower growth and conversion-related metrics.",
         "Analyze a sample social report and identify three trends."),
        ("Optimization",
         "Use performance information to improve content, timing, formats and messaging.",
         "Create three data-based optimization recommendations."),
        ("Social Media Strategy Project",
         "Combine audience research, platforms, content, campaigns and measurement into one strategy.",
         "Create a complete monthly social media strategy for a fictional brand."),
        ("Final Social Media Project",
         "Demonstrate the complete process from audience definition to content planning, campaign execution and measurement.",
         "Present a complete social media plan with calendar, sample posts, campaign and KPI framework."),
    ],

    "Content Marketing": [
        ("Content Marketing Fundamentals",
         "Understand how useful content can attract, educate and retain a defined audience.",
         "Choose a fictional business and define its content marketing purpose."),
        ("Audience & Problem Research",
         "Identify audience questions, problems, interests and information needs.",
         "Create a list of 15 audience questions for a chosen topic."),
        ("Content Strategy",
         "Connect audience needs, business goals, content themes and distribution into a coherent strategy.",
         "Create three content pillars and explain their purpose."),
        ("Content Formats",
         "Understand how articles, videos, guides, social posts, emails and other formats serve different goals.",
         "Select suitable formats for five sample content ideas."),
        ("Content Planning",
         "Organize ideas into a practical publishing plan with topics, formats, goals and deadlines.",
         "Create a two-week content calendar."),
        ("Content Writing",
         "Write clear, useful and audience-focused content with strong structure and readable language.",
         "Write a 500-word educational article or guide."),
        ("Headlines & Calls to Action",
         "Create clear headlines and calls to action that communicate value and encourage the intended next step.",
         "Write five headlines and three calls to action for the same topic."),
        ("Distribution & Promotion",
         "Plan how content reaches the audience through owned, social, search and other appropriate channels.",
         "Create a distribution plan for one piece of content."),
        ("Content Analytics",
         "Measure content performance using appropriate engagement, traffic and conversion indicators.",
         "Analyze a sample content report and identify what performed well."),
        ("Optimization & Repurposing",
         "Improve existing content and adapt one strong idea into multiple useful formats.",
         "Turn one article idea into a social post, short video idea and email outline."),
        ("Content Marketing Project",
         "Combine research, strategy, creation, distribution and measurement into a practical plan.",
         "Create a complete content campaign for a fictional business."),
        ("Final Content Portfolio Project",
         "Demonstrate the complete content workflow with strategy, original content and measurement.",
         "Submit a mini content portfolio containing strategy, calendar and at least three content pieces."),
    ],

    "Branding": [
        ("Branding Fundamentals",
         "Understand what a brand represents and how identity, perception, values and customer experience connect.",
         "Choose a fictional business and write its core brand purpose."),
        ("Audience & Positioning",
         "Define who the brand serves and how it should be positioned relative to alternatives.",
         "Create a target audience profile and one positioning statement."),
        ("Brand Purpose & Values",
         "Translate business purpose into clear values and principles that guide communication and decisions.",
         "Define a brand purpose and five practical brand values."),
        ("Brand Personality & Voice",
         "Create a recognizable personality and tone for consistent communication.",
         "Write five brand-voice rules and sample messages in that voice."),
        ("Visual Identity",
         "Understand how logo, color, typography, imagery and layout work together to create a recognizable identity.",
         "Create a visual mood board with colors, typography and image direction."),
        ("Logo & Identity Concepts",
         "Develop visual concepts that communicate the brand while remaining clear and usable.",
         "Create two logo or identity concepts and explain the design reasoning."),
        ("Brand Guidelines",
         "Document the rules that keep visual and verbal brand communication consistent.",
         "Create a mini brand guide covering logo use, colors, typography and tone."),
        ("Brand Communication",
         "Apply the identity consistently across social posts, web content and marketing materials.",
         "Create three brand communications using the same identity system."),
        ("Brand Experience",
         "Understand how customer interactions contribute to overall brand perception beyond visual design.",
         "Map five customer touchpoints and identify how the brand should appear at each."),
        ("Brand Audit",
         "Review a brand's consistency, positioning and communication and identify improvement opportunities.",
         "Perform a simple audit of a fictional or public-facing brand."),
        ("Brand Strategy Project",
         "Combine audience, positioning, values, voice and visual identity into one brand strategy.",
         "Create a complete brand strategy document for a fictional business."),
        ("Final Branding Project",
         "Demonstrate the complete branding process from research and positioning to identity and communication.",
         "Present a mini brand identity system with strategy, visual direction, guidelines and sample applications."),
    ],
}


def normalize_skill_name(name):
    return (name or "").strip().lower()


def get_non_coding_curriculum(skill):
    name = normalize_skill_name(skill.name)

    for skill_name, curriculum in NON_CODING_CURRICULUM.items():
        if normalize_skill_name(skill_name) == name:
            return curriculum

    # Safe fallback for any future non-coding skill.
    category = (skill.category or "").strip().lower()

    if "language" in category:
        return NON_CODING_CURRICULUM["English"]

    if "creative" in category or "design" in category:
        return NON_CODING_CURRICULUM["Graphic Design"]

    if "marketing" in category:
        return NON_CODING_CURRICULUM["Digital Marketing"]

    return None



# ============================================================
# DEEP LEARNING CONTENT BUILDER
# ============================================================
# The curriculum above remains the source of truth for topic titles,
# examples and practical tasks. This function turns the short source
# explanation into a learner-facing lesson with enough context to
# understand the concept before practice.
#
# IMPORTANT:
# - It does NOT change topic order/count.
# - It does NOT change task descriptions/evaluation.
# - It does NOT create new database columns.
# - It only builds the text stored in RoadmapTopic.explanation.
# ============================================================

def build_deep_explanation(
    title,
    short_explanation,
    code_example=None,
    task_description=None,
    task_type="practical",
):
    """Create structured, beginner-friendly learning content.

    The original curriculum explanation is preserved as the opening
    concept statement. The remaining sections add learning context,
    application guidance, example interpretation, common mistakes and
    a recap without changing the existing roadmap curriculum.
    """

    title = (title or "This topic").strip()
    short_explanation = (short_explanation or "").strip()
    task_description = (task_description or "").strip()

    if task_type == "coding":
        how_it_works = (
            f"When learning {title}, first identify what problem the concept "
            "solves, then understand the rules that control it. After that, "
            "read a small example from top to bottom and predict what should "
            "happen before running it. Finally, modify the example and create "
            "your own version. This sequence helps you understand the idea "
            "instead of memorising a single piece of code."
        )
        why_it_matters = (
            f"{title} is important because it is part of the core reasoning "
            "used when writing real programs. Understanding the concept lets "
            "you choose an appropriate solution, read other people's code, "
            "debug mistakes and extend a program when the requirements change."
        )
        practice_guidance = (
            "While practicing, change one part of the example at a time. "
            "Try different values, predict the output, run the program, and "
            "compare the result with your prediction. If an error appears, "
            "read the error message and identify which rule of the concept "
            "was violated."
        )
        mistakes = (
            f"Common beginner mistakes with {title} include copying syntax "
            "without understanding why it is required, changing several "
            "things at once, ignoring error messages, and assuming that an "
            "example will work for every input. A good learner checks the "
            "rules, tests small cases and explains each important line in "
            "their own words."
        )
    elif task_type == "speaking":
        how_it_works = (
            f"To learn {title}, connect the concept with real communication. "
            "First understand the meaning and pattern, then observe examples "
            "in context. Next produce your own examples, say or write them, "
            "and review whether the meaning is clear. Repeated use in short "
            "realistic situations builds stronger recall than memorising "
            "isolated words or rules."
        )
        why_it_matters = (
            f"{title} matters because communication requires more than knowing "
            "a definition. You should be able to recognise the concept when "
            "someone uses it and apply it naturally when speaking or writing."
        )
        practice_guidance = (
            "Practice with several different situations rather than repeating "
            "one sentence. Read or say your examples aloud, notice mistakes, "
            "correct them, and then create a new example without looking at "
            "the original."
        )
        mistakes = (
            f"Common mistakes while learning {title} include memorising a "
            "translation without context, using the pattern in the wrong "
            "situation, and avoiding active practice. Always check meaning, "
            "context and natural usage."
        )
    elif task_type in {"creative", "marketing"}:
        how_it_works = (
            f"Learning {title} means understanding both the principle and the "
            "decision-making behind it. Start with the objective and audience, "
            "study how the concept is applied in real work, analyse an example, "
            "then create your own version. Review the result against the "
            "original objective and improve it rather than treating the first "
            "attempt as final."
        )
        why_it_matters = (
            f"{title} is useful because professional work depends on deliberate "
            "choices. A strong result is not only visually or verbally attractive; "
            "it should solve a defined problem, communicate clearly and work for "
            "the intended audience."
        )
        practice_guidance = (
            "During practice, make a clear first attempt, explain why you made "
            "each major choice, compare the result with the objective, and make "
            "at least one improvement. Keep the reasoning behind your decisions "
            "because it will help when completing the practical challenge."
        )
        mistakes = (
            f"Common mistakes with {title} include focusing only on appearance, "
            "copying an example without understanding the reason behind it, "
            "ignoring the audience, and stopping after the first draft. Strong "
            "work is usually the result of testing and iteration."
        )
    else:
        how_it_works = (
            f"To understand {title}, begin with the main idea, identify the "
            "steps or rules involved, study an example, and then apply the "
            "same principle to a new situation. The goal is to explain the "
            "concept in your own words and use it without depending on the "
            "original example."
        )
        why_it_matters = (
            f"{title} matters because knowing a definition is different from "
            "being able to apply a concept. Understanding the reason, process "
            "and expected result makes the skill transferable to new problems."
        )
        practice_guidance = (
            "Practice by completing a small example first, then change the "
            "conditions and solve a second example independently. Compare both "
            "results and note what changed and why."
        )
        mistakes = (
            f"Common mistakes with {title} include learning only the definition, "
            "skipping the example, following steps mechanically and not checking "
            "the final result. Focus on the reason behind each step."
        )

    sections = [
        f"WHAT IS {title.upper()}?\n{short_explanation}",
        f"\nWHY IT MATTERS\n{why_it_matters}",
        f"\nHOW IT WORKS\n{how_it_works}",
    ]

    if code_example and task_type == "coding":
        code_lines = [line for line in code_example.splitlines() if line.strip()]
        if len(code_lines) > 1:
            walkthrough = (
                "Read the example from top to bottom. Identify the values, "
                "keywords, operators, blocks or method calls that directly "
                "represent the topic. Then ask what each important line does "
                "and what would change if its value or condition changed. "
                "For this lesson, the example is:\n\n"
                f"{code_example}\n\n"
                "Do not stop at getting the output. The important part is being "
                "able to explain why the program produces that output."
            )
        else:
            walkthrough = (
                "Use the example as a starting point. Read the statement, "
                "identify the part that demonstrates the topic, predict the "
                "result, and then modify one value to observe the difference."
            )
        sections.append(f"\nEXAMPLE & WALKTHROUGH\n{walkthrough}")
    else:
        sections.append(
            "\nEXAMPLE & APPLICATION\n"
            f"Take a realistic situation related to {title}. Identify the "
            "goal, apply the concept, and check whether the result solves the "
            "original requirement. Your practical task below is the point where "
            "you will demonstrate this independently."
        )

    sections.extend([
        f"\nPRACTICE GUIDANCE\n{practice_guidance}",
        f"\nCOMMON MISTAKES\n{mistakes}",
        "\nQUICK RECAP\n"
        f"You should now be able to explain what {title} is, why it is used, "
        "describe its main rules or process, understand the example, and "
        "apply the idea to a new problem. If you cannot explain the concept "
        "without looking at the lesson, review this section before moving to "
        "the practical challenge.",
    ])

    if task_description:
        sections.append(
            "\nREADY FOR THE PRACTICAL TASK\n"
            "The next step is not another reading exercise. You must apply "
            "the concept yourself. The task is evaluated before the topic is "
            "marked complete, so make sure your submission demonstrates the "
            "concept rather than only describing it."
        )

    return "\n\n".join(sections).strip()


# Coding skills that should no longer remain active.
# The project keeps exactly these five coding skills active:
# Python, Java, JavaScript, C++, SQL
DEACTIVATE_CODING_SKILLS = ["C", "C#", "PHP"]


def find_skill(name):
    """Find a skill by its exact stored name."""
    return Skill.query.filter_by(name=name).first()


def get_task_type(skill):
    category = (skill.category or "").strip().lower()

    if "coding" in category or "program" in category:
        return "coding"

    if "language" in category:
        return "speaking"

    if "creative" in category or "design" in category:
        return "creative"

    if "marketing" in category:
        return "marketing"

    return "practical"


# ============================================================
# UNIVERSAL TASK METADATA
# ============================================================
# The evaluator itself is implemented separately in the application.
# This seed only guarantees that every roadmap topic has a TopicTask
# record with a stable task_type/evaluation_mode contract.

EVALUATION_MODE_BY_TASK_TYPE = {
    "coding": "universal_coding",
    "speaking": "universal_language",
    "creative": "universal_creative",
    "marketing": "universal_marketing",
    "practical": "universal_practical",
}

def upsert_topic_task(topic):
    task = TopicTask.query.filter_by(topic_id=topic.id).first()
    if task is None:
        task = TopicTask(
            topic_id=topic.id,
            task_type=topic.task_type or "practical",
            evaluation_mode=EVALUATION_MODE_BY_TASK_TYPE.get(
                topic.task_type or "practical",
                "universal_practical"
            ),
            instructions=topic.task_description or "Complete the practical task and submit your work.",
            is_active=True,
        )
        db.session.add(task)
    else:
        task.task_type = topic.task_type or "practical"
        task.evaluation_mode = EVALUATION_MODE_BY_TASK_TYPE.get(
            topic.task_type or "practical",
            "universal_practical"
        )
        task.instructions = topic.task_description or task.instructions
        task.is_active = True
    return task


# ============================================================
# SAFE STALE-TOPIC CLEANUP
# ============================================================


def prune_stale_topics(roadmap, keep_count):
    """Safely remove old extra topics that are no longer in the curriculum.

    A topic is deleted only when it has no learner progress and no task.
    This protects existing learning/task data from accidental deletion.
    """

    stale_topics = RoadmapTopic.query.filter(
        RoadmapTopic.roadmap_id == roadmap.id,
        RoadmapTopic.order_index > keep_count
    ).order_by(
        RoadmapTopic.order_index
    ).all()

    removed = 0
    skipped = 0

    for topic in stale_topics:
        has_progress = bool(topic.progress_records)
        has_task = topic.task is not None

        if has_progress or has_task:
            skipped += 1
            print(
                f"  -> KEPT stale topic {topic.id} ({topic.title}) "
                f"because it has linked data"
            )
            continue

        db.session.delete(topic)
        removed += 1

    return removed, skipped


# ============================================================
# SEED / UPDATE ALL ACTIVE ROADMAPS
# ============================================================

with app.app_context():

    # --------------------------------------------------------
    # SAFETY CHECK
    # --------------------------------------------------------

    progress_count = TopicProgress.query.count()

    # Existing progress is allowed only when the roadmap already has the
    # same number of ordered topics as the replacement curriculum. This
    # prevents a learner's topic IDs/order from being silently remapped.
    if progress_count > 0:
        for skill in Skill.query.filter_by(is_active=True).all():
            curriculum = CODING_CURRICULUM.get(skill.name) if get_task_type(skill) == "coding" else get_non_coding_curriculum(skill)
            if not curriculum:
                continue
            roadmap = Roadmap.query.filter_by(skill_id=skill.id).first()
            existing_count = RoadmapTopic.query.filter_by(roadmap_id=roadmap.id).count() if roadmap else 0
            if roadmap and existing_count != len(curriculum):
                print()
                print("=" * 60)
                print("ROADMAP SEED STOPPED FOR SAFETY")
                print("=" * 60)
                print(f"Existing TopicProgress records: {progress_count}")
                print(f"Topic count mismatch for {skill.name}: existing={existing_count}, new={len(curriculum)}")
                print("No roadmap topics were changed.")
                print("=" * 60)
                raise SystemExit(1)

    # --------------------------------------------------------
    # EXACTLY FIVE ACTIVE CODING SKILLS
    # --------------------------------------------------------

    for name in DEACTIVATE_CODING_SKILLS:
        skill = find_skill(name)
        if skill:
            skill.is_active = False

            # Keep old records for data safety, but make sure their
            # roadmaps are also inactive so they cannot appear as
            # available learning paths.
            Roadmap.query.filter_by(
                skill_id=skill.id
            ).update({"is_active": False})

            print(f"DEACTIVATED CODING SKILL: {skill.name}")

    created_roadmaps = 0
    updated_roadmaps = 0
    created_topics = 0
    updated_topics = 0
    removed_topics = 0
    kept_linked_stale_topics = 0

    # --------------------------------------------------------
    # PROCESS ALL ACTIVE SKILLS
    # --------------------------------------------------------

    skills = Skill.query.filter_by(
        is_active=True
    ).order_by(
        Skill.id
    ).all()

    for skill in skills:

        # Five selected coding skills use their detailed
        # skill-specific curricula.
        if skill.name in CODING_CURRICULUM:
            curriculum = CODING_CURRICULUM[skill.name]
            task_type = "coding"

        else:
            # All active non-coding skills use the exact existing
            # category curriculum from the source seed.
            curriculum = get_non_coding_curriculum(skill)
            task_type = get_task_type(skill)

        if not curriculum:
            print(
                f"SKIP: No curriculum available for {skill.name}"
            )
            continue

        roadmap = Roadmap.query.filter_by(
            skill_id=skill.id
        ).first()

        if not roadmap:

            roadmap = Roadmap(
                skill_id=skill.id,
                title=f"{skill.name} Learning Roadmap",
                description=(
                    f"A structured, practical learning path "
                    f"for mastering {skill.name} step by step."
                ),
                is_active=True,
            )

            db.session.add(roadmap)
            db.session.flush()

            created_roadmaps += 1
            print(f"CREATED ROADMAP: {skill.name}")

        else:

            roadmap.title = f"{skill.name} Learning Roadmap"
            roadmap.description = (
                f"A structured, practical learning path "
                f"for mastering {skill.name} step by step."
            )
            roadmap.is_active = True

            updated_roadmaps += 1
            print(f"UPDATED ROADMAP: {skill.name}")

        existing_topics = RoadmapTopic.query.filter_by(
            roadmap_id=roadmap.id
        ).order_by(
            RoadmapTopic.order_index
        ).all()

        for index, item in enumerate(
            curriculum,
            start=1
        ):

            if task_type == "coding":

                title, explanation, code_example, task_description = item

            else:

                title, explanation, task_description = item
                code_example = None

            if index <= len(existing_topics):

                topic = existing_topics[index - 1]

                topic.title = title
                topic.explanation = build_deep_explanation(
                    title, explanation, code_example, task_description, task_type
                )
                topic.code_example = code_example
                topic.task_description = task_description
                topic.task_type = task_type
                topic.order_index = index

                updated_topics += 1

            else:

                topic = RoadmapTopic(
                    roadmap_id=roadmap.id,
                    title=title,
                    explanation=build_deep_explanation(
                        title, explanation, code_example, task_description, task_type
                    ),
                    code_example=code_example,
                    task_description=task_description,
                    task_type=task_type,
                    order_index=index,
                )

                db.session.add(topic)
                db.session.flush()

                created_topics += 1

            upsert_topic_task(topic)

        removed, skipped = prune_stale_topics(
            roadmap,
            len(curriculum)
        )

        removed_topics += removed
        kept_linked_stale_topics += skipped

        print(
            f"  -> {len(curriculum)} topics seeded "
            f"({task_type}); removed {removed} stale topic(s)"
        )

    db.session.commit()

    # --------------------------------------------------------
    # FINAL REPORT
    # --------------------------------------------------------

    print()
    print("=" * 60)
    print("SKILLSWAP - FULL ROADMAP SEED COMPLETE")
    print("=" * 60)

    print()
    print("ACTIVE CODING SKILLS:")
    print("  1. Python")
    print("  2. Java")
    print("  3. JavaScript")
    print("  4. C++")
    print("  5. SQL")

    print()
    print("NON-CODING ROADMAPS:")
    print("  Languages  -> English, Hindi, Spanish, French, German")
    print("  Creative   -> UI/UX, Graphic Design, Video Editing,")
    print("                Photography, Illustration, UI/UX Design")
    print("  Marketing  -> Digital Marketing, SEO, Social Media")
    print("                Marketing, Content Marketing, Branding")

    print()
    print(f"Roadmaps created : {created_roadmaps}")
    print(f"Roadmaps updated : {updated_roadmaps}")
    print(f"Topics created   : {created_topics}")
    print(f"Topics updated   : {updated_topics}")
    print(f"Topics removed   : {removed_topics}")
    print(f"Stale topics kept (linked data): {kept_linked_stale_topics}")
    print(
        f"Active skills    : "
        f"{Skill.query.filter_by(is_active=True).count()}"
    )
    print(
        f"Active roadmaps  : "
        f"{Roadmap.query.filter_by(is_active=True).count()}"
    )
    print(f"Total roadmaps   : {Roadmap.query.count()}")
    print(f"Total topics     : {RoadmapTopic.query.count()}")
    print("=" * 60)
