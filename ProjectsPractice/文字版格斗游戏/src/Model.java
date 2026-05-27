import java.util.Random;
public class  Model{
    public static void main(String[] args){

    }
}
interface Person{

}
abstract class Role implements Person {
    protected String name;
    protected int hp=100;
    protected int atk=20;
    abstract int attack(Role aHero, int floatNum);
}
class CreateHero{
    static public Hero create(String name){
        if(name.equals("qiaofeng")||name.equals("jiuzhimo")){
            return new Hero(name);
        }
        else return null;

    }
    static public Hero create(String name,int atk){
        if(name.equals("qiaofeng")||name.equals("jiuzhimo")){
            return new Hero(name,atk);
        }
        else return null;
    }


    static class Hero extends Role{
        private Hero(String name,int ...options){
            if (options.length > 0) {
                this.atk = options[0];
            }
            this.name=name;
        }
        @Override
        public int attack (Role aHero,int floatNum){
            aHero.hp-=atk+floatNum;
            return aHero.hp;
        }

    }
}

class Attack{
    static void chose(String role1,String role2){
        var h1=CreateHero.create(role1);
        var h2=CreateHero.create(role2);
        if(h1==null){System.out.println("您输入的第一个角色名字定义了吗");return;}
        if(h2==null){System.out.println("您输入的第二个角色名字定义了吗");return;}
        battle(h1,h2);
    }
    static void chose(String role1,int atk1,String role2,int atk2){
        var h1=CreateHero.create(role1,atk1);
        var h2=CreateHero.create(role2,atk2);
        if(h1==null){System.out.println("您输入的第一个角色名字定义了吗");return;}
        if(h2==null){System.out.println("您输入的第二个角色名字定义了吗");return;}
        battle(h1,h2);
    }
    static void battle(CreateHero.Hero h1,CreateHero.Hero h2){
        var rdm=new Random();
        while(true){
            int rdmNum1=rdm.nextInt(51)-25;
            int rdmNum2=rdm.nextInt(51)-25;
            int previousHp1=h1.hp;
            int previousHp2=h2.hp;
            h2.hp=h1.attack(h2,rdmNum1);
            if(h2.hp<=0){
                System.out.printf("%s攻击了%s,这导致%s血量清零落败。\n",h1.name,h2.name,h2.name);
                return;}
            System.out.printf("%s攻击了%s,造成%d伤害,%s还剩%d\n",h1.name,h2.name,previousHp2-h2.hp,h2.name,h2.hp);
            h1.hp=h2.attack(h1,rdmNum2);
            if(h1.hp<=0){
                System.out.printf("%s攻击了%s,这导致%s血量清零落败。\n",h2.name,h1.name,h1.name);
                return;}
            System.out.printf("%s攻击了%s,造成%d伤害,%s还剩%d\n",h2.name,h1.name,previousHp1-h1.hp,h1.name,h1.hp);
        }

    }
}


