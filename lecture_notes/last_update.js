window.onload = function() {
	
	for (element of document.getElementsByClassName('updater')) {
		element.innerHTML = 'Updated '
			+ all_files_info['./lecture_notes/' + element.getAttribute('filename')] + '.';
	}
}
