// $(document).ready(function () {
//     $("#sidebarCollapse").on("click", function () {
//         $("#sidebar").toggleClass("active");
//         $("#content").toggleClass("active");
//     });
// });

$(document).ready(function () {
    $("#sidebarCollapse").on("click", function () {
        $("#sidebar, #content").toggleClass("active");
    });

    // 🟢 کنترل باز و بسته شدن زیرمنو
    $(".dropdown-toggle").on("click", function () {
        $(this).next(".collapse").slideToggle();
        $(this).toggleClass("active"); // برای تغییر ظاهر دکمه هنگام باز بودن
    });
});
