function switchTabs(from, to) {
    $("."+from).removeClass("active").removeClass("show");
    $("."+to).addClass("active").addClass("show");
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
        console.log('genes click');
        $(".drugs").removeClass("active").removeClass("show");
        $(".genes").addClass("active").addClass("show");
    });

    $(".drugs").on("click", function () {
        console.log('drugs click');
        $(".genes").removeClass("active").removeClass("show");
        $(".drugs").addClass("active").addClass("show");
    });
}