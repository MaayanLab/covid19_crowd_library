// Even though this file is nearly identical to drugset.js, I deliberately keep them separated,
// as I expect them to diverge further on.

function gs_drawTable(url, reviewed) {
    let columns = [
        {title: "Description", data: 'description'},
        { title: "Genes", data: 'genes'},
        {title: "Enrichr link", data: 'enrichrShortId'},
    ];
    if (reviewed === 0) {
        columns.push({title: "Review"});
    }

    let columnDefs = [
        {
            targets: 0,
            width: '20%',
            render: function (data, type, row) {
                const showContacts = row['showContacts'];
                const contacts = showContacts ? `<p><b>Author:</b> ${row['authorName']}<\p><p><b>Affiliation:</b> ${row['authorAffiliation']}<\p><p><b>E-mail:</b> ${row['authorEmail']}<\p>` :
                    reviewed ? '<i class="far fa-eye-slash"></i> Author preferred not to share contact details' : `<p style="color: red"><i class="far fa-eye-slash"></i> As author preferred not to share contact details, following will not be displayed:</p><p style="color: red"><b>Author:</b> ${row['authorName']}<\p><p style="color: red"><b>Affiliation:</b> ${row['authorAffiliation']}<\p><p style="color: red"><b>E-mail:</b> ${row['authorEmail']}<\p>`;

                const date = `<p><b>Date added:</b> ${row['date'].split(' ')[0]}</p>`;
                let source;
                if (row['source'] === null) {
                    source = ''
                } else if ((row['source'].includes('http://')) || (row['source'].includes('https://'))) {
                    // let a = document.createElement('a');
                    // a.href = row['source'];
                    source = `<p><b>Source: </b><a class="wrapped" href="${row['source']}"  target="_blank">${row['source']}</a></p>`
                } else {
                    source = `<p><b>Source: </b> ${row['source']}</p>`;
                }
                const desc = `<p>${row['descrFull']}<\p>${source}${date}${contacts}`;
                return $('<div>', {
                    'class': 'enrichment-popover-button',
                    'data-toggle': 'popover',
                    'data-placement': 'bottom',
                    'data-trigger': 'focus',
                    'data-html': 'true',
                    'data-template': '<div class="popover enrichment-popover" role="tooltip"><div class="arrow"></div><h3 class="popover-header"></h3><div class="popover-body"></div></div>',
                    'data-content': desc,
                    'title': row['descrShort']
                })
                    .append(`<span tabindex="-1" style="cursor: pointer;text-decoration: underline dotted;">${row['descrShort']}</span>`)
                    .prop('outerHTML')
            },
        },
        {
            targets: 1,
            width: '50%',
            render: function (data, type, row) {
                let geneLinks = [];
                $.each(row['genes'].sort(), function (index, gene) {
                    geneLinks.push('<a class="enriched-gene-link" href="http://amp.pharm.mssm.edu/Harmonizome/gene/' + gene + '" target="_blank">' + gene + '</a>');
                });
                return $('<div>', {
                    'class': 'enrichment-popover-button',
                    'data-toggle': 'popover',
                    'data-placement': 'right',
                    'data-trigger': 'focus',
                    'data-html': 'true',
                    'data-template': '<div class="popover enrichment-popover" role="tooltip"><div class="arrow"></div><h3 class="popover-header"></h3><div class="popover-body"></div></div>',
                    'title': 'Gene set',
                    'data-content': `${geneLinks.slice(0, 20).join(" ")}<br/><a href="/covid19/genesets/${row['id']}">${geneLinks.length > 20 ? '...<br/>' : ''}View gene set page</a>`
                }).append(
                    `<span tabindex="-1" style="cursor: pointer;text-decoration: underline dotted;">${row['genes'].length} genes </span>`,
                ).prop('outerHTML')
            },
        },
        {
            targets: -1,
            className: 'dt-body-left',
            width: '30%',
            render: function (data, type, row) {
                return $('<a>', {
                    'href': `https://amp.pharm.mssm.edu/Enrichr/enrich?dataset=${row['enrichrShortId']}`,
                    'target': '_blank'
                })
                    .append('<i class="fas fa-external-link-alt ml-1" style="font-size: 0.9rem;"></i>')
                    .prop('outerHTML')
            },
        },
    ]
    if (reviewed === 0) {
        columnDefs.push({
            targets: 0,
            render: function(data, type, row) {
                return `<div class="btn-group" role="group" aria-label="Basic example"><button id="${row['id']}-geneset-approved" type="button" class="btn btn-outline-success btn-sm" onclick="clickReviewButton(${row['id']}, 1, 'geneset')"><i class="fas fa-check"></i></button><button id="${row['id']}-geneset-rejected" type="button" class="btn btn-outline-danger btn-sm" onclick="clickReviewButton(${row['id']},-1,'geneset')"><i class="fas fa-times"></i></button></div>`
            }
            
        });
    }


    let table = $('#geneset_table').DataTable({
        width: '100%',
        responsive: true,
        columns: columns,
        dom: 'B<"small"f>rt<"small row"ip>',
        buttons: [],
        columnDefs: columnDefs,
        language: {
            search: "Search in description or genes:",
            searchPlaceholder: "e.g. ACE2",
        },
        drawCallback: function () {
            // Enriched gene popover
            $('.enrichment-popover-button').popover();
        },
        serverSide: true,
        ajax: {
            url: url,
            type: 'POST',
            data: function (args) {
                return { body: JSON.stringify(args) };
            }
        },
    });
    table.columns.adjust().draw();
}

$(document).ready(function () {
    $("#submit_geneSet_button").click(function () {
        $.ajax({
            url: 'genesets',
            type: 'post',
            data: $('#geneSet_form').serialize(),
            success: function () {
                $('#geneSetModal').modal('show');
            }
        });
    });
});