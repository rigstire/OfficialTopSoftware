document.addEventListener("DOMContentLoaded", function () {
	const csBody = document.querySelector('body');
	const csNavbar = document.querySelector('#cs-navigation');
	const csToggle = document.querySelector('#cs-navigation .cs-toggle');
	const menuWrapper = document.querySelector('.cs-ul-wrapper');
	const csUL = document.querySelector('#cs-expanded');
  
	// If any of the essential elements are missing, log an error and stop.
	if (!csNavbar || !csToggle || !menuWrapper || !csUL) {
	  console.error("Navbar elements missing; please check your template.");
	  return;
	}
  
	csToggle.addEventListener('click', function () {
	  // Toggle the "open" class to show/hide the mobile menu
	  menuWrapper.classList.toggle('open');
	  csToggle.classList.toggle('cs-active');
	  csNavbar.classList.toggle('cs-active');
	  csBody.classList.toggle('cs-open');
  
	  // Update the aria-expanded attribute for accessibility
	  const expanded = csUL.getAttribute('aria-expanded');
	  csUL.setAttribute('aria-expanded', expanded === 'false' ? 'true' : 'false');
	});
  
	// Dropdown functionality (if any dropdowns are in your navbar)
	const dropDowns = Array.from(document.querySelectorAll('#cs-navigation .cs-dropdown'));
	dropDowns.forEach(item => {
	  item.addEventListener('click', () => {
		item.classList.toggle('cs-active');
	  });
	});
  });
								