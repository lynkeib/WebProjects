using System;
using Microsoft.AspNetCore.Mvc.ModelBinding;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Threading.Tasks;

namespace LanzhouBeefNoodles.Models
{
    public class Feedback
    {
        public Feedback()
        {
        }
        [BindNever]
        public int Id { get; set; }

        [Required(ErrorMessage = "Please leave your name")]
        [StringLength(20, ErrorMessage = "your name cannot exceed 20 characters")]
        public string Name { get; set; }

        [Required(ErrorMessage = "Please leave youe email")]
        [StringLength(50, ErrorMessage = "email cannot exceed 50 characters")]
        [DataType(DataType.EmailAddress, ErrorMessage = "Please use a valided email address")]
        [RegularExpression(@"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|""(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*"")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])",
            ErrorMessage = "Please use a valided email address")]
        public string Email { get; set; }

        [Required(ErrorMessage = "Please leave your feedback")]
        [StringLength(200, ErrorMessage = "Feedback cannot exceed 200 characters")]
        public string Message { get; set; }
        public DateTime CreateDateUTC { get; set; }
    }
}
