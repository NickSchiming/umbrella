var updateBtns = document.getElementsByClassName('update-carrinho')
var inputs = document.getElementsByClassName('inputquantity')


for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function () {
		var idProduto = this.dataset.produto
		var action = this.dataset.action
		updateUserOrder(idProduto, action)

	})
}


for (i = 0; i < inputs.length; i++) {
	inputs[i].addEventListener('change', function () {
		var idProduto = this.dataset.produto
		var action = this.value
		updateUserOrder(idProduto, action)
	});
}

function updateUserOrder(idProduto, action) {
	var url = '/atualizar_item/'

	fetch(url, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': csrftoken,
		},
		body: JSON.stringify({ 'idProduto': idProduto, 'action': action })
	})
		.then((response) => {
			return response.json();
		})
		.then((dados) => {
			location.reload()
		});
}



