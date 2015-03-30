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
        ArrayList<String> expressionTokens = new ArrayList<String>();
        String number = "";
        for (char ch: expression.toCharArray()) {
            if (ch == ' ') {
                continue;
            }
            if (ch == '(' || ch == ')' || isOperator(Character.toString(ch))) {
                if (!number.equals("")) {
                    expressionTokens.add(number);
                }
                expressionTokens.add(Character.toString(ch));
                number = "";
            } else if (ch >= '0' && ch <= '9') {
                number += ch;
            } else {
                throw new IllegalArgumentException("Invalid token: " + ch);
            }
        }
        if (!number.equals("")) {
            expressionTokens.add(number);
        }
        return expressionTokens;
    }

    public ArrayList<String> getTokens() {
        return tokens;
    }

    private static boolean isOperator(String token) {
        return token.equals("+") || token.equals("-") || token.equals("*") || token.equals("/");
    }

    private static int priorityOperators(String token1, String token2) {
        if (token1.equals(token2)) {
            return 0;
        }
        return ((token1.equals("+") || token1.equals("-")) &&
                (token2.equals("*") || token2.equals("/"))) ? -1 : 1;
    }

    private void reversePolishNotation(ArrayList<String> expressionTokens) {
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
        Stack<String> stack = new Stack<>();
        for (String token : tokens) {
            if (!isOperator(token)) {
                stack.push(token);
            } else {
                Double d2 = Double.valueOf(stack.pop());
                Double d1 = Double.valueOf(stack.pop());

                char t = token.charAt(0);
                Double res = t == '+' ? d1 + d2 : t == '-' ? d1 - d2 : t == '*' ? d1 * d2 : d1 / d2;
                stack.push(String.valueOf(res));
            }
        }
        return Double.valueOf(stack.pop());
    }
}
