const desktopMode = !window.matchMedia("(max-width: 900px), (max-height: 500px)").matches;
const footerClearance = $("#footer").height();
var mobileMenuClearance = 60 + footerClearance;

function descEnterAnimation(element, previousElement) {
    if (!animationRunning) {
        TweenLite.fromTo(element, 0.35, {
            top: "10px",
            opacity: 0
        }, {
            top: 0,
            opacity: 1
        }).delay(0.3).eventCallback("onStart", function() {
            if (previousElement !== undefined) {
                $(previousElement).fadeOut(0);
            }
            $(element).fadeIn(0);
        });
    }
}

function descExitAnimation(element) {
    if (!animationRunning) {
        TweenLite.to($(element), 0.3, {
            opacity: 0
        });
    }
}

var mousePos = { x: 0, y: 0 };
$(document).mousemove(function(e) {
    mousePos.x = e.pageX;
    mousePos.y = e.pageY;
});


const navItems = $(".nav-item").not(".mobile");
const navDescs = $(".infobar-content");
var displayedInfoElement = navItems.eq(0);
const togImage = $("#tog-button-desktop").find(".li-img").find(".c-hamburger");
const openWidth = 300;
const totalExpandedWidth = $("#iconbar").width() + openWidth;

var infobarRemoved = true,
    infobarOpener;

function openMenuBar(finished) {
    $(".li-text").addClass("vis");
    if (!animationRunning && infobarRemoved) {
        TweenLite.to($("#infobar"), 0.25, {
            width: openWidth,
            onStart: function() {
                if (!desktopMode) {
                    $("#disabler").fadeIn(250);
                }
                togImage.addClass("is-active");
                $(".infobar-content").fadeOut(0);
                infobarRemoved = false;
            },
            onComplete: function() {
                if (finished !== undefined) {
                    finished();
                }
            }
        });
        descEnterAnimation(displayedInfoElement);
    }
}

function closeMenuBar(finished) {
    if (!(animationRunning || infobarRemoved)) {
        descExitAnimation(displayedInfoElement);
        TweenLite.to($("#infobar"), 0.25, {
            width: 0,
            delay: 0.3,
            onStart: function() {
                if (!desktopMode) {
                    $("#disabler").fadeOut(250);
                }
                togImage.removeClass("is-active");
                $(".infobar-content").fadeOut(0);
            },
            onComplete: function() {
                if (mousePos.x > 90) {
                    $(".li-text").removeClass("vis");
                }
                infobarRemoved = true;
                if (finished !== undefined) {
                    finished();
                }
            }
        });
    }
}

let animationRunning = false;

if (desktopMode) {
    // Desktop Menu Controller
    $("#iconbar").hover(function(e) {
        if (infobarRemoved) {
            $(".li-text ").toggleClass("vis");
        };
    });

    $("#tog-button-desktop, .nav-item.desktop").not(".nav-footer").click(function(e) {
        if (infobarRemoved) {
            infobarOpener = this.innerHTML;
            openMenuBar();
        } else if (infobarOpener === this.innerHTML || this.id === 'tog-button-desktop') {
            closeMenuBar();
        }
    });
    $("#main").click(function(event) {
        if (!infobarRemoved) {
            closeMenuBar();
        }
    });
    const sidebarItems = new Array(navItems.length),
        sidebarDescs = new Array(navDescs.length);
    for (let i = 0; i < navItems.length; ++i) {
        sidebarItems[i] = navItems.eq(i);
        sidebarDescs[i] = navDescs.eq(i);
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
    $(".expand-menu-img").hover(function() {
        const expandMenuTexts = $(this).parent().children(".expand-menu-text");
        const linkImages = $(this).parent().children("img");
        var rqdiv = expandMenuTexts.eq(linkImages.index(this));
        var rqindex = linkImages.index(this);
        expandMenuTexts.each(function(index) {
            const linkImage = linkImages.eq(expandMenuTexts.index(this));
            if (index !== rqindex) {
                $(this).removeClass("active");
                linkImage.removeClass("active");
            } else {
                $(this).addClass("active");
                linkImage.addClass("active");
            }
        });
    });
} else {
    // Scrolling Toggle
    function setScrolling(scroll) {
        if ($.fn !== undefined && $.fn.fullpage !== undefined) {
            $.fn.fullpage.setAllowScrolling(scroll);
            $.fn.fullpage.setKeyboardScrolling(scroll);
        }
        $("body").css("overflow", scroll ? "auto" : "hidden");
    }

    function enableScrolling() {
        setScrolling(true);
    }

    function disableScrolling() {
        setScrolling(false);
    }
    // Mobile Menu Controller
    const dropdowns = $(".dropdown");
    const iconbar = $("#iconbar");
    const container = iconbar.find("ul");

    const borderThickness = 0;

    function viewportHeight() {
        return Math.max(document.documentElement.clientHeight, window.innerHeight || 0);
    }

    function getNextNonDesktopNavItem(navItem) {
        return $(navItem).nextAll(".nav-item").not(".desktop").eq(0);
    }

    $(document).ready(function() {
        $(".nav-item").not(".mobile").not(":hidden").eq(0).css("padding-top", 15);
    });
    $("#tog-button-mobile .li-img").click(function(e) {
        $(this).find(".c-hamburger").toggleClass("is-active");
        if (infobarRemoved) {
            TweenLite.to(iconbar, 0.3, {
                height: viewportHeight() - mobileMenuClearance,
                onComplete: disableScrolling
            });
        } else {
            for (let i = 0; i < dropdowns.length; ++i) {
                const dropdownImage = $(dropdowns[i]).find("img");
                if (dropdownImage.hasClass("inverted")) {
                    dropdownImage.removeClass("inverted")
                    const navItem = $(dropdowns[i]).parent();
                    const nextNavItem = getNextNonDesktopNavItem(navItem);
                    const nextNavItemTop = parseInt(nextNavItem.css("margin-top"));
                    const extraInfo = navItem.find(".extra-info");
                    nextNavItem.css("margin-top", nextNavItemTop - extraInfo.height())
                    extraInfo.height(0);
                }
            }
            iconbar.scrollTop(0);
            TweenLite.to(iconbar, 0.3, {
                height: 0,
                onComplete: enableScrolling
            });
        }
        infobarRemoved = !infobarRemoved;
    });

    $(window).on("resize touchmove scroll", function(e) {
        if (!infobarRemoved) {
            iconbar.height(viewportHeight() - mobileMenuClearance);
        }
    });

    $(".dropdown").click(function(e) {
        let dropdownContainer = $(this);
        if (!animationRunning) {
            const dropdownImage = dropdownContainer.find("img");
            dropdownImage.toggleClass("inverted")
            const navItem = dropdownContainer.parent();
            const nextNavItem = getNextNonDesktopNavItem(navItem);
            const extraInfo = navItem.find(".extra-info");
            const nextNavItemTop = parseInt(nextNavItem.css("margin-top"));
            const totalHeight = container.height();
            const duration = 0.3;
            let itemHeight = 0;
            if (extraInfo.height() === 0) {
                extraInfo.height("auto");
                itemHeight = extraInfo.height();
                TweenLite.fromTo(extraInfo, duration, {
                    height: 0
                }, {
                    height: itemHeight
                });
                if (nextNavItem.length > 0) {
                    TweenLite.to(nextNavItem, duration, {
                        marginTop: nextNavItemTop + itemHeight
                    });
                }
            } else {
                itemHeight = extraInfo.height();
                TweenLite.to(extraInfo, duration, {
                    height: 0
                });
                if (nextNavItem.length > 0) {
                    TweenLite.to(nextNavItem, duration, {
                        marginTop: nextNavItemTop - itemHeight
                    });
                }
            }
        }
    });
}