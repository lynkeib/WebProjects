using System;
using Microsoft.AspNetCore.Mvc;


namespace LanzhouBeefNoodles.controllers
{
    public class Test: Controller
    {
        public ActionResult index()
        {
            return Content("Hello from test index");
        }

        public String About()
        {
            return "Hello from test about";
        }

        public ActionResult Contact()
        {
            return View();
        }
    }
}
