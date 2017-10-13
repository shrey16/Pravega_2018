let width = $(window).innerWidth(),
    height = $(window).innerHeight();

const desktopMode = !window.matchMedia("(max-width: 900px), (max-height: 500px)").matches;

function execIfPresent(code) {
    return function() {
        if (code !== undefined) {
            code();
        }
    }
}

function descEnterAnimation(element, previousElement, onStart, onComplete) {
    if (noAnimationRunning()) {
        TweenLite.fromTo(element, 0.35, {
            top: "10px",
            opacity: 0
        }, {
            top: 0,
            opacity: 1
        }).delay(0.3).eventCallback("onStart", function() {
            if (previousElement !== undefined) {
                previousElement.css("display", "none");
            }
            element.css("display", "block");
            if (onStart !== undefined) {
                onStart();
            }
        }).eventCallback("onComplete", execIfPresent(onComplete));
    }
}

function descExitAnimation(element, onStart, onComplete) {
    if (noAnimationRunning()) {
        TweenLite.to(element, 0.3, {
            opacity: 0,
            onStart: execIfPresent(onStart),
            onComplete: execIfPresent(onComplete)
        });
    }
}

let currentMousePos = { x: 0, y: 0 };
$(document).mousemove(function(event) {
    currentMousePos.x = event.pageX;
    currentMousePos.y = event.pageY;
});


let displayedInfoElement = $("#infobar div:first-child ");
let togImage = $("#tog-button-desktop").find(".li-img").find("img");
const totalExpandedWidth = $("#iconbar").width() + 200;

let infobarRemoved = true,
    infobarVisible = false;

function openMenuBar(onComplete) {
    $(".li-text").addClass("vis");
    if (noAnimationRunning()) {
        TweenLite.to($("#infobar"), 0.25, {
            width: 200,
            onStart: function() {
                //animationRunning[0] = true;
                if (!desktopMode) {
                    $("#disabler").fadeIn(250);
                }
                togImage.attr("src", "img/close.png");
                //TweenLite.to($("#main"), 0.25, { css: { "transform": "translateX(200px)" } });
                //TweenLite.to($(".subject"), 0.25, { css: { "transform": "translateX(200px)" } });
                //TweenLite.to($("#fullpage"), 0.25, { css: { "width": "-=200px" } });
            },
            onComplete: function() {
                if (onComplete !== undefined) {
                    onComplete();
                }
                infobarRemoved = false;
                //animationRunning[0] = false;
            }
        });
        descEnterAnimation(displayedInfoElement);
    }
}

let previouslyExternal = false;

function closeMenuBar(onComplete, external) {
    if (noAnimationRunning()) {
        descExitAnimation(displayedInfoElement);
        TweenLite.to($("#infobar"), 0.25, {
            width: 0,
            delay: 0.3,
            onStart: function() {
                //animationRunning[1] = true;
                if (!desktopMode) {
                    $("#disabler").fadeOut(250);
                }
                togImage.attr("src", "img/hamburger.png");
                //TweenLite.to($("#main"), 0.25, { css: { "transform": "translateX(0)" } });
                //TweenLite.to($(".subject"), 0.25, { css: { "transform": "translateX(0)" } });
                //TweenLite.to($("#fullpage"), 0.25, { css: { "width": "+=200px" } });
            },
            onComplete: function() {
                if (currentMousePos.x > 90) {
                    $(".li-text").removeClass("vis");
                }
                if (onComplete !== undefined) {
                    onComplete();
                }
                infobarRemoved = true;
                //animationRunning[1] = false;
            }
        });
    }
}

let animationRunning = [];

function noAnimationRunning() {
    return !animationRunning.reduce((a, b) => a || b, false);
}

$(window).on('resize touchmove', function(event) {
    if ($(window).innerWidth() != width || $(window).innerHeight() != height) {
        width = $(window).innerWidth();
        height = $(window).innerHeight();
        //location.href = location.href;
    }
});

if (desktopMode) {
    // Desktop Menu Controller
    $("#iconbar ").hover(function(e) {
        if (infobarRemoved) {
            $(".li-text ").toggleClass("vis");
        };
    });

    $("#tog-button-desktop").click(function(e) {
        if (infobarRemoved) {
            openMenuBar();
        } else {
            closeMenuBar();
        }
    });
    $("#main").click(function(event) {
        if (!infobarRemoved) {
            closeMenuBar();
        }
    });
    let sidebarItems = new Array,
        sidebarDescs = new Array;

    const exitIndexOffset = 3,
        enterIndexOffset = 9 + exitIndexOffset;
    for (let j = 1; j <= 9; ++j) {
        const i = j - 1;
        sidebarItems[i] = $("#iconbar ul li:nth-child(" + j + ")");
        sidebarDescs[i] = $("#infobar div:nth-child(" + j + ")");
        sidebarItems[i].hover(function() {
            if (displayedInfoElement !== sidebarDescs[i]) {
                if (!infobarRemoved) {
                    descExitAnimation(displayedInfoElement);
                    descEnterAnimation(sidebarDescs[i], displayedInfoElement);
                }
                displayedInfoElement = sidebarDescs[i];
            }
        });
    };
} else {
    // Mobile Menu Controller
    animationRunning = [false, false, false, false, false, false];

    const container = $("#iconbar ul");
    window.onload = function() {
        $("#sidebar").height(0);
        $("#iconbar").height(0);
        container.height(0);
    }

    let expandedHeight = $("#tog-button-mobile").outerHeight() * $("#iconbar ul").children().length * 1.25;
    let duration = 0.3;

    const borderThickness = 0;
    let itemHeight = 250;

    $("#tog-button-mobile .li-img").click(function(e) {
        if (infobarVisible) {
            //expandedHeight = $("#iconbar").outerHeight();
            const dropdowns = $(".dropdown");
            duration = 0;
            for (let i = 0; i < dropdowns.length; ++i) {
                let dropdownImage = $(dropdowns[i]).find("img");
                if (dropdownImage.attr("src") === "img/upCaret.png") {
                    dropdownImage.attr("src", "img/downCaret.png");
                    let navItem = $(dropdowns[i]).parent();
                    let nextNavItem = navItem.next(".nav-item");
                    let extraInfo = navItem.find(".extra-info");
                    const nextNavItemTop = parseInt(nextNavItem.css("margin-top"));
                    extraInfo.height(0);
                    nextNavItem.css("margin-top", "0");
                }
            }

            duration = 0.3;
            $("#sidebar").height(0);
            TweenLite.to(container, duration, {
                height: 0,
                onStart: function() {
                    $("#tog-button-mobile").find(".li-img img").attr("src", "img/hamburger.png");
                    $("#iconbar").height(0);
                    if ($.fn !== undefined && $.fn.fullpage !== undefined) {
                        $.fn.fullpage.setAllowScrolling(true);
                        $.fn.fullpage.setKeyboardScrolling(true);
                    }
                    //$("body").css("overflow-y", "auto");
                    $("#disabler").fadeOut(100);
                }

            });

        } else {
            $("#sidebar").height("auto");
            TweenLite.to(container, duration, {
                height: expandedHeight,
                onStart: function() {
                    $("#tog-button-mobile").find(".li-img img").attr("src", "img/close.png");
                    $("#iconbar").height(screen.height);
                    if ($.fn !== undefined && $.fn.fullpage !== undefined) {
                        $.fn.fullpage.setAllowScrolling(false);
                        $.fn.fullpage.setKeyboardScrolling(false);
                    }
                    //$("body").css("overflow-y", "hidden");
                    $("#disabler").fadeIn(100);
                }
            });
        }
        infobarVisible = !infobarVisible;
    });


    $(".dropdown").click(function(e) {
        let dropdownContainer = $(this);
        if (noAnimationRunning()) {
            let dropdownImage = $(dropdownContainer).find("img");
            dropdownImage.attr("src", dropdownImage.attr("src") === "img/downCaret.png" ? "img/upCaret.png" : "img/downCaret.png");
            let navItem = $(dropdownContainer).parent();
            let nextNavItem = navItem.next(".nav-item");
            let extraInfo = navItem.find(".extra-info");
            const nextNavItemTop = parseInt(nextNavItem.css("margin-top"));
            const totalHeight = container.height();
            if (extraInfo.height() === 0) {
                extraInfo.height("auto");
                itemHeight = extraInfo.height();
                extraInfo.height(0);
                TweenLite.to(extraInfo, duration, {
                    height: itemHeight,
                    onStart: function() {
                        animationRunning[0] = true;
                    },
                    onComplete: function() {
                        animationRunning[0] = false;
                    }
                });
                if (nextNavItem.length > 0) {
                    TweenLite.to(nextNavItem, duration, {
                        marginTop: (nextNavItemTop + itemHeight),
                        onStart: function() {
                            animationRunning[1] = true;
                        },
                        onComplete: function() {
                            animationRunning[1] = false;
                        }
                    });
                }
                TweenLite.to(container, duration, {
                    height: (totalHeight + itemHeight + borderThickness),
                    onStart: function() {
                        animationRunning[2] = true;
                    },
                    onComplete: function() {
                        animationRunning[2] = false;
                    }
                });
            } else {
                itemHeight = extraInfo.height();
                TweenLite.to(extraInfo, duration, {
                    height: 0,
                    onStart: function() {
                        animationRunning[3] = true;
                    },
                    onComplete: function() {
                        animationRunning[3] = false;
                    }
                });
                if (nextNavItem.length > 0) {
                    TweenLite.to(nextNavItem, duration, {
                        marginTop: (nextNavItemTop - itemHeight),
                        onStart: function() {
                            animationRunning[4] = true;
                        },
                        onComplete: function() {
                            animationRunning[4] = false;
                        }
                    });
                }
                TweenLite.to(container, duration, {
                    height: (totalHeight - itemHeight),
                    onStart: function() {
                        animationRunning[5] = true;
                    },
                    onComplete: function() {
                        container.height(container.height() - borderThickness);
                        animationRunning[5] = false;
                    }
                });
            }
        }
    });
}
$("#disabler").height($("body").height());
