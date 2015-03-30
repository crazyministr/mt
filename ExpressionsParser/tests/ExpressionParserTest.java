import junit.framework.TestCase;

import java.util.ArrayList;

public class ExpressionParserTest extends TestCase {
    private void printTokens(String exp, ArrayList<String> tokens) {
        System.out.print("tokens for " + exp + ": ");
        for (String token: tokens) {
            System.out.print(token + " ");
        }
        System.out.println("");
    }

    public void test1() {
        String expression = "2+2";
        ExpressionsParser expressionsParser = new ExpressionsParser(expression);
        printTokens(expression, expressionsParser.getTokens());
        assertEquals(4.0, expressionsParser.eval(), 1e-13);
    }

    public void test2() {
        String expression = "1+((2+3)*4)-5";
        ExpressionsParser expressionsParser = new ExpressionsParser(expression);
        printTokens(expression, expressionsParser.getTokens());
        assertEquals(16.0, expressionsParser.eval(), 1e-13);
    }

    public void test3() {
        String expression = "-3/2";
        ExpressionsParser expressionsParser = new ExpressionsParser(expression);
        printTokens(expression, expressionsParser.getTokens());
        assertEquals(-3.0/2, expressionsParser.eval(), 1e-13);
    }

    public void test4() {
        String expression = "-(-(-2+3))";
        ExpressionsParser expressionsParser = new ExpressionsParser(expression);
        printTokens(expression, expressionsParser.getTokens());
        assertEquals(1, expressionsParser.eval(), 1e-13);
    }

    public void test5() {
        String expression = "13+21/7-2*(-3)-1";
        ExpressionsParser expressionsParser = new ExpressionsParser(expression);
        printTokens(expression, expressionsParser.getTokens());
        assertEquals(21, expressionsParser.eval(), 1e-13);
    }
}
