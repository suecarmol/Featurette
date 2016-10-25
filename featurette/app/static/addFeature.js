$('#users').removeClass('active');
$('#clients').removeClass('active');
$('#product_areas').removeClass('active');
$('#home').addClass('active');

document.getElementById("target-date").flatpickr({
	minDate: "today",
	maxDate: "2050-12-31",
	enableTime: false,
	altInput: true
});
