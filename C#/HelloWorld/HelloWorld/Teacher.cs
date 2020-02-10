using System;
namespace HelloWorld
{
    class Teacher: Member, IPayee
    {
        public string Subject;

        public Teacher()
        {
        }

        public void Pay()
        {
            Console.WriteLine("Pay Techer");
        }
    }
}
