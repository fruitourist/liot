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
	MainButton.setText("ЗАПИСАТЬСЯ");
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
		$(this).addClass('select_service-selected');
		selectedServicesIndexes.push(serviceIndex);
	} else {
		$(this).removeClass('select_service-selected');
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
		let div = document.createElement('div');
		div.classList.add('select_date');
		div.onclick = function() {
			if (selectedDateIndex != null) {
				$('.select_date')[selectedDateIndex].classList.remove('select_date-selected');
			}
			$(this).addClass('select_date-selected');
			selectedDateIndex = i;
			loadTimes(i);
		};
		div.textContent = window.dates[i].toLocaleDateString('ru-RU', {'day': '2-digit', 'month': '2-digit'});

		$('#select_date_and_time-dates').append(div);
	}
}

function loadTimes(selectedDateIndex) {
	$('#select_date_and_time-times').empty();
	
	for (let i = 0; i < window.times[selectedDateIndex].length; i++) {
		let div = document.createElement('div');
		div.classList.add('select_time');
		div.onclick = function() {
			if (selectedTimeIndex != null) {
				$('.select_time')[selectedTimeIndex].classList.remove('select_time-selected');
			}
			$(this).addClass('select_time-selected');
			selectedTimeIndex = i;
		};
		div.textContent = window.times[selectedDateIndex][i].toLocaleTimeString('ru-RU', {'hour': '2-digit', 'minute': '2-digit'});

		$('#select_date_and_time-times').append(div);
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

		let selectedDateString = $('.select_date')[selectedDateIndex].textContent;
		let selectedTimeString = $('.select_time')[selectedTimeIndex].textContent;

		let requestParams = {
			'description': `Стрижка для тебя на ${selectedDateString} в ${selectedTimeString}`,
			'prices': JSON.stringify(prices),
			'payload': JSON.stringify({
				'init_message_id': initMessageId,
				'selected_date_string': selectedDateString,
				'selected_time_string': selectedTimeString,
			})
		}

		let requestURL = new URL(`https://fruitourist.ru/liot/make_order/create_invoice_link`);
		requestURL.searchParams.set('description', requestParams['description']);
		requestURL.searchParams.set('prices', requestParams['prices']);
		requestURL.searchParams.set('payload', requestParams['payload']);

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