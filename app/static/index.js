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

function* counter(index) {
  while (index >= 0) {
    yield index++;
  }
}

function addMetaField(setType) {
    let form = $(`#meta-${setType}-form`);
    let count;
    if (setType === 'drug') {
        count = window.drugSetMetaCounter.next().value;
    }
    else if (setType === 'gene') {
        count = window.geneSetMetaCounter.next().value;
    }
    const meta_input =
        `        <div class="input-group mt-3">\n` +
        `            <div class="input-group-prepend">\n` +
        `                <span class="input-group-text">Parameter</span>\n` +
        `            </div>\n` +
        `            <input type="text" class="form-control" aria-label="Matadata parameter name ${count}" name="name_${count}">\n` +
        `            <div class="input-group-prepend">\n` +
        `                <span class="input-group-text">Value</span>\n` +
        `            </div>\n` +
        `            <input type="text" class="form-control" aria-label="Matadata parameter value ${count}" name="val_${count}">\n` +
        `        </div>`;
    form.append(meta_input);
}