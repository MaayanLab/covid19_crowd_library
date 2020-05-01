function switchButtonRecolor(id, reviewed, set_type) {
    switch (reviewed) {
        case -1:
            $(`#${id}-${set_type}-approved`).removeClass('btn-success').addClass('btn-outline-success');
            $(`#${id}-${set_type}-rejected`).removeClass('btn-outline-danger').addClass('btn-danger');
            break;
        case 1:
            $(`#${id}-${set_type}-rejected`).removeClass('btn-danger').addClass('btn-outline-danger')
            $(`#${id}-${set_type}-approved`).removeClass('btn-outline-success').addClass('btn-success')
            break;
        default:
            $(`#${id}-${set_type}-approved`).removeClass('btn-success').addClass('btn-outline-success');
            $(`#${id}-${set_type}-rejected`).removeClass('btn-danger').addClass('btn-outline-danger')
    }
}

function clickReviewButton(id, reviewed, set_type) {
    $.post('review', {id: id, reviewed: reviewed, set_type: set_type});
    switchButtonRecolor(id, reviewed, set_type)
}

function activateCategoryButton(current, category) {
    return current === category ? 'btn-primary' : 'btn-outline-primary'
}

function clickCategoryButton(id, category, set_type) {
    $.post('review', {id: id, set_type: set_type, category: category});
    $(`.btn-cat-${id}`).removeClass('btn-primary').addClass('btn-outline-primary');
    $(`#${id}-${category}`).removeClass('btn-outline-primary').addClass('btn-primary');
}