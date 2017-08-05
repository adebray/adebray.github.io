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

window.onload = function() {
	if (document.URL === 'https://adebray.github.io/') window.location = '//www.ma.utexas.edu/users/a.debray/';
	document.getElementById('grad_year').innerHTML = go_card[my_year(new Date())];
	document.getElementById('footer-text').innerHTML = 'This page last updated ' + all_files_info['./index.html'];
}
