from app import app, db
from models import Skill, Assessment, AssessmentQuestion


# ============================================================
# SKILLS
# ============================================================

skills_data = [
    # CODING
    {
        "name": "Python",
        "slug": "python",
        "category": "coding",
        "description": "Learn Python programming from fundamentals to advanced concepts."
    },
    {
        "name": "JavaScript",
        "slug": "javascript",
        "category": "coding",
        "description": "Learn JavaScript for web development and programming."
    },
    {
        "name": "Java",
        "slug": "java",
        "category": "coding",
        "description": "Learn Java programming and object-oriented development."
    },
    {
        "name": "C",
        "slug": "c",
        "category": "coding",
        "description": "Learn C programming fundamentals and problem solving."
    },
    {
        "name": "C++",
        "slug": "cpp",
        "category": "coding",
        "description": "Learn C++ programming, OOP and problem solving."
    },
    {
        "name": "C#",
        "slug": "csharp",
        "category": "coding",
        "description": "Learn C# programming and application development."
    },
    {
        "name": "PHP",
        "slug": "php",
        "category": "coding",
        "description": "Learn PHP for backend and web development."
    },
    {
        "name": "SQL",
        "slug": "sql",
        "category": "coding",
        "description": "Learn SQL and relational database management."
    },

    # LANGUAGES
    {
        "name": "English",
        "slug": "english",
        "category": "languages",
        "description": "Improve English speaking, writing, listening and communication."
    },
    {
        "name": "Hindi",
        "slug": "hindi",
        "category": "languages",
        "description": "Learn Hindi communication, vocabulary and grammar."
    },
    {
        "name": "Spanish",
        "slug": "spanish",
        "category": "languages",
        "description": "Learn Spanish speaking, writing and everyday communication."
    },
    {
        "name": "French",
        "slug": "french",
        "category": "languages",
        "description": "Learn French vocabulary, grammar and communication."
    },
    {
        "name": "German",
        "slug": "german",
        "category": "languages",
        "description": "Learn German communication, vocabulary and grammar."
    },

    # CREATIVE
    {
        "name": "UI/UX Design",
        "slug": "ui_ux",
        "category": "creative",
        "description": "Learn user interface and user experience design."
    },
    {
        "name": "Graphic Design",
        "slug": "graphic-design",
        "category": "creative",
        "description": "Learn visual design, composition, typography and branding."
    },
    {
        "name": "Video Editing",
        "slug": "video-editing",
        "category": "creative",
        "description": "Learn video editing, storytelling and post-production."
    },
    {
        "name": "Photography",
        "slug": "photography",
        "category": "creative",
        "description": "Learn photography fundamentals, composition and visual storytelling."
    },
    {
        "name": "Illustration",
        "slug": "illustration",
        "category": "creative",
        "description": "Learn digital and traditional illustration techniques."
    },

    # MARKETING
    {
        "name": "Digital Marketing",
        "slug": "digital-marketing",
        "category": "marketing",
        "description": "Learn digital marketing strategies and campaign planning."
    },
    {
        "name": "SEO",
        "slug": "seo",
        "category": "marketing",
        "description": "Learn search engine optimization and organic growth."
    },
    {
        "name": "Social Media Marketing",
        "slug": "social-media-marketing",
        "category": "marketing",
        "description": "Learn social media strategy, content and audience growth."
    },
    {
        "name": "Content Marketing",
        "slug": "content-marketing",
        "category": "marketing",
        "description": "Learn content strategy, creation and distribution."
    },
    {
        "name": "Branding",
        "slug": "branding",
        "category": "marketing",
        "description": "Learn brand identity, positioning and brand strategy."
    },
]


# ============================================================
# ASSESSMENT QUESTIONS
#
# Format:
# "skill-slug": [
#     (question, correct_answer, difficulty),
# ]
#
# Difficulty:
# Beginner / Intermediate / Pro
# ============================================================

assessment_data = {

    # ========================================================
    # PYTHON
    # ========================================================

    "python": [
        (
            """What is the exact output?

def modify(data):
    data += [4]
    return data

numbers = [1, 2, 3]
result = modify(numbers)

print(numbers)
print(result)""",
            "[1, 2, 3, 4] | [1, 2, 3, 4]",
            "Beginner"
        ),
        (
            """What is the exact output?

x = 10

def test():
    x = 20

    def inner():
        print(x)

    x = 30
    inner()

test()""",
            "30",
            "Beginner"
        ),
        (
            """What is the exact output?

items = [1, 2, 3, 4, 5]

result = list(
    map(
        lambda x: x * 2,
        filter(lambda x: x % 2 != 0, items)
    )
)

print(result)""",
            "[2, 6, 10]",
            "Beginner"
        ),
        (
            """What is the exact output?

x = [1, 2]
y = x
y.append(3)

print(x is y)
print(x)""",
            "True | [1, 2, 3]",
            "Beginner"
        ),
        (
            """What is the exact output?

def func(value, cache={}):
    if value not in cache:
        cache[value] = value * value
    return cache

print(func(2))
print(func(3))

cache_result = func(2)
cache_result[4] = 16

print(func(4))""",
            "{2: 4} | {2: 4, 3: 9} | {2: 4, 3: 9, 4: 16}",
            "Intermediate"
        ),
        (
            """What is the exact output?

class A:
    value = 10

    def __init__(self):
        self.value = 20

    def get_value(self):
        return self.value


class B(A):
    value = 30

    def get_value(self):
        return super().get_value() + 10


obj = B()

print(obj.value)
print(obj.get_value())""",
            "20 | 30",
            "Intermediate"
        ),
        (
            """What is the exact output?

def outer():
    x = 10

    def first():
        nonlocal x
        x += 5
        return x

    def second():
        nonlocal x
        x *= 2
        return x

    return first, second

a, b = outer()

print(a())
print(b())
print(a())""",
            "15 | 30 | 35",
            "Intermediate"
        ),
        (
            """What is the exact output?

def numbers():
    for i in range(5):
        yield i

g = numbers()

print(next(g))
print(list(g))
print(next(g, "Finished"))""",
            "0 | [1, 2, 3, 4] | Finished",
            "Pro"
        ),
        (
            """What is the exact output?

def decorator(func):
    def wrapper(*args, **kwargs):
        print("Before")
        result = func(*args, **kwargs)
        print("After")
        return result

    return wrapper

@decorator
def calculate(a, b):
    return a * b

print(calculate(3, 4))""",
            "Before | After | 12",
            "Pro"
        ),
        (
            """What is the exact output?

class A:
    def __init__(self):
        self.value = 10

    def __getattribute__(self, name):
        if name == "value":
            return object.__getattribute__(self, name) + 5
        return object.__getattribute__(self, name)

obj = A()

print(obj.value)
print(obj.__dict__["value"])""",
            "15 | 10",
            "Pro"
        ),
    ],


    # ========================================================
    # JAVASCRIPT
    # ========================================================

    "javascript": [
        (
            """What is the exact output?

let x = 10;

function test() {
    let x = 20;
    console.log(x);
}

test();
console.log(x);""",
            "20 | 10",
            "Beginner"
        ),
        (
            """What is the exact output?

const arr = [1, 2, 3];
const result = arr.map(x => x * 2);

console.log(result);""",
            "[2, 4, 6]",
            "Beginner"
        ),
        (
            """What is the exact output?

console.log(typeof null);
console.log(typeof undefined);""",
            "object | undefined",
            "Beginner"
        ),
        (
            """What is the exact output?

const a = "5";
const b = 2;

console.log(a + b);
console.log(a - b);""",
            "52 | 3",
            "Beginner"
        ),
        (
            """What is the exact output?

var x = 1;

function test() {
    console.log(x);
    var x = 2;
}

test();""",
            "undefined",
            "Intermediate"
        ),
        (
            """What is the exact output?

const obj = {
    value: 10,
    getValue() {
        return this.value;
    }
};

const fn = obj.getValue;

console.log(fn());""",
            "undefined",
            "Intermediate"
        ),
        (
            """What is the exact output?

function outer() {
    let count = 0;

    return function () {
        count++;
        return count;
    };
}

const fn = outer();

console.log(fn());
console.log(fn());
console.log(fn());""",
            "1 | 2 | 3",
            "Intermediate"
        ),
        (
            """What is the exact output?

console.log("A");

setTimeout(() => {
    console.log("B");
}, 0);

Promise.resolve().then(() => {
    console.log("C");
});

console.log("D");""",
            "A | D | C | B",
            "Pro"
        ),
        (
            """What is the exact output?

const obj = {
    x: 10,
    method() {
        return () => this.x;
    }
};

const fn = obj.method();

console.log(fn());""",
            "10",
            "Pro"
        ),
        (
            """What is the exact output?

const a = {};
const b = {};

console.log(a === b);
console.log(Object.is(NaN, NaN));""",
            "false | true",
            "Pro"
        ),
    ],


    # ========================================================
    # JAVA
    # ========================================================

    "java": [
        (
            """What is the output?

int x = 10;
System.out.println(x++ + ++x);""",
            "22",
            "Beginner"
        ),
        (
            """What is the output?

String a = "hello";
String b = new String("hello");

System.out.println(a == b);
System.out.println(a.equals(b));""",
            "false | true",
            "Beginner"
        ),
        (
            """What is the output?

int[] arr = {1, 2, 3};
System.out.println(arr[1]);""",
            "2",
            "Beginner"
        ),
        (
            """What is the output?

for (int i = 0; i < 3; i++) {
    System.out.print(i);
}""",
            "012",
            "Beginner"
        ),
        (
            """What is the output?

class A {
    void show() {
        System.out.println("A");
    }
}

class B extends A {
    void show() {
        System.out.println("B");
    }
}

A obj = new B();
obj.show();""",
            "B",
            "Intermediate"
        ),
        (
            """What is the output?

static int count = 0;

static void test() {
    count++;
}

test();
test();

System.out.println(count);""",
            "2",
            "Intermediate"
        ),
        (
            """What is the output?

try {
    int x = 10 / 0;
    System.out.println(x);
} catch (ArithmeticException e) {
    System.out.println("Error");
}""",
            "Error",
            "Intermediate"
        ),
        (
            """What is printed?

class Test {
    static {
        System.out.print("S");
    }

    {
        System.out.print("I");
    }

    Test() {
        System.out.print("C");
    }
}

new Test();
new Test();""",
            "SICIC",
            "Pro"
        ),
        (
            """What is the output?

String s = null;

try {
    System.out.println(s.length());
} catch (NullPointerException e) {
    System.out.println("NPE");
} finally {
    System.out.println("Done");
}""",
            "NPE | Done",
            "Pro"
        ),
        (
            """What is the output?

Integer a = 127;
Integer b = 127;

Integer c = 128;
Integer d = 128;

System.out.println(a == b);
System.out.println(c == d);""",
            "true | false",
            "Pro"
        ),
    ],


    # ========================================================
    # C
    # ========================================================

    "c": [
        (
            """What is the output?

int x = 5;
printf("%d", ++x);""",
            "6",
            "Beginner"
        ),
        (
            """What is the output?

int a = 10;
int b = 3;

printf("%d", a / b);""",
            "3",
            "Beginner"
        ),
        (
            """What is the output?

int arr[] = {10, 20, 30};
printf("%d", *(arr + 1));""",
            "20",
            "Beginner"
        ),
        (
            """What is the output?

char str[] = "Hello";
printf("%zu", strlen(str));""",
            "5",
            "Beginner"
        ),
        (
            """What is the output?

int x = 10;
int *p = &x;

*p = 20;

printf("%d", x);""",
            "20",
            "Intermediate"
        ),
        (
            """What is the output?

void change(int *p) {
    *p = *p + 10;
}

int x = 5;
change(&x);

printf("%d", x);""",
            "15",
            "Intermediate"
        ),
        (
            """What is the output?

int x = 5;

if (x > 3)
    if (x > 10)
        printf("A");
    else
        printf("B");""",
            "B",
            "Intermediate"
        ),
        (
            """What does this print?

int x = 10;
printf("%d", *(&x));""",
            "10",
            "Pro"
        ),
        (
            """What is the output?

int arr[3] = {1, 2, 3};
int *p = arr;

printf("%d", *(p + 2));""",
            "3",
            "Pro"
        ),
        (
            """What is the output?

static int x = 5;

void test() {
    static int x = 10;
    x++;
    printf("%d ", x);
}

test();
test();""",
            "11 12",
            "Pro"
        ),
    ],


    # ========================================================
    # C++
    # ========================================================

    "cpp": [
        (
            """What is the output?

int x = 10;
cout << ++x;""",
            "11",
            "Beginner"
        ),
        (
            """What is the output?

vector<int> v = {1, 2, 3};
cout << v[1];""",
            "2",
            "Beginner"
        ),
        (
            """What is the output?

string a = "Hello";
string b = "World";

cout << a + " " + b;""",
            "Hello World",
            "Beginner"
        ),
        (
            """What is the output?

int a = 10;
int& ref = a;

ref = 20;

cout << a;""",
            "20",
            "Beginner"
        ),
        (
            """What is printed?

class A {
public:
    virtual void show() {
        cout << "A";
    }
};

class B : public A {
public:
    void show() override {
        cout << "B";
    }
};

A* obj = new B();
obj->show();""",
            "B",
            "Intermediate"
        ),
        (
            """What is the output?

int x = 10;

auto lambda = [&x]() {
    x += 5;
};

lambda();

cout << x;""",
            "15",
            "Intermediate"
        ),
        (
            """What is the output?

vector<int> v = {1, 2, 3, 4};

auto it = v.begin();
++it;

cout << *it;""",
            "2",
            "Intermediate"
        ),
        (
            """What is printed?

class Test {
public:
    Test() {
        cout << "C";
    }

    ~Test() {
        cout << "D";
    }
};

{
    Test t;
}

cout << "X";""",
            "CDX",
            "Pro"
        ),
        (
            """What is the output?

unique_ptr<int> p = make_unique<int>(10);
unique_ptr<int> q = move(p);

cout << *q;
cout << (p == nullptr);""",
            "10 | 1",
            "Pro"
        ),
        (
            """What is the output?

int x = 10;

auto f = [x]() mutable {
    x++;
    return x;
};

cout << f();
cout << x;""",
            "11 | 10",
            "Pro"
        ),
    ],


    # ========================================================
    # C#
    # ========================================================

    "csharp": [
        (
            """What is the output?

int x = 10;
Console.WriteLine(++x);""",
            "11",
            "Beginner"
        ),
        (
            """What is the output?

string a = "hello";
string b = new string("hello".ToCharArray());

Console.WriteLine(a == b);""",
            "True",
            "Beginner"
        ),
        (
            """What is the output?

int[] arr = {1, 2, 3};
Console.WriteLine(arr[2]);""",
            "3",
            "Beginner"
        ),
        (
            """What is the output?

var numbers = new[] {1, 2, 3};

var result = numbers.Select(x => x * 2);

Console.WriteLine(string.Join(",", result));""",
            "2,4,6",
            "Beginner"
        ),
        (
            """What is printed?

class A {
    public virtual void Show() {
        Console.WriteLine("A");
    }
}

class B : A {
    public override void Show() {
        Console.WriteLine("B");
    }
}

A obj = new B();
obj.Show();""",
            "B",
            "Intermediate"
        ),
        (
            """What is the output?

int x = 10;

Action action = () => {
    x += 5;
};

action();

Console.WriteLine(x);""",
            "15",
            "Intermediate"
        ),
        (
            """What is the output?

var values = new List<int> {1, 2, 3};

var result = values
    .Where(x => x > 1)
    .Select(x => x * 10);

Console.WriteLine(string.Join(",", result));""",
            "20,30",
            "Intermediate"
        ),
        (
            """What is the output?

int x = 10;

object obj = x;

Console.WriteLine(obj.GetType().Name);""",
            "Int32",
            "Pro"
        ),
        (
            """What is printed?

async Task<int> GetValue() {
    await Task.Delay(1);
    return 10;
}

var result = GetValue().Result;
Console.WriteLine(result);""",
            "10",
            "Pro"
        ),
        (
            """What is the output?

int? x = null;

Console.WriteLine(x ?? 50);""",
            "50",
            "Pro"
        ),
    ],


    # ========================================================
    # PHP
    # ========================================================

    "php": [
        (
            """What is the output?

$x = 10;
echo $x + 5;""",
            "15",
            "Beginner"
        ),
        (
            """What is the output?

$a = "5";
$b = 2;

echo $a + $b;""",
            "7",
            "Beginner"
        ),
        (
            """What is the output?

$arr = [10, 20, 30];
echo $arr[1];""",
            "20",
            "Beginner"
        ),
        (
            """What is the output?

$a = 10;
$b = "10";

var_dump($a == $b);
var_dump($a === $b);""",
            "true | false",
            "Beginner"
        ),
        (
            """What is the output?

function test() {
    static $x = 0;
    $x++;
    return $x;
}

echo test();
echo test();
echo test();""",
            "123",
            "Intermediate"
        ),
        (
            """What is the output?

$a = [1, 2, 3];

foreach ($a as &$value) {
    $value *= 2;
}

print_r($a);""",
            "[2, 4, 6]",
            "Intermediate"
        ),
        (
            """What is the output?

$name = "PHP";

$fn = function() use ($name) {
    return $name;
};

echo $fn();""",
            "PHP",
            "Intermediate"
        ),
        (
            """What is the output?

class A {
    public function show() {
        echo "A";
    }
}

class B extends A {
    public function show() {
        echo "B";
    }
}

$obj = new B();
$obj->show();""",
            "B",
            "Pro"
        ),
        (
            """What is the output?

$a = null;

echo $a ?? "default";""",
            "default",
            "Pro"
        ),
        (
            """What is the output?

$arr = [1, 2, 3];

$result = array_map(
    fn($x) => $x * $x,
    $arr
);

print_r($result);""",
            "[1, 4, 9]",
            "Pro"
        ),
    ],


    # ========================================================
    # SQL
    # ========================================================

    "sql": [
        (
            """A table has rows with salaries 1000, 2000 and 3000.
What does AVG(salary) return?""",
            "2000",
            "Beginner"
        ),
        (
            """What does COUNT(*) count in SQL?""",
            "Rows",
            "Beginner"
        ),
        (
            """Which SQL clause filters rows before grouping?""",
            "WHERE",
            "Beginner"
        ),
        (
            """Which SQL clause filters grouped results?""",
            "HAVING",
            "Beginner"
        ),
        (
            """Given employees(id, department_id, salary), write the SQL expression
to return the maximum salary for each department.""",
            "SELECT department_id, MAX(salary) FROM employees GROUP BY department_id",
            "Intermediate"
        ),
        (
            """What does INNER JOIN return when two tables are joined?""",
            "Matching rows from both tables",
            "Intermediate"
        ),
        (
            """What is the difference between WHERE and HAVING?""",
            "WHERE filters rows before grouping; HAVING filters groups after grouping",
            "Intermediate"
        ),
        (
            """Given employees(id, salary), write a query that returns employees
whose salary is greater than the average salary.""",
            "SELECT * FROM employees WHERE salary > (SELECT AVG(salary) FROM employees)",
            "Pro"
        ),
        (
            """What does a window function allow you to calculate without collapsing rows?""",
            "Calculations across related rows while preserving individual rows",
            "Pro"
        ),
        (
            """Which SQL isolation problem occurs when one transaction reads
data written by another uncommitted transaction?""",
            "Dirty read",
            "Pro"
        ),
    ],


    # ========================================================
    # ENGLISH
    # ========================================================

    "english": [
        (
            "Identify the correct tense: 'She has been working here for five years.'",
            "Present perfect continuous",
            "Beginner"
        ),
        (
            "What is the plural form of 'analysis'?",
            "analyses",
            "Beginner"
        ),
        (
            "What is the comparative form of 'good'?",
            "better",
            "Beginner"
        ),
        (
            "Identify the adjective: 'The extremely talented student won.'",
            "talented",
            "Beginner"
        ),
        (
            "Change to passive voice: 'The team completed the project.'",
            "The project was completed by the team",
            "Intermediate"
        ),
        (
            "Correct the sentence: 'Neither of the answers are correct.'",
            "Neither of the answers is correct",
            "Intermediate"
        ),
        (
            "What type of clause is 'because she was tired'?",
            "Adverbial clause",
            "Intermediate"
        ),
        (
            "Explain the difference between 'affect' and 'effect'.",
            "Affect is usually a verb; effect is usually a noun",
            "Pro"
        ),
        (
            "Convert to reported speech: He said, 'I am working.'",
            "He said that he was working",
            "Pro"
        ),
        (
            "Identify the rhetorical device: 'The wind whispered through the trees.'",
            "Personification",
            "Pro"
        ),
    ],


    # ========================================================
    # HINDI
    # ========================================================

    "hindi": [
        (
            "‘लड़का’ शब्द का बहुवचन क्या है?",
            "लड़के",
            "Beginner"
        ),
        (
            "‘सुंदर’ किस प्रकार का शब्द है?",
            "विशेषण",
            "Beginner"
        ),
        (
            "‘मैं स्कूल जाता हूँ’ में क्रिया कौन-सी है?",
            "जाता हूँ",
            "Beginner"
        ),
        (
            "‘दिन’ का विलोम शब्द क्या है?",
            "रात",
            "Beginner"
        ),
        (
            "‘राम ने खाना खाया’ वाक्य में कर्ता कौन है?",
            "राम",
            "Intermediate"
        ),
        (
            "‘जो मेहनत करता है, वह सफल होता है’ में आश्रित उपवाक्य कौन-सा है?",
            "जो मेहनत करता है",
            "Intermediate"
        ),
        (
            "‘आँखों का तारा’ मुहावरे का अर्थ क्या है?",
            "बहुत प्रिय व्यक्ति",
            "Intermediate"
        ),
        (
            "‘चरण कमल’ में कौन-सा अलंकार है?",
            "रूपक",
            "Pro"
        ),
        (
            "‘कनक कनक ते सौ गुनी’ में कौन-सा अलंकार है?",
            "यमक",
            "Pro"
        ),
        (
            "‘वीरों का कैसा हो वसंत’ पंक्ति में प्रमुख रस कौन-सा है?",
            "वीर रस",
            "Pro"
        ),
    ],


    # ========================================================
    # SPANISH
    # ========================================================

    "spanish": [
        (
            "What is the Spanish translation of 'house'?",
            "casa",
            "Beginner"
        ),
        (
            "What is the plural of 'libro'?",
            "libros",
            "Beginner"
        ),
        (
            "What is the present tense of 'hablar' for 'yo'?",
            "hablo",
            "Beginner"
        ),
        (
            "What is the opposite of 'grande'?",
            "pequeño",
            "Beginner"
        ),
        (
            "Conjugate 'ser' for 'nosotros' in the present tense.",
            "somos",
            "Intermediate"
        ),
        (
            "What is the preterite form of 'tener' for 'yo'?",
            "tuve",
            "Intermediate"
        ),
        (
            "Translate: 'I have been studying Spanish for two years.'",
            "He estado estudiando español durante dos años",
            "Intermediate"
        ),
        (
            "What is the subjunctive present form of 'ser' for 'yo'?",
            "sea",
            "Pro"
        ),
        (
            "Translate: 'If I had known, I would have told you.'",
            "Si lo hubiera sabido, te lo habría dicho",
            "Pro"
        ),
        (
            "Which tense is 'hubiera sabido'?",
            "Pluperfect subjunctive",
            "Pro"
        ),
    ],


    # ========================================================
    # FRENCH
    # ========================================================

    "french": [
        (
            "What is the French word for 'book'?",
            "livre",
            "Beginner"
        ),
        (
            "What is the plural of 'cheval'?",
            "chevaux",
            "Beginner"
        ),
        (
            "Conjugate 'être' for 'je' in the present tense.",
            "suis",
            "Beginner"
        ),
        (
            "What is the opposite of 'grand'?",
            "petit",
            "Beginner"
        ),
        (
            "Conjugate 'avoir' for 'nous' in the present tense.",
            "avons",
            "Intermediate"
        ),
        (
            "What is the passé composé of 'aller' for 'je'?",
            "je suis allé",
            "Intermediate"
        ),
        (
            "Translate: 'I have been working since morning.'",
            "Je travaille depuis ce matin",
            "Intermediate"
        ),
        (
            "What is the subjunctive present of 'être' for 'je'?",
            "sois",
            "Pro"
        ),
        (
            "Translate: 'If I had known, I would have come.'",
            "Si j'avais su, je serais venu",
            "Pro"
        ),
        (
            "Which tense is 'j'aurais fait'?",
            "Conditional perfect",
            "Pro"
        ),
    ],


    # ========================================================
    # GERMAN
    # ========================================================

    "german": [
        (
            "What is the German word for 'house'?",
            "Haus",
            "Beginner"
        ),
        (
            "What is the plural of 'Kind'?",
            "Kinder",
            "Beginner"
        ),
        (
            "Conjugate 'sein' for 'ich'.",
            "bin",
            "Beginner"
        ),
        (
            "What is the opposite of 'groß'?",
            "klein",
            "Beginner"
        ),
        (
            "What is the dative form of 'der Mann'?",
            "dem Mann",
            "Intermediate"
        ),
        (
            "What is the past participle of 'gehen'?",
            "gegangen",
            "Intermediate"
        ),
        (
            "Translate: 'I have been living here for two years.'",
            "Ich lebe seit zwei Jahren hier",
            "Intermediate"
        ),
        (
            "What is Konjunktiv II of 'sein' for 'ich'?",
            "wäre",
            "Pro"
        ),
        (
            "Translate: 'If I had known, I would have helped you.'",
            "Wenn ich es gewusst hätte, hätte ich dir geholfen",
            "Pro"
        ),
        (
            "What grammatical case is used after 'mit'?",
            "Dative",
            "Pro"
        ),
    ],


    # ========================================================
    # UI/UX DESIGN
    # ========================================================
    "ui_ux": [
        
    ("""A mobile app has a primary CTA button that users frequently miss even though it has a bright color. The button is placed below several secondary actions and has weak visual hierarchy.

What UX principle should be improved first?""", "visual hierarchy", "Beginner"),

    ("""A designer uses red text on a green background for an important status message. Some users cannot distinguish the message properly.

What accessibility problem is most likely occurring?""", "color contrast", "Beginner"),

    ("""A checkout form asks users to enter their phone number twice, even though the first value can already be validated.

Which UX problem does this primarily create?""", "redundant input", "Beginner"),

    ("""A navigation menu contains 18 equally prominent options, making it difficult for users to decide where to go.

Which UX principle suggests reducing the user's decision burden by organizing or grouping choices?""", "chunking", "Beginner"),

    ("""An e-commerce app changes its checkout button from "Place Order" to "Continue". Usability testing shows users hesitate because they are unsure what will happen after clicking it.

Which UX concept has been weakened?""", "affordance", "Intermediate"),

    ("""A dashboard contains many cards. Eye-tracking shows that users repeatedly scan between unrelated sections before finding important information.

Which design technique would best improve the information structure?""", "visual grouping", "Intermediate"),

    ("""A designer creates a form where the error message appears only after the user submits the entire form. Users then have to search through multiple fields to find what went wrong.

What interaction design principle should be applied to improve this?""", "immediate feedback", "Intermediate"),

    ("""A product team runs an A/B test where Version A increases conversion by 8%, but the sample size is small and the confidence interval is very wide.

Should the team immediately conclude that Version A is better? Explain the statistical UX research issue.""", "no|insufficient sample size|insufficient evidence|not statistically significant", "Pro"),

    ("""A design system defines spacing tokens as 4px, 8px, 12px, 16px, 24px and 32px. A designer repeatedly introduces custom values such as 13px, 19px and 27px for individual components.

What design-system principle is being violated?""", "design token consistency", "Pro"),

    ("""A UX team discovers that users complete a task successfully but repeatedly make unnecessary navigation steps. The completion rate is high, but task time and interaction count are significantly higher than expected.

Which usability metric should the team primarily investigate?""", "efficiency|task efficiency|time on task|interaction count", "Pro"),
],


    # ========================================================
    # GRAPHIC DESIGN
    # ========================================================

    "graphic_design": [
        (
            "What are the three primary colors in traditional subtractive color theory?",
            "Red, Yellow, Blue",
            "Beginner"
        ),
        (
            "What does typography primarily control?",
            "The visual appearance and arrangement of text",
            "Beginner"
        ),
        (
            "What is visual hierarchy?",
            "Organizing elements so their importance is visually communicated",
            "Beginner"
        ),
        (
            "What does contrast help establish?",
            "Difference and emphasis between visual elements",
            "Beginner"
        ),
        (
            "What is the difference between RGB and CMYK?",
            "RGB is additive for screens; CMYK is subtractive for print",
            "Intermediate"
        ),
        (
            "What is kerning?",
            "Adjusting spacing between individual letter pairs",
            "Intermediate"
        ),
        (
            "What is the purpose of a grid system?",
            "To create consistent alignment and structure",
            "Intermediate"
        ),
        (
            "What is the difference between vector and raster graphics?",
            "Vector graphics use mathematical paths; raster graphics use pixels",
            "Pro"
        ),
        (
            "What does Gestalt proximity mean?",
            "Elements close to each other are perceived as related",
            "Pro"
        ),
        (
            "Why is color contrast important for accessibility?",
            "It improves readability and allows users with visual limitations to distinguish content",
            "Pro"
        ),
    ],


    # ========================================================
    # VIDEO EDITING
    # ========================================================

    "video_editing": [
        (
            "What is the purpose of a timeline in video editing?",
            "To arrange and edit media clips in sequence",
            "Beginner"
        ),
        (
            "What does FPS stand for?",
            "Frames Per Second",
            "Beginner"
        ),
        (
            "What is a cut?",
            "A transition from one shot directly to another",
            "Beginner"
        ),
        (
            "What is B-roll?",
            "Supplementary footage used to support the main footage",
            "Beginner"
        ),
        (
            "What is the purpose of color correction?",
            "To correct exposure, white balance and color inconsistencies",
            "Intermediate"
        ),
        (
            "What is color grading?",
            "Styling footage to create a specific visual mood or look",
            "Intermediate"
        ),
        (
            "What is keyframing?",
            "Defining values at specific points in time so properties can change over time",
            "Intermediate"
        ),
        (
            "What is bitrate?",
            "The amount of data used to represent video or audio per unit of time",
            "Pro"
        ),
        (
            "Why can excessive compression produce visible artifacts?",
            "Compression removes or approximates information, causing loss of detail and visual errors",
            "Pro"
        ),
        (
            "What is the purpose of an audio compressor?",
            "To reduce dynamic range by controlling differences between loud and quiet signals",
            "Pro"
        ),
    ],


    # ========================================================
    # PHOTOGRAPHY
    # ========================================================

    "photography": [
        (
            "What are the three main exposure controls?",
            "Aperture, shutter speed, ISO",
            "Beginner"
        ),
        (
            "What does aperture control?",
            "Lens opening and depth of field",
            "Beginner"
        ),
        (
            "What does shutter speed control?",
            "Exposure duration and motion blur",
            "Beginner"
        ),
        (
            "What does ISO control?",
            "Sensor sensitivity and image noise",
            "Beginner"
        ),
        (
            "What is depth of field?",
            "The range of distances appearing acceptably sharp",
            "Intermediate"
        ),
        (
            "What is white balance?",
            "Adjusting color temperature so neutral objects appear neutral",
            "Intermediate"
        ),
        (
            "What is the rule of thirds?",
            "Dividing the frame into a 3x3 grid and placing important elements near intersections",
            "Intermediate"
        ),
        (
            "What is dynamic range?",
            "The range between the darkest and brightest detail a camera can capture",
            "Pro"
        ),
        (
            "What is focal length?",
            "The optical distance that determines angle of view and magnification",
            "Pro"
        ),
        (
            "Why does increasing ISO often increase visible noise?",
            "Higher ISO amplifies the sensor signal and also amplifies noise",
            "Pro"
        ),
    ],


    # ========================================================
    # ILLUSTRATION
    # ========================================================

    "illustration": [
        (
            "What is line weight?",
            "The thickness or variation of a drawn line",
            "Beginner"
        ),
        (
            "What is silhouette?",
            "A solid shape showing the outer contour of a subject",
            "Beginner"
        ),
        (
            "What is negative space?",
            "The empty space surrounding or between subjects",
            "Beginner"
        ),
        (
            "What is gesture drawing?",
            "A quick drawing capturing movement, pose and overall action",
            "Beginner"
        ),
        (
            "What is perspective?",
            "A system for representing three-dimensional depth on a two-dimensional surface",
            "Intermediate"
        ),
        (
            "What is foreshortening?",
            "Representing an object so it appears shorter due to its angle toward the viewer",
            "Intermediate"
        ),
        (
            "What is value in drawing?",
            "The lightness or darkness of a color or tone",
            "Intermediate"
        ),
        (
            "What is atmospheric perspective?",
            "Using reduced contrast, saturation and detail to suggest distance",
            "Pro"
        ),
        (
            "Why is edge control important in illustration?",
            "It controls visual focus, depth and separation between forms",
            "Pro"
        ),
        (
            "What is the difference between additive and subtractive color mixing?",
            "Additive mixing combines light; subtractive mixing combines pigments or inks",
            "Pro"
        ),
    ],


    # ========================================================
    # DIGITAL MARKETING
    # ========================================================

    "digital_marketing": [
        (
            "What does CTR stand for?",
            "Click Through Rate",
            "Beginner"
        ),
        (
            "What does CPC stand for?",
            "Cost Per Click",
            "Beginner"
        ),
        (
            "What does SEO stand for?",
            "Search Engine Optimization",
            "Beginner"
        ),
        (
            "What is a conversion?",
            "A desired action completed by a user",
            "Beginner"
        ),
        (
            "What is a marketing funnel?",
            "The stages a prospect moves through from awareness to conversion",
            "Intermediate"
        ),
        (
            "What is customer acquisition cost?",
            "The average cost required to acquire one customer",
            "Intermediate"
        ),
        (
            "What is A/B testing?",
            "Comparing two versions to determine which performs better",
            "Intermediate"
        ),
        (
            "Why can attribution models produce different ROI results?",
            "Different models assign conversion credit to different touchpoints",
            "Pro"
        ),
        (
            "What is lifetime customer value?",
            "The expected total value generated by a customer over the relationship",
            "Pro"
        ),
        (
            "What is incrementality testing?",
            "Measuring conversions caused by marketing that would not have occurred without it",
            "Pro"
        ),
    ],


    # ========================================================
    # SEO
    # ========================================================

    "seo": [
        (
            "What does SEO stand for?",
            "Search Engine Optimization",
            "Beginner"
        ),
        (
            "What is a search query?",
            "The words or phrase entered into a search engine",
            "Beginner"
        ),
        (
            "What is a title tag?",
            "The HTML title element describing a webpage",
            "Beginner"
        ),
        (
            "What is a backlink?",
            "A link from another website to your website",
            "Beginner"
        ),
        (
            "What is search intent?",
            "The underlying purpose behind a user's search",
            "Intermediate"
        ),
        (
            "What is canonicalization?",
            "Specifying the preferred URL among duplicate or similar pages",
            "Intermediate"
        ),
        (
            "What is crawl budget?",
            "The number of URLs a search engine crawler is willing or able to crawl",
            "Intermediate"
        ),
        (
            "Why can duplicate content cause indexing problems?",
            "Search engines may struggle to determine which version should be indexed or ranked",
            "Pro"
        ),
        (
            "What is structured data?",
            "Machine-readable markup that helps search engines understand page content",
            "Pro"
        ),
        (
            "What is the difference between crawling, indexing and ranking?",
            "Crawling discovers pages; indexing stores and understands them; ranking orders relevant results",
            "Pro"
        ),
    ],


    # ========================================================
    # SOCIAL MEDIA MARKETING
    # ========================================================

    "social_media_marketing": [
        (
            "What is engagement rate?",
            "The level of interaction with content relative to an audience or reach metric",
            "Beginner"
        ),
        (
            "What is organic reach?",
            "People who see content without paid promotion",
            "Beginner"
        ),
        (
            "What is a social media CTA?",
            "A call to action asking users to take a desired action",
            "Beginner"
        ),
        (
            "What is a content calendar?",
            "A planned schedule of content publishing",
            "Beginner"
        ),
        (
            "What is audience segmentation?",
            "Dividing an audience into groups based on shared characteristics",
            "Intermediate"
        ),
        (
            "What is social listening?",
            "Monitoring conversations and mentions to understand audience sentiment and trends",
            "Intermediate"
        ),
        (
            "What is community management?",
            "Building and maintaining relationships with an online audience",
            "Intermediate"
        ),
        (
            "Why can high engagement still produce poor campaign results?",
            "Engagement may not translate into the desired business outcome",
            "Pro"
        ),
        (
            "What is dark social?",
            "Content sharing or traffic that is difficult for analytics systems to attribute",
            "Pro"
        ),
        (
            "What is a holdout group in social advertising?",
            "A control group intentionally excluded from advertising to measure incremental impact",
            "Pro"
        ),
    ],


    # ========================================================
    # CONTENT MARKETING
    # ========================================================

    "content_marketing": [
        (
            "What is content marketing?",
            "Creating and distributing valuable content to attract and retain an audience",
            "Beginner"
        ),
        (
            "What is a blog post?",
            "A written piece of content published online",
            "Beginner"
        ),
        (
            "What is a CTA?",
            "Call To Action",
            "Beginner"
        ),
        (
            "What is a target audience?",
            "The specific group a piece of content is intended for",
            "Beginner"
        ),
        (
            "What is a content pillar?",
            "A major recurring topic that organizes a content strategy",
            "Intermediate"
        ),
        (
            "What is content repurposing?",
            "Adapting existing content into different formats or channels",
            "Intermediate"
        ),
        (
            "What is topical authority?",
            "Demonstrated depth and breadth of useful content around a subject",
            "Intermediate"
        ),
        (
            "Why should content strategy be connected to search intent?",
            "It helps content satisfy the actual information need behind searches",
            "Pro"
        ),
        (
            "What is content decay?",
            "A decline in traffic, relevance or performance of previously successful content",
            "Pro"
        ),
        (
            "What is a content gap analysis?",
            "Identifying useful topics or information competitors cover that your content lacks",
            "Pro"
        ),
    ],


    # ========================================================
    # BRANDING
    # ========================================================

    "branding": [
        (
            "What is a brand identity?",
            "The visual and verbal elements used to represent a brand",
            "Beginner"
        ),
        (
            "What is a logo?",
            "A visual mark representing a brand",
            "Beginner"
        ),
        (
            "What is brand color?",
            "A color associated with and consistently used by a brand",
            "Beginner"
        ),
        (
            "What is a tagline?",
            "A short phrase communicating a brand idea or promise",
            "Beginner"
        ),
        (
            "What is brand positioning?",
            "How a brand is deliberately perceived relative to competitors",
            "Intermediate"
        ),
        (
            "What is a brand archetype?",
            "A recognizable personality pattern used to shape brand character",
            "Intermediate"
        ),
        (
            "What is brand equity?",
            "The value created by people's awareness, associations and perception of a brand",
            "Intermediate"
        ),
        (
            "What is a brand promise?",
            "The consistent value or experience a brand commits to delivering",
            "Pro"
        ),
        (
            "What is brand architecture?",
            "The structure defining relationships among a company's brands, products and sub-brands",
            "Pro"
        ),
        (
            "Why is consistency important in brand identity?",
            "It strengthens recognition, trust and coherent perception across touchpoints",
            "Pro"
        ),
    ],
}


# ============================================================
# SEED SKILLS
# ============================================================
def seed_skills():
    with app.app_context():

        added = 0
        skipped = 0

        # Existing skills ek baar mein load karo
        existing_skills = {
            skill.slug: skill
            for skill in Skill.query.all()
        }

        for data in skills_data:

            # Slug already exists
            if data["slug"] in existing_skills:
                skipped += 1
                continue

            # Name already exists but slug different ho
            existing_by_name = Skill.query.filter(
                Skill.name == data["name"]
            ).first()

            if existing_by_name:
                skipped += 1
                continue

            skill = Skill(
                name=data["name"],
                slug=data["slug"],
                category=data["category"],
                description=data["description"]
            )

            db.session.add(skill)
            added += 1

        # Saare new skills ek saath save
        db.session.commit()

        print("========================================")
        print("SkillSwap Skill Seed Complete")
        print("========================================")
        print(f"Skills added   : {added}")
        print(f"Skills skipped : {skipped}")
        print(f"Total skills   : {Skill.query.count()}")
        print("========================================")
# ============================================================
# SEED ASSESSMENTS
# ============================================================

def seed_assessments():
    with app.app_context():

        assessments_added = 0
        questions_added = 0
        questions_updated = 0

        for skill_slug, questions in assessment_data.items():

            # ------------------------------------------------
            # FIND SKILL
            # ------------------------------------------------
            skill = Skill.query.filter_by(
                slug=skill_slug
            ).first()

            if not skill:
                print(
                    f"⚠️ Skill not found: {skill_slug}"
                )
                continue

            # ------------------------------------------------
            # FIND / CREATE ASSESSMENT
            # ------------------------------------------------
            assessment = Assessment.query.filter_by(
                skill_id=skill.id
            ).first()

            if not assessment:

                assessment = Assessment(
                    skill_id=skill.id,
                    title=f"{skill.name} Teaching Assessment",
                    description=(
                        f"Assessment to determine teaching "
                        f"level for {skill.name}."
                    ),
                    passing_score=0
                )

                db.session.add(assessment)
                db.session.flush()

                assessments_added += 1

            # ------------------------------------------------
            # EXISTING QUESTIONS
            # ------------------------------------------------
            existing_questions = {
                q.question.strip(): q
                for q in assessment.questions
            }

            # ------------------------------------------------
            # ADD / UPDATE QUESTIONS
            #
            # Supported formats:
            #
            # 3 values:
            # (
            #     question,
            #     correct_answer,
            #     difficulty
            # )
            #
            # 4 values:
            # (
            #     question,
            #     correct_answer,
            #     difficulty,
            #     question_type
            # )
            # ------------------------------------------------

            for item in questions:

                if len(item) == 3:

                    question_text = item[0]
                    correct_answer = item[1]
                    difficulty = item[2]

                    # Default for old questions
                    question_type = "text"

                elif len(item) == 4:

                    question_text = item[0]
                    correct_answer = item[1]
                    difficulty = item[2]
                    question_type = item[3]

                else:

                    print(
                        f"⚠️ Invalid assessment question "
                        f"format for {skill_slug}"
                    )

                    continue

                question_text = (
                    question_text.strip()
                )

                correct_answer = (
                    correct_answer.strip()
                )

                question_type = (
                    question_type.strip().lower()
                )

                # ------------------------------------------------
                # VALID QUESTION TYPES
                # ------------------------------------------------
                if question_type not in {
                    "text",
                    "output",
                    "code"
                }:

                    print(
                        f"⚠️ Invalid question type "
                        f"'{question_type}' "
                        f"for {skill_slug}"
                    )

                    question_type = "text"

                # ------------------------------------------------
                # EXISTING QUESTION
                # ------------------------------------------------
                existing = existing_questions.get(
                    question_text
                )

                if existing:

                    # Update existing question type
                    changed = False

                    if existing.correct_answer != correct_answer:

                        existing.correct_answer = (
                            correct_answer
                        )

                        changed = True

                    if existing.difficulty != difficulty:

                        existing.difficulty = (
                            difficulty
                        )

                        changed = True

                    if existing.question_type != question_type:

                        existing.question_type = (
                            question_type
                        )

                        changed = True

                    if changed:
                        questions_updated += 1

                    continue

                # ------------------------------------------------
                # NEW QUESTION
                # ------------------------------------------------
                question = AssessmentQuestion(
                    assessment_id=assessment.id,

                    question=question_text,

                    # MCQ fields intentionally blank
                    option_a="",
                    option_b="",
                    option_c="",
                    option_d="",

                    correct_answer=correct_answer,

                    difficulty=difficulty,

                    question_type=question_type
                )

                db.session.add(question)

                questions_added += 1

                existing_questions[
                    question_text
                ] = question

        # ------------------------------------------------
        # SAVE
        # ------------------------------------------------
        db.session.commit()

        print()
        print("========================================")
        print("SkillSwap Assessment Seed Complete")
        print("========================================")
        print(
            f"Assessments added  : {assessments_added}"
        )
        print(
            f"Questions added    : {questions_added}"
        )
        print(
            f"Questions updated  : {questions_updated}"
        )
        print(
            f"Total assessments  : "
            f"{Assessment.query.count()}"
        )
        print(
            f"Total questions    : "
            f"{AssessmentQuestion.query.count()}"
        )
        print("========================================")
# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    seed_skills()
    seed_assessments()