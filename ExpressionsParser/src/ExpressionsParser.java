/*************
 https://en.wikipedia.org/wiki/Shunting-yard_algorithm
 Kobylenko Darya, gr. 3743
 Malashenkov Anton, gr. 3743
*************/

import java.util.ArrayList;
import java.util.Stack;

public class ExpressionsParser {
    private ArrayList<String> tokens = new ArrayList<>();

    public ExpressionsParser(String expression) {
        ArrayList<String> expressionTokens = prepareParsing(expression);
        reversePolishNotation(expressionTokens);
    }

    private ArrayList<String> prepareParsing(String expression) {
        /***
         * Analysis of expression into tokens
         *
         * @param expression The input expression
         * @return array with tokens
         */
        ArrayList<String> expressionTokens = new ArrayList<>();
        String number = "";
        for (char ch: expression.toCharArray()) {
            if (ch == ' ') {
                continue;
            }
            if (ch == '(' || ch == ')' || isOperator(Character.toString(ch))) {
                if (!number.equals("")) {
                    if (expressionTokens.size() > 0 && expressionTokens.get(expressionTokens.size() - 1).equals("-")) {
                        if (expressionTokens.size() > 1) {
                            String prevToken = expressionTokens.get(expressionTokens.size() - 2);
                            if (prevToken.equals("(")) {
                                expressionTokens.remove(expressionTokens.size() - 1);
                                number = "-" + number;
                            }
                        } else {
                            expressionTokens.remove(expressionTokens.size() - 1);
                            number = "-" + number;
                        }
                    }
                    expressionTokens.add(number);
                }
                expressionTokens.add(Character.toString(ch));
                number = "";
            } else if (ch >= '0' && ch <= '9') {
                number += ch;
            } else {
                throw new IllegalArgumentException("Unknown token: " + ch);
            }
        }
        if (!number.equals("")) {
            expressionTokens.add(number);
        }
        return expressionTokens;
    }

    public ArrayList<String> getTokens() {
        /***
         * @return array of tokens
         */
        return tokens;
    }

    private static boolean isOperator(String token) {
        /***
         * @param token any token
         * @return true if then <item>token</item> is operator
         */
        return token.equals("+") || token.equals("-") || token.equals("*") || token.equals("/");
    }

    private static int priorityOperators(String token1, String token2) {
        /***
         * Checking for priotiry operators
         *
         * @params token1 token2 any tokens
         * @return <int>0</int> if operators is equals else
         *         <int>-1</int> if <item>token1</item> has low priority else <int>1</int>
         */
        if (token1.equals(token2)) {
            return 0;
        }
        return ((token1.equals("+") || token1.equals("-")) &&
                (token2.equals("*") || token2.equals("/"))) ? -1 : 1;
    }

    private void reversePolishNotation(ArrayList<String> expressionTokens) {
        /***
         * Properly algorithm
         * Algorithm name is <algoname>Reverse Polish Notation</algoname> or
         * <algoname>Shunting-yard algorithm</algoname>
         *
         * Analysis input tokens and makes a sequence of tokens according to the algorithm
         *
         * Saving occurs in the <class_field>this.token</class_field>
         */
        Stack<String> stack = new Stack<>();
        for (String token : expressionTokens) {
            if (isOperator(token))
            {
                while (!stack.empty() && isOperator(stack.peek())) {
                    if (priorityOperators(token, stack.peek()) <= 0) {
                        tokens.add(stack.pop());
                    } else {
                        break;
                    }
                }
                stack.push(token);
            } else if (token.equals("(")) {
                stack.push(token);
            } else if (token.equals(")")) {
                while (!stack.empty() && !stack.peek().equals("(")) {
                    tokens.add(stack.pop());
                }
                stack.pop();
            } else {
                tokens.add(token);
            }
        }
        while (!stack.empty()) {
            tokens.add(stack.pop());
        }
    }

    public double eval() {
        /***
         * Calculating result based on the <class_field>this.token</class_field>
         *
         * @return result of calculation
         */
        Stack<String> stack = new Stack<>();
        for (String token : tokens) {
            if (!isOperator(token)) {
                stack.push(token);
            } else {
                char t = token.charAt(0);
                Double y = Double.valueOf(stack.pop());
                if (stack.empty()) {
                    if (t == '-') {
                        y = -y;
                        stack.push(y.toString());
                    } else {
                        throw new IllegalArgumentException("Incorrect token: " + t);
                    }
                } else {
                    Double x = Double.valueOf(stack.pop());
                    Double res = t == '+' ? x + y : t == '-' ? x - y : t == '*' ? x * y : x / y;
                    stack.push(String.valueOf(res));
                }
            }
        }
        return Double.valueOf(stack.pop());
    }
}
