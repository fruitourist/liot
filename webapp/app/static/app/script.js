/* Cart Vars */
var selectedServicesIndexes = new Array();
var selectedDateIndex = null;
var selectedTimeIndex = null;


/* Telegram Vars */
var MainButton = window.Telegram.WebApp.MainButton;
var BackButton = window.Telegram.WebApp.BackButton;
MainButton.hide();
BackButton.hide();
MainButton.setText("ВЫБРАТЬ ДАТУ И ВРЕМЯ");


/* Sections */

var currentSection = 'select_services';

function loadSelectServices() {
	MainButton.setText("ВЫБРАТЬ ДАТУ И ВРЕМЯ");
	$('#select_date_and_time').hide();
	$('#select_services').show();
	currentSection = 'select_services';
}

function loadSelectDateAndTime() {
	MainButton.setText("ЗАКАЗАТЬ");
	$('#select_services').hide();
	$('#select_date_and_time-times').hide();
	loadDates();
	$('#select_date_and_time').show();
	currentSection = 'select_date_and_time';
}


/* select_services */

$('.select_service').click(function() {
	const serviceIndex = parseInt($(this).attr('data-service_index'));
	if (!selectedServicesIndexes.includes(serviceIndex)) {
		selectedServicesIndexes.push(serviceIndex);
	} else {
		selectedServicesIndexes.splice(selectedServicesIndexes.indexOf(serviceIndex), 1);
	}

	if (selectedServicesIndexes.length > 0) {
		if (!MainButton.isVisible) {
			MainButton.show();
		}
	} else {
		if (MainButton.isVisible) {
			MainButton.hide();
		}
	}
});


/* select_date_and_time */

function loadDates() {
	$('#select_date_and_time-dates').empty();
	
	for (let i = 0; i < window.dates.length; i++) {
		let input = document.createElement('input');
		input.classList.add('select_date');
		input.type = 'radio';
		input.name = 'select_date';
		input.onclick = function() {
			selectedDateIndex = i;
			loadTimes(i);
		};
		const text = window.dates[i].toLocaleDateString('ru-RU');
		const br = document.createElement('br');

		$('#select_date_and_time-dates').append(input);
		$('#select_date_and_time-dates').append(text);
		$('#select_date_and_time-dates').append(br);
	}
}

function loadTimes(selectedDateIndex) {
	$('#select_date_and_time-times').empty();
	
	for (let i = 0; i < window.times[selectedDateIndex].length; i++) {
		let input = document.createElement('input');
		input.classList.add('select_time');
		input.type = 'radio';
		input.name = 'select_time';
		input.onclick = function() {
			selectedTimeIndex = i;
		};
		const text = window.times[selectedDateIndex][i].toLocaleTimeString('ru-RU');
		const br = document.createElement('br');

		$('#select_date_and_time-times').append(input);
		$('#select_date_and_time-times').append(text);
		$('#select_date_and_time-times').append(br);
	}

	$('#select_date_and_time-times').show();
}


/* Telegram Funcs */

MainButton.onClick(function() {
	if (currentSection == 'select_services') {
		loadSelectDateAndTime();
		if (!BackButton.isVisible) {
			BackButton.show();
		}
	} else if (currentSection == 'select_date_and_time') {

		let prices = new Array();
		for (let selectedServiceIndex of selectedServicesIndexes) {
			prices.push({
				'label': window.services[selectedServiceIndex].title,
				'amount': window.services[selectedServiceIndex].price * 100
			})
		}

		let requestParams = {
			'prices': prices,
		}

		let requestURL = new URL(`https://127.0.0.1/liot/make_order/create_invoice_link`);
		let requestURLPrices = JSON.stringify(requestParams['prices']);
		requestURL.searchParams.set('prices', requestURLPrices);

		let xhr = new XMLHttpRequest();
		xhr.open('GET', requestURL);
		xhr.send();
		xhr.onload = function() {
			window.Telegram.WebApp.openInvoice(JSON.parse(xhr.response).result);
		}
	}
});

BackButton.onClick(function() {
	if (currentSection == 'select_date_and_time') {
		loadSelectServices();
		if (BackButton.isVisible) {
			BackButton.hide();
		}
	}
});

window.Telegram.WebApp.onEvent('invoiceClosed', function(object) {
	if (object.status == 'pending' || object.status == 'paid') {
		window.Telegram.WebApp.close();
	}
});