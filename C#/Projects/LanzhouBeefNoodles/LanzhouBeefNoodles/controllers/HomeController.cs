using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;

// For more information on enabling Web API for empty projects, visit https://go.microsoft.com/fwlink/?LinkID=397860

namespace LanzhouBeefNoodles.controllers
{
    //[Route("[controller]/[action]")]
    public class HomeController : Controller
    {
        // Get: /<controller>/
        public string index()
        {
            return "Hello from home";
        }
        public string About()
        {
            return "Hello from about";
        }
    }
}
