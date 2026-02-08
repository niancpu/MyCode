package P2469ConverTemperature;
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.Arrays;
public class Main {
    public static void main(String[] args){
        var s=new Solution();
        double c=36.5;
        System.out.println(Arrays.toString(s.convertTemperature(c)));

    } }
class Solution {
    public double[] convertTemperature(double c) {
        var tmptr=new double[2];
        tmptr[0]=BigDecimal.valueOf(c+273.15)
                .setScale(5,RoundingMode.HALF_UP)
                .doubleValue();
        tmptr[1]=BigDecimal.valueOf(c*1.80+32.00)
                .setScale(5,RoundingMode.HALF_UP)
                .doubleValue();


        return tmptr;
    }
}
