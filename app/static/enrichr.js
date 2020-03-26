function sendToEnrichr(button) {
    // Get genes
    var genes = Object.values($(button).parents('.popover').find('.enriched-gene-link').map(function (index, elem) {
        return $(elem).text()
    }));

    // Create Form
    var $form = $('<form>', {
        'method': 'post',
        'action': 'https://amp.pharm.mssm.edu/Enrichr/enrich',
        'target': '_blank',
        'enctype': 'multipart/form-data'
    })
        .append($('<input>', {'type': 'hidden', 'name': 'list', 'value': genes.join('\n')}))
        .append($('<input>', {
            'type': 'hidden',
            'name': 'description',
            'value': 'Enriched ' + $(button).parents('.popover').find('b').first().text() + ' targets from X2K'
        }));

    // Submit
    $(button).parents('.popover').append($form);
    $form.submit();
    $form.remove();
}

function DTblify(json) {
    let dataArray = [];
    for (let i = 0; i < json.length; i++) {
        // Links to enriched genes
        let enrichedLinks = [];
        $.each(json[i]['genes'].split('\n'), function (index, gene) {
            enrichedLinks.push('<a class="enriched-gene-link" href="http://amp.pharm.mssm.edu/Harmonizome/gene/' + gene + '" target="_blank">' + gene + '</a>');
        });

        // Data Array
        dataArray[i] = [
            json[i]['descrShort'],
            $('<div>', {
                'class': 'enrichment-popover-button',
                'data-toggle': 'popover',
                'data-placement': 'left',
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
    }
    console.log(dataArray);
    return dataArray;
}


$(document).ready(function () {
    $.get("enrichr", function (data) {
        $('#enrichr_table').DataTable({
            width: '100%',
            data: DTblify(JSON.parse(data)),
            responsive: true,
            columns: [
                {title: "Description"},
                // {title: "Author"},
                // {title: "Full description"}
                // {title: "Affiliation"}
                // {title: "E-mail"}
                {title: "Genes"}
            ],
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
});
