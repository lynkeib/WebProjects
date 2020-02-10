using System;
using System.Collections;

namespace HelloWorld
{
    class Program
    {
        static void Main(string[] args)
        {
            var name = Util.Console.Ask("Name?");
            var grade = int.Parse(Util.Console.Ask("Grade?"));
            var birthday = Util.Console.Ask("Birthday?");
            var student = new Student(name, grade, birthday);
            //student.Name = Util.Console.Ask("Name?");
            student.print();
        }
    }

    class Member
    {
        public string Name;
        public int Grade;
        protected string Birthday { set; get; }

        public void print()
        {
            System.Console.WriteLine(Name);
            System.Console.WriteLine(Grade);
            System.Console.WriteLine(Birthday);
        }
    }

    class Student : Member
    {
        public Student(string name, int grade, string birthday)
        {
            System.Console.WriteLine("Creating Student");
            Name = name;
            Grade = grade;
            Birthday = birthday;
        }
        ~Student()
        {
            System.Console.Write("Deleting Student");
        }
        
    }

}
