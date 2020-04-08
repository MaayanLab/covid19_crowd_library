function switchTabs(from, to) {
    $("." + from).removeClass("active").removeClass("show");
    $("." + to).addClass("active").addClass("show");
    // location.hash change triggers scrolling to the anchor, so it's disabled
    // location.hash = 'nav-'+ to +'-table';
}

function navTabsSync(def) {
    if (location.hash !== '') {
        $('a[href="' + location.hash + '"]').tab('show');
    } else {
        $('a[href="' + def + '"]').tab('show');
    }

    $("a[data-toggle='tab']").on("shown.bs.tab", function (e) {
        var hash = $(e.target).attr("href");
        if (hash.substr(0, 1) === "#") {
            var position = $(window).scrollTop();
            location.replace("#" + hash.substr(1));
            $(window).scrollTop(position);
        }
    });

    $(".genes").on("click", function () {
        switchTabs('drugs', 'genes');
    });

    $(".drugs").on("click", function () {
        switchTabs('genes', 'drugs');
    });
}

function addMetaField(form) {
    const meta_input =
        '        <div class="input-group mb-3">\n' +
        '            <div class="input-group-prepend">\n' +
        '                <span class="input-group-text">Parameter</span>\n' +
        '            </div>\n' +
        '            <input type="text" class="form-control" aria-label="Matadata parameter name">\n' +
        '            <div class="input-group-prepend">\n' +
        '                <span class="input-group-text">Value</span>\n' +
        '            </div>\n' +
        '            <input type="text" class="form-control" aria-label="Matadata parameter value">\n' +
        '        </div>';
    $(form).prepend(meta_input);
}

function validateForm() {
    $('.needs-validation').on('submit', function(e) {

    });
}