$(function() {
	// Carregamento via AJAX simples
	$('#num_users').load('http://127.0.0.1:8000/num_users/');

	$.get($('#love').attr('href'), function(data) {
		if (data.status) {
			$("#num_loves").text(data.loves);
		}
	});

	// Opinioes
	$('#love').click(function(e) {
		// Evita o comportamento padrao
		e.preventDefault();
		// Captura o endereco
		url = $(this).attr('href');
		console.log(url);

		//// Poderia ser feito com post e enviar um JSON como segundo parametro
		// id = $(this).attr('data-id');
		// $.post(url, {JSON AQUI}, function(data) {});

		$.get(url, function(data) {
			if (data.status) {
				$("#num_loves").text(data.loves);
				$("#love").css('color', 'red');
				// $("#love").attr("disabled", true); // amor restrito :'(
			}
		});
	});

});
