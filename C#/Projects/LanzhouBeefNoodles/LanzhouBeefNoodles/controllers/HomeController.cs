using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using LanzhouBeefNoodles.Models;
using Microsoft.AspNetCore.Mvc;

// For more information on enabling Web API for empty projects, visit https://go.microsoft.com/fwlink/?LinkID=397860

namespace LanzhouBeefNoodles.controllers
{
    //[Route("[controller]/[action]")]
    public class HomeController : Controller
    {
        private INoodleRepository _noodleRepository;
        public HomeController(INoodleRepository noodleRepository)
        {
            _noodleRepository = noodleRepository;

        }
        // Get: /<controller>/
        public IActionResult Index()
        {
            var noodles = _noodleRepository.GetAllNoodles();
            return View(noodles);
        }
        public string About()
        {
            return "Hello from about";
        }
    }
}
