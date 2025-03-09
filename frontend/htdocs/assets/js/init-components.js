document.addEventListener("DOMContentLoaded", function() {
	// Init Sidenav
	M.Sidenav.init(document.querySelectorAll(".sidenav"), {});
	document.querySelector("#toggle_sidenav").addEventListener("click", function() {
		var elem = document.querySelector(".sidenav");
		var instance = M.Sidenav.getInstance(elem);
		if (instance.isOpen) {
			instance.close();
		} else {
			instance.open();
		}
	});
});