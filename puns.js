const categories = ['meta', 'food', 'math', 'CS', 'other',
                    'lang', 'sci', 'music', 'hum', 'holidays',
                    'longer', 'top']

// An array of all elements with a 'p' tag
let pars = undefined

window.onload = function() {
	document.getElementById('footer-text').innerHTML = 'This page last updated ' + all_files_info['./puns.html'];
	pars = Array.from(document.getElementsByTagName('p'));
	let pun_filter = document.getElementById('filter');
	pun_filter.onchange = function() {
		const to_filter = pun_filter.value;
		if (to_filter == "show_all") show_all();
		else if (to_filter === "") return;
		else show_only(to_filter);
	}
}

/* stat should be one of "none" or "inherit", corresponding to
   hiding or showing the category in question.
 */
function update(category, stat) {
	pars.forEach(par => {
		if (par.className.split(' ').indexOf(category) !== -1)
			par.style.display = stat;
	});
}

function show(category) {
	update(category, "inherit");
}

function hide(category) {
	update(category, "none");
}

// show all puns. All of them. That's a lot of puns.
function show_all() {
	categories.forEach(category => show(category));
}

/* Show only puns of the specified category.
   The same pun may belong to several categories.
 */
function show_only(category) {
	hide_all();
	show(category);
}

// Useful for testing if anything was misclassified
function hide_all() {
	categories.forEach(category => hide(category));
}
