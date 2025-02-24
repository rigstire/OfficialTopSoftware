document.addEventListener("DOMContentLoaded", function () {
	const csBody = document.querySelector('body');
	const csNavbar = document.querySelector('#cs-navigation');
	const csToggle = document.querySelector('#cs-navigation .cs-toggle');
	const menuWrapper = document.querySelector('.cs-ul-wrapper');
	const csUL = document.querySelector('#cs-expanded');
  
	csToggle.addEventListener('click', function () {
	  // Toggle the mobile menu visibility by adding/removing the "open" class
	  menuWrapper.classList.toggle('open');
  
	  // Optionally toggle other classes (for styling or scrolling behavior)
	  csToggle.classList.toggle('cs-active');
	  csNavbar.classList.toggle('cs-active');
	  csBody.classList.toggle('cs-open');
  
	  // Update the aria-expanded attribute for accessibility
	  const expanded = csUL.getAttribute('aria-expanded');
	  csUL.setAttribute('aria-expanded', expanded === 'false' ? 'true' : 'false');
	});
  
	// Optional: Code for dropdown functionality (if you have dropdowns in your navbar)
	const dropDowns = Array.from(document.querySelectorAll('#cs-navigation .cs-dropdown'));
	dropDowns.forEach(item => {
	  item.addEventListener('click', () => {
		item.classList.toggle('cs-active');
	  });
	});
  });
  