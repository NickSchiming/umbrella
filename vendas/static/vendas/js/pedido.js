
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
    // console.log("total forms: ", total);
    btn.closest('.item_pedido-form').remove();
    var forms = $('.item_pedido-form');
    // console.log("forms length: ", forms.length);
    var formlength = forms.length - 1;
    var idstring = '#id_' + prefix_tag + '-TOTAL_FORMS';
    $(idstring).val(parseInt(formlength));
    // console.log("formlength: ", formlength);
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
    // console.log("elemento: ", $(el));
    if ($( el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
    if (el.id) el.id = el.id.replace(id_regex, replacement);
    if (el.name) el.name = el.name.replace(id_regex, replacement);
    
};



var total_form = parseInt($('#id_item_pedido_set-TOTAL_FORMS').val());
// var total_form_var_header = parseInt($('#id_inspection_variable_header-TOTAL_FORMS').val());

var arr = [];
// var variable_header_arr = [];
// {#Store the value of the id in an initial array in the event the form is manipulated#}
for (var i = 0; i < total_form; i++) {
    arr[i] = $("#id_item_pedido_set-" + i + "-id").val();
}
// for (var i = 0; i < total_form_var_header; i++) {
//     variable_header_arr[i] = $("#id_inspection_variable_header-" + i + "-id").val();
// }

$("form").submit(function () {
    // Let's find the input to check
    var current_form = parseInt($('#id_item_pedido_set-TOTAL_FORMS').val());
    // {#Go through the current form and assign the initial id values to the lines. #}
    for (var i = 0; i < current_form; i++) {
        var input = $("<input>")
            .attr("id", "id_item_pedido_set-" + i + "-id")
            .attr("hidden", "hidden").val(arr[i]);
        $("form").append(input)
    }
});
