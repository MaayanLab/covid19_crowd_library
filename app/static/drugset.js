// Even though this file is nearly identical to geneset.js, I deliberately keep them separated,
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
    return source.replace(r, '<a href="$1">$1</a>')
}

function ds_drawTable(url, reviewed) {
    let columns = [
        {title: "Description", data: 'descrShort'},
        {title: "Drugs", data: 'drugs', orderable: false},
    ];
    if (reviewed === 0) {
        columns.push({title: "Review", data: 'id', orderable: false});
    }

    let columnDefs = [
        {
            targets: 0,
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
            targets: 1,
            width: '30%',
            render: function (data, type, row) {
                let drugLinks = [];
                $.each(row['drugs'].sort(), function (index, drug) {
                    drugLinks.push('<a class="drug-link" href="#" target="_blank">' + drug + '</a>');
                });
                return $('<div>', {
                    'class': 'enrichment-popover-button',
                    'data-toggle': 'popover',
                    'data-placement': 'right',
                    'data-trigger': 'focus',
                    'data-html': 'true',
                    'data-template': '<div class="popover enrichment-popover" role="tooltip"><div class="arrow"></div><h3 class="popover-header"></h3><div class="popover-body"></div></div>',
                    'title': 'Drug set',
                    'data-content': `${drugLinks.slice(0, 20).join(" ")}<br/><a href="/covid19/drugsets/${row['id']}">${drugLinks.length > 20 ? '...<br/>' : ''}View drug set page</a>`
                })
                    .append(
                        `<span tabindex="-1" style="cursor: pointer;text-decoration: underline dotted;">${row['drugs'].length} drugs </span>`,
                    )
                    .prop('outerHTML')
                    
            }
        },
    ]
    if (reviewed === 0) {
        columnDefs.push({
            targets: -1,
            render: function (data, type, row) {
                return `<div class="btn-group" role="group" aria-label="Basic example"><button id="${row['id']}-drugset-approved" type="button" class="btn btn-outline-success btn-sm" onclick="clickReviewButton(${row['id']}, 1, 'drugset')"><i class="fas fa-check"></i></button><button id="${row['id']}-drugset-rejected" type="button" class="btn btn-outline-danger btn-sm" onclick="clickReviewButton(${row['id']},-1, 'drugset')"><i class="fas fa-times"></i></button></div>`
            }
        });
    }

    let table = $('#drugset_table').DataTable({
        width: '100%',
        responsive: true,
        columns: columns,
        dom: 'B<"small"f>rt<"small row"ip>',
        buttons: [],
        columnDefs: columnDefs,
        language: {
            search: "Search in description, metadata or drugs:",
            searchPlaceholder: "e.g. Remdesivir",
        },
        drawCallback: function () {
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
    });
    table.columns.adjust().draw()
}

$(document).ready(function () {
    $("#submit_drugSet_button").click(function (e) {
        let form = $('#drugSet_form');
        form.addClass('was-validated');
        if (!form[0].checkValidity()) {
            e.preventDefault();
            e.stopPropagation();
        } else {
            $.ajax({
                url: 'drugsets',
                type: 'post',
                data: form.serialize(),
                success: function () {
                    $('#drugSetModal').modal('show');
                }
            });
        }
    });
});