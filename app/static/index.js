function navTabsSync() {
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