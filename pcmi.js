// returns true if date between 0 and num_days in the future.
const is_sooner_than = function(num_days, talk_date) {
	/* Talks should still be listed as "upcoming" on the day of. Therefore we want to compare the two days
	   at midnight, rather than one at midnight and one at some other time, so we zero out the finer-grained
	   information from today's date.
	 */
	let today = new Date();
	today.setHours(0);
	today.setMinutes(0);
	today.setSeconds(0);
	today.setMilliseconds(0);

	const milliseconds = new Date(talk_date) - today;
	if (milliseconds < 0)
		return false;
	const days = milliseconds/(1000*60*60*24);
	return days <= num_days;
}

// Returns a list of all upcoming talks
const get_upcoming_talks = function() {
	/* getElementByClassName returns an HTML collection, which is not an array, so we convert it to
	   an array using Array.from()
	 */
	let schedule_list = Array.from(document.getElementById('all_talks').getElementsByTagName('li'));
	let td = schedule_list.filter(talk => is_sooner_than(7, talk.getAttribute('date')));
	return td;
}

const populate_upcoming_talks = function() {
	document.getElementById('upcoming_talks').innerHTML =
		'<ul>' +
		// take each upcoming talk and turn it into a string.
		// then concatenate them
		get_upcoming_talks().map(talk_node => talk_node.outerHTML).join('') + 
		'</ul>'
}




window.onload = function() {
	populate_upcoming_talks();
	document.getElementById('footer-text').innerHTML = 'This page last updated ' +
		all_files_info['/home/users/a.debray/public_html/pcmi_prep.html'];

}
