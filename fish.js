const main = function() {
	let _ = document.getElementById('input_fish').value;
	let rand = Boolean(Math.round(Math.random()));
	let answer = "yeah!";
	if (rand) {
		answer = "nope."
	}
	document.getElementById('answer_fish').innerHTML = answer;
}
