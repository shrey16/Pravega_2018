"use strict";
//jQuery time
var current_fs, next_fs, previous_fs; //fieldsets
var left, opacity, scale; //fieldset properties which we will animate
var animating; //flag to prevent quick multi-click glitches
var legends;

const field_error_element = "h2";
const required_marker = "<span style=\"color:red; font-size:2.5em;\"> *</span>";

$(document).ready(function() {
    legends = $("#progressbar li");
    legends.css('width', (100 / legends.length) + '%');
    if (desktopMode) {
        $("#progressbar").css("left", "calc(50% - " + (legends.length / 2) + " * " + legends.width() + "px");
    }
    legends.removeClass("active");
    var index = 0;
    legends.eq(index).addClass('active');
    var found_errors = false;
    $("fieldset").each(function(current_index) {
        $(this).find("label").each(function() {
            if ($(this).next().prop("required")) {
                $(this).append(required_marker);
            }
        })
        if (!(found_errors) && $(this).find(".errors").length > 0) {
            console.log($(this));
            index = current_index;
            found_errors = true;
        }
    });
    for (let i = 0; i < index; ++i) {
        goForward($("fieldset").get(i), 0);
    }
    $(".delete-row").hide();
});


// Ugly hack,
// but jQuery does not support event bindings on dynamically added elements properly,
// so we resort to this workaround.
//
// It's not all bad as even though it runs a lot, it's short.
window.setInterval(function() {
    if ($(".participant-formset").length <= 1) {
        $(".delete-row").hide();
    } else {
        $(".delete-row").show();
    }
}, 20);

function goForward(elem, duration) {
    var current_fs = $(elem).parent();
    var next_fs = $(elem).parent().next();
    if ($(elem).is('fieldset')) {
        current_fs = $(elem);
        next_fs = $(elem).next();
    }
    animating = true;
    current_fs.find(".field-error").remove();
    //activate next step on progressbar using the index of next_fs
    legends.eq($("fieldset").index(next_fs)).addClass("active");
    //show the next fieldset
    next_fs.show();
    //hide the current fieldset with style
    current_fs.animate({
        opacity: 0
    }, {
        step: function(now, mx) {
            //as the opacity of current_fs reduces to 0 - stored in "now"
            //1. scale current_fs down to 80%
            scale = 1 - (1 - now) * 0.2;
            //2. bring next_fs from the right(50%)
            left = (now * 50) + "%";
            //3. increase opacity of next_fs to 1 as it moves in
            opacity = 1 - now;
            current_fs.css({
                'transform': 'scale(' + scale + ')',
                'position': 'absolute'
            });
            next_fs.css({
                'left': left,
                'opacity': opacity
            });
        },
        duration: duration,
        complete: function() {
            current_fs.hide();
            animating = false;
        }
        //this comes from the custom easing plugin
    });
}

function goBackward(elem, duration) {
    var current_fs = $(elem).parent();
    var previous_fs = $(elem).parent().prev();
    //de-activate current step on progressbar
    legends.eq($("fieldset").index(current_fs)).removeClass("active");
    //show the previous fieldset
    previous_fs.show();
    //hide the current fieldset with style
    current_fs.animate({
        opacity: 0
    }, {
        step: function(now, mx) {
            //as the opacity of current_fs reduces to 0 - stored in "now"
            //1. scale previous_fs from 80% to 100%
            scale = 0.8 + (1 - now) * 0.2;
            //2. take current_fs to the right(50%) - from 0%
            left = ((1 - now) * 50) + "%";
            //3. increase opacity of previous_fs to 1 as it moves in
            opacity = 1 - now;
            current_fs.css({
                'left': left
            });
            previous_fs.css({
                'transform': 'scale(' + scale + ')',
                'opacity': opacity
            });
        },
        duration: duration,
        complete: function() {
            current_fs.hide();
            animating = false;
        }
        //this comes from the custom easing plugin
    });
}

function trimColon(string) {
    return string.replace(':', '');
}

function getTextWithoutSpan(element) {
    return $(element).contents().filter(function() {
        return this.nodeType == 3;
    }).text();
}

$("#continue").click(function() {
    if (document.getElementById("understood").checked) {
        if (animating) {
            return false;
        }
        goForward(this, 300);
    }
})
$(".next").click(function() {
    if (animating) {
        return false;
    }
    var allowNext = true;
    current_fs = $(this).parent();
    current_fs.find("input").each(function(index) {
        const error_id = $(this).prop("id") + "-error";
        if ($(this).prop("required") && $(this).prop("value") === "") {
            if (current_fs.find("#" + error_id).length == 0) {
                current_fs.prepend("<" + field_error_element + " id=\"" + error_id + "\" class=\"field-error\">" + trimColon(getTextWithoutSpan($(this).prev())) + " is required</" + field_error_element + ">");
            }
            allowNext = false;
        } else {
            current_fs.find("#" + error_id).remove();
        }
    });
    if (allowNext) {
        goForward(this, 300);
    }
});

$(".previous").click(function() {
    if (animating) {
        return false;
    }
    animating = true;
    goBackward(this, 300);
});

function getFileName(path) {
    var filePath = path.replace(/\\/g, "/")
    return filePath.substr(filePath.lastIndexOf("/") + 1, filePath.length);
}

function getFormReport(fieldset) {
    var content = "";
    fieldset.find("label").each(function() {
        const input = $(this).next();
        const data = input.val();
        const marked = (input.prop('required') && (data == null || data.trim() == ""));
        const color = marked ? ' style=\"color: red;\"' : '';
        var text = "<tr><td class=\"field-label\"" + color + ">" + trimColon(getTextWithoutSpan($(this))) + ":  </td>";
        text += "<td" + color + ">  " + ((input.prop("type") === "file") ? getFileName(data) : data) + "</td></tr>";
        content += text;
    });
    return content;
}

$("#review-button").click(function() {
    const review_data = $("#review table");
    review_data.find("tr").remove();
    const legends = $("#progressbar li");
    var content = ""
    $(".real").each(function(index) {
        if (this.id !== "review") {
            const legend = legends.eq(index + 1 /* skip rules */ ).text();
            content += "<tr><td class=\"fieldset-legend\" colspan=\"2\">" + legend + "</td></tr>"
            if (this.id === "participants") {
                $(this).find(".participant-formset").each(function(index) {
                    content += "<tr><td class=\"fieldset-legend\" colspan=\"2\">Participant " + (index + 1) + "</td></tr>" + getFormReport($(this));
                })
            } else {
                content += getFormReport($(this));
            }
        }
    });
    review_data.append(content);
});
