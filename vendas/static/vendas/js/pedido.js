$('#add-form').click(function () {
    var form_idx = $('#id_item_pedido_set-TOTAL_FORMS').val();
    $('#form-group').append($('#empty_form').html().replace(/__prefix__/g, form_idx));
    $('#id_item_pedido_set-TOTAL_FORMS').val(parseInt(form_idx) + 1);
});

$(document).on('click', '#rmv-form', function (e) {
    e.preventDefault();
    deleteForm('item_pedido_set', $(this));
    return false;
});



function deleteForm(prefix_tag, btn) {
    var total = parseInt($('#id_' + prefix_tag + '-TOTAL_FORMS').val());
    btn.closest('.item_pedido-form').remove();
    var forms = $('.item_pedido-form');
    var formlength = forms.length - 1;
    var idstring = '#id_' + prefix_tag + '-TOTAL_FORMS';
    $(idstring).val(parseInt(formlength));
    for (var i = 0, formCount = formlength; i < formCount; i++) {
        $(forms.get(i)).find(':input').each(function () {
            updateElementIndex(this, prefix_tag, i);
        });
        $(forms.get(i)).find('label').each(function () {
            updateElementIndex(this, prefix_tag, i);
        });
    }
    return false;
};

function updateElementIndex(el, prefix_tag, ndx) {
    var id_regex = new RegExp('(' + prefix_tag + '-\\d+)');
    var replacement = prefix_tag + '-' + ndx;
    if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
    if (el.id) el.id = el.id.replace(id_regex, replacement);
    if (el.name) el.name = el.name.replace(id_regex, replacement);

};



var total_form = parseInt($('#id_item_pedido_set-TOTAL_FORMS').val());

var arr = [];
for (var i = 0; i < total_form; i++) {
    arr[i] = $("#id_item_pedido_set-" + i + "-id").val();
}


$("form").submit(function () {
    var current_form = parseInt($('#id_item_pedido_set-TOTAL_FORMS').val());
    for (var i = 0; i < current_form; i++) {
        var input = $("<input>")
            .attr("id", "id_item_pedido_set-" + i + "-id")
            .attr("hidden", "hidden").val(arr[i]);
        $("form").append(input)
    }
});

$('#btn').on('click', function () {
    alert('Text1 changed!');
});

$('#oi').on('input', function () {
    alert('Text1 changed!');
});
