 var options = {
     onKeyPress: function (telefone, e, field, options) {
         var masks = ['(00)00000-0000', '(00)0000-00000'];
         var mask = (telefone.length > 13) ? masks[0] : masks[1];
        $('.mask-telefone').mask(mask, options);
    }
};

$(function () {
    $('.mask-telefone').mask('(00)0000-0000', options);
    $('.mask-cpf').mask('000.000.000-00', { reverse: true });
    $('.mask-datanasc').mask('00/00/0000');
})
