window.onload = function() {
	for (element of document.getElementsByClassName('updater')) {
		element.innerHTML = 'Upated ' + all_files_info['./lecture_notes/' + element.filename];
	}
}
