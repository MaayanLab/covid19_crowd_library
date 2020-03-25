$(document).ready(function () {
    $.get("enrichr", function (data) {
        $('#enrichr_table').DataTable({
            width: '100%',
            data: JSON.parse(data),
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
