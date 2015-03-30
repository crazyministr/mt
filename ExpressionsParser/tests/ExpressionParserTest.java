import junit.framework.TestCase;

public class ExpressionParserTest extends TestCase {
    public void test1() {
        ExpressionsParser expressionsParser = new ExpressionsParser("2+2");
        assertEquals(4.0, (double) expressionsParser.eval(), 1e-13);
    }

    public void test2() {
        ExpressionsParser expressionsParser = new ExpressionsParser("5+((1+2)*4)-3");
        assertEquals(14.0, (double) expressionsParser.eval(), 1e-13);
    }

    public void test3() {
        ExpressionsParser expressionsParser = new ExpressionsParser("3/2");
        assertEquals(3.0/2, (double) expressionsParser.eval(), 1e-13);
    }
}
