// Even though this file is nearly identical to drugset.js, I deliberately keep them separated,
// as I expect them to diverge further on.

function gs_DTblify(json, reviewed) {
    let dataArray = [];
    for (let i = 0; i < json.length; i++) {
        let geneLinks = [];
        $.each(json[i]['genes'].sort(), function (index, gene) {
            geneLinks.push('<a class="enriched-gene-link" href="http://amp.pharm.mssm.edu/Harmonizome/gene/' + gene + '" target="_blank">' + gene + '</a>');
        });
        const showContacts = json[i]['showContacts'];
        const contacts = showContacts ? `<p><b>Author:</b> ${json[i]['authorName']}<\p><p><b>Affiliation:</b> ${json[i]['authorAffiliation']}<\p><p><b>E-mail:</b> ${json[i]['authorEmail']}<\p>` :
            reviewed ? '<i class="far fa-eye-slash"></i> Author preferred not to share contact details' : `<p style="color: red"><i class="far fa-eye-slash"></i> As author preferred not to share contact details, following will not be displayed:</p><p style="color: red"><b>Author:</b> ${json[i]['authorName']}<\p><p style="color: red"><b>Affiliation:</b> ${json[i]['authorAffiliation']}<\p><p style="color: red"><b>E-mail:</b> ${json[i]['authorEmail']}<\p>`;
        let source;
        if (json[i]['source'] === null) {
            source = ''
        } else if ((json[i]['source'].includes('http://')) || (json[i]['source'].includes('https://'))) {
            // let a = document.createElement('a');
            // a.href = json[i]['source'];
            source = `<p><b>Source: </b><a class="wrapped" href="${json[i]['source']}"  target="_blank">${json[i]['source']}</a></p>`
        } else {
            source = `<p><b>Source: </b> ${json[i]['source']}</p>`;
        }
        const date = `<p><b>Date added:</b> ${json[i]['date'].split(' ')[0]}</p>`;
        const meta = json[i]['meta'] ? renderMeta(JSON.parse(json[i]['meta'])): '';
        const desc = `<p>${json[i]['descrFull']}<\p>${source}${meta}${date}${contacts}`;

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
                'title': 'Gene set',
                'data-content': `${geneLinks.slice(0, 20).join(" ")}<br/><a href="/covid19/genesets/${json[i]['id']}">${geneLinks.length > 20 ? '...<br/>' : ''}View gene set page</a>`
            })
                .append(
                    `<span tabindex="-1" style="cursor: pointer;text-decoration: underline dotted;">${json[i]['genes'].length} genes </span>`,
                )
                .prop('outerHTML'),
            $('<a>', {
                'href': `https://amp.pharm.mssm.edu/Enrichr/enrich?dataset=${json[i]['enrichrShortId']}`,
                'target': '_blank'
            })
                .append('<i class="fas fa-external-link-alt ml-1" style="font-size: 0.9rem;"></i>')
                .prop('outerHTML'),
            json[i]['genes']
        ];
        if (reviewed === 0) {
            dataArray[i].push(`<div class="btn-group" role="group" aria-label="Basic example"><button id="${json[i]['id']}-geneset-approved" type="button" class="btn btn-outline-success btn-sm" onclick="clickReviewButton(${json[i]['id']}, 1, 'geneset')"><i class="fas fa-check"></i></button><button id="${json[i]['id']}-geneset-rejected" type="button" class="btn btn-outline-danger btn-sm" onclick="clickReviewButton(${json[i]['id']},-1,'geneset')"><i class="fas fa-times"></i></button></div>`);
        }
    }
    return dataArray;
}

function renderMeta(meta) {
    let tmp = [];
    for (let m in meta) {
        tmp.push(`<p><b>${m}</b>: ${meta[m]}<\p>`);
    }

    return tmp.join('\n');
}

function gs_drawTable(reviewed) {
    let columns = [
        {title: "Description"},
        {title: "Genes"},
        {title: "Enrichr link"},
        {title: "Hidden genes"}
    ];
    if (reviewed === 0) {
        columns.push({title: "Review"});
    }

    $.get("genesets", {reviewed: reviewed}, function (data) {
        let table = $('#geneset_table').DataTable({
            width: '100%',
            data: gs_DTblify(JSON.parse(data), reviewed),
            responsive: true,
            columns: columns,
            dom: 'B<"small"f>rt<"small row"ip>',
            buttons: [],
            columnDefs: [
                {
                    targets: 0,
                    width: '50%'
                },
                {
                    targets: 0,
                    width: '20%'
                },
                {
                    targets: -1,
                    className: 'dt-body-left',
                    width: '30%'
                },
                {
                    targets: 3,
                    visible: false
                }
            ],
            language: {
                search: "Search in description or genes:",
                searchPlaceholder: "e.g. ACE2",
            },
            drawCallback: function () {
                // Enriched gene popover
                $('.enrichment-popover-button').popover();
            }
        });
        table.columns.adjust().draw();
    });
}

$(document).ready(function () {
    $("#submit_geneSet_button").click(function (e) {
        let form = $('#geneSet_form');
        form.addClass('was-validated');
        if (!form[0].checkValidity()) {
            e.preventDefault();
            e.stopPropagation();
        } else {
            $.ajax({
                url: 'genesets',
                type: 'post',
                data: form.serialize(),
                success: function () {
                    $('#geneSetModal').modal('show');
                }
            });
        }
    });
});