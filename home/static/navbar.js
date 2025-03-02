document.addEventListener("DOMContentLoaded", function () {
	const csBody = document.querySelector('body');
	const csNavbar = document.querySelector('#cs-navigation');
	const csToggle = document.querySelector('#cs-navigation .cs-toggle');
	const menuWrapper = document.querySelector('.cs-ul-wrapper');
	const csUL = document.querySelector('#cs-expanded');
  
<<<<<<< HEAD
	// If any essential element is missing, log an error and stop further execution.
=======
	// If any of the essential elements are missing, log an error and stop.
>>>>>>> 3d907c7d27d58b4b696bbf45883c3843e7e66ffe
	if (!csNavbar || !csToggle || !menuWrapper || !csUL) {
	  console.error("Navbar elements missing; please check your template.");
	  return;
	}
  
	csToggle.addEventListener('click', function () {
<<<<<<< HEAD
	  // Toggle the mobile menu visibility by adding/removing the "open" class
=======
	  // Toggle the "open" class to show/hide the mobile menu
>>>>>>> 3d907c7d27d58b4b696bbf45883c3843e7e66ffe
	  menuWrapper.classList.toggle('open');
	  csToggle.classList.toggle('cs-active');
	  csNavbar.classList.toggle('cs-active');
	  csBody.classList.toggle('cs-open');
  
	  // Update the aria-expanded attribute for accessibility
	  const expanded = csUL.getAttribute('aria-expanded');
	  csUL.setAttribute('aria-expanded', expanded === 'false' ? 'true' : 'false');
	});
  
<<<<<<< HEAD
	// Optional: Dropdown functionality (if dropdowns exist in your navbar)
=======
	// Dropdown functionality (if any dropdowns are in your navbar)
>>>>>>> 3d907c7d27d58b4b696bbf45883c3843e7e66ffe
	const dropDowns = Array.from(document.querySelectorAll('#cs-navigation .cs-dropdown'));
	dropDowns.forEach(item => {
	  item.addEventListener('click', () => {
		item.classList.toggle('cs-active');
	  });
	});
  });
<<<<<<< HEAD
  
  
=======
								
>>>>>>> 3d907c7d27d58b4b696bbf45883c3843e7e66ffe
