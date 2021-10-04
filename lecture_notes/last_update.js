window.onload = function() {
	Array.from(document.getElementsByClassName('updater')).forEach(element =>
		element.innerHTML = 'Updated '
			+ all_files_info['/export/userswww/adebray/WWW/lecture_notes/' + element.getAttribute('filename')] + '.'
	);
}
