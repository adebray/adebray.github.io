/* Calculates what year of grad school I'm in, based on the current date.
   Or, "I'm procrastinating on reading about Čech cohomology."
 */

// Going from ints to cardinal numbers.
const go_card = ['zeroth', 'first', 'second', 'third', 'fourth', 'fifth', 'sixth']

/* Returns the year of grad school I'm in, as a number. This is defined
   to be 1 + the number of years elapsed since August 1, 2015.
   curr_time is a Date object.
 */
const my_year = function(curr_time) {
	let delta_year = curr_time.getFullYear() - 2015
	// note: getMonth is zero-indexed
	if (curr_time.getMonth() + 1 >= 8) delta_year++;
	return delta_year;
}

// also an easter egg that I decided to make
const get_cookie_value_by_key = function(name) {
  var match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
  if (match) return match[2];
}

// TODO: what is Purdue's equivalent?
//const UT_login_name = function() {
//	return get_cookie_value_by_key("utlogin-name").replace('+', ' ');
//}

window.onload = function() {
//	document.getElementById('grad_year').innerHTML = go_card[my_year(new Date())] + '-year';
//	document.getElementById('footer-text').innerHTML = 'This page last updated ' +
		all_files_info['/export/userswww/adebray/WWW/index.html'];
	
/*	if (UT_login_name() != null) {
		let the_32 = document.getElementById('off_by_one');
		the_32.title = "Click me!";
		the_32.onclick = function() {
			alert('Hello, ' + UT_login_name() + '!');
		}
	} */
}
