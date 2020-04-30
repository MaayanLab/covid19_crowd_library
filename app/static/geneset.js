// Even though this file is nearly identical to drugset.js, I deliberately keep them separated,
// as I expect them to diverge further on.

function renderMeta(meta) {
    let tmp = [];
    for (let m in meta) {
        tmp.push(`<p><b>${m}</b>: ${meta[m]}<\p>`);
    }

    return tmp.join('\n');
}

function urlfy(source) {
    let r = /(https?:\/\/[^\s]+\.\w{2,}(\/*\w*\-*)*)\??(\w*\-*)*\=?(\w*\-*\w*\&*)*/g;
    return source.replace(r, '<a href="$1" target="_blank">$1</a>')
}

function gs_drawTable(url, reviewed, overlap_url) {
    let columns = [
        {
            data: null,
            defaultContent: '',
            className: 'select-checkbox',
            orderable: false
        },
        {title: "Description", data: 'description'},
        {title: "Genes", data: 'genes', orderable: false},
        {title: "Enrichr link", data: 'enrichrShortId', orderable: false},
    ];
    if (reviewed === 0) {
        columns.push({title: "Review", data: 'id', orderable: false});
    }

    let columnDefs = [
        {
            orderable: false,
            className: 'select-checkbox',
            targets:   0
        },
        {
            targets: 1,
            width: '70%',
            render: function (data, type, row) {
                const showContacts = row['showContacts'];
                const contacts = showContacts ? `<p><b>Author:</b> ${row['authorName']}<\p><p><b>Affiliation:</b> ${row['authorAffiliation']}<\p><p><b>E-mail:</b> ${row['authorEmail']}<\p>` :
                    reviewed ? '<i class="far fa-eye-slash"></i> Author preferred not to share contact details' : `<p style="color: red"><i class="far fa-eye-slash"></i> As author preferred not to share contact details, following will not be displayed:</p><p style="color: red"><b>Author:</b> ${row['authorName']}<\p><p style="color: red"><b>Affiliation:</b> ${row['authorAffiliation']}<\p><p style="color: red"><b>E-mail:</b> ${row['authorEmail']}<\p>`;
                let source;
                if (row['source'] === null) {
                    source = ''
                } else if (row['source'].includes('http')) {
                    source = `<p><b>Source: </b><p class="wrapped">${urlfy(row['source'])}</p></p>`
                } else {
                    source = `<p><b>Source: </b> ${row['source']}</p>`;
                }
                const dateObj = new Date(row['date'])
                const dateStr = `${dateObj.getFullYear()}-${dateObj.getMonth()+1}-${dateObj.getDate()}`
                const date = `<p><b>Date added:</b> ${dateStr}</p>`;
                const meta = row['meta'] ? renderMeta(row['meta']) : '';
                const desc = `<p>${row['descrFull']}<\p>${source}${meta}${date}${contacts}`;

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
            targets: 2,
            width: '15%',
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
                    'data-content': `${geneLinks.slice(0, 20).join(" ")}<br/><a href="/covid19/genesets/${row['id']}" target="_blank">${geneLinks.length > 20 ? '...<br/>' : ''}View gene set page</a>`
                }).append(
                    `<span tabindex="-1" style="cursor: pointer;text-decoration: underline dotted;">${row['genes'].length} genes </span>`,
                ).prop('outerHTML')
            },
        },
        {
            targets: 3,
            className: 'dt-body-left',
            width: '15%',
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
            targets: -1,
            render: function(data, type, row) {
                return `<div class="btn-group" role="group" aria-label="Basic example"><button id="${row['id']}-geneset-approved" type="button" class="btn btn-outline-success btn-sm" onclick="clickReviewButton(${row['id']}, 1, 'geneset')"><i class="fas fa-check"></i></button><button id="${row['id']}-geneset-rejected" type="button" class="btn btn-outline-danger btn-sm" onclick="clickReviewButton(${row['id']},-1,'geneset')"><i class="fas fa-times"></i></button></div>`
            }
            
        });
    }


    let table = $('#geneset_table').DataTable({
        autoWidth: false,
        width: '100%',
        responsive: true,
        columns: columns,
        dom: '<"small row"<"col-sm-12 col-md-3"B><"col-sm-12 col-md-9"f>>rt<"small row"ip>',
        columnDefs: columnDefs,
        language: {
            search: "Search in description, metadata or genes:",
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
                return { body: JSON.stringify(args), reviewed: reviewed };
            }
        },
        select: {
            style:    'multi',
            selector: 'td:first-child'
        },
        buttons: [
            {
                extend: 'selected',
                text: 'Draw a Venn diagram',
                className: 'btn btn-outline-primary btn-sm',
                action: function ( e, dt, node, config ) {
                    const rows = dt.rows( { selected: true } );
                    // if (rows.count() <= 5){
                        const ids = rows.data().map(i=>i.id).join(",")
                        window.location.href = overlap_url + "/" + ids
                    // }else{
                    //     $('#overlapModalText').text("Max five rows")
                    //     $('#overlapError').modal({ show: true});
                    // }
                    // alert( 'There are '+rows.count()+'(s) selected in the table' );
                }
            }
        ],
        order: [[ 1, 'asc' ]]
    });
    table.columns.adjust().draw();
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