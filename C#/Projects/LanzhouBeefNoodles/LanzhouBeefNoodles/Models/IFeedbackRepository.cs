using System;
using System.Collections.Generic;

namespace LanzhouBeefNoodles.Models
{
    public interface IFeedbackRepository
    {
        IEnumerable<Feedback> GetAllFeedbacks();
        void AddFeedback(Feedback feedback);
    }
}
