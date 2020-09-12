package thread;

// 多线程创建， 方式一： 继承于Thread类
// 1、 创建一个继承与Thread类的子类
// 2、 重写Thread类的run方法 -> 将此线程执行的操作声明在run()中
// 3、 创建Thread类的子类的对象
// 4、 通过此对象调用start()


// 1、 创建一个继承与Thread类的子类
class MyClass extends Thread {
    public MyClass() {
    }
    // 2、 重写Thread类的run方法
    @Override
    public void run(){
        for(int i = 0; i < 100; i++){
            if(i % 2 == 0){
                System.out.println(Thread.currentThread().getName() + ":" + i);
            }
        }
    }
}

public class ThreadTest {
    public static void main(String[] args) {
        //3、 创建Thread类的子类的对象
        MyClass myClass = new MyClass();
        MyClass myClass2 = new MyClass();
        // 4、 通过此对象调用start()
        myClass.start();
        // 不可重复调用start
        myClass2.start();
        for(int i = 0; i < 100; i++){
            if(i % 2 != 0){
                System.out.println(Thread.currentThread().getName() + "*************");
            }
        }
    }
}
