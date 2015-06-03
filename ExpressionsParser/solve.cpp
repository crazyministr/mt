/**
Написать простой калькулятор, который вычисляет выражения в исходном тексте и
заменяет их результатами вычисления.
Замене подвергаются выражения, взятые в специальные операторные скобки [[[ и ]]].
Калькулятор должен реализовывать как минимум арифметические операции с целыми и вещественными числами и
возможность изменять последовательность выполнения операций с помощью скобок.
Пример: текст «(2.2+3*8)/2=[[[(2.2+3*8)/2]]]» должен быть заменен на «(2+3*8)/2=13.1».

Для решения поставленной задачи будем использовать алгоритм "Обратной польской записи", описанный здесь:
https://en.wikipedia.org/wiki/Shunting-yard_algorithm

**/


#include <stdio.h> // for freopen
#include <stdlib.h> // for malloc
#include <string.h> // for string
#include <vector> // for vector
#include <stack> // for stack
#include <sstream> // for istringstream
#include <iostream>

using namespace std;

#define BUFFER_SIZE 256

FILE* in = stdin;
FILE* out = stdout;

vector<string> tokens, polish_tokens;

bool is_operator(string x) {
    return (x == "+" || x == "-" || x == "*" || x == "/");
}

void parse_expression(string expression) {
	/*
		В данную функцию переаётся строка expression
		Это входная строка, которую мы распарсим, прежде чем производить вычисления
		то что распарсим, сохраним в вектор tokens

		т.е. если входная строка 2+2, то вектор tokens будет содержать 3 элемента: 2, +, 2
	*/

    tokens.clear(); // очищаем вектор
    string number; // переменная number, в которую будем сохранять число
    for (int i = 0; i < (int) expression.size(); i++) {
        if (expression[i] == ' ')
            continue;

        stringstream ss;     //
        string current;      //
        ss << expression[i]; // эти 4 строчки из char делают string
        ss >> current;       // 
        if (expression[i] == '(' || expression[i] == ')' || is_operator(current)) { // если текущий символ скобка или оператор (+ - / *)
            if ((int) number.size() > 0) { // если длина строки больше нуля, значит там есть какое-то число и его нужно записать в вектор tokens
                tokens.push_back(number); // записываем строку number в вектор tokens
            }
            tokens.push_back(current); // записываем текущий симпол выражения в вектор tokens
            number = ""; // очищаем строку, отвечающую за число
        } else { // иначе
            int j = i;
            while ((expression[j] >= '0' && expression[j] <= '9') || expression[j] == '.') { // до тех пор пока идут цифры или точка, записываем это в строку number
                number = number + expression[j]; // дописываем очередной символ (цифру или точку) в строку number
                j++;  // увеличиваем счётчик
            }
            i = j - 1; // отератор основного цикла сдвигаем за прочитанное число
        }
    }
    if ((int) number.size() > 0) { // если после всего цикла в переменной number что-то осталось, то нужно записать это в вектор tokens
        tokens.push_back(number); // записываем это в вектор tokens
    }
}

int priority_operation(string x, string y) {
	/**
		Функция принимает 2 оператора
		Возвращает 0, если операторы одинаковы
		Возвращает -1, если приоритет первого меньше, чем приоритет второго
		Возвращает 1 если приоритет первого больше, чем приоритет второго
	**/
    if (x == y)
        return 0;

    return ((x == "+" || x == "-") &&
            (y == "*" || y == "/")) ? -1 : 1;
}

double parse_double(string s) {
	/**
		Функция принимает строку, которую пытаюется превратить в double (вещественное число)
	**/
    istringstream i(s); // закидываем строку в поток
    double x;
    if (!(i >> x)) // парсим её в переменную x и стразу проверяем, нормально ли распарсилось
        return 0;
    return x;
}

string double_to_string(double x) {
	/**
		функци принимает вещественное число и преобразовывает его в double
		Всё на подобии функции parse_double()
	**/
    ostringstream strs;
    strs << x;
    string str = strs.str();
    return str;
}

double eval() {
	/**
		Функция, которая по вектору polish_tokens вычисляет значение исходного выражения
		Вначале исходного файла есть ссылка, где почитать про Обратную польскую запись
	**/
    stack<string> _stack; // заводим стек для вычислений
    for (int i = 0; i < (int) polish_tokens.size(); i++) { // идём циклом по вектору
        if (is_operator(polish_tokens[i])) { // если текущий токен является оператором, то нужно достать из стека 2 элемента и произвести над ними эту операцию
            double y = parse_double(_stack.top()); // берём из вершины стека строку и сразу парсим её в double
            _stack.pop(); // удаляем элемент на вершине стека
            double x = parse_double(_stack.top()); // берём второй элемент на вершине стека
            _stack.pop(); // снова удаляем вершину стека
            if (polish_tokens[i] == "+") // если операция есть +
                _stack.push(double_to_string(x + y));  // положить в стек сумму x и y
            else if (polish_tokens[i] == "-") // дальше аналогично
                _stack.push(double_to_string(x - y));
            else if (polish_tokens[i] == "*")
                _stack.push(double_to_string(x * y));
            else if (polish_tokens[i] == "/")
                _stack.push(double_to_string(x / y));
        } else {
            _stack.push(polish_tokens[i]); // если polish_tokens[i] не являелось оператор (это значит, что это число), то положить его в стек
        }
    }
    string s = _stack.top(); // взять вершину стека и сохранить в строку s
    _stack.pop(); // удалить вершину стека
    return parse_double(s); // распарить строку s (которая является конечным ответом) и вернуть этот ответ
}

double polish(string expression) {
	/**
		функция принимает строку expression из которой сделает обратную польскую запись (сохраняя её в вектор polish_tokens)
		и вызовет функцию eval(), которая и вычислит результат
	**/
    parse_expression(expression); // вызываем функцию parse_expression, передавая туда строку expression
    polish_tokens.clear(); // очищаем вектор
    stack<string> _stack; // создаём стек
    for (int i = 0; i < (int) tokens.size(); i++) { // идём циклом по вектору tokens
        if (is_operator(tokens[i])) { // если текущий символ является оператором
            while (!_stack.empty() && is_operator(_stack.top())) { // пока стек не пустой и на вершине стека лежит оператор
                if (priority_operation(tokens[i], _stack.top()) <= 0) { // проверяем приоритет оператора (если первого меньше либо равен второму)
                    string s = _stack.top(); // взять элемент с вершины стека
                    _stack.pop(); // удалть элемент с вершины стека
                    polish_tokens.push_back(s); // записать элемент в вектор polish_tokens
                }
                else
                    break; // выйти из while
            }
            _stack.push(tokens[i]); // положить tokens[i] в стек
        } else if (tokens[i] == "(") { // если текущий токен является открывающей скобочкой
            _stack.push(tokens[i]); // положить её в стек
        } else if (tokens[i] == ")") { // если текущий токен является закрывабщей скобочкой
            while (!_stack.empty() && _stack.top() != "(") { // пока стек не пустой и на вершине НЕ открывающая скобочка
                string s = _stack.top(); // взять элемент с вершины стека
                _stack.pop(); // удалть элемент с вершины стека
                polish_tokens.push_back(s); // записать элемент в вектор polish_tokens
            }
            _stack.pop(); // удалить элемент с вершины стека
        } else {
            polish_tokens.push_back(tokens[i]); // иначе записать текущий токен в вектор polish_tokens
        }
    }
    while (!_stack.empty()) { // пока стек не пустой
        string s = _stack.top(); // взять элемент с вершины стека
        _stack.pop(); // удалть элемент с вершины стека
        polish_tokens.push_back(s); // записать элемент в вектор polish_tokens
    }
    return eval(); // вызвать функцию eval() и вернуть её результат
}

void calculation(char* buffer, int length) {
	/**
		функция, котороая принимает buffer и его длину
		Далее ищет в буфере промежуток [[[ ]]] и всё, что между этими скобками передаёт в функцию polish(), которая и вернёт ответ
	**/
    // строка в коротую будем посимвольно собирать выражение, которое потом будем вычислять
    string expression = "";
    for (int i = 0; i < length; i++) {
        if (buffer[i] == '[' && i + 2 < length && buffer[i + 1] == '[' && buffer[i + 2] == '[') { // если текущий символ [ и два следующий тоже [, то это есть начало выражения
            int j = i + 3;
            while (true) {
                if (buffer[j] == ']' && j + 2 < length && buffer[j + 1] == ']' && buffer[j + 2] == ']') { // если текущий символ ], и 2 следующий тоже ], то это есть конец выражения
                    j += 2;
                    i = j;
                    break;
                }
                expression += buffer[j]; // дописать в expression очереной символ
                j += 1;
            }
            double result = polish(expression);
            fprintf(out, " %.3lf ", result); // выводит ответ в поток вывода out. Выводится он как %.3lf - это значит вывести вещественное число с 3мя цифрами после точки
        } else {
            fprintf(out, "%c", buffer[i]); // инача этот символ buffer[i] является каким-то тексот вне скобок [[[ ]]] и мы его просто выводим
        }
    }
}

void run_solution() {
    char* buffer = (char*)malloc(BUFFER_SIZE * sizeof(char*));
    // сколько до этого было считано в массив
    int last = 0;
    // ВО сколько раз был увеличен наш изначальный массив
    int factor = 1;
    // функция fgets считывает с потока ввода данные до перевода строки
    // считываем с файла/консоли, кладем в место, начинающееся с buffer
    // + last(начиная с last-ой ячейке в массиве buffer)
    // количество -- BUFFER_SIZE * factor(изначальный размер буффера,
    // умноженный на увеличение массива) - last(сколько уже в массиве было
    // данных)
    while (fgets(buffer + last, (BUFFER_SIZE * factor) - last, in))
    {
        int length = strlen(buffer); // считаем длину строки
        // если последний символ не \n, значит строка слишком большая для
        // массива, давайте увеличим массив
        if (buffer[length - 1] != '\n')
        {
            char* buffer2 = (char*)malloc(BUFFER_SIZE * sizeof(char*) * factor * 2);  // записать элемент в вектор polish_tokens
            memmove(buffer2, buffer, BUFFER_SIZE * factor); // копируем то, что в нём было в новый массив
            last = BUFFER_SIZE * factor; // запоминаем сколько символов уже в нём есть
            factor *= 2; // обновляем коэффициент увеличения
            buffer = buffer2; // меняем массивы
            continue;
        }
        // мы прочитали очередную часть текста до перевода строки и попытаемся её вычислить
        calculation(buffer, length);
    }
}

int main(int argc, char * argv[]) {
	// при запуске программы можно передавать аргументы
	// они будут сохранятся в массив argv, в переменной argc будет их количество
	// нулевым элементом массива argv время является название запускаемого файла
    if (argc > 3) {
        printf("Слишком много аргументов");
        return 1;
    }
    if (argc > 1) {
        in = fopen(argv[1], "r"); // если передан файл из которого нужно читать, то откроем его в переменную in
        if (in == NULL) {
            printf("Ошибка чтения файла: %s\n", argv[1]);
            return 1;
        }
        if (argc == 3) { // аналогично с файлом, в который нужно вывести данные
            out = fopen(argv[2], "w"); //
        }
    }
    run_solution(); // вызвать функцию run_solution(), которая является точкой входа в основное решение
    return 0;
}
