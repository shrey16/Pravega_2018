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
let togImage = $("#tog-button-desktop").find(".li-img").find(".c-hamburger");
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
                togImage.addClass("is-active");
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
                togImage.removeClass("is-active");
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

    const borderThickness = 0;

    $("#tog-button-mobile .li-img").click(function(e) {
        $(this).find(".c-hamburger").toggleClass("is-active");
        $("man").toggleClass("noscroll");
        if (infobarVisible) {
            const dropdowns = $(".dropdown");
            for (let i = 0; i < dropdowns.length; ++i) {
                const dropdownImage = $(dropdowns[i]).find("img");
                if (dropdownImage.hasClass("inverted")) {
                    dropdownImage.removeClass("inverted")
                    const navItem = $(dropdowns[i]).parent();
                    const nextNavItem = navItem.next(".nav-item");
                    const extraInfo = navItem.find(".extra-info");
                    const nextNavItemTop = parseInt(nextNavItem.css("margin-top"));
                    extraInfo.height(0);
                    nextNavItem.css("margin-top", "0");
                }
            }
            TweenLite.to($("#iconbar"), 0.3, {
                height: 0,
                onStart: function() {
                    if ($.fn !== undefined && $.fn.fullpage !== undefined) {
                        $.fn.fullpage.setAllowScrolling(true);
                        $.fn.fullpage.setKeyboardScrolling(true);
                    }
                }

            });
        } else {
            TweenLite.to($("#iconbar"), 0.3, {
                height: screen.height,
                onStart: function() {
                    if ($.fn !== undefined && $.fn.fullpage !== undefined) {
                        $.fn.fullpage.setAllowScrolling(false);
                        $.fn.fullpage.setKeyboardScrolling(false);
                    }
                }
            });
        }
        infobarVisible = !infobarVisible;
    });


    $(".dropdown").click(function(e) {
        let dropdownContainer = $(this);
        if (noAnimationRunning()) {
            const dropdownImage = dropdownContainer.find("img");
            if (dropdownImage.hasClass("inverted")) {
                dropdownImage.removeClass("inverted");
            } else {
                dropdownImage.addClass("inverted");
            }
            const navItem = dropdownContainer.parent();
            const nextNavItem = navItem.next(".nav-item");
            const extraInfo = navItem.find(".extra-info");
            const nextNavItemTop = parseInt(nextNavItem.css("margin-top"));
            const totalHeight = container.height();
            const duration = 0.3;
            let itemHeight = 0;
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
