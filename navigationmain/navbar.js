document.addEventListener('DOMContentLoaded', function() {
	const mobileMenuIcon = document.getElementById('mobile-menu-icon');
	const mobileNav = document.getElementById('mobile-nav');
  
	mobileMenuIcon.addEventListener('click', function() {
	  mobileNav.classList.toggle('active');
	});
  
	// Close mobile menu when any link is clicked
	const mobileNavLinks = document.querySelectorAll('.mobile-nav-menu li a');
	mobileNavLinks.forEach(function(link) {
	  link.addEventListener('click', function() {
		mobileNav.classList.remove('active');
	  });
	});
  });
  