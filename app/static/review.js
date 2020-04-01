function switchButtonRecolor(id, reviewed) {
    switch (reviewed) {
        case -1:
            $(`#${id}-approved`).removeClass('btn-success').addClass('btn-outline-success');
            $(`#${id}-rejected`).removeClass('btn-outline-danger').addClass('btn-danger');
            break;
        case 1:
            $(`#${id}-rejected`).removeClass('btn-danger').addClass('btn-outline-danger')
            $(`#${id}-approved`).removeClass('btn-outline-success').addClass('btn-success')
            break;
        default:
            $(`#${id}-approved`).removeClass('btn-success').addClass('btn-outline-success');
            $(`#${id}-rejected`).removeClass('btn-danger').addClass('btn-outline-danger')
    }
}

function clickReviewButton(id, reviewed, url) {
    $.post(url, {id: id, reviewed: reviewed});
    switchButtonRecolor(id, reviewed)
}