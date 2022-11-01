var updateBtns = document.getElementsByClassName('update-carrinho')

for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function () {
		var idProduto = this.dataset.produto
		var action = this.dataset.action
		console.log('idProduto:', idProduto, 'Action:', action)
		console.log('USER:', user)

		if (user == 'AnonymousUser') {
			addCookieItem(idProduto, action)
		} else {
			updateUserOrder(idProduto, action)
		}
	})
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
		.then((data) => {
			location.reload()
		});
}

function addCookieItem(idProduto, action) {
	console.log('User is not authenticated')

	if (action == 'add') {
		if (carrinho[idProduto] == undefined) {
			carrinho[idProduto] = { 'quantidade': 1 }

		} else {
			carrinho[idProduto]['quantidade'] += 1
		}
	}

	if (action == 'remove') {
		carrinho[idProduto]['quantidade'] -= 1

		if (carrinho[idProduto]['quantidade'] <= 0) {
			console.log('Item should be deleted')
			delete cart[idProduto];
		}
	}
	console.log('CARRINHO:', carrinho)
	document.cookie = 'carrinho=' + JSON.stringify(cart) + ";domain=;path=/"

	location.reload()
}


