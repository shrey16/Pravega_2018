'use strict';

$(document).ready(function() {
    $('html, body').scrollTop(0);

    const desktopMode = !window.matchMedia("(max-width: 900px), (max-height: 500px)").matches;

    $(window).on('load', function() {
        setTimeout(function() {
            $('html, body').scrollTop(0);
        }, 0);
    });

    var keys = [37, 38, 39, 40];

    function preventDefault(e) {
        e = e || window.event;
        if (e.preventDefault) {
            e.preventDefault();
        }
        e.returnValue = false;
    }

    function keydown(e) {
        for (let i = keys.length; i--;) {
            if (e.keyCode === keys[i]) {
                preventDefault(e);
                return;
            }
        }
    }

    function wheel(e) {
        preventDefault(e);
    }

    function disable_scroll() {
        if (window.addEventListener) {
            window.addEventListener('DOMMouseScroll', wheel, false);
        }
        window.onmousewheel = document.onmousewheel = wheel;
        document.onkeydown = keydown;
    }

    function enable_scroll() {
        if (window.removeEventListener) {
            window.removeEventListener('DOMMouseScroll', wheel, false);
        }
        window.onmousewheel = document.onmousewheel = document.onkeydown = null;
    }

    mobileMenuClearance = 60;

    var pra = document.getElementById("pra"),
        v = document.getElementById("v-logo"),
        ega = document.getElementById("ega"),
        year = document.getElementById("year"),
        title = document.getElementById("title"),
        sidebar = document.getElementById("sidebar"),
        footer = document.getElementById("footer"),
        floatingFooter = document.getElementById("floating-footer"),
        black_trans = document.getElementById("black-trans");

    disable_scroll();

    var start = new TimelineLite();

    start.from(v, 1.2, { opacity: 0 }).from(pra, 0.4, { opacity: 0 }, "pravega").from(ega, 0.4, { opacity: 0 }, "pravega")
        .to(year, 0.4, {
            opacity: 1,
            onComplete: function() {
                enable_scroll();
                $("#scroll_me_arrow").fadeIn(100);
            }
        }, "top");

    var scroll_up = new TimelineLite();

    if (desktopMode) {
        scroll_up.to($("#scroll_me_arrow"), 0.1, { opacity: "0" }, "scrollup")
            .to($("#home"), 0.5, { opacity: 0 })
            .from(sidebar, 0.5, { left: "-100px" }, "scrollup")
            .to(floatingFooter, 0.5, { css: { "transform": "translateX(0) scale(0.6)" } }, "scrollup")
            .to(black_trans, 0.5, { opacity: 0 }, "scrollup");
    } else {
        scroll_up.to($("#home"), 0.5, { opacity: "0" }, "scrollup")
            .to($("#scroll_me_arrow"), 0.1, { opacity: "0" }, "scrollup")
            .to(black_trans, 0.5, {
                opacity: "0",
                onComplete: function() {
                    $("#black_trans").css("visibility", "hidden");
                }
            }, "scrollup")
            .to(footer, 0.5, { bottom: "0" }, "scrollup")
            .to($(".notification"), 0.5, { opacity: 1 }, "scrollup");
    }

    scroll_up.pause();
    var originalYOffset = 0,
        currYOffset;

    $(window).scroll(function(e) {
        currYOffset = window.pageYOffset;
        if (infobarRemoved) {
            if (currYOffset > originalYOffset) {
                scroll_up.play();
                mobileMenuClearance = 60 + footerClearance;
            } else {
                if (!window.matchMedia("(max-width: 900px), (max-height: 500px)").matches) {
                    closeMenuBar(function() {
                        $(".li-text").removeClass("vis");
                    });
                    scroll_up.reverse();
                } else {
                    scroll_up.reverse();
                }
                mobileMenuClearance = 60;
            }
            enable_scroll();
        }
    });

    $("#scroll_me_arrow").on("click", function(e) {

        e.preventDefault();

        $("body, html").animate({
            scrollTop: window.innerHeight / 2
        }, 200);
    });
});