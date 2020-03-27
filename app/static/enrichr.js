function DTblify(json, reviewed) {
    let dataArray = [];
    for (let i = 0; i < json.length; i++) {
        // Links to enriched genes
        let enrichedLinks = [];
        $.each(json[i]['genes'].split('\n').sort(), function (index, gene) {
            enrichedLinks.push('<a class="enriched-gene-link" href="http://amp.pharm.mssm.edu/Harmonizome/gene/' + gene + '" target="_blank">' + gene + '</a>');
        });
        const showContacts = json[i]['showContacts'];
        const contacts = showContacts ? `<p><b>Author:</b> ${json[i]['authorName']}<\p><p><b>Affiliation:</b> ${json[i]['authorAffiliation']}<\p><p><b>E-mail:</b> ${json[i]['authorEmail']}<\p>` :
            reviewed ? '<i class="far fa-eye-slash"></i> Author preferred not to share contact details' : `<p style="color: red"><i class="far fa-eye-slash"></i> As author preferred not to share contact details, following will not be shown:</p><p style="color: red"><b>Author:</b> ${json[i]['authorName']}<\p><p style="color: red"><b>Affiliation:</b> ${json[i]['authorAffiliation']}<\p><p style="color: red"><b>E-mail:</b> ${json[i]['authorEmail']}<\p>`;
        let desc = `<p>${json[i]['descrFull']}<\p>${contacts}`;

        // Data Array
        dataArray[i] = [
            $('<div>', {
                'class': 'enrichment-popover-button',
                'data-toggle': 'popover',
                'data-placement': 'bottom',
                'data-html': 'true',
                'data-template': '<div class="popover enrichment-popover" role="tooltip"><div class="arrow"></div><h3 class="popover-header"></h3><div class="popover-body"></div></div>',
                'data-content': desc,
                'title': json[i]['descrShort']
            })
                .append(`<span style="cursor: pointer;text-decoration: underline dotted;">${json[i]['descrShort']}</span>`)
                .prop('outerHTML'),
            $('<div>', {
                'class': 'enrichment-popover-button',
                'data-toggle': 'popover',
                'data-placement': 'bottom',
                // 'data-trigger': 'focus',
                'data-html': 'true',
                'data-template': '<div class="popover enrichment-popover" role="tooltip"><div class="arrow"></div><h3 class="popover-header"></h3><div class="popover-body"></div></div>',
                'title': 'Gene set',
                'data-content': enrichedLinks.join(" ")
            })
                .append(
                    `<span style="cursor: pointer;text-decoration: underline dotted;">${json[i]['genes'].split('\n').length} genes </span><a href="https://amp.pharm.mssm.edu/Enrichr/enrich?dataset=${json[i]['enrichrShortId']}" target="_blank">En<span style="color: red">rich</span>r<i class="fas fa-external-link-alt ml-1"></i></a>`,
                )
                .prop('outerHTML')
        ];
        if (reviewed === 0) {
            dataArray[i].push(`<div class="btn-group" role="group" aria-label="Basic example"><button type="button" class="btn btn-outline-success btn-sm" onclick="$.post('review', {id: ${json[i]['id']}, reviewed: 1})"><i class="fas fa-check"></i></button><button type="button" class="btn btn-outline-danger btn-sm" onclick="$.post('review', {id: ${json[i]['id']}, reviewed: -1})"><i class="fas fa-times"></i></button></div>`);
        }
    }
    return dataArray;
}

function drawTable(reviewed) {
    let columns = [
        {title: "Description"},
        {title: "Genes"}];
    if (reviewed === 0) {
        columns.push({title: "Review"});
    }

    $.get("enrichr", {reviewed: reviewed}, function (data) {
        $('#enrichr_table').DataTable({
            width: '100%',
            data: DTblify(JSON.parse(data), reviewed),
            responsive: true,
            columns: columns,
            dom: 'B<"small"f>rt<"small row"ip>',
            buttons: [
                'copy',
                {
                    extend: 'excel',
                    exportOptions: {
                        columns: [0, 1, 2]
                    }
                }
            ],
            columnDefs: [
                // {sortable: false, targets: 5},
                // Sorting removed temporarily
                // {
                //     targets: [3, 4],
                //     visible: false,
                //     searchable: false,
                // },
            ],
            drawCallback: function () {
                // Enriched gene popover
                $('.enrichment-popover-button').popover();
            }
        });
    });
}