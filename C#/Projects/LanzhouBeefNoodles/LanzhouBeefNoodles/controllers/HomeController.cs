using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using LanzhouBeefNoodles.Models;
using Microsoft.AspNetCore.Mvc;
using LanzhouBeefNoodles.ViewModels;

// For more information on enabling Web API for empty projects, visit https://go.microsoft.com/fwlink/?LinkID=397860

namespace LanzhouBeefNoodles.controllers
{
    //[Route("[controller]/[action]")]
    public class HomeController : Controller
    {
        private INoodleRepository _noodleRepository;
        private IFeedbackRepository _feedbackRepository;

        public HomeController(INoodleRepository noodleRepository, IFeedbackRepository feedbackRepository)
        {
            _noodleRepository = noodleRepository;
            _feedbackRepository = feedbackRepository;

        }
        // Get: /<controller>/
        public IActionResult Index()
        {
            //var noodles = _noodleRepository.GetAllNoodles();
            var viewModel = new HomeViewModel()
            {
                Feedbacks = _feedbackRepository.GetAllFeedbacks().ToList(),
                Noodels = _noodleRepository.GetAllNoodles().ToList()
            };
            return View(viewModel);
        }
        public string About()
        {
            return "Hello from about";
        }

        public IActionResult Detail(int id)
        {
            return View(_noodleRepository.GetNoodleById(id));
        }
    }
}
