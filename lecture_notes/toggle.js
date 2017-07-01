// for hiding and showing lists.
// source: http://stackoverflow.com/a/17561122

/* Toggle a list from hidden to shown
	'head' is the h3 header: we switch ▾ and ▸
	'body' is the text to be hidden or shown
 */
function toggle_list(head_id, body_id) {
	const list = document.getElementById(body_id);
	const head = document.getElementById(head_id);

	if (list.style.display == "none") {
		list.style.display = "block";
		head.innerText = '▾' + head.innerText.substr(1);
	} else {
		list.style.display = "none";
		head.innerText = '▸' + head.innerText.substr(1);
	}
}
