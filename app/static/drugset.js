// Even though this file is nearly identical to geneset.js, I deliberately keep them separated,
// as I expect them to diverge further on.

//Array to hold the checked ids
var checkboxes = []

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

function ds_drawTable(url, wrapper, reviewed, overlap_url, category = 0) {
    let columns = [
        {
            data: null,
            defaultContent: '',
            className: 'select-checkbox',
            orderable: false
        },
        {title: "Description", data: 'descrShort'},
        {title: "Drugs", data: 'drugs', orderable: false},
        {title: "<span style='color: dodgerblue;'>DrugEn</span><span style='color: #ff3581;'>rich</span><span style='color: dodgerblue;'>r</span> link", data: 'enrichrShortId', orderable: false},
    ];
    if (reviewed === 0) {
        columns.push({title: "Category", data: 'category', orderable: false});
        columns.push({title: "Review", data: 'id', orderable: false});
    }
    if (wrapper === 'drugset_table') {
        columns.push({title: "Category", data: 'category', orderable: false});
    }
    let columnDefs = [
        {
            orderable: false,
            className: 'select-checkbox',
            targets: 0
        },
        {
            targets: 1,
            width: '85%',
            render: function (data, type, row) {
                const showContacts = row['showContacts'];
                const contacts = showContacts ? `<p><b>Author:</b> ${row['authorName']}<\p><p><b>Affiliation:</b> ${row['authorAffiliation']}<\p><p><b>E-mail:</b> ${row['authorEmail']}<\p>` :
                    reviewed ? '<i class="far fa-eye-slash"></i> Author preferred not to share contact details' : `<p style="color: red"><i class="far fa-eye-slash"></i> As author preferred not to share contact details, following will not be displayed:</p><p style="color: red"><b>Author:</b> ${row['authorName']}<\p><p style="color: red"><b>Affiliation:</b> ${row['authorAffiliation']}<\p><p style="color: red"><b>E-mail:</b> ${row['authorEmail']}<\p>`;
                let source;
                if (row['source'] === null) {
                    source = '';
                } else if (row['source'].includes('http')) {
                    source = `<p><b>Source: </b><p class="wrapped">${urlfy(row['source'])}</p></p>`
                }

                const dateObj = new Date(row['date'])
                const dateStr = `${dateObj.getFullYear()}-${dateObj.getMonth() + 1}-${dateObj.getDate()}`
                const date = `<p><b>Date added:</b> ${dateStr}</p>`;
                const meta = row['meta'] ? renderMeta(row['meta']) : '';
                const desc = `<p>${row['descrFull']}<\p>${source}${meta}${date}${contacts}`;

                return $('<div>', {
                    'class': 'enrichment-popover-button',
                    'data-toggle': 'popover',
                    'data-placement': 'bottom',
                    'data-trigger': 'focus',
                     'data-delay': '{ "show": 0, "hide": 4000 }',
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
                let drugLinks = [];
                $.each(row['drugs'].sort(), function (index, drug) {
                    drugLinks.push(`<a class="drug-link" href="https://amp.pharm.mssm.edu/covid19/drugs/${drug}" target="_blank">${drug}</a>`);
                });
                return $('<div>', {
                    'class': 'enrichment-popover-button',
                    'data-toggle': 'popover',
                    'data-placement': 'right',
                    'data-trigger': 'focus',
                    'data-html': 'true',
                    'data-template': '<div class="popover enrichment-popover" role="tooltip"><div class="arrow"></div><h3 class="popover-header"></h3><div class="popover-body"></div></div>',
                    'title': 'Drug set',
                    'data-content': `${drugLinks.slice(0, 20).join(" ")}<br/><a href="/covid19/drugsets/${row['id']}" target="_blank">${drugLinks.length > 20 ? '...<br/>' : ''}View drug set page</a>`
                })
                    .append(
                        `<span tabindex="-1" style="cursor: pointer;text-decoration: underline dotted;">${row['drugs'].length} drugs </span>`,
                    )
                    .prop('outerHTML')

            }
        },
        {
            targets: 3,
            className: 'dt-body-left',
            width: '15%',
            render: function (data, type, row) {
                return $('<a>', {
                    'href': `https://amp.pharm.mssm.edu/DrugEnrichr/enrich?dataset=${row['enrichrShortId']}`,
                    'target': '_blank'
                })
                    .append('<i class="fas fa-external-link-alt ml-1" style="font-size: 0.9rem;"></i>')
                    .prop('outerHTML')
            },
        },
    ]
    if (reviewed === 0) {
        columnDefs.push({
            targets: -2,
            render: function (data, type, row) {
                return `<div class="btn-group" role="group" aria-label="Basic example">
                            <button id="${row['id']}-1" type="button" class="btn btn-cat-${row['id']} ${activateCategoryButton(1, row['category'])} btn-sm"
                                    onclick="clickCategoryButton(${row['id']}, 1, 'drugset')"><i class="fas fa-globe"></i></button>
                            <button id="${row['id']}-2" type="button" class="btn btn-cat-${row['id']} ${activateCategoryButton(2, row['category'])} btn-sm"
                                    onclick="clickCategoryButton(${row['id']}, 2, 'drugset')"><i class="fas fa-flask"></i></button>
                            <button id="${row['id']}-3" type="button" class="btn btn-cat-${row['id']} ${activateCategoryButton(3, row['category'])} btn-sm"
                                    onclick="clickCategoryButton(${row['id']}, 3, 'drugset')"><i class="fas fa-calculator"></i></button>
                            <button id="${row['id']}-4" type="button" class="btn btn-cat-${row['id']} ${activateCategoryButton(4, row['category'])} btn-sm"
                                    onclick="clickCategoryButton(${row['id']}, 4, 'drugset')"><i class="fab fa-twitter"></i></button>
                        </div>`
            }
        });
        columnDefs.push({
            targets: -1,
            render: function (data, type, row) {
                return `<div class="btn-group" role="group" aria-label="Basic example">
                            <button id="${row['id']}-drugset-approved" type="button" class="btn btn-outline-success btn-sm" 
                                    onclick="clickReviewButton(${row['id']}, 1, 'drugset')"><i class="fas fa-check"></i></button>
                            <button id="${row['id']}-drugset-rejected" type="button" class="btn btn-outline-danger btn-sm" 
                                    onclick="clickReviewButton(${row['id']},-1, 'drugset')"><i class="fas fa-times"></i></button>
                        </div>`
            }
        });
    }

    if (wrapper === 'drugset_table') {
        let type_switch = {1: 'fas fa-globe', 2: 'fas fa-flask', 3: 'fas fa-calculator', 4: 'fab fa-twitter'};
        columnDefs.push({
            targets: -1,
            render: function (data, type, row) {
                return `<i class="${type_switch[row['category']]}"></i>`
            }
        });
    }

    let table = $(`#${wrapper}`).DataTable({
        width: '100%',
        autoWidth: false,
        responsive: true,
        columns: columns,
        dom: '<"small row"<"col-sm-12 col-md-3"B><"col-sm-12 col-md-9"f>>rt<"small row"ip>',
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
                return {body: JSON.stringify(args), reviewed: reviewed, category: category};
            }
        },
        select: {
            style: 'multi',
            selector: 'td:first-child'
        },
        buttons: [
            {
                extend: 'selected',
                text: 'Draw a Venn diagram',
                className: 'btn btn-outline-primary btn-sm',
                action: function (e, dt, node, config) {
                    // if (rows.count() <= 5){
                    const ids = checkboxes.join(",")
                    window.location.href = overlap_url + "/" + ids
                    // }else{
                    //     $('#overlapModalText').text("Max five rows")
                    //     $('#overlapError').modal({ show: true});
                    // }
                    // alert( 'There are '+rows.count()+'(s) selected in the table' );
                }
            }
        ],
        order: [[1, 'asc']]
    });
    table.columns.adjust().draw()
    // console.log(table.rows( { selected: true } ).data());
    // $('#drugset_table').on( 'click', 'tbody tr', function () {
    //     console.log(table.rows( { selected: true } ).data());
    // } );
    table.on( 'select', function ( e, dt, type, indexes ) {
        if ( type === 'row' ) {
            var data = table.rows( indexes ).data().pluck( 'id' );
            checkboxes.push(data[0])
            // do something with the ID of the selected items
        }
    });
    table.on( 'deselect', function ( e, dt, type, indexes ) {
        if ( type === 'row' ) {
            var data = table.rows( indexes ).data().pluck( 'id' );
            checkboxes = checkboxes.filter(i=>i!==data[0])
            // do something with the ID of the selected items
        }
    });
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