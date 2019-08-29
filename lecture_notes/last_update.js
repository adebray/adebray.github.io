window.onload = function() {
	Array.from(document.getElementsByClassName('updater')).forEach(element =>
		element.innerHTML = 'Updated '
			+ all_files_info['/home/a.debray/public_html/lecture_notes/' + element.getAttribute('filename')] + '.'
	);
}
