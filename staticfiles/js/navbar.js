document.addEventListener("DOMContentLoaded", function () {
	const mobileMenuIcon = document.getElementById("mobile-menu-icon");
	const mobileNav = document.getElementById("mobile-nav");
  
	if (!mobileMenuIcon || !mobileNav) {
	  console.error("Mobile menu elements not found; please check your template.");
	  return;
	}

	function toggleMobileNav() {
		mobileNav.classList.toggle("active");
		mobileMenuIcon.classList.toggle("active");
	}

	function closeMobileNav() {
		mobileNav.classList.remove("active");
		mobileMenuIcon.classList.remove("active");
	}
  
	// Toggle mobile nav
	mobileMenuIcon.addEventListener("click", function(e) {
		e.preventDefault();
		e.stopPropagation();
		toggleMobileNav();
	});
  
	// Close mobile nav when any link is clicked
	const mobileNavLinks = document.querySelectorAll(".mobile-nav-menu li a");
	mobileNavLinks.forEach(function(link) {
	  link.addEventListener("click", function(e) {
		setTimeout(() => {
			closeMobileNav();
		}, 150);
	  });
	});
  
	// Close mobile nav when clicking outside
	document.addEventListener("click", function(e) {
		if (!mobileMenuIcon.contains(e.target) && !mobileNav.contains(e.target)) {
			closeMobileNav();
		}
	});

	// Handle escape key
	document.addEventListener("keydown", function(e) {
		if (e.key === "Escape" && mobileNav.classList.contains("active")) {
			closeMobileNav();
		}
	});

	// Close menu when window is resized to desktop
	window.addEventListener("resize", function() {
		if (window.innerWidth > 768 && mobileNav.classList.contains("active")) {
			closeMobileNav();
		}
	}, { passive: true });
}); 