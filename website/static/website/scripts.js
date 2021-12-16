$(function() {
    let $nav = $("nav"),
    $clone = $nav.before($nav.clone().addClass("clone"));

    $(window).on("scroll", function() {
        let fromTop = $(window).scrollTop();
        $("body").toggleClass("down", (fromTop > 100));
    });
});