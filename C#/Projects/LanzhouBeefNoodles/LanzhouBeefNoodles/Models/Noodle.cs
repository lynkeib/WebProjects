﻿using System;
namespace LanzhouBeefNoodles.Models
{
    public class Noodle
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public string ShortDescription { get; set; }
        public string LongDescription { get; set; }
        public float Price { get; set; }
        public string ImageUrl { get; set; }
    }
}
