window.onload = function() {
	Array.from(document.getElementsByClassName('updater')).forEach(element =>
		element.innerHTML = 'Updated '
			+ all_files_info['./lecture_notes/' + element.getAttribute('filename')] + '.'
	);
}
