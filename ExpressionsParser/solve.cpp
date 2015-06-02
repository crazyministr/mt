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
#include <stdlib.h>
#include <string.h> // for string
#include <iostream>
#include <vector> // for vector
#include <stack> // for stack
#include <sstream> // for istringstream

using namespace std;

#define BUFFER_SIZE 256

FILE* in = stdin;
FILE* out = stdout;

vector<string> tokens, polish_tokens;

bool is_operator(string x) {
    return (x == "+" || x == "-" || x == "*" || x == "/");
}

void parse_expression(string expression) {
    tokens.clear();
    string number;
    for (int i = 0; i < (int) expression.size(); i++) {
        if (expression[i] == ' ')
            continue;

        stringstream ss;
        string current;
        ss << expression[i];
        ss >> current;
        if (expression[i] == '(' || expression[i] == ')' || is_operator(current)) {
            if ((int) number.size() > 0) {
                // if ((int) tokens.size() > 0 && tokens[(int) tokens.size() - 1] == "-") {
                //     if ((int) tokens.size() > 1) {
                //         string prev_token = tokens[(int) tokens.size() - 2];
                //         if (prev_token == "(") {
                //             tokens.pop_back();
                //             number = "-" + number;
                //         }
                //     } else {
                //         tokens.pop_back();
                //         number = "-" + number;
                //     }
                // }
                tokens.push_back(number);                
            }
            tokens.push_back(current);
            number = "";
        } else {
            int j = i;
            while ((expression[j] >= '0' && expression[j] <= '9') || expression[j] == '.') {
                number = number + expression[j];
                j++;
            }
            i = j - 1;
        }
    }
    if ((int) number.size() > 0) {
        tokens.push_back(number);
    }
}

bool priority_operation(string x, string y) {
    if (x == y)
        return 0;

    return ((x == "+" || x == "-") &&
            (y == "*" || y == "/")) ? -1 : 1;
}

double parse_double(string s) {
    istringstream i(s);
    double x;
    if (!(i >> x))
        return 0;
    return x;
}

string double_to_string(double x) {
    ostringstream strs;
    strs << x;
    string str = strs.str();
    return str;
}

double eval() {
    stack<string> _stack;
    for (int i = 0; i < (int) polish_tokens.size(); i++) {
        if (is_operator(polish_tokens[i])) {
            double y = parse_double(_stack.top());
            _stack.pop();
            double x = parse_double(_stack.top());
            _stack.pop();
            if (polish_tokens[i] == "+")
                _stack.push(double_to_string(x + y));
            else if (polish_tokens[i] == "-")
                _stack.push(double_to_string(x - y));
            else if (polish_tokens[i] == "*")
                _stack.push(double_to_string(x * y));
            else if (polish_tokens[i] == "/")
                _stack.push(double_to_string(x / y));
        } else {
            _stack.push(polish_tokens[i]);
        }
    }
    string s = _stack.top();
    _stack.pop();
    return parse_double(s);
}

double polish(string expression) {
    parse_expression(expression);
    polish_tokens.clear();
    stack<string> _stack;
    for (int i = 0; i < (int) tokens.size(); i++) {
        if (is_operator(tokens[i])) {
            while (!_stack.empty() && is_operator(_stack.top())) {
                if (priority_operation(tokens[i], _stack.top()) <= 0) {
                    string s = _stack.top();
                    _stack.pop();
                    polish_tokens.push_back(s);
                }
                else
                    break;
            }
            _stack.push(tokens[i]);
        } else if (tokens[i] == "(") {
            _stack.push(tokens[i]);
        } else if (tokens[i] == ")") {
            while (!_stack.empty() && _stack.top() != "(") {
                string s = _stack.top();
                _stack.pop();
                polish_tokens.push_back(s);
            }
            _stack.pop();
        } else {
            polish_tokens.push_back(tokens[i]);
        }
    }
    while (!_stack.empty()) {
        string s = _stack.top();
        _stack.pop();
        polish_tokens.push_back(s);
    }
    return eval();
}

void calculation(char* buffer, int length) {
    // строка в коротую будем посимвольно собирать выражение, которое потом будем вычислять
    string expression = "";
    for (int i = 0; i < length; i++) {
        if (buffer[i] == '[' && i + 2 < length && buffer[i + 1] == '[' && buffer[i + 2] == '[') {
            int j = i + 3;
            while (true) {
                if (buffer[j] == ']' && j + 2 < length && buffer[j + 1] == ']' && buffer[j + 2] == ']') {
                    j += 2;
                    i = j;
                    break;
                }
                expression += buffer[j];
                j += 1;
            }
            double result = polish(expression);
            fprintf(out, " %.3lf ", result);
        } else {
            fprintf(out, "%c", buffer[i]);
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
        // считаем длину строки
        int length = strlen(buffer);
        // если последний символ не \n, значит строка слишком большая для
        // массива, давайте увеличим массив
        if (buffer[length - 1] != '\n')
        {
            // создаем массив в два раза больше чем был
            char* buffer2 = (char*)malloc(BUFFER_SIZE * sizeof(char*) * factor * 2);
            // копируем то, что в нём было в новый массив
            memmove(buffer2, buffer, BUFFER_SIZE * factor);
            // запоминаем сколько символов уже в нём есть
            last = BUFFER_SIZE * factor;
            // обновляем коэффициент увеличения
            factor *= 2;
            // меняем массивы
            buffer = buffer2;
            // продолжаем считывать
            continue;
        }
        // мы прочитали очередную часть текста до перевода строки и попытаемся её вычислить
        calculation(buffer, length);
    }
}

int main(int argc, char * argv[]) {
    if (argc > 3) {
        printf("Слишком много аргументов");
        return 1;
    }
    if (argc > 1) {
        in = fopen(argv[1], "r");
        if (in == NULL) {
            printf("Ошибка чтения файла: %s\n", argv[1]);
            return 1;
        }
        if (argc == 3) {
            out = fopen(argv[2], "w");
        }
    }
    run_solution();
    return 0;
}
