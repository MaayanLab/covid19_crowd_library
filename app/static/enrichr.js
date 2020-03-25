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
    for (var i = 0; i < json.length; i++) {

        // Links to enriched genes
        var enrichedLinks = [];
        $.each(json[i][enriched], function (index, gene) {
            enrichedLinks.push('<a class="enriched-gene-link" href="http://amp.pharm.mssm.edu/Harmonizome/gene/' + gene + '" target="_blank">' + gene + '</a>');
        });

        // Data Array
        dataArray[i] = [i + 1,
            firstCol.prop('outerHTML'),
            json[i]["pvalue"].toPrecision(4),
            json[i]["zscore"].toFixed(2),
            json[i]["combinedScore"].toFixed(2),
            $('<div>', {
                'class': 'enrichment-popover-button',
                'data-toggle': 'popover',
                'data-placement': 'left',
                'data-html': 'true',
                'data-template': '<div class="popover enrichment-popover" role="tooltip"><div class="arrow"></div><h3 class="popover-header"></h3><div class="popover-body"></div></div>',
                'title': enriched.replace('enriched', 'Overlapping <button class="float-right enrichr-button" onclick="sendToEnrichr(this, event);">En<span class="red">rich</span>r<i class="fas fa-external-link-alt ml-1"></i></button>'),
                'data-content': '<b>' + json[i]["name"].split(/[-_]/)[0] + '</b> targets <span class="font-italic">' + json[i][enriched].length + ' genes</span> from the input gene list.<br>' + metaDiv.prop('outerHTML') + '<div class="my-1">The full list of ' + enriched.replace('enriched', '').toLowerCase() + ' is available below:</div>' + enrichedLinks.join(" ")
            })
                .css('cursor', 'pointer')
                .css('text-decoration', 'underline')
                .css('text-decoration-style', 'dotted')
                .append(json[i][enriched].length + ' ' + enriched.replace('enriched', '').toLowerCase())
                .prop('outerHTML')
        ];
    }
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
                {title: "Enrichr link"},
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
