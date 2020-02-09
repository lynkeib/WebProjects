using System;
using System.Collections;

namespace HelloWorld
{
    class Program
    {
        static void Main(string[] args)
        {
            ArrayList al = new ArrayList();
            al.Add(1);
            al.Add("ss");
            foreach (var i in al)
            {
                Console.WriteLine(i);
            }
            
        }
    }
}
