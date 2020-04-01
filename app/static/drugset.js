// Even though this file is nearly identical to geneset.js, I deliberately keep them separated,
// as I expect them to diverge further on.

function ds_DTblify(json, reviewed) {
    let dataArray = [];
    for (let i = 0; i < json.length; i++) {
        let drugLinks = [];
        $.each(json[i]['drugs'].sort(), function (index, drug) {
            drugLinks.push('<a class="drug-link" href="#" target="_blank">' + drug + '</a>');
        });
        const showContacts = json[i]['showContacts'];
        const contacts = showContacts ? `<p><b>Author:</b> ${json[i]['authorName']}<\p><p><b>Affiliation:</b> ${json[i]['authorAffiliation']}<\p><p><b>E-mail:</b> ${json[i]['authorEmail']}<\p>` :
            reviewed ? '<i class="far fa-eye-slash"></i> Author preferred not to share contact details' : `<p style="color: red"><i class="far fa-eye-slash"></i> As author preferred not to share contact details, following will not be shown:</p><p style="color: red"><b>Author:</b> ${json[i]['authorName']}<\p><p style="color: red"><b>Affiliation:</b> ${json[i]['authorAffiliation']}<\p><p style="color: red"><b>E-mail:</b> ${json[i]['authorEmail']}<\p>`;
        const source = json[i]['source'] === null ? '' : `<p><b>Source:</b> ${json[i]['source']}</p>`;
        const date = `<p><b>Date added:</b> ${json[i]['date'].split(' ')[0]}</p>`;
        const desc = `<p>${json[i]['descrFull']}<\p>${source}${date}${contacts}`;

        // Data Array
        dataArray[i] = [
            $('<div>', {
                'class': 'enrichment-popover-button',
                'data-toggle': 'popover',
                'data-placement': 'bottom',
                'data-trigger': 'focus',
                'data-html': 'true',
                'data-template': '<div class="popover enrichment-popover" role="tooltip"><div class="arrow"></div><h3 class="popover-header"></h3><div class="popover-body"></div></div>',
                'data-content': desc,
                'title': json[i]['descrShort']
            })
                .append(`<span tabindex="-1" style="cursor: pointer;text-decoration: underline dotted;">${json[i]['descrShort']}</span>`)
                .prop('outerHTML'),
            $('<div>', {
                'class': 'enrichment-popover-button',
                'data-toggle': 'popover',
                'data-placement': 'right',
                'data-trigger': 'focus',
                'data-html': 'true',
                'data-template': '<div class="popover enrichment-popover" role="tooltip"><div class="arrow"></div><h3 class="popover-header"></h3><div class="popover-body"></div></div>',
                'title': 'Drug set',
                'data-content': `${drugLinks.slice(0, 20).join(" ")}<br/><a href="/covid19/drugsets/${json[i]['id']}">${drugLinks.length > 20 ? '...<br/>' : ''}View drug set page</a>`
            })
                .append(
                    `<span tabindex="-1" style="cursor: pointer;text-decoration: underline dotted;">${json[i]['drugs'].length} drugs </span>`,
                )
                .prop('outerHTML')
        ];
        if (reviewed === 0) {
            dataArray[i].push(`<div class="btn-group" role="group" aria-label="Basic example"><button id="${json[i]['id']}-drugset-approved" type="button" class="btn btn-outline-success btn-sm" onclick="clickReviewButton(${json[i]['id']}, 1, 'drugset')"><i class="fas fa-check"></i></button><button id="${json[i]['id']}-drugset-rejected" type="button" class="btn btn-outline-danger btn-sm" onclick="clickReviewButton(${json[i]['id']},-1, 'drugset')"><i class="fas fa-times"></i></button></div>`);
        }
    }
    return dataArray;
}

function ds_drawTable(reviewed) {
    let columns = [
        {title: "Description"},
        {title: "Drugs"}
    ];
    if (reviewed === 0) {
        columns.push({title: "Review"});
    }

    $.get("drugsets", {reviewed: reviewed}, function (data) {
        $('#drugset_table').DataTable({
            width: '100%',
            data: ds_DTblify(JSON.parse(data), reviewed),
            responsive: true,
            columns: columns,
            dom: 'B<"small"f>rt<"small row"ip>',
            buttons: [],
            columnDefs: [
                {
                    targets: -1,
                    className: 'dt-body-left'
                }
            ],
            language: {
                search: "Search in description or drugs:",
                searchPlaceholder: "e.g. Remdesivir",
            },
            drawCallback: function () {
                $('.enrichment-popover-button').popover();
            }
        });
    });
}

$(document).ready(function () {
    $("#submit_drugSet_button").click(function () {
        $.ajax({
            url: 'drugsets',
            type: 'post',
            data: $('#drugSet_form').serialize(),
            success: function () {
                $('#drugSetModal').modal('show');
            }
        });
    });
});