using System;
using System.Collections;

namespace HelloWorld
{
    class Program
    {
        static void Main(string[] args)
        {
            var student = new Student();
            student.Name = Util.Console.Ask("Name?");
            System.Console.Write(student.Name);
        }
    }

    class Student
    {
        public string Name { set; get; }
        public int Phone { set; get; }
    }
}
