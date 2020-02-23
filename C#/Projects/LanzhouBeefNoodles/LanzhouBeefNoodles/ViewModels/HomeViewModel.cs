using System;
using LanzhouBeefNoodles.Models;
using System.Collections.Generic;

namespace LanzhouBeefNoodles.ViewModels
{
    public class HomeViewModel
    {
        public HomeViewModel()
        {
        }
        public IList<Noodle> Noodels { get; set; }
        public IList<Feedback> Feedbacks { get; set; }
    }
}
