#pragma checksum "/Users/chengyinliu/D/Projects/WebProjects/C#/Projects/LanzhouBeefNoodles/LanzhouBeefNoodles/Views/Home/Index.cshtml" "{ff1816ec-aa5e-4d10-87f7-6f4963833460}" "1f088b8e38539b3febb95f33fadd30b64e26b8e6"
// <auto-generated/>
#pragma warning disable 1591
[assembly: global::Microsoft.AspNetCore.Razor.Hosting.RazorCompiledItemAttribute(typeof(AspNetCore.Views_Home_Index), @"mvc.1.0.view", @"/Views/Home/Index.cshtml")]
namespace AspNetCore
{
    #line hidden
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Threading.Tasks;
    using Microsoft.AspNetCore.Mvc;
    using Microsoft.AspNetCore.Mvc.Rendering;
    using Microsoft.AspNetCore.Mvc.ViewFeatures;
    [global::Microsoft.AspNetCore.Razor.Hosting.RazorSourceChecksumAttribute(@"SHA1", @"1f088b8e38539b3febb95f33fadd30b64e26b8e6", @"/Views/Home/Index.cshtml")]
    public class Views_Home_Index : global::Microsoft.AspNetCore.Mvc.Razor.RazorPage<LanzhouBeefNoodles.ViewModels.HomeViewModel>
    {
        #pragma warning disable 1998
        public async override global::System.Threading.Tasks.Task ExecuteAsync()
        {
            WriteLiteral("\r\n");
            WriteLiteral("\r\n");
            WriteLiteral("\r\n");
#nullable restore
#line 9 "/Users/chengyinliu/D/Projects/WebProjects/C#/Projects/LanzhouBeefNoodles/LanzhouBeefNoodles/Views/Home/Index.cshtml"
  
    ViewData["Title"] = "Index";

#line default
#line hidden
#nullable disable
            WriteLiteral("\r\n\r\n\r\n<h2>Product List</h2>\r\n");
#nullable restore
#line 16 "/Users/chengyinliu/D/Projects/WebProjects/C#/Projects/LanzhouBeefNoodles/LanzhouBeefNoodles/Views/Home/Index.cshtml"
 foreach (var noodle in Model.Noodels)
{

#line default
#line hidden
#nullable disable
            WriteLiteral("    <div class=\"col-sm-4 col-lg-4 col-md-4\">\r\n        <div class=\"thumbnail\">\r\n            <img");
            BeginWriteAttribute("src", " src=\"", 447, "\"", 469, 1);
#nullable restore
#line 20 "/Users/chengyinliu/D/Projects/WebProjects/C#/Projects/LanzhouBeefNoodles/LanzhouBeefNoodles/Views/Home/Index.cshtml"
WriteAttributeValue("", 453, noodle.ImageUrl, 453, 16, false);

#line default
#line hidden
#nullable disable
            EndWriteAttribute();
            BeginWriteAttribute("alt", " alt=\"", 470, "\"", 476, 0);
            EndWriteAttribute();
            WriteLiteral(">\r\n            <div class=\"caption\">\r\n                <h3 class=\"pull-right\">￥");
#nullable restore
#line 22 "/Users/chengyinliu/D/Projects/WebProjects/C#/Projects/LanzhouBeefNoodles/LanzhouBeefNoodles/Views/Home/Index.cshtml"
                                   Write(noodle.Price);

#line default
#line hidden
#nullable disable
            WriteLiteral("</h3>\r\n                <h3>\r\n                    <a>");
#nullable restore
#line 24 "/Users/chengyinliu/D/Projects/WebProjects/C#/Projects/LanzhouBeefNoodles/LanzhouBeefNoodles/Views/Home/Index.cshtml"
                  Write(noodle.Name);

#line default
#line hidden
#nullable disable
            WriteLiteral("</a>\r\n                </h3>\r\n                <p>");
#nullable restore
#line 26 "/Users/chengyinliu/D/Projects/WebProjects/C#/Projects/LanzhouBeefNoodles/LanzhouBeefNoodles/Views/Home/Index.cshtml"
              Write(noodle.ShortDescription);

#line default
#line hidden
#nullable disable
            WriteLiteral("</p>\r\n            </div>\r\n        </div>\r\n    </div>\r\n");
#nullable restore
#line 30 "/Users/chengyinliu/D/Projects/WebProjects/C#/Projects/LanzhouBeefNoodles/LanzhouBeefNoodles/Views/Home/Index.cshtml"
}

#line default
#line hidden
#nullable disable
            WriteLiteral("\r\n<h2>Feedback</h2>\r\n<div class=\"list-group\">\r\n");
#nullable restore
#line 34 "/Users/chengyinliu/D/Projects/WebProjects/C#/Projects/LanzhouBeefNoodles/LanzhouBeefNoodles/Views/Home/Index.cshtml"
     foreach (var feedback in Model.Feedbacks)
    {

#line default
#line hidden
#nullable disable
            WriteLiteral("        <a class=\"list-group-item\">\r\n            <div class=\"d-flex w-100 justify-content-between\">\r\n                <h5 class=\"list-group-item-heading\">");
#nullable restore
#line 38 "/Users/chengyinliu/D/Projects/WebProjects/C#/Projects/LanzhouBeefNoodles/LanzhouBeefNoodles/Views/Home/Index.cshtml"
                                               Write(feedback.Name);

#line default
#line hidden
#nullable disable
            WriteLiteral("</h5>\r\n                <small class=\"pull-right\">");
#nullable restore
#line 39 "/Users/chengyinliu/D/Projects/WebProjects/C#/Projects/LanzhouBeefNoodles/LanzhouBeefNoodles/Views/Home/Index.cshtml"
                                     Write(feedback.CreateDateUTC);

#line default
#line hidden
#nullable disable
            WriteLiteral("</small>\r\n            </div>\r\n            <p class=\"list-group-item-text\">");
#nullable restore
#line 41 "/Users/chengyinliu/D/Projects/WebProjects/C#/Projects/LanzhouBeefNoodles/LanzhouBeefNoodles/Views/Home/Index.cshtml"
                                       Write(feedback.Message);

#line default
#line hidden
#nullable disable
            WriteLiteral("</p>\r\n        </a>\r\n");
#nullable restore
#line 43 "/Users/chengyinliu/D/Projects/WebProjects/C#/Projects/LanzhouBeefNoodles/LanzhouBeefNoodles/Views/Home/Index.cshtml"
    }

#line default
#line hidden
#nullable disable
            WriteLiteral("</div>\r\n");
        }
        #pragma warning restore 1998
        [global::Microsoft.AspNetCore.Mvc.Razor.Internal.RazorInjectAttribute]
        public global::Microsoft.AspNetCore.Mvc.ViewFeatures.IModelExpressionProvider ModelExpressionProvider { get; private set; }
        [global::Microsoft.AspNetCore.Mvc.Razor.Internal.RazorInjectAttribute]
        public global::Microsoft.AspNetCore.Mvc.IUrlHelper Url { get; private set; }
        [global::Microsoft.AspNetCore.Mvc.Razor.Internal.RazorInjectAttribute]
        public global::Microsoft.AspNetCore.Mvc.IViewComponentHelper Component { get; private set; }
        [global::Microsoft.AspNetCore.Mvc.Razor.Internal.RazorInjectAttribute]
        public global::Microsoft.AspNetCore.Mvc.Rendering.IJsonHelper Json { get; private set; }
        [global::Microsoft.AspNetCore.Mvc.Razor.Internal.RazorInjectAttribute]
        public global::Microsoft.AspNetCore.Mvc.Rendering.IHtmlHelper<LanzhouBeefNoodles.ViewModels.HomeViewModel> Html { get; private set; }
    }
}
#pragma warning restore 1591
